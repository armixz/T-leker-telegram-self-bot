from telethon import TelegramClient,events,utils
from telethon import functions, types
from telethon.tl.functions.users import GetFullUserRequest
from help_center import help_text
from os import getcwd
#  Remember to use your own values from my.telegram.org!
api_id = "2421227"
api_hash = "5cfbdb99e4477b828bf06a9cd1efeead"

client = TelegramClient('session_name', api_id, api_hash)


## get help
@client.on(events.NewMessage(outgoing=True,pattern=r'(?i).*/help'))
async def help(event):
 
    result = help_text.all_help
    await event.edit(str(result))


## ping To check if the robot is online
@client.on(events.NewMessage(outgoing=True,pattern=r'(?i).*/ping'))
async def ping(event):
    chat = event.message.chat_id
    print(chat)
    result = f"T-leker is online ✅ \n 🤖 chat id : {chat} "
    await event.edit(result)


## Get a chat history
@client.on(events.NewMessage(outgoing=True,pattern=r'(?i).*/his'))
async def his(event):
    command = str(event.raw_text).split(" ")
    chat = event.message.chat_id
    result = f'📡 History {command[1]} previous messages for this conversation \n\n'
    async for message in client.iter_messages(chat,limit = int(command[1])) :
        result += str(f"{message.sender_id} : {message.text} \n")
    
    print(dir(message))
    await event.edit(result)

## get full info From a users
@client.on(events.NewMessage(outgoing=True,pattern=r'(?i).*/info'))
async def info(event):
    chat = event.message.chat_id

    ## a if , for get info with reply
    if event.is_reply:
        replied = await event.get_reply_message()
        sender = replied.sender
        chat = sender.id

    try:
        full = await client(GetFullUserRequest(chat))
        result = f'''👤 User First name : {full.user.first_name}
👤 user number id : {full.user.id}
⛓ is self : {full.user.is_self}
⛓ contact : {full.user.contact}
⛓ mutual contact : {full.user.mutual_contact}
❌ deleted : {full.user.deleted}
🤖 bot : {full.user.bot}
🤖 bot info version : {full.user.bot_info_version}
🤖 bot chat history : {full.user.bot_chat_history}
☎️ phone number : {full.user.phone}
🎇 user profile photo id : {full.user.photo.photo_id}
🎆 user profile has video : {full.user.photo.has_video}
    '''
    except TypeError:
        ## if user send /info command in group
        result = "❌this is a group❌\njust for users"
        
    await event.edit(str(result))


## Spammer to send a large number of messages
@client.on(events.NewMessage(outgoing=True,pattern=r'(?i).*/spm'))
async def spm(event):
    command = str(event.raw_text)
    command = command.split(" ")
    text = command[1]
    number = command[2]
    print(text)
    print(number)
    for i in range(0,int(number)):
        await event.respond(str(text))
    

## Delete a large number of messages
@client.on(events.NewMessage(outgoing=True,pattern=r'(?i).*/delete'))
async def delete(event):
    command = str(event.raw_text).split(" ")
    chat = event.message.chat_id
    async for message in client.iter_messages(chat,limit = int(command[1])+1) :
        await client.delete_messages(chat, message)

## profile saver
@client.on(events.NewMessage(outgoing=True,pattern=r'(?i).*/save_profile'))
async def save_profile(event):
    await event.edit("Downloading....")
    try:
        if event.is_reply:
            replied = await event.get_reply_message()
            sender = replied.sender
            path = getcwd()
            await client.download_profile_photo(sender,path)
            await event.edit('Profile saved ✅'.format(sender.username))
    except Exception as ex:
        await event.edit("Download failed ❌ \n Error {}".format(ex))

    if not event.is_reply:
         await event.edit("💢Please reply to the user you want to save profile.💢")
        
client.start()
client.run_until_disconnected()
