from typing import Union

import requests as req


class YaDiskUploader:

    def __init__(self, token):
        self.token = token

    @property
    def token(self):
        return self.__token

    @token.setter
    def token(self, token):
        self.__token = token

    def __get_headers(self) -> dict:
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def __get_upload_link(self, disk_file_path: str) -> dict:
        upload_link = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.__get_headers()
        params = {'path': disk_file_path, 'overwrite': 'false'}
        response = req.get(upload_link, params=params, headers=headers)
        return response.json()

    def upload_file_to_disk(self, disk_file_path: str, data: bin) -> Union[Exception, str, int]:
        href = self.__get_upload_link(disk_file_path).get('href', '')
        if not href:
            return -1
        response = req.put(href, data)
        response.raise_for_status()
        if response.status_code == 201:
            return 'Success'

    def create_folder(self, folder_path: str) -> Union[Exception, str]:
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.__get_headers()
        params = {'path': folder_path}
        response = req.put(url, headers=headers, params=params)
        response.raise_for_status()
        if response.status_code == 201:
            return 'Success'
