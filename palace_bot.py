# # import asyncio
# # import re
# # from telethon import TelegramClient, events
# # import requests
# # import os
# # from dotenv import load_dotenv

# # load_dotenv()

# # # 🔐 Твій Telegram API ID/Hash
# # api_id = os.getenv("API_ID")
# # api_hash = os.getenv("API_HASH")

# # # 🤖 Дані Telegram-бота
# # BOT_TOKEN = os.getenv("BOT_TOKEN")
# # CHAT_ID = os.getenv("CHAT_ID")

# # # 🧾 Правила фільтрації: назва → макс. ціна
# # FILTER_RULES = {
# #     "King": 4.5,
# #     "Doodles Dark Mode": 11,
# #     "Mememania": 4.5,
# #     "Pengu Valentines": 15,
# #     "Cool Blue Pengu": 80,
# #     "Blue Pengu": 35
# # }

# # # 📤 Надсилання повідомлення
# # def send_telegram_message(text):
# #     url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
# #     payload = {"chat_id": CHAT_ID, "text": text}
# #     try:
# #         res = requests.post(url, data=payload)
# #         if not res.ok:
# #             print(f"❗️Помилка надсилання: {res.text}")
# #     except Exception as e:
# #         print(f"❗️Помилка при надсиланні: {e}")

# # # 🌟 Перевірка на "гарні номери"
# # def is_special_number(n):
# #     str_n = str(n)

# #     # 1–30
# #     if 1 <= n <= 30:
# #         return True

# #     # Сотні, тисячі
# #     if n % 100 == 0 or n % 1000 == 0:
# #         return True

# #     # Дзеркальні типу 1221
# #     if str_n == str_n[::-1]:
# #         return True

# #     # Всі однакові цифри (наприклад, 111, 2222)
# #     if len(set(str_n)) == 1:
# #         return True

# #     return False

# # # 🧠 Фільтрація повідомлень
# # def filter_message(msg_text):
# #     name_match = re.search(r'Name:\s*(.+?)\s+#(\d+)', msg_text)
# #     cost_match = re.search(r'Cost:\s*([\d.]+)\s*TON', msg_text)

# #     if not name_match or not cost_match:
# #         return None

# #     raw_name = name_match.group(1).strip()
# #     number = int(name_match.group(2))
# #     cost = float(cost_match.group(1))
# #     normalized_name = raw_name.lower()

# #     # 🔍 Перевірка по назві та ціні
# #     for key in FILTER_RULES:
# #         if key.lower() in normalized_name:
# #             max_price = FILTER_RULES[key]
# #             if cost < max_price:
# #                 return f"🔎 Знайдено фільтрований стікер:\n{raw_name} #{number}, {cost} TON"

# #     # 💎 Перевірка на гарні номери
# #     if is_special_number(number):
# #         return f"🌟 Знайдено гарний номер:\n{raw_name} #{number}, {cost} TON"

# #     return None

# # # 🤖 Telegram-клієнт
# # client = TelegramClient('session_name', api_id, api_hash)

# # @client.on(events.NewMessage(chats='palaceoffers'))
# # async def handler(event):
# #     msg = event.message.message
# #     result = filter_message(msg)
# #     if result:
# #         send_telegram_message(result)
# #         print(f"✅ Сповіщення: {result}")
# #     else:
# #         print("— Пропущено")

# # async def main():
# #     print("✅ Бот слухає @palaceoffers у реальному часі...")
# #     await client.start()
# #     await client.run_until_disconnected()

# # if __name__ == '__main__':
# #     asyncio.run(main())


# import asyncio
# import re
# import requests
# import os
# from dotenv import load_dotenv
# from telethon import TelegramClient, events
# from telethon.sessions import StringSession
# from fastapi import FastAPI
# import uvicorn
# import threading

# load_dotenv()

# api_id = int(os.getenv("API_ID"))
# api_hash = os.getenv("API_HASH")
# BOT_TOKEN = os.getenv("BOT_TOKEN")
# CHAT_ID = os.getenv("CHAT_ID")
# SESSION_STRING = os.getenv("SESSION_STRING")  # Рядок сесії

# FILTER_RULES = {
#     "King": 8,
#     "Doodles Dark Mode": 15,
#     "Mememania": 7,
#     "Pengu Valentines": 20,
#     "Cool Blue Pengu": 80,
#     "Blue Pengu": 39
# }

# def send_telegram_message(text):
#     url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
#     payload = {"chat_id": CHAT_ID, "text": text}
#     try:
#         res = requests.post(url, data=payload)
#         if not res.ok:
#             print(f"❗️Помилка надсилання: {res.text}")
#     except Exception as e:
#         print(f"❗️Помилка при надсиланні: {e}")

# def is_special_number(n):
#     str_n = str(n)
#     if 1 <= n <= 30:
#         return True
#     if n % 100 == 0 or n % 1000 == 0:
#         return True
#     if str_n == str_n[::-1]:
#         return True
#     if len(set(str_n)) == 1:
#         return True
#     return False

# def filter_message(msg_text):
#     name_match = re.search(r'Name:\s*(.+?)\s+#(\d+)', msg_text)
#     cost_match = re.search(r'Cost:\s*([\d.]+)\s*TON', msg_text)
#     if not name_match or not cost_match:
#         return None
#     raw_name = name_match.group(1).strip()
#     number = int(name_match.group(2))
#     cost = float(cost_match.group(1))
#     normalized_name = raw_name.lower()

#     for key in FILTER_RULES:
#         if key.lower() in normalized_name:
#             max_price = FILTER_RULES[key]
#             if cost < max_price:
#                 return f"🔎 Знайдено фільтрований стікер:\n{raw_name} #{number}, {cost} TON"

#     # if is_special_number(number):
#     #     return f"🌟 Знайдено гарний номер:\n{raw_name} #{number}, {cost} TON"

#     # 💎 Перевірка на гарні номери з обмеженням по ціні
#     if is_special_number(number) and cost <= 20:
#         return f"🌟 Знайдено гарний номер:\n{raw_name} #{number}, {cost} TON"

#     return None

# client = TelegramClient(StringSession(SESSION_STRING), api_id, api_hash)

# @client.on(events.NewMessage(chats='palaceoffers'))
# async def handler(event):
#     msg = event.message.message
#     result = filter_message(msg)
#     if result:
#         send_telegram_message(result)
#         print(f"✅ Сповіщення: {result}")
#     else:
#         print("— Пропущено")

# app = FastAPI()

# @app.get("/")
# async def root():
#     return {"status": "Bot is running"}

# async def start_bot():
#     await client.start()
#     print("✅ Бот слухає @palaceoffers у реальному часі...")
#     await client.run_until_disconnected()

# def run_bot_loop():
#     asyncio.run(start_bot())

# if __name__ == "__main__":
#     # Запускаємо Telegram-бота в окремому потоці
#     threading.Thread(target=run_bot_loop, daemon=True).start()

#     # Запускаємо FastAPI сервер на 0.0.0.0:10000 (порт можна змінити)
#     uvicorn.run(app, host="0.0.0.0", port=10000)

import asyncio
import re
import requests
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from fastapi import FastAPI
import uvicorn
import threading

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SESSION_STRING = os.getenv("SESSION_STRING")  # Строка сесії

# 🔍 Назва → [макс ціна, макс ціна за гарний номер]
FILTER_RULES = {
    "King": [8, 30],
    "Doodles Dark Mode": [15, 40],
    "Mememania": [7, 18],
    "Pengu Valentines": [20, 50],
    "Cool Blue Pengu": [80, 110],
    "Pengu CNY": [60, 110],
    "Blue Pengu": [39, 55],
    "Error Pixel": [6, 15],
    "Retro Pixel": [6, 15]
}

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        res = requests.post(url, data=payload)
        if not res.ok:
            print(f"❗️Помилка надсилання: {res.text}")
    except Exception as e:
        print(f"❗️Помилка при надсиланні: {e}")

def is_special_number(n, allow_advanced=False):
    str_n = str(n)

    # Базові гарні номери
    if 1 <= n <= 30:
        return True
    if n % 100 == 0 or n % 1000 == 0:
        return True
    if len(set(str_n)) == 1:
        return True

    if allow_advanced:
        # Дзеркальні (типу 1221, 6556)
        if str_n == str_n[::-1]:
            return True

        # Послідовність (123, 4567)
        is_increasing = ''.join(sorted(str_n)) == str_n and len(set(str_n)) == len(str_n)
        if is_increasing:
            return True

    return False

def filter_message(msg_text):
    name_match = re.search(r'Name:\s*(.+?)\s+#(\d+)', msg_text)
    cost_match = re.search(r'Cost:\s*([\d.]+)\s*TON', msg_text)

    if not name_match or not cost_match:
        return None

    raw_name = name_match.group(1).strip()
    number = int(name_match.group(2))
    cost = float(cost_match.group(1))
    normalized_name = raw_name.lower()

    matched_key = None
    for key in FILTER_RULES:
        if key.lower() in normalized_name:
            matched_key = key
            break

    if matched_key:
        max_normal_price, max_special_price = FILTER_RULES[matched_key]

        # 🔍 Перевірка по ціні
        if cost < max_normal_price:
            return f"🔎 Знайдено фільтрований стікер:\n{raw_name} #{number}, {cost} TON"

        # 💎 Гарний номер (розширений)
        if is_special_number(number, allow_advanced=True) and cost <= max_special_price:
            return f"🌀 Знайдено гарний номер (розширено):\n{raw_name} #{number}, {cost} TON"


    else:
        # 📦 Інші колекції — тільки базові гарні номери ≤ 20 TON
        if is_special_number(number) and cost <= 20:
            return f"🌟 Знайдено гарний номер:\n{raw_name} #{number}, {cost} TON"

    return None

client = TelegramClient(StringSession(SESSION_STRING), api_id, api_hash)

@client.on(events.NewMessage(chats='palaceoffers'))
async def handler(event):
    msg = event.message.message
    result = filter_message(msg)
    if result:
        send_telegram_message(result)
        print(f"✅ Сповіщення: {result}")
    else:
        print("— Пропущено")

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Bot is running"}

async def start_bot():
    await client.start()
    print("✅ Бот слухає @palaceoffers у реальному часі...")
    await client.run_until_disconnected()

def run_bot_loop():
    asyncio.run(start_bot())

if __name__ == "__main__":
    threading.Thread(target=run_bot_loop, daemon=True).start()
    uvicorn.run(app, host="0.0.0.0", port=10000)
