import telebot
import os
import sys
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.snowball import SnowballStemmer
import nltk


# Validate bot token exists
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    print("Error: BOT_TOKEN environment variable is not set!")
    sys.exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# Download NLTK data only if not already present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Downloading NLTK punkt tokenizer...")
    nltk.download('punkt')

stemmer = SnowballStemmer("russian")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '/help':
        bot.send_message(message.chat.id, 'Напиши Доброе утро')
    elif is_good_morning_nltk(message.text.lower()):
        bot.send_message(message.chat.id, 'Хуютра!', reply_to_message_id=message.message_id)

def is_good_morning(message):
    return 'утра' in message or 'утро' in message

def is_good_morning_nltk(message):
    for sentence in sent_tokenize(message, language="russian"):
        for word in word_tokenize(sentence, language="russian"):
            stem = stemmer.stem(word)
            if stem == 'утр':
                return True
    return False

# Start polling with proper error handling and reasonable interval
if __name__ == "__main__":
    try:
        print("Starting bot...")
        bot.polling(none_stop=True, interval=1)  # 1 second interval instead of 0
    except Exception as e:
        print(f"Bot polling error: {e}")
        sys.exit(1)
