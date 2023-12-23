import logging
import random
import time

import colorlogs
from telegram import BotCommand, Update, User
from telegram.constants import ChatAction, ParseMode
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater, AIORateLimiter


colorlogs.install()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def run_bot() -> None:
    pass

if __name__ == "__main__":
    random.seed(time.time())
    run_bot()