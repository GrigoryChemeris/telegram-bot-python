import os
import json
import random
from dotenv import load_dotenv  # Убедитесь, что у вас установлен python-dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

# Загружаем переменные окружения
load_dotenv()

# Получаем токен из переменной окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Загружаем слова и предложения из JSON файла
with open('words.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

words = data['words']
sentences = data['sentences']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = "Привет! Я ваш Telegram-бот. Каждый день я буду присылать вам слово и предложение."
    await update.message.reply_text(welcome_message)
    await send_random_word_and_sentence(update)

async def send_random_word_and_sentence(update: Update):
    word_entry = random.choice(words)
    sentence_entry = random.choice(sentences)

    word_message = f"Слово: {word_entry['word']}\nТранскрипция: {word_entry['transcription']}\nПеревод: {word_entry['translation']}"
    sentence_message = f"Предложение: {sentence_entry['sentence']}\nТранскрипция: {sentence_entry['transcription']}\nПеревод: {sentence_entry['translation']}"

    await update.message.reply_text(word_message)
    await update.message.reply_text(sentence_message)

async def send_another_word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_random_word_and_sentence(update)

async def send_another_sentence(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await send_random_word_and_sentence(update)

async def oath_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    oath_message = "Текст присяги: \nТранскрипция: \nПеревод: "
    await update.message.reply_text(oath_message)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.Text("Ещё слово"), send_another_word))
    app.add_handler(MessageHandler(filters.Text("Ещё предложение"), send_another_sentence))
    app.add_handler(MessageHandler(filters.Text("Текст присяги"), oath_text))

    app.run_polling()
