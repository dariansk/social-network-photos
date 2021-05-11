import sys
from vkapi import VkUser
from yadiskapi import YaDisk

VK_TOKEN = ''
VK_API_VERSION = '5.130'
YANDEX_DISK_TOKEN = ''

if __name__ == '__main__':
    vk_user_id = input('Введите ID пользователя Вконтакте: ')
    if not vk_user_id.isdecimal():
        print("Некорректные данные.")
        sys.exit()
    else:
        vk_user_id = int(vk_user_id)
        vk_api_user = VkUser(VK_TOKEN, VK_API_VERSION)
        album_id = vk_api_user.get_albums(vk_user_id)
        photos_count = input('Сколько фотографий вы хотите сохранить на Яндекс.Диск: ')
        if not photos_count.isdecimal():
            photos_count = 5
        else:
            photos_count = int(photos_count)
        urls = vk_api_user.get_photos(vk_user_id, album_id, photos_count)
        yadisk_api_user = YaDisk(YANDEX_DISK_TOKEN)
        yadisk_api_user.upload(urls, vk_user_id)