#!/usr/bin/python3
import json
import matrix
import firestore

from pythorhead import Lemmy
from pythorhead.types import ModlogActionType,ListingType

def run(lemmy, l_user, l_inst, live, room, muser, mpw, mserver, pm_modlogs):
  processed_modlogs = {}
  processed_modlogs['removed_posts'] = []
  doc = f'{l_user}.{l_inst}'
  if live:
    processed_modlogs = firestore.get("modlogs", doc)
  if processed_modlogs is None:
    processed_modlogs = {}
  if 'removed_posts' not in processed_modlogs:
    processed_modlogs['removed_posts'] = []

  # get list of subscribed commmunities
  # NB: this should really be moderated communities
  #     but a bug prevents that from working correctly
  commlist = []
  cl = lemmy.community.list(type_=ListingType.Subscribed)
  n = 1
  while len(cl)>0:
    for cc in cl:
      commlist.append(cc['community']['id'])
    n+=1
    cl = lemmy.community.list(type_=ListingType.Subscribed, page=n)

  # Get the modlog for each community
  for c in commlist:
    ml = lemmy.modlog.get(community_id=c,type_=ModlogActionType.ModRemovePost,limit=4)

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
        processed_modlogs['removed_posts'].append(log['mod_remove_post']['id'])
        # Post to Matrix
        matrix.post(f'[modlog] {msg}', room, muser, mpw, mserver)
        # Send PM to the poster
        if pm_modlogs is True:
          pm_msg = f"Dear {msg_to},\n\nYour post {msg}\n\nIf you are able to correct this please feel free to re-post."
          lemmy.private_message.create(recipient_id=log['post']['creator_id'],content=pm_msg)

  if live:
    firestore.set("modlogs", doc, processed_modlogs)
