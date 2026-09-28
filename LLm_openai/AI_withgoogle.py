from google import genai
import os
import asyncio
import pathlib
from dotenv import load_dotenv

# Load all project credentials from the single root environment file.
load_dotenv(dotenv_path=pathlib.Path(__file__).resolve().parent.parent / ".env")
api_key = os.getenv("api_key_google")
client = genai.Client(api_key=api_key)

async def video_understanding(filepath):
    try:
        file_path = pathlib.Path(filepath)


        # 1. Upload the file.
        upload_result = await client.aio.files.upload(
            file=file_path,
            config={'display_name': file_path.name} # Use the original file name.
        )
        
        print(f"⏳ فایل آپلود شد. وضعیت فعلی: {upload_result.state}")

        # 2. Wait until Google changes the file state from PROCESSING to ACTIVE.
        current_file = upload_result
        while current_file.state.name == "PROCESSING":
            print("... گوگل در حال پردازش ویدیو است (2 ثانیه صبر) ...")
            await asyncio.sleep(2)
            # Fetch the latest file state.
            current_file = await client.aio.files.get(name=upload_result.name)

        if current_file.state.name == "FAILED":
            return "❌ پردازش ویدیو شکست خورد."

        print("✅ ویدیو آماده شد! ارسال به جمینای...")

        # 3. Send the processed file to the model.
        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash", # Use the configured Gemini model.
            contents=[
                current_file,"این فایل را خلاصه کن"
            ]
        )
        
        return response.text

    except Exception as e:
        print(f"❌ Error: {e}")
        return f"Error: {e}"
