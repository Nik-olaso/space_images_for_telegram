import requests
import helper_script
import argparse
from pathlib import Path


def fetch_spacex_launches(launch_id, args_path):
    api_spacex_url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    spacex_response = requests.get(api_spacex_url)
    spacex_response.raise_for_status()
    space_photo_links = [api_spacex_url for api_spacex_url in spacex_response.json()["links"]["flickr"]["original"]]
    for number, link in enumerate(space_photo_links, start=1):
        spacex_url_format = helper_script.get_picture_format(link)
        spacex_filename = f"spacex_{number}{spacex_url_format}"
        spacex_params = {}
        helper_script.download_picture(spacex_response, link, spacex_params, args_path, spacex_filename)


def main():
    parser = argparse.ArgumentParser(description="Это скрипт создан для скачивания фотографий с баз SpaceX")
    parser.add_argument("--id", default = "5eb87d46ffd86e000604b388", help="укажите id запуска")
    parser.add_argument("--path", default="all_images", help="в какую папку загружать картинки")    
    args = parser.parse_args()
    launch_id = args.id
    args_path = args.path    
    Path(args_path).mkdir(parents=True, exist_ok=True)
    try:
        fetch_spacex_launches(launch_id, args_path)
    except (requests.exceptions.HTTPError, requests.exceptions.JSONDecodeError):
        print("Вероятно, у Вас есть ошибка в ссылке")


if __name__ == "__main__":
    main()
