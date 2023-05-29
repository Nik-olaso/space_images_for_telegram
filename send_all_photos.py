import telegram
import time
from pathlib import Path
import os 
import random
import argparse
from dotenv import load_dotenv
import helper_script


def send_all_images(args_time, args_path, bot, chat_id): 
    files = os.listdir(args_path)
    random.shuffle(files)
    for file in files:
        helper_script.send_picture(bot, args_path, file, chat_id)
        time.sleep(args_time)


def main():
    load_dotenv()
    Path("all_images").mkdir(parents=True, exist_ok=True)  
    telegram_bot_token = os.environ["TELEGRAM_BOT_TOKEN"]
    bot = telegram.Bot(telegram_bot_token)
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    parser = argparse.ArgumentParser(description="Этот скрипт создан для отправки всех фотографий в бесконечном цикле")
    parser.add_argument("--time", default=14400, help="время между отправкой картинок в секундах", type=int)
    parser.add_argument("--path", default = "all_images", help="выбор определенной папки", type=str)    
    args = parser.parse_args()
    args_time = args.time
    args_path = args.path
    while True: 
        try:
            send_all_images(args_time, args_path, bot, chat_id)
        except (telegram.error.BadRequest, telegram.error.TimedOut) as ex:
            time.sleep(60)
            continue  
            

if __name__ == "__main__":
   main()