import os
from time import sleep
from asyncio import sleep, wait
import asyncio
import better_profanity
from better_profanity import profanity
from SpamRefiner.events import register
from SpamRefiner import spam, SUDO_USERS
from SpamRefiner.nospam.helpers.admin_rights import user_is_ban_protected
from telethon import functions, types, events
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
from SpamRefiner import MONGO_DB_URL
client = MongoClient()
client = MongoClient(MONGO_DB_URL)
db = client["spamrefiner"]
sellers = db.seller




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

async def get_user_from_event(event):
    """ Get the user from argument or replied message. """
    try:
        args = (event.message.text).split(" ", 1)[1]
    except:
        args = None
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            return await event.reply("`Pass the user's username, id or reply!`")

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            return await event.reply(str(err))

    return user_obj, extra





async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        return await event.reply(str(err))

    return user_obj

#=========================RefineSellings======================

custom_badwords = ['sell', 'selling', 'buy', 'selling-prime', '100rs', '150rs', 'Cheap', 'Fixed-Rate']

@register(pattern="^/refineselling(?: |$)(.*)")
async def nosell(sell):
  if sell.fwd_from:
    return
  if sell.is_private:
    return
  if MONGO_DB_URL is None:
    return
  if not await can_change_info(message=sell):
    await sell.reply("**You Don't have permission to use this**")
    return 
  input = sell.pattern_match.group(1)
  chats = sellers.find({})
  if not input:
    for c in chats:
      if sell.chat_id == c["id"]:
        await sell.reply(
          "Please provide some input yes or no.\n\nCurrent setting is : **on**"
          )
        return
    await sell.reply(
        "Please provide some input yes or no.\n\nCurrent setting is : **off**"
        )
  elif input == "on":
      if sell.is_group:
        for c in chats:
          if sell.chat_id == c["id"]:
            return await sell.reply(
              "SellingRefiner filter is already activated for this chat."
              )
        sellers.insert_one({"id": sell.chat_id})
        await sell.reply("SellingRefiner filter turned on for this chat.")
          
  elif input == "off":
      if sell.is_group:
        for c in chats:
          if sell.chat_id == c["id"]:
            sellers.delete_one({"id": sell.chat_id})
            return await sell.reply("SellingRefiner filter turned off for this chat.")
        await sell.reply("SellingRefiner filter isn't turned on for this chat.")
  else:
        await sell.reply("I only understand by on or off")
        

@spam.on(events.NewMessage(pattern=None))
async def del_sell(sell):
  if sell.is_private:
    return
  if MONGO_DB_URL is None:
    return
  msg = str(sell.text)
  sender = await sell.get_sender()
  let = sender.username
  user_id = await get_user_from_event(sell)
  if sell.is_group:
    if (await is_register_admin(sell.input_chat, sell.message.sender_id)):
      return
    if user_id in SUDO_USERS:
        return
    pass
  chats = sellers.find({})
  for c in chats:
    if sell.text:
      if sell.chat_id == c['id']:
        if better_profanity.profanity.contains_profanity(custom_badwords):
          await sell.delete()
          if sender.username is None:
            st = sender.first_name
            hh = sender.id
            final = f"[{st}](tg://user?id={hh}) **{msg}** is detected as a selling word and your message has been deleted"
          else:
            final = f'@{let} **{msg}** is Detected as a selling word and your message has been deleted'
            dev = await sell.respond(final)
            await asyncio.sleep(3)
            await dev.delete()


__plugin_name__ = "nosell"

help_plus = """
Here is help for **SpamRefine**
SpamRefine Make Your Group Spam Free:
**Example:** `/refineselling on`
"""
