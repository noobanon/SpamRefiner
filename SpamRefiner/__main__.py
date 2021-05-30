from sys import argv, exit
from SpamRefiner import spam
from SpamRefiner import TOKEN

import SpamRefiner.events

try:
    spam.start(bot_token=TOKEN)
    LOGGER.info("Bot is alive")
except Exception:
    print("Your Bot Token Isn't Invalid")
    exit(1)

if len(argv) not in (1, 3, 4):
    spam.disconnect()
else:
    spam.run_until_disconnected()
