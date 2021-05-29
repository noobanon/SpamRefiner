import logging
import os
import sys
import time
import os
import urllib.parse as urlparse
import json
from logging import basicConfig
from logging import DEBUG
from logging import getLogger
from logging import INFO
from telethon import TelegramClient

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
    
    DB_URI = os.environ.get("DATABASE_URL")
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TEMP_DOWNLOAD_DIRECTORY", "./")
    SUDO_USERS = list(SUDO_USERS)
    
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
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
            
api_id = API_ID
api_hash = API_HASH
spam = TelegramClient("SpamRefiner", API_ID, API_HASH)
    
