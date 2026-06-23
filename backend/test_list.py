import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def test_list():
    api_key = os.getenv("EVOLUTION_API_KEY", "changeme-secret-key")
    base_url = "http://localhost:8182" # exposed to host
    instance = "bot-umkm"
    phone = "6285719454968" # the user phone number seen in logs

    headers = {
        "apikey": api_key,
        "Content-Type": "application/json"
    }

    url = f"{base_url}/message/sendList/{instance}"
    payload = {
        "number": phone,
        "title": "FinanceBot",
        "description": "Test list message",
        "buttonText": "Pilih Menu",
        "footerText": "Footer",
        "sections": [
            {
                "title": "Menu",
                "rows": [
                    {
                        "title": "Row 1",
                        "description": "Desc 1",
                        "rowId": "1"
                    }
                ]
            }
        ]
    }

    print(f"Sending request to {url}...")
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Body: {response.text}")

if __name__ == "__main__":
    asyncio.run(test_list())
