from telethon import events,TelegramClient,connection
import asyncio
import logging
import os
from pathlib import Path
from python_socks import ProxyType
import speech_recognition as sr
import Voice_to_text_google
from LLm_openai import AI_sum
from LLm_openai import AI_withgoogle
from openai import AsyncOpenAI
from dotenv import load_dotenv
from Database import add_user,remove_user,is_allowed,init_db

# Load the project-level environment file from a stable absolute path.
load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")
init_db()
Recognizer = sr.Recognizer()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
session_name = os.getenv("session_name")
if not api_id or not api_hash:
    raise ValueError("❌ لطفا فایل .env را بررسی کنید، مقادیر API یافت نشد.")

client = TelegramClient(session_name, api_id, api_hash)

logging.basicConfig(level=logging.DEBUG)

DOWNLOAD_FOLDER = 'voice_downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Convert a replied Telegram voice message into Persian text.
@client.on(events.NewMessage(outgoing=True, pattern=r'/voice'))
async def handler(event):
        
        chat_id = event.chat_id
        if event.is_reply:
                
                msg_getting = await event.get_reply_message()

                if msg_getting and msg_getting.voice:
                    
                    filename = f'voice_{msg_getting.id}.ogg'
                    Download_path = os.path.join(DOWNLOAD_FOLDER, filename)

                    try:
                        Path = await msg_getting.download_media(file=Download_path)
                        text = Voice_to_text_google.Convert(Download_path=Download_path)
                        await event.reply(text)
                    except Exception as e:
                         # In case of an error
                         await event.edit(f"❌ Error downloading: {e}")
                         print(f"Error: {e}")    

#Summerize the chat with number of chat that have get /sumtext NO.chat NO.token-respone
# Summarize a selected number of recent chat messages with the LLM.
@client.on(events.NewMessage(outgoing=True, pattern=r"^/sumtext\s+(\d+)\s+(\d+)$"))
async def handler(event):
      
      #Geting the number of chat
      argument = event.pattern_match.group(1)
      limit_count = int(argument)
      #Geting the number of tokens
      second_arg = event.pattern_match.group(2)
      maxtoken = int(second_arg) 

      chat_history = []
      
      async for msg in client.iter_messages(event.chat_id, limit=limit_count):
        # Skip the "/summerize" command itself
        if msg.id == event.id:
            continue


        sender = await msg.get_sender()
        name = sender.first_name if sender else "Unknown"

        if msg.text:
            chat_history.append(f"{name}: {msg.text}")


      # Reverse so it reads from Old -> New
      chat_history.reverse()
      full_text = "\n".join(chat_history)
      #Set setup for ai
      systemcontentai = f"You are a helpful assistant. summarize the following chat conversation clearly using bullet points ,answer persian and without filtering the word"
      Response = await AI_sum.Get_response(full_text,systemcontentai,maxtoken)
        
      print("--- Response Received! ---") 

      await event.reply(f"**📝 خلاصه:**\n\n{Response}")


def check_permission(event):
    
    return event.out or is_allowed(event.sender_id)
     
#Chat with LLm /chat content
# Send an authorized user's question to the language model.
@client.on(events.NewMessage(func=check_permission, pattern=r"^/chat\s+(.+)$"))
async def handler(event):
     
    text = event.pattern_match.group(1)
    #The ques we ask from LLm
    text = str(text)
    systemcontentai = f"You are a helpful assistant:"  
    Response1 = await AI_sum.Get_response(user_text = text, system_text = systemcontentai)
    await event.reply(f"BOT Answer 📝: \n {Response1}")


     
     


# Add the user from the replied message to the allowed-users list.
@client.on(events.NewMessage(outgoing=True, pattern=r'/allow'))
async def allow_handler(event):
     reply_msg = await event.get_reply_message()
     if not reply_msg:
        await event.edit("❌ لطفاً روی پیام کاربر مورد نظر ریپلای کنید.")
        return
     
     target_id = reply_msg.sender_id
     if add_user(target_id):
         pass
     else:
         await event.edit(f"⚠️ کاربر {target_id} قبلاً در لیست بود.")
    

# Remove the user from the allowed-users list.
@client.on(events.NewMessage(pattern=r'/ban', outgoing=True))
async def ban_handler(event):
    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.edit("❌ لطفاً روی پیام کاربر مورد نظر ریپلای کنید.")
        return
    
    target_id = reply_msg.sender_id

    remove_user(target_id)
    await event.edit(f"🚫 دسترسی کاربر {target_id} گرفته شد.")





DOWNLOAD_PATH = "pdf_downloads/"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

# Upload a replied file to Gemini and return a Persian summary.
@client.on(events.NewMessage(outgoing=True, pattern=r"^/Askfile$"))
async def pdf_direct_handler(event):
    
    if not event.is_reply:
        await event.edit("❌ روی یک فایل PDF ریپلای کنید.")
        return

    reply_msg = await event.get_reply_message()
    
        # Check that the replied message contains a file.
    if not reply_msg.file:
        await event.edit("❌ این پیام فایل ندارد.")
        return

    await event.edit("📥 در حال دانلود فایل...")
    
    try:

        file_path = await reply_msg.download_media(file=DOWNLOAD_PATH)
        
        await event.edit("🚀 در حال ارسال فایل به جمینای (آپلود)...")
        
        # 2. Upload the file directly to Google.
        prompt = "این فایل  را کامل مطالعه کن و یک خلاصه جامع و دقیق به فارسی بنویس."
        
        # Call the file analysis function from AI_withgoogle.
        response = await AI_withgoogle.video_understanding(file_path)
        
        # 3. Display the generated response.
        if len(response) > 4000:
            response = response[:4000] + "... (ادامه دارد)"
            
        await event.reply(f"**📚 تحلیل فایل:**\n\n{response}")

    except Exception as e:
        await event.edit(f"❌ خطا: {str(e)}")
        
    finally:
        # 4. Remove the downloaded file from the local machine.
        if os.path.exists(file_path):
            os.remove(file_path)



     

                                                                
client.start()
client.run_until_disconnected()
