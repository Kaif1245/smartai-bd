import os
from openai import OpenAI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# =========================
# ENVIRONMENT VARIABLES
# =========================

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is missing")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing")

client = OpenAI(api_key=OPENAI_API_KEY)


# =========================
# AI FUNCTION
# =========================

async def ask_ai(prompt: str) -> str:
    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        return response.output_text

    except Exception as e:
        print("AI ERROR:", e)
        return "দুঃখিত, AI এখন কাজ করছে না। একটু পরে আবার চেষ্টা করুন।"


# =========================
# START MENU
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("🤖 AI Chat", callback_data="ai_chat"),
            InlineKeyboardButton("📄 CV Maker", callback_data="cv")
        ],
        [
            InlineKeyboardButton("✍️ Cover Letter", callback_data="cover"),
            InlineKeyboardButton("🌐 Translator", callback_data="translate")
        ],
        [
            InlineKeyboardButton("💎 Premium", callback_data="premium")
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🤖 *SmartAI BD*-তে স্বাগতম!\n\n"
        "আমি তোমাকে সাহায্য করতে পারি:\n\n"
        "🤖 AI Chat\n"
        "📄 CV তৈরি\n"
        "✍️ Cover Letter\n"
        "🌐 Translation\n"
        "💎 Premium Features\n\n"
        "নিচের Menu থেকে একটি অপশন নির্বাচন করো।",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


# =========================
# BUTTON HANDLER
# =========================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "ai_chat":

        context.user_data["mode"] = "ai"

        await query.message.reply_text(
            "🤖 AI Chat চালু হয়েছে!\n\n"
            "এখন আমাকে যেকোনো প্রশ্ন লিখে পাঠাও।"
        )

    elif query.data == "cv":

        context.user_data["mode"] = "cv"

        await query.message.reply_text(
            "📄 CV Maker\n\n"
            "তোমার তথ্য পাঠাও। যেমন:\n\n"
            "Name: Md Morsalin\n"
            "Age: 25\n"
            "Education: HSC\n"
            "Experience: 2 years\n"
            "Skills: Computer, English\n\n"
            "আমি এগুলো দিয়ে একটি professional CV তৈরি করব।"
        )

    elif query.data == "cover":

        context.user_data["mode"] = "cover"

        await query.message.reply_text(
            "✍️ Cover Letter Maker\n\n"
            "Job title এবং তোমার সম্পর্কে কিছু তথ্য পাঠাও।\n\n"
            "উদাহরণ:\n"
            "Job: Warehouse Worker\n"
            "Experience: 1 year\n"
            "Country: Denmark"
        )

    elif query.data == "translate":

        context.user_data["mode"] = "translate"

        await query.message.reply_text(
            "🌐 Translator চালু হয়েছে!\n\n"
            "যে text translate করতে চাও সেটা পাঠাও।\n\n"
            "উদাহরণ:\n"
            "English → Bangla\n"
            "Bangla → English"
        )

    elif query.data == "premium":

        await query.message.reply_text(
            "💎 Premium Features\n\n"
            "🚀 Unlimited AI Chat\n"
            "📄 Advanced CV Maker\n"
            "✍️ Professional Cover Letter\n"
            "📑 PDF Assistant\n"
            "🌐 Unlimited Translation\n\n"
            "💰 Premium system আমরা পরের ধাপে সেটআপ করব।"
        )


# =========================
# MESSAGE HANDLER
# =========================

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not update.message or not update.message.text:
        return

    text = update.message.text
    mode = context.user_data.get("mode", "ai")

    # -------------------------
    # AI CHAT
    # -------------------------

    if mode == "ai":

        answer = await ask_ai(text)

        await update.message.reply_text(answer)

    # -------------------------
    # CV MAKER
    # -------------------------

    elif mode == "cv":

        prompt = f"""
Create a professional CV from the following information.

Information:
{text}

Make the CV clean, professional and suitable for job applications.
Use clear sections:
- Personal Information
- Career Objective
- Education
- Work Experience
- Skills
- Languages

If some information is missing, do not invent it.
"""

        answer = await ask_ai(prompt)

        await update.message.reply_text(answer)

    # -------------------------
    # COVER LETTER
    # -------------------------

    elif mode == "cover":

        prompt = f"""
Write a professional job application cover letter using this information:

{text}

Make it professional, natural and suitable for an international job application.
Do not invent qualifications or experience.
"""

        answer = await ask_ai(prompt)

        await update.message.reply_text(answer)

    # -------------------------
    # TRANSLATOR
    # -------------------------

    elif mode == "translate":

        prompt = f"""
Translate the following text.

Text:
{text}

If the user writes Bangla, translate it into natural English.
If the user writes English, translate it into natural Bangla.

Return only the translation.
"""

        answer = await ask_ai(prompt)

        await update.message.reply_text(answer)


# =========================
# HELP COMMAND
# =========================

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "📚 Commands\n\n"
        "/start - Main Menu\n"
        "/help - Help\n\n"
        "AI Chat ব্যবহার করতে /start চাপো।"
    )


# =========================
# MAIN
# =========================

def main():

    application = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler
        )
    )

    print("SmartAI BD Bot is running...")

    application.run_polling()


if __name__ == "__main__":
    main()
