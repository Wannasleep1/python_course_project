from pprint import pprint
from typing import List

import operator as op
import os.path
import requests as req


class VKPhotoDownloader:
    # Токен с текста задания.
    TOKEN = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
    URL = 'https://api.vk.com/method/photos.get'

    def __init__(self, user_id: int):
        self.user_id = user_id

    @property
    def user_id(self) -> int:
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id: int) -> None:
        self.__verify_int(user_id)
        self.__user_id = user_id

    @staticmethod
    def __verify_int(number: int) -> None:
        if not isinstance(number, int):
            raise TypeError('Входные данные должны быть целым числом.')

    @staticmethod
    def __check_if_number_is_in_interval(number: int) -> None:
        if not 0 < number <= 1000:
            raise ValueError('Количество фотографий должно быть в диапазоне от 1 до 1000.')

    def __verify_quantity(self, qty):
        self.__verify_int(qty)
        self.__check_if_number_is_in_interval(qty)

    def __get_params(self, qty: int) -> dict:
        self.__verify_quantity(qty)
        return {
            'access_token': self.TOKEN,
            'owner_id': self.user_id,
            'album_id': 'profile',
            'count': qty,
            'extended': 1,
            'photo_sizes': 1,
            'v': '5.131',
        }

    @staticmethod
    def __leave_photos_with_max_size(photos_data_lst: List[dict]) -> None:
        for photo_dict in photos_data_lst:
            max_size_photo = sorted(photo_dict['sizes'], key=op.itemgetter('height', 'width'), reverse=True)[0]
            photo_dict['sizes'] = max_size_photo

    def get_photos_data_from_account(self, qty: int = 5) -> List[dict]:
        params = self.__get_params(qty)
        photos_data = req.get(self.URL, params=params)
        photos_data.raise_for_status()
        photos_data_lst = photos_data.json()['response']['items']
        return photos_data_lst

    def get_photos_data_with_max_size_from_account(self, qty: int = 5):
        photos_data_lst = self.get_photos_data_from_account(qty)
        self.__leave_photos_with_max_size(photos_data_lst)
        return photos_data_lst

    @staticmethod
    def get_photo_download_link(photo_data: dict) -> str:
        return photo_data['sizes']['url']

    @staticmethod
    def get_photo(url: str) -> bin:
        photo = req.get(url)
        photo.raise_for_status()
        return photo.content

    @staticmethod
    def save_photo_on_pc(photo: bin, path: str, photo_name: str) -> None:
        with open(os.path.join(path, photo_name + '.jpeg'), 'wb') as ph:
            ph.write(photo)
