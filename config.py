import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID")) if os.getenv("CHANNEL_ID") else None
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASS", "change_me")
DATA_DIR = os.path.join(os.getcwd(), "data")
LEAD_TEXT_FILE = os.path.join(DATA_DIR, "lead_magnet.txt")
LEAD_PDF_FILE = os.path.join(DATA_DIR, "lead.pdf")

DEFAULT_WELCOME = "Добро пожаловать! Чтобы получить материал — нажмите кнопку и подтвердите подписку."
