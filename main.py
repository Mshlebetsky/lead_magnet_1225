
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.utils.markdown import hlink
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re

import re


def clean_html(text: str) -> str:
    """
    Убирает все неподдерживаемые Telegram HTML-теги.
    Оставляет только допустимые: <b>, <i>, <u>, <s>, <code>, <pre>, <a href="...">
    """
    # Убираем все теги кроме разрешённых
    allowed_tags = ['b', 'strong', 'i', 'em', 'u', 's', 'strike', 'code', 'pre', 'a', 'tg-spoiler']

    # Простое удаление всех тегов кроме разрешённых
    def remove_tag(match):
        tag = match.group(1).lower()
        if tag in allowed_tags:
            return match.group(0)  # оставляем
        return ''  # удаляем

    clean_text = re.sub(r'</?([^ >]+)[^>]*>', remove_tag, text)
    return clean_text



import os
from jinja2 import Template

TOKEN = os.getenv("BOT_TOKEN", "YOUR_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@yourchannel")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
CHANNEL_LINK = f"https://t.me/{CHANNEL_ID.replace('@', '')}"

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

LEAD_PATH = "lead.html"
PDF_PATH = "lead.pdf"

def load_lead():
    if not os.path.exists(LEAD_PATH):
        return "<h2>Лид-магнит пока не установлен</h2>"
    return open(LEAD_PATH, "r", encoding="utf-8").read()

@dp.message(CommandStart())
async def start(msg: Message):
    status = await bot.get_chat_member(CHANNEL_ID, msg.from_user.id)
    if status.status in ("member", "administrator", "creator"):
        await msg.answer("Вы подписаны! Отправляю ваш лид-магнит…")

        if os.path.exists(PDF_PATH):
            await msg.answer_document(types.FSInputFile(PDF_PATH))
        else:
            await msg.answer(clean_html(load_lead()))
    else:
        await msg.answer(f"Чтобы получить лид-магнит, подпишитесь на канал:\n"
        f"{hlink('Перейти к каналу', f'https://t.me/{CHANNEL_ID.replace("@", "")}')}"

                         )


@dp.message(F.text.startswith("/admin"))
async def admin_login(msg: Message):
    parts = msg.text.split(maxsplit=1)
    if len(parts) == 1 or parts[1] != ADMIN_PASSWORD:
        await msg.answer("Неверный пароль")
        return

    await msg.answer("Добро пожаловать в админ-панель!"
                     "Команды:\n"
                     "/set_html – загрузить новый HTML лид-магнит\n"
                     "/set_pdf – загрузить PDF лид-магнит\n")

@dp.message(F.text == "/set_html")
async def set_html(msg: Message):
    await msg.answer("Отправьте HTML-файл лид-магнита")
    dp.message.register(process_html, F.document)

async def process_html(msg: Message):
    file = msg.document
    if not file.file_name.endswith(".html"):
        await msg.answer("Нужен HTML-файл")
        return
    path = f"./{file.file_name}"
    await bot.download(file, path)
    os.replace(path, LEAD_PATH)
    await msg.answer("HTML лид-магнит обновлён")

@dp.message(F.text == "/set_pdf")
async def set_pdf(msg: Message):
    await msg.answer("Отправьте PDF-файл лид-магнита")
    dp.message.register(process_pdf, F.document)

async def process_pdf(msg: Message):
    file = msg.document
    if not file.file_name.endswith(".pdf"):
        await msg.answer("Нужен PDF-файл")
        return
    path = f"./{file.file_name}"
    await bot.download(file, path)
    os.replace(path, PDF_PATH)
    await msg.answer("PDF лид-магнит обновлён")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    print(CHANNEL_ID, TOKEN)
    asyncio.run(main())

