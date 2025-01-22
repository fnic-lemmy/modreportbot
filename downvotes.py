#!/usr/bin/python3

import requests
import json
import sys
import string
from pythorhead import Lemmy
from pythorhead.types import SortType,ListingType

def run(lemmy, live):
  threshold = -5 # posts below this score will be flagged

  try:
    mposts = lemmy.post.list(sort=SortType.New, type_=ListingType.ModeratorView, limit=10)
  except Exception as e:
    print(f'cannot get moderator posts: {e}\n')

  posts = mposts

  for p in posts:
    if p["hidden"] is True:
      break

    if p['counts']['score'] < threshold:
      if live:
        try:
          lemmy.report(p["post"]["id"], f'Downvoted - Score {p["counts"]["score"]}') # raise report
        except Exception as e:
          print("unable to raise report: {e}")
          return
        try:
          lemmy.post.hide(p["post"]["id"], True)
        except Exception as e:
          print(f'cannot hide post: {e}\n')

  return
