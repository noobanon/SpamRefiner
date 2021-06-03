import logging
import os
import sys
import time
import os
from motor import motor_asyncio
import urllib.parse as urlparse
import json
from logging import basicConfig
from logging import DEBUG
from logging import getLogger
from logging import INFO
from telethon import TelegramClient, events, sync
from pyrogram import Client

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

LOGGER = logging.getLogger(__name__)
ENV = bool(os.environ.get("ENV", True))

if ENV:
    TOKEN = os.environ.get("TOKEN", None)
    
    SUDO_USERS = {int(x) for x in os.environ.get("SUDO_USERS", "").split()}
    
    API_KEY = os.environ.get("API_KEY", None)
    API_HASH = os.environ.get("API_HASH", None)
    CONSOLE_LOGGER_VERBOSE = os.environ.get("CONSOLE_LOGGER_VERBOSE", "False")
    DB_URI = os.environ.get("DATABASE_URL")
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    SUDO_USERS = list(SUDO_USERS)
    
    MONGO_DB_URL = os.environ.get("MONGO_DB_URI", None)
    TEMPORARY_DATA = os.environ.get("TEMPORARY_DATA", None)
        
    if CONSOLE_LOGGER_VERBOSE:
        basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=DEBUG
        )
    else:
        basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=INFO
        )
    LOGS = getLogger(__name__)

MONGO_CLIENT = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL)
db = MONGO_CLIENT.spamrefiner
#start bot
print("INITIALIZING ....")
pbot = Client("spamrefiner", bot_token=TOKEN, api_id, api_hash)
api_id = API_KEY
api_hash = API_HASH
spam = TelegramClient("SpamRefiner", api_id, api_hash)
spam.start(bot_token=TOKEN)    
pbot.start()
