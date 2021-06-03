from SpamRefiner import spam
from telethon import custom, events, Button
from telethon import types
from telethon.tl import functions


PM_START_TEXT = """Hi I'm a SpamRefiner Bot Built in Python Using Telethon For More Use /help"""

@register(pattern="^/start$")
async def start(event):
  if not event.is_group:
    await spam.send_message(
      event.chat_id,
      PM_START_TEXT,
      buttons=[
        [
          Button.url(
            "Add To Group  👥", "t.me/SpamRefineRobot?startgroup=true"
            ),
          ],
        ],
      )
  else:
    await event.reply("Hey I'm Alive")

HELP_TEXT = """Hi I'm Spam Refiner Bot Built in Python"""

@register(pattern="^/help$")
async def help(event):
  if not event.is_group:    
    await event.reply(HELP_TEXT)
  else:
    await event.reply(
      "Contact me in PM to get the help menu",
      buttons=[[Button.url("Help ", "t.me/SpamKiller?start=help")]],
      )

__plugin_name__ = "_main"

help_plus = """
This Is Help Menu Of *SpamRefiner*
"""
