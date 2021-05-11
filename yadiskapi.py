import os
import shutil
import sys
import time
import requests
from tqdm import tqdm


class YaDisk:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Content-Type': 'application/json',
        'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_upload_link(self, yadisk_filepath):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {'path': yadisk_filepath, 'overwrite': 'false'}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload(self, urls, user_id):
        yandex_folder_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        folder_name = f'{user_id} vk photos'
        params = {'path': folder_name}
        response = requests.put(url=yandex_folder_url, headers=headers, params=params)
        if response.status_code == 201:
            if os.path.exists('photos_tmp'):
                shutil.rmtree('photos_tmp')
            os.mkdir('photos_tmp')
            print(f'Прогресс загрузки файлов на Яндекс.Диск в папку с именем "{folder_name}":')
            for filename in tqdm(urls):
                time.sleep(0.5)
                with open(f'photos_tmp/{filename}', 'wb'):
                    href = self.get_upload_link(yadisk_filepath=f'{folder_name}/{filename}').get('href', '')
                response = requests.put(href, data=requests.get(urls[filename]).content)
                response.raise_for_status()
                if response.status_code != 201:
                    print('Ошибка загрузки на Я.Диск')
                    sys.exit()
            shutil.rmtree('photos_tmp')
            print('Все фото успешно загружены на Яндекс.Диск')
        else:
            print('Ошибка загрузки на Яндекс.Диск')
            sys.exit()

