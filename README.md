# modreportbot
Posts Lemmy reports to Matrix

This is designed to run on Google Cloud Run.
Passwords need to be stored in Google Secret Manager.
The backing database is Firebase which needs to be activated for your project.

NB: Do not use FLAG_DOWNVOTES and NOTIFY_NEW with the same bot - they both mark posts in the same way so this has the potential to cause conflicts.

