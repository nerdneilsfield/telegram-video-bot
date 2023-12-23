import logging
import random
import time

import coloredlogs
from telegram import BotCommand, Update, User
from telegram.constants import ChatAction, ParseMode
from telegram.ext import CallbackContext, CommandHandler, filters, MessageHandler, Updater, AIORateLimiter, Application, ApplicationBuilder

import config
from regex import RegexFilter

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
coloredlogs.install(logger=logger)


async def is_bot_mentioned(update: Update, context: CallbackContext) -> bool:
    try:
        message = update.message

        if message.chat.type == "private":
            return True

        if message.text is not None and ("@" + context.bot.username) in message.text:
            return True

        if message.reply_to_message is not None:
            if message.reply_to_message.from_user.id == context.bot.id:
                return True
    except:
        return True 
    else:
        return False


async def message_handler(update: Update, context: CallbackContext, message=None, use_new_dialog_timeout=True) -> None:
    is_bot_mentioned_ = await is_bot_mentioned(update, context)
    if not is_bot_mentioned_:
        return

    _message = message or update.message.text

    logger.info("message: {_message}")

    if RegexFilter.is_bilibili_url(_message):
        await update.message.reply_text("Yep, you send a bilibili url", parse_mode=ParseMode.MARKDOWN)
    


async def start_handler(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Yep, the robot is running!", parse_mode=ParseMode.MARKDOWN)

async def version_handler(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f"Version: {config.VERSION}", parse_mode=ParseMode.MARKDOWN)

async def error_handle(update: Update, context: CallbackContext) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    try:
        # collect error message
        tb_list = traceback.format_exception(
            None, context.error, context.error.__traceback__
        )
        tb_string = "".join(tb_list)
        update_str = update.to_dict() if isinstance(update, Update) else str(update)
        message = (
            f"在更新地时候发生了错误\n"
            f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
            "</pre>\n\n"
            f"<pre>{html.escape(tb_string)}</pre>"
        )

        # split text into multiple messages due to 4096 character limit
        for message_chunk in split_text_into_chunks(message, 4096):
            try:
                await context.bot.send_message(
                    update.effective_chat.id, message_chunk, parse_mode=ParseMode.HTML
                )
            except telegram.error.BadRequest:
                # answer has invalid characters, so we send it without parse_mode
                await context.bot.send_message(update.effective_chat.id, message_chunk)
    except:
        await context.bot.send_message(
            update.effective_chat.id, "error handler 发生了一些错误"
        )

async def post_init(application: Application):
    await application.bot.set_my_commands(
        [
            BotCommand("/start", "start the bot!"),
            BotCommand("/version", "show the bot's version"),
        ]
    )


def run_bot() -> None:
    application = (
        ApplicationBuilder()
        .token(config.telegram_token)
        .concurrent_updates(True)
        .rate_limiter(AIORateLimiter(max_retries=5))
        .http_version("1.1")
        .get_updates_http_version("1.1")
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start", start_handler, filters=None))
    application.add_handler(CommandHandler("version", version_handler, filters=None))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    application.add_error_handler(error_handle)

    application.run_polling()

if __name__ == "__main__":
    random.seed(time.time())
    run_bot()