# modreportbot
Posts Lemmy reports to Matrix

This is designed to run on Google Cloud Run.
Passwords need to be stored in Google Secret Manager.
The backing database is Firebase which needs to be activated for your project.

There are some extra features:
* FLAG_DOWNVOTES - sends a notification when a post is downvoted below -5
* PRIVATEMESSAGES - sends a notification when a PM is received
* GET_REPORTS - sends a notification when a post is reported
* NOTIFY_NEW - sends a notification on new posts
* GET_MODLOG - notifies on events in the modlog
* MODLOG_PM - notifies the user via DM when posts have been modded
