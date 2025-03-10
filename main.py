import requests
import asyncio
import urllib.parse
import time

public_urls = ['https://disk.yandex.ru/i/1p9XkHlnYpzJLw',
              'https://disk.yandex.ru/i/eve4KnyRRseMzw']

token = 'y0__xDUukgYl-81IOblu000m24KFgB-EMyKkJyD5pCXHOJ3Y9w'
save_path = ''

function_called = False
lock = asyncio.Lock()
last_called_time = None


# Функция для получения файла с Яндекс-Диска
async def download_file_from_yandex_disk(token, public_url, save_path):
    global function_called, last_called_time
    async with lock:
        current_time = asyncio.get_event_loop().time()
        # Проверяем, прошло ли 10 секунд с последнего вызова функции
        if function_called and (current_time - last_called_time < 10):
            print("Вызываем следующий файл спустя 10 секунд.")
            time.sleep(11 - current_time//10000)

        url = f'https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_url}'
        headers = {'Authorization': f'OAuth {token}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            public_key = response.json().get('public_key')
            save_path = response.json().get('name')

        else:
            raise Exception(f'Ошибка при получении ключа: {response.text}')

        public_key = urllib.parse.quote(public_key)
        url2 = f'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={public_key}'

        # Получаем ссылку для скачивания файла
        response2 = requests.get(url2, headers=headers)
        if response2.status_code == 200:
            download_url = response2.json().get('href')
            print('doe', download_url)
            if download_url != '':
                file_response = requests.get(download_url)
                with open(save_path, 'wb') as f:
                    f.write(file_response.content)
                print(f'Файл загружен и сохранён как {save_path}')
            else:
                print(f'Ошибка сохранения файла')

        # Обновляем состояние
        function_called = True
        last_called_time = current_time

for url in public_urls:
    public_url = urllib.parse.quote(url)
    asyncio.run(download_file_from_yandex_disk(token, public_url, save_path))