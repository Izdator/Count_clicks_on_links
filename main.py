import os
import argparse
from urllib.parse import urlparse
import requests
from dotenv import load_dotenv

def shorten_link(token, user_url):
    url = 'https://api.vk.com/method/utils.getShortLink'
    params = {
        'access_token': token,
        'v': '5.131',
        'url': user_url
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data['response']['short_url']

def count_clicks(token, user_url):
    url = 'https://api.vk.com/method/utils.getLinkStats'
    params = {
        'access_token': token,
        'v': '5.131',
        'url': user_url
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data['response']['clicks']

def is_shorten_link(user_url):
    url_components = urlparse(user_url)
    return url_components.netloc == 'vk.cc'

if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument('user_url', type=str)
    parser.add_argument('--token', type=str, default=os.environ.get("API_VK_TOKEN"))

    args = parser.parse_args()

    if not args.token:
        print("Ошибка: Токен доступа не указан. Убедитесь, что он установлен в переменной окружения API_VK_TOKEN или передан в аргументах.")

    user_url = args.user_url

    try:
        if is_shorten_link(user_url):
            print('Количество кликов:', count_clicks(args.token, user_url))
        else:
            print('Сокращенная ссылка:', shorten_link(args.token, user_url))
    except Exception as e:
        print(f'Ошибка: {e}')
