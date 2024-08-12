#!/bin/bash
project="fnic-2024"
region="europe-west1"
matrix_room="!ckizGZoefGVpbVxjZN:matrix.org"
flag_dv="TRUE"
flag_pm="TRUE"

gc_deploy() {
  gcloud run jobs deploy modreportbot-$1 --project=$project --region=$region --source . --set-env-vars=LEMMY_USER="fnicmodbot",LEMMY_INSTANCE="$2",MATRIX_USER="@fnic_reports:matrix.org",MATRIX_SERVER="matrix.org",MATRIX_ROOM="$matrix_room",FLAG_DOWNVOTES="$flag_dv",GET_MESSAGES="$flag_pm" --set-secrets="LEMMY_PW=fnicmodbot-$1:latest","MATRIX_PW=fnicreports:latest" &
}

gc_deploy "lemmings-world" "lemmings.world"
gc_deploy "dbzer0" "lemmy.dbzer0.com"
gc_deploy "lemm-ee" "lemm.ee"
gc_deploy "sffa" "sffa.community"
gc_deploy "lemmy-world" "lemmy.world"

wait

