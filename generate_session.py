from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("Відкрий цей код, скопіюй і збережи рядок сесії нижче:\n")
    print(client.session.save())
