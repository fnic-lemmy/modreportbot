#!/usr/bin/python3

import asyncio

from nio import AsyncClient, MatrixRoom, RoomMessageText

async def main(msg, room, user, pw, server) -> None:
    client = AsyncClient("https://matrix.org", user)
    #client.add_event_callback(message_callback, RoomMessageText)

    print(await client.login(pw))
    # "Logged in as @alice:example.org device id: RANDOMDID"

    # If you made a new room and haven't joined as that user, you can use
    # await client.join("your-room-id")

    await client.room_send(
        # Watch out! If you join an old room you'll see lots of old messages
        room_id = room,
        message_type="m.room.message",
        content={"msgtype": "m.text", "body": msg},
    )
    #await client.sync_forever(timeout=30000)  # milliseconds
    await client.close()

def post(msg, room, user, pw, server):
    asyncio.run(main(msg, room, user, pw, server))
