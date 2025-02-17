#!/usr/bin/python3

import asyncio

from nio import AsyncClient, MatrixRoom, RoomMessageText
import re

def markdown_to_html(value):
    markdown = re.compile("\[([^\]\[]+)\]\(([^)]+)\)")
    bold = re.compile("\*\*([^*]+)\*\*")
    newvalue = markdown.sub(r'<a href="\2">\1</a>', value)
    return bold.sub(r'<b>\1</b>', newvalue)

def remove_markdown(value):
    markdownbold = re.compile("\*\*\[([^\]\[]+)\]\(([^)]+)\)\*\*")
    markdown = re.compile("\[([^\]\[]+)\]\(([^)]+)\)")
    newvalue = markdownbold.sub(r'\1', value) # if in bold return text
    return markdown.sub(r'\2', newvalue) # if not bold return url

async def main(msg, room, user, pw, server) -> None:
    client = AsyncClient(f"https://{server}", user)
    #client.add_event_callback(message_callback, RoomMessageText)

    if pw is not None:
      print(await client.login(pw))
    # "Logged in as @alice:example.org device id: RANDOMDID"

    # If you made a new room and haven't joined as that user, you can use
    # await client.join("your-room-id")

    fmsg = markdown_to_html(msg)
    pmsg = remove_markdown(msg)

    await client.room_send(
        # Watch out! If you join an old room you'll see lots of old messages
        room_id = room,
        message_type="m.room.message",
        content={"msgtype": "m.notice",
          "body": pmsg,
          "format": "org.matrix.custom.html",
          "formatted_body": fmsg
        }
    )
    #await client.sync_forever(timeout=30000)  # milliseconds
    await client.close()

def post(msg, room, user, pw, server):
    asyncio.run(main(msg, room, user, pw, server))

