import logging
from quart import Quart, request, jsonify
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Quart(__name__)

# Токен вашего бота
TOKEN = "7836666684:AAH5rCZhhkZ5aqsvjlBZtcLyUMDwt0nVIvY"

# Создание Application
application = Application.builder().token(TOKEN).build()

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug("Обработка команды /start")
    user = update.message.from_user
    first_name = user.first_name
    last_name = user.last_name
    user_id = user.id

    if first_name or last_name:
        await update.message.reply_text(f"Здравствуйте, {first_name} {last_name}!\nНу и чем я тебе могу помочь?")
    else:
        await update.message.reply_text(f"Здравствуйте, {user_id}!\nНу и чем я тебе могу помочь?")

# Обработчик обычных сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.debug("Обработка обычного сообщения")
    txt = update.message.text
    await update.message.reply_text(f'Ну что это за вопрос: "{txt}"?\n А поконкретнее можно?')

# Корневой маршрут
@app.route('/')
async def home():
    return 'WEB SERVICE STARTED'

# Обработчик вебхука
@app.route('/webhook', methods=['POST'])
async def webhook():
    try:
        data = await request.get_json()
        logger.debug(f"Received data: {data}")

        if not data:
            return jsonify({"status": "error", "message": "No JSON data received"}), 400

        # Если данные не являются обновлением Telegram, просто вернем их обратно
        if "update_id" not in data:
            return jsonify({"status": "ok", "received_data": data}), 200

        # Инициализация Application, если еще не инициализирован
        if not application.running:
            logger.debug("Инициализация Application")
            await application.initialize()

        # Если это обновление Telegram, обрабатываем его
        update = Update.de_json(data, application.bot)
        logger.debug(f"Обработка обновления: {update}")

        # Обработка команды /start
        if update.message and update.message.text == "/start":
            await start(update, None)
        # Обработка обычных сообщений
        elif update.message and update.message.text:
            await echo(update, None)

        return jsonify({"status": "ok"}), 200
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Запуск Quart-приложения
    app.run(port=5000)
