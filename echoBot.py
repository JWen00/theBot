from fbchat import *
import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path="config/.env", verbose=True)

class EchoBot(Client): 
    async def on_message(self, mid=None, author_id=None, message_object=None, thread_id=None,
                         thread_type=ThreadType.USER, at=None, metadata=None, msg=None):
        await self.mark_as_delivered(thread_id, message_object.uid)
        await self.mark_as_read(thread_id)

        # If you're not the author, echo
        if author_id == self.uid:
            await self.delete_messages([mid])
            print("Sending new message") 

            await self.send(
                Message(text="Trashed that!"), 
                thread_id=thread_id, 
                thread_type=thread_type
            )
            print("Sent new message") 

loop = asyncio.get_event_loop()


async def start():
    client = EchoBot(loop=loop)
    print("Logging in...")

    USERNAME = os.getenv("FB_USERNAME")
    PASSWORD = os.getenv("FB_PASS")

    await client.start(USERNAME, PASSWORD)
    client.listen()


loop.run_until_complete(start())
loop.run_forever()

