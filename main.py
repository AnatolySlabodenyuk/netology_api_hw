import configparser
import json
from tqdm import tqdm

from vk_class import VKApi
from yd_class import YDApi

config = configparser.ConfigParser()
config.read('settings.ini')
access_token_vk = config['Main']['access_token_vk']


def main():
    input_vk_id = input('Введите VK id cтраницы, откуда будут скачаны фото:\n')
    authorization_token_yd = input('Введите токен Яндекc Диска, на который будут загружены фото:\n')

    vk_item = VKApi(access_token=access_token_vk)
    yd_item = YDApi(authorization_token=authorization_token_yd)

    photo_urls = vk_item.get_photos_origin_url(owner_id=input_vk_id, count=5)
    photo_likes = vk_item.get_photos_likes(owner_id=input_vk_id, count=5)
    photo_sizes = vk_item.get_photos_sizes(owner_id=input_vk_id, count=5)

    folder_on_disk_name = 'new_folder'
    yd_item.create_folder(path_to_folder=folder_on_disk_name)
    photo_count = 0
    result_list = []
    for url in tqdm(photo_urls, desc='Загрузка фото на Яндекс Диск'):
        file_name = f'{photo_likes[photo_count]}_{photo_count}'
        yd_item.upload_file_from_url(
            path_to_upload_file_in_disk=f'{folder_on_disk_name}/{file_name}',
            url_to_file=url,
            filename=file_name
        )

        result_list.append(
            {
                'file_name': file_name,
                'size': f'{photo_sizes[photo_count][0]}x{photo_sizes[photo_count][1]}'
            }
        )

        photo_count += 1

    with open('result.json', 'w') as result_file:
        result_file.write(json.dumps(result_list, indent=2))

    print(f'\nГотово!\n'
          f'Фото загружены на Яндекс Диск в папку {folder_on_disk_name}\n'
          f'Информация о загруженных фото находится в файле result.json')


if __name__ == '__main__':
    main()
