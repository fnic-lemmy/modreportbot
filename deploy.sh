#!/bin/bash
gcloud config set project fnic-2024
gcloud run jobs deploy modreportbot-lemmings-world --region europe-west1 --source . --set-env-vars=LEMMY_USER="fnicmodbot",LEMMY_INSTANCE="lemmings.world",MATRIX_USER="@fnic_reports:matrix.org",MATRIX_SERVER="matrix.org",MATRIX_ROOM="!TcCyUEXBiAZZOviESk:matrix.org" --set-secrets="LEMMY_PW=fnicmodbot-lemmings-world:latest","MATRIX_PW=fnicreports:latest"
gcloud run jobs deploy modreportbot-dbzer0 --region europe-west1 --source . --set-env-vars=LEMMY_USER="fnicmodbot",LEMMY_INSTANCE="lemmy.dbzer0.com",MATRIX_USER="@fnic_reports:matrix.org",MATRIX_SERVER="matrix.org",MATRIX_ROOM="!TcCyUEXBiAZZOviESk:matrix.org" --set-secrets="LEMMY_PW=fnicmodbot-dbzer0:latest","MATRIX_PW=fnicreports:latest"
