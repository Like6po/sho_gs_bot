import os

from dotenv import load_dotenv

load_dotenv('.env.dist')

BOT_TOKEN = os.getenv("BOT_TOKEN")

admins = [
    os.getenv("ADMIN_ID"),
]

WIT_TOKEN=os.getenv("WIT_TOKEN")
