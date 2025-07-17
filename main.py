import logging
import os
import json
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = os.getenv("BOT_TOKEN")
DATA_FILE = "files.json"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Загрузка базы
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        file_db = json.load(f)
else:
    file_db = []

# Главное меню
main_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add("📘 Нақшаҳо", "📄 Фармонҳо", "📝 Протоколҳо")
main_menu.add("🗂️ Санадҳо", "📚 Нақшаи яксоата (Конспект)", "📖 Китобҳо")
main_menu.add("🎓 Аёниятҳо", "📑 Дастурамалҳо", "📊 Гузоришҳо")
main_menu.add("📅 Ҷадвалҳо", "🧾 Маводҳои дигар", "🔍 Поиск")

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("📂 МЕНЮИ АСОСӢ", reply_markup=main_menu)

@dp.message_handler(lambda msg: msg.text == "🔍 Поиск")
async def ask_search(message: types.Message):
    await message.answer("Калимаи ҷустуҷӯро ворид кунед:")

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def save_document(message: types.Message):
    if message.caption:
        file_info = {
            "file_id": message.document.file_id,
            "file_name": message.document.file_name,
            "caption": message.caption.lower()
        }
        file_db.append(file_info)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(file_db, f, ensure_ascii=False, indent=2)
        await message.reply("✅ Ҳуҷҷат бо муваффақият сабт шуд.")
    else:
        await message.reply("❗Лутфан барои ҳуҷҷат тавсиф (caption) илова намоед.")

@dp.message_handler()
async def handle_search(message: types.Message):
    keyword = message.text.lower()
    results = [doc for doc in file_db if keyword in doc["caption"]]
    if results:
        for doc in results:
            await message.answer_document(doc["file_id"], caption=doc["caption"])
    else:
        await message.answer("❌ Ҳуҷҷат ёфт нашуд.")

if__name__=='__main__':
    executor.start_polling(dp, skip_updates=True)
