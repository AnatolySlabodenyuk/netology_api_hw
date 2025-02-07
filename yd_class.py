import requests
from logger import setup_logger

logger = setup_logger()


class YDApi:
    def __init__(self, authorization_token: str):
        self.base_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        self.headers = {
            'Authorization': f'OAuth {authorization_token}'
        }

    def create_folder(self, path_to_folder: str):
        create_folder_params = {
            'path': path_to_folder
        }
        try:
            requests.put(
                url=f'{self.base_url}',
                headers=self.headers,
                params=create_folder_params
            )

            logger.info(f"Папка успешно создана по пути {path_to_folder}")

        except Exception as err:
            logger.error(f"Ошибка при создании папки: {err}")

    def _get_upload_href(self, path_to_upload_file_in_disk: str) -> str | None:
        get_upload_href_params = {
            'path': path_to_upload_file_in_disk
        }
        try:
            resp = requests.get(
                url=f'{self.base_url}/upload',
                headers=self.headers,
                params=get_upload_href_params
            )
            logger.info(f"Ссылка для загрузки файла на Я.Диск была получена {resp.json()['href']}")

            return resp.json()['href']

        except Exception as err:
            logger.error(f"Ошибка при получении ссылки: {err}")

    def upload_file_from_local(self, path_to_upload_file_in_disk: str, file_name: str):
        files = {'file': open(file_name, 'rb')}

        try:
            requests.put(
                url=self._get_upload_href(path_to_upload_file_in_disk),
                files=files
            )
            logger.info(f"Локальный успешно загружен на Яндекс Диск")

        except Exception as err:
            logger.error(f"Ошибка при загрузке локального файла: {err}")

    def upload_file_from_url(self, path_to_upload_file_in_disk: str, url_to_file: str, filename: str):
        file_content = requests.get(url=url_to_file).content
        files = {'file': (filename, file_content)}

        try:
            requests.put(
                url=self._get_upload_href(path_to_upload_file_in_disk),
                files=files
            )
            logger.info(f"Файл по ссылке успешно загружен на Яндекс Диск")

        except Exception as err:
            logger.error(f"Ошибка при загрузке файла по ссылке: {err}")
