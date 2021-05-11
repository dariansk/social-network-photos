import sys
import requests
import time
import json
from tqdm import tqdm


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.token = token
        self.version = version
        self.params = {
        'access_token': self.token,
        'v': self.version
        }

    def get_albums(self, owner_id):
        getalbums_url = self.url + 'photos.getAlbums'
        getalbums_params = {
        'owner_id': owner_id,
        'need_system': 1
        }
        albums_ids = []
        albums_select_number = []
        albums_select_name = []
        albums_size = []
        count = 0
        response = requests.get(getalbums_url, params={**self.params, **getalbums_params})
        if response.status_code == 200 and 'error' not in response.json():
            for items in tqdm(response.json()['response']['items']):
                time.sleep(0.33)
                count += 1
                albums_ids.append(items['id'])
                albums_select_number.append(count)
                albums_select_name.append(items['title'])
                albums_size.append((items['size']))
            for album in albums_select_number:
                print(f'{album} : "{albums_select_name[albums_select_number.index(album)]}"')
            print('Введите номер альбома, который хотите сохранить.')
            album_number = input()
            if album_number.isdecimal() and int(album_number) in albums_select_number:
                    return albums_ids[int(album_number) - 1]
            else:
                print('Такой альбом не существует.')
                sys.exit()
        elif 'error' in response.json():
            print(f'{response.json()["error"]["error_msg"]}. '
                  f'Код ошибки: ' f'{response.json()["error"]["error_code"]}.')
            sys.exit()
        else:
            print('Произошла ошибка.')
            sys.exit()

    def get_photos(self, owner_id, album_id, photos_count=5):
        getphotos_url = self.url + 'photos.get'
        getphotos_params = {
            'owner_id': owner_id,
            'album_id': album_id,
            'extended': 1,
            'feed_type': 'photo',
            'photo_sizes': 1,
            'offset': 0,
            'count': 1
        }
        response = requests.get(getphotos_url, params={**self.params, **getphotos_params})
        if response.status_code == 200 and 'error' not in response.json():
            actual_photos_count = response.json()['response']['count']
            sizes_dict = {}
            urls_dict = {}
            output_data = []
            if photos_count == 0:
                print('В альбоме нет фотографий.')
                sys.exit()
            if photos_count > actual_photos_count:
                photos_count = actual_photos_count
            print('Получение фото из альбома:')
            while getphotos_params['offset'] <= photos_count - 1:
                for items in tqdm(response.json()['response']['items']):
                    time.sleep(0.33)
                    if str(items['likes']['count']) + '.jpg' not in sizes_dict and \
                            str(items['likes']['count']) + ' ' + str(items['date']) + '.jpg' not in sizes_dict:
                        height = 0
                        max_size_type = ''
                        max_size_url = ''
                        for size in items['sizes']:
                            if size['height'] == 0:
                                max_size_type = size['type']
                                max_size_url = size['url']
                            elif height < size['height']:
                                height = size['height']
                                max_size_type = size['type']
                                max_size_url = size['url']
                        sizes_dict[str(items['likes']['count']) + '.jpg'] = max_size_type
                        urls_dict[str(items['likes']['count']) + '.jpg'] = max_size_url
                    elif str(items['likes']['count']) + '.jpg' in sizes_dict:
                        height = 0
                        max_size_type = ''
                        max_size_url = ''
                        for size in items['sizes']:
                            if size['height'] == 0:
                                max_size_type = size['type']
                                max_size_url = size['url']
                            if height < size['height']:
                                height = size['height']
                                max_size_type = size['type']
                                max_size_url = size['url']
                        sizes_dict[str(items['likes']['count']) + ' ' + str(items['date']) + '.jpg'] = max_size_type
                        urls_dict[str(items['likes']['count']) + ' ' + str(items['date']) + '.jpg'] = max_size_url
                getphotos_params['offset'] += 1
                response = requests.get(getphotos_url, params={**self.params, **getphotos_params})
            output_dict = {}
            print()
            print('Сохранение параметров фото в файл output.json:')
            with open('output.json', 'w') as file:
                for item in tqdm(sizes_dict):
                    time.sleep(0.33)
                    output_dict['file_name'] = item
                    output_dict['size'] = sizes_dict[item]
                    output_data.append(output_dict)
                    output_dict = {}
                json.dump(output_data, file, ensure_ascii=False, indent=2)
            return urls_dict
        elif 'error' in response.json():
            print(
                f'{response.json()["error"]["error_msg"]}. Код ошибки: '
                f'{response.json()["error"]["error_code"]}.')
            sys.exit()
        else:
            print('Что-то пошло не так.')
            sys.exit()