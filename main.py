from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import openai

# Настройка OpenAI API
openai.api_key = "your-openai-api-key"

# Функция для обработки сообщений
async def handle_message(update: Update, context):
    user_message = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}]
    )
    bot_response = response['choices'][0]['message']['content']
    await update.message.reply_text(bot_response)

# Запуск бота
if __name__ == "__main__":
    application = ApplicationBuilder().token("your-telegram-bot-token").build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()
