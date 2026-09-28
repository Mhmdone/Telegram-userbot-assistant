import asyncio
from openai import AsyncOpenAI
import os
import httpx
from pathlib import Path
from dotenv import load_dotenv

# Load all project credentials from the single root environment file.
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
api_key = os.getenv("api_key_openai")
base_url = os.getenv("base_url_openai")

client = AsyncOpenAI(
    api_key = api_key,
    base_url = base_url
    )


async def Get_response(user_text, system_text, maxtoken=4000):
    
    try:    

        response = await client.chat.completions.create(
            model="gemini-2.5-flash", 
            n=1,
            max_tokens = maxtoken,
            messages=[
                {"role": "system", "content": system_text },
                {"role": "user", "content": user_text }
            ]
        )
        x = response.choices[0].message.content

    except Exception as e:
        print(f"❌ Error:Some problem occurred{e}")

    
    return x
