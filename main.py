import os
import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiohttp import web

API_TOKEN = os.getenv("BOT_TOKEN", "8849638950:AAH590EsISHKHITh2IOtyl4esQ1nvoYLrf0")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- TUGMALAR DIZAYNI ---
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Nomer olish"), KeyboardButton(text="🛍 Buyurtma berish")],
        [KeyboardButton(text="🛒 Buyurtmalar"), KeyboardButton(text="👔 Kabinet")],
        [KeyboardButton(text="🗣 Pul ishlash"), KeyboardButton(text="💵 Pul kiritish")],
        [KeyboardButton(text="🆘 Support"), KeyboardButton(text="💡 Ma’lumotnoma")]
    ],
    resize_keyboard=True
)

# --- /START ---
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    user_name = message.from_user.full_name
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    text = (
        f"👋 <b>Salom! {user_name}</b> @SMM_abdumutalov_bot ga xush kelibsiz!\n\n"
        f"<blockquote>🌐 Biz sizning ijtimoiy tarmoqlardagi faoliyatingizni oshirish uchun barcha kerakli xizmatlarni taqdim etamiz.</blockquote>\n\n"
        f"📌 <i>Botdan foydalanishni tushunmasangiz Ma'lumotnoma bo'limiga kiring.</i>\n\n"
        f"🌐 <b>Bizni tanlaganingizdan xursandmiz!</b>\n"
        f"<code>{now}</code>"
    )
    
    await message.answer(text=text, parse_mode=ParseMode.HTML, reply_markup=main_keyboard)

@dp.message(F.text == "🛍 Buyurtma berish")
async def buyurtma_handler(message: types.Message):
    await message.answer("SMM xizmatlari turini tanlang:\n\n1. Instagram\n2. Telegram\n3. YouTube")

@dp.message(F.text == "🆘 Support")
async def support_handler(message: types.Message):
    await message.answer("Savol va murojaatlar uchun admin: @abdumutalov_v")

@dp.message(F.text == "👔 Kabinet")
async def kabinet_handler(message: types.Message):
    await message.answer(f"🆔 Sizning ID: <code>{message.from_user.id}</code>\n👤 Ism: {message.from_user.full_name}")

@dp.message()
async def default_handler(message: types.Message):
    await message.answer("Tanlangan bo'lim bo'yicha ishlanmoqda...")

# Render uchun kichik veb-server (server o'chib qolmasligi uchun)
async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    print("SMM Bot ishga tushdi...")
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
