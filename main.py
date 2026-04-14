from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

TOKEN = os.getenv("TOKEN")

def main_menu():
    keyboard = [
        [InlineKeyboardButton("📋 Информация о подготовке к ПЭТ КТ иследованию", callback_data="prep")],
        [InlineKeyboardButton("📍 Наш адрес,открыть в 2GIS", url="https://2gis.kz/astana/search/Мангилик%20ел%2080")],
    ]
    return InlineKeyboardMarkup(keyboard)

def prep_menu():
    keyboard = [
        [InlineKeyboardButton("📥 Скачать инструкцию", callback_data="pdf")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Меню",
        reply_markup=main_menu()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query.data == "prep":
        await query.answer()
        await query.edit_message_text(
            text="📋 Информация о подготовке к ПЭТ КТ иследованию",
            reply_markup=prep_menu()
        )
    elif query.data == "pdf":
        await query.answer()
        await context.bot.send_document(
            chat_id=query.from_user.id,
            document=open("prep.pdf", "rb"),
            caption="📋 Полная инструкция по подготовке к ПЭТ КТ"
        )
    elif query.data == "back":
        await query.answer()
        await query.edit_message_text(
            text="Меню",
            reply_markup=main_menu()
        )

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")
    def log_message(self, format, *args):
        pass

def run_health_server():
    server = HTTPServer(("0.0.0.0", 8080), HealthHandler)
    server.serve_forever()

threading.Thread(target=run_health_server, daemon=True).start()

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
