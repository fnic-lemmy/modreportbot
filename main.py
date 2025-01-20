import sys
import os
import modreport

# Retrieve Job-defined env vars
TASK_INDEX = os.getenv("CLOUD_RUN_TASK_INDEX", 0)
TASK_ATTEMPT = os.getenv("CLOUD_RUN_TASK_ATTEMPT", 0)

BOTUSER = os.getenv("LEMMY_USER",0)
BOTPW = os.getenv("LEMMY_PW", 0)
BOTINSTANCE = os.getenv("LEMMY_INSTANCE", 0)
MATRIXROOM = os.getenv("MATRIX_ROOM", 0)
MATRIXUSER = os.getenv("MATRIX_USER", 0)
MATRIXPW = os.getenv("MATRIX_PW", 0)
MATRIXSERVER = os.getenv("MATRIX_SERVER", 0)
DOWNVOTES = os.getenv("FLAG_DOWNVOTES", 0)
PRIVATEMESSAGES = os.getenv("GET_MESSAGES", 0)
MODREPORTS = os.getenv("GET_REPORTS", 0)
NEWPOSTS = os.getenv("NOTIFY_NEW", 0)

def main(user, pw, inst, room, muser, mpw, mserver, dv, pm, reports, newposts):

    modreport.run(user, pw, inst, room, muser, mpw, mserver, dv, pm, reports, newposts, True)
    return "modreportbot"

# Start script
if __name__ == "__main__":
    try:
        main(BOTUSER, BOTPW, BOTINSTANCE, MATRIXROOM, MATRIXUSER, MATRIXPW, MATRIXSERVER, DOWNVOTES, PRIVATEMESSAGES, MODREPORTS, NEWPOSTS)
    except Exception as err:
        message = (
            f"Task #{TASK_INDEX}, " + f"Attempt #{TASK_ATTEMPT} failed: {str(err)}"
        )

        print(message)
        sys.exit(1)  # Retry Job Task by exiting the process
