#!/usr/bin/python3

import requests
import json
import sys
import string
import matrix
from pythorhead import Lemmy

def run(lemmy, live, room, muser, mpw, mserver):
  try:
    pms = lemmy.private_message.list(page = 1, unread_only = True)
  except Exception as e:
    print(f'cannot get private messages: {e}\n')
    return

  for p in pms['private_messages']:
    rtxt = f"From: {p['creator']['display_name']} <{p['creator']['actor_id']}>\nTo: {p['recipient']['display_name']} <{p['recipient']['actor_id']}>\n{p['private_message']['content']}\n"
    print(rtxt)

    if live:
      matrix.post(rtxt, room, muser, mpw, mserver)

      try:
        lemmy.private_message.mark_as_read(p['private_message']['id'], True)
      except Exception as e:
        print(f'cannot mark as read: {e}\n')

  return
