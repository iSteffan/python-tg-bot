import asyncio
import re
from telethon import TelegramClient, events
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# 🔐 Твій Telegram API ID/Hash
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

# 🤖 Дані Telegram-бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# 🧾 Правила фільтрації: назва → макс. ціна
FILTER_RULES = {
    "King": 4.5,
    "Doodles Dark Mode": 11,
    "Mememania": 4.5,
    "Pengu Valentines": 15,
    "Cool Blue Pengu": 80,
    "Blue Pengu": 35
}

# 📤 Надсилання повідомлення
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text}
    try:
        res = requests.post(url, data=payload)
        if not res.ok:
            print(f"❗️Помилка надсилання: {res.text}")
    except Exception as e:
        print(f"❗️Помилка при надсиланні: {e}")

# 🌟 Перевірка на "гарні номери"
def is_special_number(n):
    str_n = str(n)

    # 1–30
    if 1 <= n <= 30:
        return True

    # Сотні, тисячі
    if n % 100 == 0 or n % 1000 == 0:
        return True

    # Дзеркальні типу 1221
    if str_n == str_n[::-1]:
        return True

    # Всі однакові цифри (наприклад, 111, 2222)
    if len(set(str_n)) == 1:
        return True

    return False

# 🧠 Фільтрація повідомлень
def filter_message(msg_text):
    name_match = re.search(r'Name:\s*(.+?)\s+#(\d+)', msg_text)
    cost_match = re.search(r'Cost:\s*([\d.]+)\s*TON', msg_text)

    if not name_match or not cost_match:
        return None

    raw_name = name_match.group(1).strip()
    number = int(name_match.group(2))
    cost = float(cost_match.group(1))
    normalized_name = raw_name.lower()

    # 🔍 Перевірка по назві та ціні
    for key in FILTER_RULES:
        if key.lower() in normalized_name:
            max_price = FILTER_RULES[key]
            if cost < max_price:
                return f"🔎 Знайдено фільтрований стікер:\n{raw_name} #{number}, {cost} TON"

    # 💎 Перевірка на гарні номери
    if is_special_number(number):
        return f"🌟 Знайдено гарний номер:\n{raw_name} #{number}, {cost} TON"

    return None

# 🤖 Telegram-клієнт
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(chats='palaceoffers'))
async def handler(event):
    msg = event.message.message
    result = filter_message(msg)
    if result:
        send_telegram_message(result)
        print(f"✅ Сповіщення: {result}")
    else:
        print("— Пропущено")

async def main():
    print("✅ Бот слухає @palaceoffers у реальному часі...")
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
