import requests

from logger import setup_logger

logger = setup_logger()


class VKApi:
    def __init__(self, access_token: str, v: int = 5.199):
        self.base_url = 'https://api.vk.ru/method/'
        self.params = {
            'access_token': access_token,
            'v': v
        }

    def _get_photos_items(self, owner_id: str, count: int, album_id: str = 'profile', extended: int = 1) -> list:
        params = {
            'owner_id': owner_id,
            'count': count,
            'album_id': album_id,
            'extended': extended
        }
        self.params.update(params)

        try:
            resp = requests.post(
                url=f'{self.base_url}photos.get',
                params=self.params
            )

            logger.info(f"Данные по фото из ВК получены успешно")

            items = resp.json()['response']['items']
            return items

        except Exception as err:
            logger.error(f"Ошибка при получении данных с ВК: {err}")

    def get_photos_origin_url(self, owner_id: str, count: int, album_id: str = 'profile', extended: int = 1) -> list:
        items = self._get_photos_items(owner_id, count, album_id, extended)
        orig_photo_urls = [item['orig_photo']['url'] for item in items]
        return orig_photo_urls

    def get_photos_likes(self, owner_id: str, count: int, album_id: str = 'profile', extended: int = 1) -> list:
        items = self._get_photos_items(owner_id, count, album_id, extended)
        likes = [item['likes']['count'] for item in items]
        return likes

    def get_photos_sizes(self, owner_id: str, count: int, album_id: str = 'profile', extended: int = 1) -> list:
        items = self._get_photos_items(owner_id, count, album_id, extended)
        orig_photo_heights = [item['orig_photo']['height'] for item in items]
        orig_photo_widths = [item['orig_photo']['width'] for item in items]
        heights_widths_list = []
        for i in range(len(orig_photo_heights)):
            heights_widths_list.append((orig_photo_heights[i], orig_photo_widths[i]))

        return heights_widths_list
