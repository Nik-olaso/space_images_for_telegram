import telegram
import os 
import random
from pathlib import Path
import argparse
import helper_script
from dotenv import load_dotenv


def send_one_file(args_file, args_path, bot, chat_id):
    helper_script.send_picture(bot, args_path, args_file, chat_id)


def send_random_photo(args_path, bot, chat_id):
    files = os.listdir(args_path)
    random.shuffle(files)
    helper_script.send_picture(bot, args_path, files[0], chat_id)


def main():
    load_dotenv()    
    Path("all_images").mkdir(parents=True, exist_ok=True)
    telegram_bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    bot = telegram.Bot(telegram_bot_token)
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    parser = argparse.ArgumentParser(description="Этот скрипт создан для отправки одной любой или определенной фотографии")
    parser.add_argument("--file", help="выбор определенной фотографии", type=str)  
    parser.add_argument("--path", default = "all_images", help="выбор определенной папки", type=str)    
    args = parser.parse_args()
    args_file = args.file
    args_path = args.path
    if args_file:
        send_one_file(args_file, args_path, bot, chat_id)
    else:
        send_random_photo(args_path, bot, chat_id)
    

if __name__ == "__main__":
    main()


