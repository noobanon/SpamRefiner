from sys import argv, exit
from SpamRefiner import spam
from SpamRefiner import TOKEN, LOGGER, pbot
import importlib
import asyncio
import SpamRefiner.events
from SpamRefiner.nospam import to_load
import uvloop
from pyrogram import idle


HELP = {}
IMPORTED = {}


for load in to_load:
    imported = importlib.import_module("SpamRefiner.nospam." + load)
    if not hasattr(imported, "__plugin_name__"):
        imported.__plugin_name__ = imported.__name__

    if not imported.__plugin_name__.lower() in IMPORTED:
        IMPORTED[imported.__plugin_name__.lower()] = imported

    if hasattr(imported, "help_plus") and imported.help_plus:
        HELP[imported.__plugin_name__.lower()] = imported

loop = asyncio.get_event_loop()

async def start_bot():
    print("+===============================================================+")
    print("|                 SpamRefiner  Is Now Alive                     |")
    print("+===============+===============+===============+===============+")
    print("BOT STARTED !")
    await idle()

try:
    spam.start(bot_token=TOKEN)
    LOGGER.info("Bot is now alive")
except Exception:
    print("Make Sure Your Bot Token is Valid")
    exit(1)

if len(argv) not in (1, 3, 4):
    spam.disconnect()
else:
    spam.run_until_disconnected()

if __name__ == "__main__":
    uvloop.install()
    loop.run_until_complete(start_bot())
