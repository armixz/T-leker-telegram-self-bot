#! /bin/python
from telethon import TelegramClient,events
from telethon.tl.functions.users import GetFullUserRequest
from help_center import help_text
from os import  getcwd, remove
from subprocess import getoutput
from requests import get
from colorama import init,Fore
from datetime import datetime, time
init()

#  Remember to use your own values from my.telegram.org!
api_id = "2421227"
api_hash = "5cfbdb99e4477b828bf06a9cd1efeead"

client = TelegramClient('session_name', api_id, api_hash)




def loger(log_text):
    now = datetime.now()
    # H:M:S
    time_now = now.strftime("%H:%M:%S")
    log_text = f"[{time_now}] {log_text}\n"
    log_file = open("t-leker_log.log" , "ab")
    log_file.write(log_text.encode())
    log_file.close()
    print(log_text)


loger(Fore.RED+"[*]"+Fore.GREEN+"T-leker Started..."+Fore.RESET+'\t You can get ping')


## get help
@client.on(events.NewMessage(outgoing=True,pattern=r'(?i).*/help'))
async def help(event):

    result = help_text.all_help
    await event.edit(str(result))


## ping To check if the robot is online
@client.on(events.NewMessage(outgoing=True,pattern=r'(?i).*/ping'))
async def ping(event):
    sender = await event.get_sender()
    chat = event.message.chat_id
    loger(Fore.RED+"[*]"+Fore.YELLOW+f"{sender.username}"+Fore.RESET+" Get ping on this chat : "+Fore.GREEN+f"{chat}"+Fore.RESET)
    result = f"T-leker is online ✅ \n 🤖 chat id : {chat} "
    await event.edit(result)


## Get a chat history
@client.on(events.NewMessage(outgoing=True,pattern=r'(?i).*/his'))
async def his(event):
    try:
        command = str(event.raw_text).split(" ")
        chat = event.message.chat_id
        result = f'📡 History {command[1]} previous messages for this conversation \n\n'
        async for message in client.iter_messages(chat,limit = int(command[1])) :
            result += str(f"{message.sender_id} : {message.text} \n")
        await event.edit(result)

        sender = await event.get_sender()
        chat = event.message.chat_id
        loger(Fore.RED+"[*]"+Fore.YELLOW+f"{sender.username}"+Fore.RESET+f" Get {command[1]} message history on this chat : "+Fore.GREEN+f"{chat}"+Fore.RESET)
    except IndexError:
        await event.edit("❌ Set number!")
        sender = await event.get_sender()
        chat = event.message.chat_id
        loger(Fore.RED+"[*]"+Fore.YELLOW+f"{sender.username}"+Fore.RESET+f" Get message history on this chat : "+Fore.GREEN+f"{chat}"+Fore.RED+" but not set number"+Fore.RESET)
## get full info From a users
@client.on(events.NewMessage(outgoing=True,pattern=r'(?i).*/info'))
async def info(event):
    chat = event.message.chat_id
    sender = await event.get_sender()
    loger(Fore.RED+"[*]"+Fore.YELLOW+f"{sender.username}"+Fore.RESET+" Get information this chat : "+Fore.GREEN+f"{chat}"+Fore.RESET)
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
        chat = event.message.chat_id
        sender = await event.get_sender()
        loger(Fore.RED+"[*]"+Fore.YELLOW+f"{sender.username}"+Fore.RESET+" Get information this chat : "+Fore.GREEN+f"{chat}"+Fore.RED+" But this chat a group"+Fore.RESET)
    await event.edit(str(result))


## Spammer to send a large number of messages
@client.on(events.NewMessage(outgoing=True,pattern=r'(?i).*/spm'))
async def spm(event):
    command = str(event.raw_text)
    command = command.split(" ")
    text = command[1]
    number = command[2]
    for i in range(0,int(number)):
        await event.respond(str(text))
        chat = event.message.chat_id
        sender = await event.get_sender()
    
    loger(Fore.RED+"[*]"+Fore.YELLOW+f"{sender.username}"+Fore.RESET+f" Start Spam attack in range 0,{number} on this chat : "+Fore.GREEN+f"{chat}"+Fore.RESET)

## Delete a large number of messages
@client.on(events.NewMessage(outgoing=True,pattern=r'(?i).*/delete'))
async def delete(event):
    try:
        command = str(event.raw_text).split(" ")
        chat = event.message.chat_id
        sender = await event.get_sender()
        loger(Fore.RED+"[*]"+Fore.YELLOW+f"{sender.username}"+Fore.RESET+f" Delete {command[1]} on this chat : "+Fore.GREEN+f"{chat}"+Fore.RESET)
        async for message in client.iter_messages(chat,limit = int(command[1])+1) :
            await client.delete_messages(chat, message)
    except IndexError:
        await event.edit("❌ Set number!")
        loger(Fore.RED+"[*]"+Fore.YELLOW+f"{sender.username}"+Fore.RESET+f" try to Delete {command[1]} on this chat : "+Fore.GREEN+f"{chat}"+Fore.RED+" but Forget Set Number For Delete")
## profile saver
@client.on(events.NewMessage(outgoing=True,pattern=r'(?i).*/save_profile'))
async def save_profile(event):
    await event.edit("Downloading....")
    try:
        if event.is_reply:
            replied = await event.get_reply_message()
            sender = replied.sender
            log_sender = await event.get_sender()
            loger(Fore.RED+"[*]"+Fore.YELLOW+f"{log_sender.username}"+Fore.RESET+f" save profile this user : "+Fore.GREEN+f"{sender.username} : {sender.id}"+Fore.RESET)
            path = getcwd()
            await client.download_profile_photo(sender,path)
            await event.edit('Profile saved ✅'.format(sender.username))
    except Exception as ex:
        await event.edit("Download failed ❌ \n Error {}".format(ex))
        loger(Fore.RED+"[*]"+Fore.YELLOW+f"{log_sender.username}"+Fore.RESET+f" save profile this user : "+Fore.GREEN+f"{sender.username} : {sender.id}"+Fore.RED+f"But Download failed \n ERROR : {ex}"+Fore.RESET)
    if not event.is_reply:
        await event.edit("💢Please reply to the user you want to save profile.💢")
        loger(Fore.RED+"[*]"+Fore.YELLOW+f"{log_sender.username}"+Fore.RESET+f" save profile this user : "+Fore.GREEN+f"{sender.username} : {sender.id}"+Fore.RED+f"But Not reply to the user want to save profile."+Fore.RESET)

@client.on(events.NewMessage(outgoing=True,pattern=r'(?i).*/cmd'))
async def cmd(event):
    command = str(event.raw_text)
    command = command.replace("/cmd ",'')
    output = getoutput(command)
    await event.edit(f"{output}")
    log_sender = await event.get_sender()
    loger(Fore.RED+"[*]"+Fore.YELLOW+f"{log_sender.username}"+Fore.RESET+f" run this command on system : {command} "+Fore.RESET)


@client.on(events.NewMessage(outgoing=True,pattern=r'(?i).*/get_site'))
async def cmd(event):
    command = str(event.raw_text)
    command = command.replace("/get_site ",'') 
    try :
        response = get(f"{command}")
        fo = open("index.html", "wb")
        fo.write(response.content)
        fo.close()
        chat = event.message.chat_id
        await client.send_file(chat,'./index.html')
        remove('./index.html')
        log_sender = await event.get_sender()
        loger(Fore.RED+"[*]"+Fore.YELLOW+f"{log_sender.username}"+Fore.RESET+f" Get this site : {command} "+Fore.RESET)
    
    except Exception as ex:
        await event.edit(str(ex))
        loger(Fore.RED+"[*]"+Fore.YELLOW+f"{log_sender.username}"+Fore.RESET+f" Get this site : {command} "+Fore.RED+" But Get Error"+Fore.RESET)


@client.on(events.NewMessage(outgoing=True,pattern=r'(?i).*/turn_off'))
async def turn_off(event):
    await event.edit("T-leker turned off 💢")
    sender = await event.get_sender()
    loger(Fore.RED+"[*]"+Fore.YELLOW+f"{sender.username}"+Fore.RESET+f" Turned off T-leker"+Fore.RESET)
    
    exit(0)

client.start()
client.run_until_disconnected()
