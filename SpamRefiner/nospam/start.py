from SpamRefiner import spam
from telethon import custom, events, Button
from telethon import types
from telethon.tl import functions
from SpamRefiner.events import register
from datetime import datetime

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

HELP_TEXT = """Hi I'm Spam Refiner Bot Built in Python Using Telethon:\n
**SpamRefiner**:\n
Example: `/refineabuse` Get Current Chat Status
`/refineabuse on` Turn on abuse protection
`/refineselling on|off` Turn on Selling Protection """

@register(pattern="^/help")
async def help(event):
  if not event.is_group:    
    await event.reply(HELP_TEXT)
  else:
    await event.reply(
      "Contact me in PM to get the help menu",
      buttons=[[Button.url("Help ", "t.me/SpamRefineRobot?start=help")]],
      )

@register(pattern="^/ping$")
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    pong = await event.reply("Pong!")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await pong.edit("Pong!\n{}".format(ms))
   
__plugin_name__ = "start"

help_plus = """
This Is Help Menu Of *SpamRefiner*
"""
