#!/bin/bash
gcloud run jobs deploy modreportbot --region europe-west1 --project bots-424808 --source . --set-env-vars=LEMMY_USER="eric",LEMMY_INSTANCE="feddit.uk",MATRIX_USER="@robot_bunny:matrix.org",MATRIX_SERVER="matrix.org",MATRIX_ROOM="!JvATVaovRwoZeJNnas:beeper.com",FLAG_DOWNVOTES="FALSE",GET_MESSAGES="TRUE",NOTIFY_NEW="FALSE" --set-secrets="LEMMY_PW=eric:latest","MATRIX_PW=robotbunny:latest" &

gcloud run jobs deploy modreportbot-notify --region europe-west1 --project bots-424808 --source . --set-env-vars=LEMMY_USER="charles_petrescu",LEMMY_INSTANCE="feddit.uk",MATRIX_USER="@robot_bunny:matrix.org",MATRIX_SERVER="matrix.org",MATRIX_ROOM="!JvATVaovRwoZeJNnas:beeper.com",FLAG_DOWNVOTES="FALSE",GET_MESSAGES="TRUE",NOTIFY_NEW="TRUE" --set-secrets="LEMMY_PW=charles:latest","MATRIX_PW=robotbunny:latest" &

wait

