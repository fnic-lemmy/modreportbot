#!/usr/bin/python3
import json
import matrix
import firestore

from pythorhead import Lemmy
from pythorhead.types import ModlogActionType,ListingType

def removed_posts(lemmy, live, c, available_communities, room, muser, mpw, mserver):
  ml = lemmy.modlog.get(community_id=c,type_=ModlogActionType.ModRemovePost,limit=4)
  processed = []
  ppid = 0

  for log in ml['removed_posts']:
    if ppid == log['mod_remove_post']['post_id']:
      continue # skip duplicates
    ppid = log['mod_remove_post']['post_id']

    if log['mod_remove_post']['id'] in processed_modlogs['removed_posts']:
      break # stop processing if we've already seen a log as they are in descending order

    if "reason" in log['mod_remove_post']:
      reason = log['mod_remove_post']['reason']
    else:
      reason = "None given"
    msg = f"\"{log['post']['name']}\" in \"{log['community']['name']}\" has been removed due to reason: {reason}"
    print(f"{log['mod_remove_post']['id']} {msg}")
    user=lemmy.user.get(person_id=log['post']['creator_id']) # look up user
    if 'display_name' in user['person_view']['person']:
      msg_to = user['person_view']['person']['display_name']
    else:
      msg_to = user['person_view']['person']['name']

    if live:
      processed.append(log['mod_remove_post']['id']) # mark modlog as processed
      if c in available_communities['removed_posts']: # only perform actions if we've seen the community before
        # Post to Matrix
        matrix.post(f'[modlog] {msg}', room, muser, mpw, mserver)
        # Send PM to the poster
        if pm_modlogs is True:
          pm_msg = f"Dear {msg_to},\n\nYour post {msg}\n\nIf you are able to correct this please feel free to re-post."
          lemmy.private_message.create(recipient_id=log['post']['creator_id'],content=pm_msg)

  return(processed)


def run(lemmy, l_user, l_inst, live, room, muser, mpw, mserver, pm_modlogs):
  processed_modlogs = {}
  processed_modlogs['removed_posts'] = []

  available_communities = {}
  available_communities['removed_posts'] = []

  doc = f'{l_user}.{l_inst}'
  if live:
    processed_modlogs = firestore.get("modlogs", doc)
  if processed_modlogs is None:
    processed_modlogs = {}
  if 'removed_posts' not in processed_modlogs:
    processed_modlogs['removed_posts'] = []

  if live:
    available_communities = firestore.get("modlog_communities", doc)
  if available_communities is None:
    available_communities = {}
  if 'removed_posts' not in available_communities:
    available_communities['removed_posts'] = []

  # get list of moderated commmunities
  commlist = []
  moduser = lemmy.user.get(username=l_user) # we don't need l_inst as we're logged on to that instance
  if moduser:
    for c in moduser['moderates']:
      commlist.append(c['community']['id'])
  else:
    print(f"cannot get user {l_user}@{l_inst}")
    return

  # Get the modlog for each community
  for c in commlist:
    processed = removed_posts(lemmy, live, c, available_communities, room, muser, mpw, mserver)

    if live:
      processed_modlogs['removed_posts'].extend(processed)
      if c not in available_communities['removed_posts']: # this is a new community, we need to add it so actions happen for new logs
        print(f'community with id {c} not seen previously, adding')
        available_communities['removed_posts'].append(c)

  if live:
    firestore.set("modlogs", doc, processed_modlogs)
    firestore.set("modlog_communities", doc, available_communities)
