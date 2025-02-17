#!/usr/bin/python3

import requests
import json
import sys
import string
import matrix
from pythorhead import Lemmy
from pythorhead.types import SortType,ListingType

def run(lemmy, live, room, muser, mpw, mserver):
  try:
    mposts = lemmy.post.list(sort=SortType.New, type_=ListingType.Subscribed, limit=10)
  except Exception as e:
    print(f'cannot get subscribed posts: {e}\n')

  posts = mposts

  for p in posts:
    if p["read"] is True:
      if (p["post"]["featured_community"] is True) or (p["post"]["featured_local"] is True):
        continue # skip past pinned posts
      break

    if live:
      lemmyverselink = "https://lemmyverse.link/" + p['post']['ap_id'][8:]
      # post to matrix
      mtxt = f"New: [**[{p['community']['name']}]({p['community']['ap_id']})**] {p['post']['name']}\n[[Direct]({p['post']['ap_id']})] [[Lemmyverse]({lemmyverselink})]"
      matrix.post(mtxt, room, muser, mpw, mserver)

      try:
        lemmy.post.mark_as_read(p["post"]["id"], True)
      except Exception as e:
        print(f'cannot mark as read: {e}\n')

  return
