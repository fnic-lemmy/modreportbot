#!/bin/bash
gcloud config set project bots-424808
gcloud run jobs deploy modreportbot --source . --set-env-vars=LEMMY_USER="eric",LEMMY_INSTANCE="feddit.uk",MATRIX_USER="@robot_bunny:matrix.org",MATRIX_SERVER="matrix.org",MATRIX_ROOM="!JvATVaovRwoZeJNnas:beeper.com" --set-secrets="LEMMY_PW=eric:latest","MATRIX_PW=robotbunny:latest"
