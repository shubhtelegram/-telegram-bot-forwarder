import logging
from telegram import Update, InputMediaPhoto, InputMediaVideo
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# This list should hold the chat ids of the channels and groups you want to forward to.
CHANNELS_GROUPS = [
    '@your_channel_1',
    '@your_channel_2',
    'your_group_chat_id',  # Group chat ID
]

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I will forward your messages to all the channels and groups.')

def forward_message(update: Update, context: CallbackContext) -> None:
    """Forward the received message to all channels and groups"""
    # Forward text messages
    if update.message.text:
        for chat_id in CHANNELS_GROUPS:
            context.bot.forward_message(chat_id=chat_id, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
    
    # Forward photos
    elif update.message.photo:
        for chat_id in CHANNELS_GROUPS:
            context.bot.send_photo(chat_id=chat_id, photo=update.message.photo[-1].file_id)
    
    # Forward videos
    elif update.message.video:
        for chat_id in CHANNELS_GROUPS:
            context.bot.send_video(chat_id=chat_id, video=update.message.video.file_id)
    
    # Forward audio
    elif update.message.audio:
        for chat_id in CHANNELS_GROUPS:
            context.bot.send_audio(chat_id=chat_id, audio=update.message.audio.file_id)
    
    # Forward documents
    elif update.message.document:
        for chat_id in CHANNELS_GROUPS:
            context.bot.send_document(chat_id=chat_id, document=update.message.document.file_id)
    
    # Forward other types of media (voice, animation, etc.)
    else:
        pass  # Handle other types if needed

def main() -> None:
    # Replace 'YOUR_API_KEY' with your Bot's API token
    updater = Updater("YOUR_API_KEY")
    
    dispatcher = updater.dispatcher
    
    # Start command handler
    dispatcher.add_handler(CommandHandler("start", start))
    
    # Message handler to forward messages
    dispatcher.add_handler(MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.audio | Filters.document, forward_message))
    
    # Start the Bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
