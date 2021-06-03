import os
from time import sleep
from asyncio import sleep, wait
import asyncio
import better_profanity
from telethon import events
from better_profanity import profanity
from SpamRefiner.events import register
from SpamRefiner import spam
from telethon import functions, types
from telethon.tl import types
from telethon.tl.functions.users import GetFullUserRequest
from telethon.utils import pack_bot_file_id
from telethon.utils import get_input_location
from telethon import (TelegramClient, events, functions)
from telethon.tl.types import DocumentAttributeAudio

from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.messages import ForwardMessagesRequest, SendMessageRequest

from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.errors import (BadRequestError, ChatAdminRequiredError,
                             ImageProcessFailedError, PhotoCropSizeSmallError,
                             UserAdminInvalidError)
from telethon.errors.rpcerrorlist import (UserIdInvalidError,
                                          MessageTooLongError)
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
from telethon.tl.functions.messages import (UpdatePinnedMessageRequest, EditMessageRequest)
from telethon.tl.types import (PeerChannel, ChannelParticipantsAdmins,
                               ChatAdminRights, ChatBannedRights,
                               MessageEntityMentionName, MessageMediaPhoto,
                               ChannelParticipantsBots, User, UserFull)
from telethon.tl.types import ChannelParticipantsBanned, ChannelParticipantCreator, ChannelParticipantsKicked

from pymongo import MongoClient
from SpamRefiner import MONGO_DB_URI
client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["spamrefiner"]
spammers = db.spammer

CMD_STARTERS = "/"

#========================================Module======================================================================================
#def imports

async def can_change_info(message):
    result = await spam(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (isinstance(
        p, types.ChannelParticipantAdmin) and p.admin_rights.change_info)

async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):

        return isinstance(
            (
                await spam(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerChat):

        ui = await spam.get_peer_id(user)
        ps = (
            await spam(functions.messages.GetFullChatRequest(chat.chat_id))
        ).full_chat.participants.participants
        return isinstance(
            next((p for p in ps if p.user_id == ui), None),
            (types.ChatParticipantAdmin, types.ChatParticipantCreator),
        )
    return None

#import abuse file
profanity.load_censor_words_from_file("./abuse_wordlist.txt")

@register(pattern="^/refineabuse ?(.*)")
async def profanity(event):
  if event.fwd_from:
    return
  if event.is_private:
    return
  if MONGO_DB_URI is None:
    return
  if not await can_change_info(message=event):
    await event.reply("**You Don't have permission to use this**")
    return 
  input = event.pattern_match.group(1)
  chats = spammers.find({})
  if not input:
    for c in chats:
      if event.chat_id == c["id"]:
        await event.reply(
          "Please provide some input yes or no.\n\nCurrent setting is : **on**"
          )
        return
      await event.reply(
        "Please provide some input yes or no.\n\nCurrent setting is : **off**"
        )
      return
    if input == "on":
      if event.is_group:
        chats = spammers.find({})
        for c in chats:
          if event.chat_id == c["id"]:
            await event.reply(
              "AbuseRefiner filter is already activated for this chat."
              )
            return
          spammers.insert_one({"id": event.chat_id})
          await event.reply("AbuseRefiner filter turned on for this chat.")
          
    if input == "off":
      if event.is_group:
        chats = spammers.find({})
        for c in chats:
          if event.chat_id == c["id"]:
            spammers.delete_one({"id": event.chat_id})
            await event.reply("AbuseRefiner filter turned off for this chat.")
            return
        await event.reply("AbuseRefiner filter isn't turned on for this chat.")
        if not input == "on" and not input == "off":
            await event.reply("I only understand by on or off")
            return
        

@spam.on(events.NewMessage(pattern=None))
async def del_profanity(event):
  if event.is_private:
    return
  if MONGO_DB_URI is None:
    return
  msg = str(event.text)
  sender = await event.get_sender()
  let = sender.username
  if event.is_group:
    if (await is_register_admin(event.input_chat, event.message.sender_id)):
      return
    pass
  chats = spammers.find({})
  for c in chats:
    if event.text:
      if event.chat_id == c['id']:
        if better_profanity.profanity.contains_profanity(msg):
          await event.delete()
          if sender.username is None:
            st = sender.first_name
            hh = sender.id
            final = f"[{st}](tg://user?id={hh}) **{msg}** is detected as a slang word and your message has been deleted"
          else:
            final = f'@{let} **{msg}** is detected as a slang word and your message has been deleted'
            dev = await event.respond(final)
            await asyncio.sleep(5)
            await dev.delete()


__plugin_name__ = "nospam"

help_plus = """
Here is help for **SpamRefine**
SpamRefine Make Your Group Spam Free:
**Example:** `/refineabuse on`
"""
