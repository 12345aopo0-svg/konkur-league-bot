import os
import sqlite3
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")

# Database
db = sqlite3.connect("bot.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    name TEXT,
    grade TEXT,
    study_goal REAL DEFAULT 0,
    test_goal INTEGER DEFAULT 0,
    city TEXT
)
""")
db.commit()


def main_keyboard():
    return ReplyKeyboardMarkup([
        ["👤 ثبت‌نام", "👤 پروفایل من"],
        ["🎯 هدف امروز", "📝 گزارش روزانه"],
        ["📊 آمار من", "🏆 رتبه‌بندی"],
        ["👥 تیم من", "🔥 چالش هفتگی"],
        ["📝 آزمون‌ها", "📈 ثبت نتیجه آزمون"],
        ["🔥 زنجیره مطالعه", "📖 راهنما"]
    ], resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 به لیگ کنکور خوش آمدی!\n\n"
        "از منوی زیر استفاده کن:",
        reply_markup=main_keyboard()
    )


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
        (user_id,)
    )
    db.commit()

    await update.message.reply_text(
        "👤 ثبت‌نام در لیگ کنکور\n\n"
        "لطفاً نام و نام خانوادگی خود را ارسال کن."
    )

    context.user_data["register_step"] = "name"


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    cursor.execute(
        "SELECT name, grade, study_goal, test_goal, city "
        "FROM users WHERE user_id=?",
        (user_id,)
    )
    user = cursor.fetchone()

    if not user or not user[0]:
        await update.message.reply_text(
            "❌ هنوز ثبت‌نام نکرده‌ای.\n"
            "ابتدا روی 👤 ثبت‌نام بزن."
        )
        return

    await update.message.reply_text(
        f"👤 پروفایل من\n\n"
        f"📌 نام: {user[0]}\n"
        f"📚 پایه: {user[1]}\n"
        f"⏱️ هدف مطالعه: {user[2]} ساعت\n"
        f"📝 هدف تست: {user[3]}\n"
        f"🏙️ شهر: {user[4]}"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.effective_user.id

    if context.user_data.get("register_step") == "name":
        cursor.execute(
            "UPDATE users SET name=? WHERE user_id=?",
            (text, user_id)
        )
        db.commit()

        context.user_data["register_step"] = "grade"

        await update.message.reply_text(
            "📚 پایه یا وضعیت تحصیلی‌ات را ارسال کن.\n"
            "مثال: دوازدهم / پشت‌کنکوری"
        )
        return

    if context.user_data.get("register_step") == "grade":
        cursor.execute(
            "UPDATE users SET grade=? WHERE user_id=?",
            (text, user_id)
        )
        db.commit()

        context.user_data["register_step"] = "study_goal"

        await update.message.reply_text(
            "⏱️ هدف مطالعه روزانه‌ات چند ساعت است؟\n"
            "مثال: 8"
        )
        return

    if context.user_data.get("register_step") == "study_goal":
        try:
            goal = float(text)
        except ValueError:
            await update.message.reply_text("لطفاً فقط عدد وارد کن. مثال: 8")
            return

        cursor.execute(
            "UPDATE users SET study_goal=? WHERE user_id=?",
            (goal, user_id)
        )
        db.commit()

        context.user_data["register_step"] = "test_goal"

        await update.message.reply_text(
            "📝 هدف تست روزانه‌
