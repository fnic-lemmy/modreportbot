#!/usr/bin/python3

import asyncio

from nio import AsyncClient, MatrixRoom, RoomMessageText
import re

def urlify2(value):
    urlfinder = re.compile("\[([^\]]+)\]\(([^)]+)\)")
    return urlfinder.sub(r'<a href="\2">\1</a>', value)

async def main(msg, room, user, pw, server) -> None:
    client = AsyncClient(f"https://{server}", user)
    #client.add_event_callback(message_callback, RoomMessageText)

    print(await client.login(pw))
    # "Logged in as @alice:example.org device id: RANDOMDID"

    # If you made a new room and haven't joined as that user, you can use
    # await client.join("your-room-id")

    fmsg = urlify2(msg)

    await client.room_send(
        # Watch out! If you join an old room you'll see lots of old messages
        room_id = room,
        message_type="m.room.message",
        content={"msgtype": "m.notice",
          "body": msg,
          "format": "org.matrix.custom.html",
          "formatted_body": fmsg
        }
    )
    #await client.sync_forever(timeout=30000)  # milliseconds
    await client.close()

def post(msg, room, user, pw, server):
    asyncio.run(main(msg, room, user, pw, server))

