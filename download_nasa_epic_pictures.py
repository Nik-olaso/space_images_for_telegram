import requests
import helper_script
import datetime
import os
from pathlib import Path
from dotenv import load_dotenv
import argparse

def fetch_nasa_epic_pictures(args_path,  nasa_token):
    nasa_epic_url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {
        "api_key" : nasa_token,
    }
    nasa_epic_response = requests.get(nasa_epic_url, params=params)
    nasa_epic_response.raise_for_status()
    nasa_epic_response = nasa_epic_response.json()
    for number, nasa_epic_item in enumerate(nasa_epic_response, start=1):
        nasa_epic_date = nasa_epic_item["date"]
        nasa_epic_name = nasa_epic_item["image"]
        nasa_epic_date = datetime.datetime.fromisoformat(nasa_epic_date).strftime("%Y/%m/%d")
        nasa_epic_picture_format = helper_script.get_picture_format(f"https://api.nasa.gov/EPIC/archive/natural/{nasa_epic_date}/png/{nasa_epic_name}.png")
        nasa_epic_link = f"https://api.nasa.gov/EPIC/archive/natural/{nasa_epic_date}/png/{nasa_epic_name}.png"
        nasa_epic_filename = f"nasa_epic_{number}{nasa_epic_picture_format}"
        nasa_epic_params = {nasa_token}
        helper_script.download_picture(nasa_epic_response, nasa_epic_params, nasa_epic_link, args_path, nasa_epic_filename)            


def main():
    load_dotenv()
    nasa_token = os.environ["NASA_TOKEN"]
    Path("all_images").mkdir(parents=True, exist_ok=True)  
    parser = argparse.ArgumentParser(description="Это скрипт создан для скачивания фотографий с баз NASA, фотографии из категории EPIC")
    parser.add_argument("--path", default="all_images", help="в какую папку загружать картинки")    
    args = parser.parse_args()
    args_path = args.path
    Path(args_path).mkdir(parents=True, exist_ok=True)  
    try:
        fetch_nasa_epic_pictures(args_path, nasa_token)    
    except (requests.exceptions.HTTPError, requests.exceptions.JSONDecodeError):
        print("Вероятно, у Вас есть ошибка в ссылке")

if __name__ == "__main__":
    main()
