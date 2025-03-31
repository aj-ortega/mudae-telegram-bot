import requests
import logging
from datetime import datetime, timedelta
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ContextTypes
import pytz
from config import token

print(token)
url="https://api.waifu.pics/sfw/waifu"
TIME_LIMIT=10
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

async def waifu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("entra")
    response = requests.get(url)
    print(response)
    img = response.json()

    await update.message.reply_photo(photo=img["url"], caption="toma tu imagen maricon")

async def claim(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    if update.message.reply_to_message:
        original_date = update.message.reply_to_message.date.replace(tzinfo=None)  
        current_time = datetime.now(pytz.utc).replace(tzinfo=None)

        time_difference = current_time - original_date
        if time_difference  > timedelta(minutes=TIME_LIMIT):
            await update.message.reply_text('llegaste tarde, ya no es menor, buscate una de tu tamano')
        else:
            await update.message.reply_text(f'waifu exclavizada por {user.username}')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(rf'Hi {user.mention_html()}!', reply_markup=ForceReply(selective=True))


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)


def main() -> None:
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("waifu", waifu))
    app.add_handler(CommandHandler("claim", claim))

    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
