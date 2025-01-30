#!/usr/bin/python3
import json
import matrix
import firestore

from pythorhead import Lemmy
from pythorhead.types import ModlogActionType,ListingType

def removed_posts(lemmy, live, c, available_communities, processed_modlogs, room, muser, mpw, mserver, pm_modlogs):
  ml = lemmy.modlog.get(community_id=c,type_=ModlogActionType.ModRemovePost,limit=4)
  processed = []
  ppid = 0

  for log in ml['removed_posts']:
    if ppid == log['mod_remove_post']['post_id']:
      continue # skip duplicates
    ppid = log['mod_remove_post']['post_id']

    if log['mod_remove_post']['id'] in processed_modlogs:
      break # stop processing if we've already seen a log as they are in descending order

    if "reason" in log['mod_remove_post']:
      reason = log['mod_remove_post']['reason']
    else:
      reason = "(not specified)"
    msg = f"\"{log['post']['name']}\" in \"{log['community']['name']}\" has been removed due to reason: {reason}"
    print(f"{log['mod_remove_post']['id']} {msg}")

    if pm_modlogs is True:
      user=lemmy.user.get(person_id=log['post']['creator_id']) # look up user
      if 'display_name' in user['person_view']['person']:
        msg_to = user['person_view']['person']['display_name']
      else:
        msg_to = user['person_view']['person']['name']

    if live:
      processed.append(log['mod_remove_post']['id']) # mark modlog as processed
      if c in available_communities: # only perform actions if we've seen the community before
        # Post to Matrix
        matrix.post(f'[modlog] {msg}', room, muser, mpw, mserver)
        # Send PM to the poster
        if pm_modlogs is True:
          pm_msg = f"Dear {msg_to},\n\nYour post {msg}\n\nIf you are able to correct this please feel free to re-post."
          lemmy.private_message.create(recipient_id=log['post']['creator_id'],content=pm_msg)

  return(processed)

def removed_comments(lemmy, live, c, available_communities, processed_modlogs, room, muser, mpw, mserver, pm_modlogs):
  ml = lemmy.modlog.get(community_id=c,type_=ModlogActionType.ModRemoveComment,limit=4)
  processed = []
  ppid = 0

  for log in ml['removed_comments']:
    if log['mod_remove_comment']['id'] in processed_modlogs:
      break # stop processing if we've already seen a log as they are in descending order

    if "reason" in log['mod_remove_comment']:
      reason = log['mod_remove_comment']['reason']
    else:
      reason = "(not specified)"
    msg = f"\"{log['comment']['content']}\" under post \"{log['post']['name']}\" ({log['post']['ap_id']}) in \"{log['community']['name']}\" has been removed due to reason: {reason}"
    print(f"{log['mod_remove_comment']['id']} {msg}")
    if pm_modlogs is True:
      user=lemmy.user.get(person_id=log['commenter']['id']) # look up user
      if 'display_name' in user['person_view']['person']:
        msg_to = user['person_view']['person']['display_name']
      else:
        msg_to = user['person_view']['person']['name']

    if live:
      processed.append(log['mod_remove_comment']['id']) # mark modlog as processed
      if c in available_communities: # only perform actions if we've seen the community before
        # Post to Matrix
        matrix.post(f'[modlog] {msg}', room, muser, mpw, mserver)
        # Send PM to the poster
        if pm_modlogs is True:
          pm_msg = f"Dear {msg_to},\n\nYour comment;\n```\n{log['comment']['content']}\n```\nunder the post \"{log['post']['name']}\" in \"{log['community']['name']}\" has been removed due to reason: {reason}"
          lemmy.private_message.create(recipient_id=log['post']['creator_id'],content=pm_msg)

  return(processed)

def added_to_community(lemmy, live, c, available_communities, processed_modlogs, room, muser, mpw, mserver, pm_modlogs):
  ml = lemmy.modlog.get(community_id=c,type_=ModlogActionType.ModAddCommunity,limit=4)
  processed = []
  ppid = 0

  for log in ml['added_to_community']:
    if log['mod_add_community']['id'] in processed_modlogs:
      break # stop processing if we've already seen a log as they are in descending order
    if log['mod_add_community']['removed'] is not False:
      break # not interested in removed mods

    msg = f"\"{log['modded_person']['name']}\" has been added as a mod for \"{log['community']['name']}\" by \"{log['moderator']['name']}\""
    print(f"{log['mod_add_community']['id']} {msg}")

    if pm_modlogs is True:
      if 'display_name' in user['modded_person']:
        msg_to = user['modded_person']['display_name']
      else:
        msg_to = user['modded_person']['name']

    if live:
      processed.append(log['mod_add_community']['id']) # mark modlog as processed
      if c in available_communities: # only perform actions if we've seen the community before
        # Post to Matrix
        matrix.post(f'[modlog] {msg}', room, muser, mpw, mserver)
        # Send PM to the poster
        if pm_modlogs is True:
          pm_msg = f"Dear {msg_to},\n\nYou have been added as a moderator for \"{log['community']['name']}\"."
          lemmy.private_message.create(recipient_id=log['modded_person']['id'],content=pm_msg)

  return(processed)


def banned_from_communiy(lemmy, live, c, available_communities, processed_modlogs, room, muser, mpw, mserver, pm_modlogs):
  ml = lemmy.modlog.get(community_id=c,type_=ModlogActionType.ModBanFromCommunity,limit=4)
  processed = []
  ppid = 0

  for log in ml['banned_from_community']:
    if log['mod_ban_from_community']['id'] in processed_modlogs:
      break # stop processing if we've already seen a log as they are in descending order
    if log['mod_ban_from_community']['banned'] is not True:
      break # not interested in unbans

    if "reason" in log['mod_ban_from_community']:
      reason = log['mod_ban_from_community']['reason']
    else:
      reason = "(not specified)"

    if "expires" in log['mod_ban_from_community']: # suspect a permanent ban won't have an expiry date
      expires = log['mod_ban_from_community']['expires']
    else:
      expires = "(not specified)"

    msg = f"\"{log['banned_person']['name']}\" has been banned from \"{log['community']['name']}\" until {expires} due to reason: {reason}"
    print(f"{log['mod_ban_from_community']['id']} {msg}")
    if pm_modlogs is True:
      if 'display_name' in user['banned_person']:
        msg_to = user['banned_person']['display_name']
      else:
        msg_to = user['banned_person']['name']

    if live:
      processed.append(log['mod_ban_from_community']['id']) # mark modlog as processed
      if c in available_communities: # only perform actions if we've seen the community before
        # Post to Matrix
        matrix.post(f'[modlog] {msg}', room, muser, mpw, mserver)
        # Send PM to the poster
        if pm_modlogs is True:
          pm_msg = f"Dear {msg_to},\n\nYou have been banned from \"{log['community']['name']}\" until {expires} due to reason: {reason}"
          lemmy.private_message.create(recipient_id=log['banned_person']['id'],content=pm_msg)

  return(processed)



def run(lemmy, l_user, l_inst, live, room, muser, mpw, mserver, pm_modlogs):
  processed_modlogs = {}
  processed_modlogs['removed_posts'] = []
  processed_modlogs['removed_comments'] = []
  processed_modlogs['added_to_community'] = []
  processed_modlogs['banned_from_community'] = []

  available_communities = {}
  available_communities['removed_posts'] = []
  available_communities['removed_comments'] = []
  available_communities['added_to_community'] = []
  available_communities['banned_from_community'] = []

  doc = f'{l_user}.{l_inst}'
  if live:
    processed_modlogs = firestore.get("modlogs", doc)
  if processed_modlogs is None:
    processed_modlogs = {}
  if 'removed_posts' not in processed_modlogs:
    processed_modlogs['removed_posts'] = []
  if 'removed_comments' not in processed_modlogs:
    processed_modlogs['removed_comments'] = []
  if 'added_to_community' not in processed_modlogs:
    processed_modlogs['added_to_community'] = []
  if 'banned_from_community' not in processed_modlogs:
    processed_modlogs['banned_from_community'] = []

  if live:
    available_communities = firestore.get("modlog_communities", doc)
  if available_communities is None:
    available_communities = {}
  if 'removed_posts' not in available_communities:
    available_communities['removed_posts'] = []
  if 'removed_comments' not in available_communities:
    available_communities['removed_comments'] = []
  if 'added_to_community' not in available_communities:
    available_communities['added_to_community'] = []
  if 'banned_from_community' not in available_communities:
    available_communities['banned_from_community'] = []

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
    # process removed posts
    processed = removed_posts(lemmy, live, c, available_communities['removed_posts'], processed_modlogs['removed_posts'], room, muser, mpw, mserver, pm_modlogs)

    if live:
      processed_modlogs['removed_posts'].extend(processed)
      if c not in available_communities['removed_posts']: # this is a new community, we need to add it so actions happen for new logs
        print(f'community with id {c} not seen previously for removed_posts, adding')
        available_communities['removed_posts'].append(c)

    # process removed comments
    processed = removed_comments(lemmy, live, c, available_communities['removed_comments'], processed_modlogs['removed_comments'], room, muser, mpw, mserver, pm_modlogs)

    if live:
      processed_modlogs['removed_comments'].extend(processed)
      if c not in available_communities['removed_comments']: # this is a new community, we need to add it so actions happen for new logs
        print(f'community with id {c} not seen previously for removed_comments, adding')
        available_communities['removed_comments'].append(c)

    # process added mods
    # NB: Sending PMs for this action is disabled
    processed = added_to_community(lemmy, live, c, available_communities['added_to_community'], processed_modlogs['added_to_community'], room, muser, mpw, mserver, False)

    if live:
      processed_modlogs['added_to_community'].extend(processed)
      if c not in available_communities['added_to_community']: # this is a new community, we need to add it so actions happen for new logs
        print(f'community with id {c} not seen previously for added_to_community, adding')
        available_communities['added_to_community'].append(c)

    # process removed comments
    processed = banned_from_community(lemmy, live, c, available_communities['banned_from_community'], processed_modlogs['banned_from_community'], room, muser, mpw, mserver, pm_modlogs)

    if live:
      processed_modlogs['banned_from_community'].extend(processed)
      if c not in available_communities['banned_from_community']: # this is a new community, we need to add it so actions happen for new logs
        print(f'community with id {c} not seen previously for banned_from_community, adding')
        available_communities['banned_from_community'].append(c)



  if live:
    firestore.set("modlogs", doc, processed_modlogs)
    firestore.set("modlog_communities", doc, available_communities)
