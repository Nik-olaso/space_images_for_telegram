import requests
import helper_script
import os
from pathlib import Path
import argparse
from dotenv import load_dotenv


def fetch_nasa_apod_pictures(args_path, args_count, nasa_token):
    nasa_url = "https://api.nasa.gov/planetary/apot"    
    params = {
        "api_key" : nasa_token,
        "count" : args_count
    }
    nasa_apod_response = requests.get(nasa_url, params=params)    
    nasa_apod_response.raise_for_status()
    nasa_apod_response_links = nasa_apod_response.json()
    for number, nasa_link in enumerate(nasa_apod_response_links, start=1):
        nasa_apod_format = helper_script.get_picture_format(nasa_link["url"])
        nasa_apod_filename = f"nasa_apod_{number}{nasa_apod_format}"
        nasa_apod_params = {}
        helper_script.download_picture(nasa_apod_response, nasa_link["url"], nasa_apod_params, args_path, nasa_apod_filename)


def main():
    load_dotenv()
    nasa_token = os.environ["NASA_TOKEN"]
    Path("all_images").mkdir(parents=True, exist_ok=True)  
    parser = argparse.ArgumentParser(description="Это скрипт создан для скачивания фотографий с баз NASA, фотографии из категории APOD")
    parser.add_argument("--count", default=40, help="количество картинок nasa_apod")
    parser.add_argument("--path", default = "all_images", help="в какую папку загружать картинки")    
    args = parser.parse_args()
    args_count = args.count
    args_path = args.path
    Path(args_path).mkdir(parents=True, exist_ok=True)
    try:
        fetch_nasa_apod_pictures(args_path, args_count, nasa_token)    
    except (requests.exceptions.HTTPError, requests.exceptions.JSONDecodeError):
        print("Вероятно, у Вас есть ошибка в ссылке")

if __name__ == "__main__":
    main()
