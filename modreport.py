#!/usr/bin/python3

import json
import sys
import string
import firestore
import matrix
import downvotes
import privatemsg
import newposts
from pythorhead import Lemmy

def run(user, pw, instance, room, muser, mpw, mserver, dv, pm, reports, np, live):
  posted_reports = { }
  posted_reports["posts"] = []
  posted_reports["comments"] = []
  doc = f'{user}.{instance}'
  if live:
    posted_reports = firestore.get("modreports", doc)
  if posted_reports is None:
    posted_reports = {}
  if "posts" not in posted_reports:
    posted_reports["posts"] = []
  if "comments" not in posted_reports:
    posted_reports["comments"] = []

  #print(posted_reports)

  lemmy = Lemmy(f'https://{instance}', raise_exceptions=True)
  try:
    lemmy.log_in(user, pw)
  except Exception as e:
    print(f'login failed: {e}\n')
    sys.exit(1)

  if np == "TRUE":
    newposts.run(lemmy, live, room, muser, mpw, mserver)

  if dv == "TRUE":
    downvotes.run(lemmy, live)

  if pm == "TRUE":
    privatemsg.run(lemmy, live, room, muser, mpw, mserver)

  if reports != "TRUE":
    # not getting reports so nothing more to do
    return

  try:
    reports = lemmy.post.report_list(unresolved_only = "true")
  except Exception as e:
    print(f'cannot get post reports: {e}\n')
    sys.exit(1) 
    
  if reports is not None:
    for report in reports:
      if posted_reports["posts"] and (report["post_report"]["id"] in posted_reports["posts"]):
        print(f'id {report["post_report"]["id"]} already posted')
        continue

      #print(report)
      rtxt = f'Report: {report["post_report"]["reason"]}\n'
      rtxt += f'Community: {report["community"]["name"]}\n'
      rtxt += f'Post: {report["post"]["ap_id"]} {report["post"]["name"]}\n'
      rtxt += f'Comments: {report["counts"]["comments"]} 👍{report["counts"]["upvotes"]} 👎{report["counts"]["downvotes"]}\n'

      print(rtxt)
      if live:
        matrix.post(rtxt, room, muser, mpw, mserver)
      posted_reports["posts"].append(report["post_report"]["id"])


  try:
    reports = lemmy.comment.report_list(unresolved_only = "true")
    #print(reports)
  except Exception as e:
    print(f'cannot get comment reports: {e}\n')
    sys.exit(1) 

  if reports is not None:
    for report in reports:
      if posted_reports["comments"] and (report["comment_report"]["id"] in posted_reports["comments"]):
        print(f'id {report["comment_report"]["id"]} already posted')
        continue

      rtxt = f'Report: {report["comment_report"]["reason"]}\n'
      rtxt += f'Community: {report["community"]["name"]}\n'
      rtxt += f'Comment: {report["comment"]["content"]}\n'
      rtxt += f'Replies: {report["counts"]["child_count"]} 👍{report["counts"]["upvotes"]} 👎{report["counts"]["downvotes"]}\n'

      print(rtxt)
      if live:
        matrix.post(rtxt, room, muser, mpw, mserver)
      posted_reports["comments"].append(report["comment_report"]["id"])

  if live:
    firestore.set("modreports", doc, posted_reports)
