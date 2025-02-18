#!/usr/bin/python3

import requests
import json
import sys
import string
import re
import matrix
from pythorhead import Lemmy

def run(lemmy, live, room, muser, mpw, mserver):
  try:
    pms = lemmy.private_message.list(page = 1, unread_only = True)
  except Exception as e:
    print(f'cannot get private messages: {e}\n')
    return

  for p in pms['private_messages']:
    if 'display_name' in p['creator']:
      dm_from = p['creator']['display_name']
    else:
      dm_from = p['creator']['name']

    g = re.search(r'https://(.*)/u/(.*)', p['creator']['actor_id'])
    if g is not None:
      from_inst = g.group(1)
      from_user = g.group(2)
      dm_from_addr = f'@{from_user}@{from_inst}'
    else:
      dm_from_addr = p['creator']['actor_id']

    if 'display_name' in p['recipient']:
      dm_to = p['recipient']['display_name']
    else:
      dm_to = p['recipient']['name']

    g = re.search(r'https://(.*)/u/(.*)', p['recipient']['actor_id'])
    if g is not None:
      to_inst = g.group(1)
      to_user = g.group(2)
      dm_to_addr = f'@{to_user}@{to_inst}'
    else:
      dm_to_addr = p['recipient']['actor_id']

    rtxt = f"DM: [{dm_to}] From: {dm_from} <{dm_from_addr}>\nTo: {dm_to} <{dm_to_addr}>\n{p['private_message']['content']}\n"
    print(rtxt)

    if live:
      matrix.post(rtxt, room, muser, mpw, mserver)

      try:
        lemmy.private_message.mark_as_read(p['private_message']['id'], True)
      except Exception as e:
        print(f'cannot mark as read: {e}\n')

  return
