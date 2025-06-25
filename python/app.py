"""Bot de ejemplo con autenticaci\xc3\xb3n simple."""

from flask import Flask, jsonify
from telegram import Update
from telegram.ext import (
    Updater, CommandHandler, MessageHandler, Filters,
    ConversationHandler, CallbackContext
)
import config

app = Flask(__name__)

# Definimos los estados de la conversaci\xc3\xb3n
ASK_USER, ASK_PASS = range(2)


def start(update: Update, context: CallbackContext) -> int:
    """Entrada de la conversaci\xc3\xb3n."""
    update.message.reply_text("Por favor, ingrese su usuario:")
    return ASK_USER


def ask_user(update: Update, context: CallbackContext) -> int:
    """Guarda el usuario y pide la contrase\xc3\xb1a."""
    context.user_data['username'] = update.message.text.strip()
    update.message.reply_text("Ingrese su contrase\xc3\xb1a:")
    return ASK_PASS


def ask_pass(update: Update, context: CallbackContext) -> int:
    """Verifica las credenciales."""
    password = update.message.text.strip()
    username = context.user_data.get('username')
    if username in config.USERS and config.USERS[username] == password:
        update.message.reply_text(f"Bienvenido, {username}")
    else:
        update.message.reply_text("Credenciales incorrectas.")
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancela la conversaci\xc3\xb3n."""
    update.message.reply_text("Operaci\xc3\xb3n cancelada.")
    return ConversationHandler.END


# Configuramos el bot con polling
updater = Updater(token=config.API_KEY, use_context=True)
dispatcher = updater.dispatcher

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        ASK_USER: [MessageHandler(Filters.text & ~Filters.command, ask_user)],
        ASK_PASS: [MessageHandler(Filters.text & ~Filters.command, ask_pass)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

dispatcher.add_handler(conv_handler)
updater.start_polling()


@app.route('/')
def index():
    """Endpoint simple para verificar que la app est\xc3\xa1 viva."""
    return jsonify({'status': 'bot running'})


if __name__ == '__main__':
    # Ejecutamos la aplicaci\xc3\xb3n Flask
    app.run(port=5000)
