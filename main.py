from typing import Union, List
from progress.bar import IncrementalBar
from photo_downloader import VKPhotoDownloader
from uploader import YaDiskUploader


def main(folder_path: str, token: str, user_id: int, qty: int = 5) -> Union[Exception, List[dict]]:
    photos_downloader = VKPhotoDownloader(user_id)
    photos_data_lst = photos_downloader.get_photos_data_with_max_size_from_account(qty)
    yad_uploader = YaDiskUploader(token)
    yad_uploader.create_folder(folder_path)
    photos_info_lst = []
    bar = IncrementalBar('Countdown', max=len(photos_data_lst))
    for item in photos_data_lst:
        bar.next()
        photo_info = {}
        photo_name = f'{item["id"]}' + '.jpeg'
        photo_yad_path = folder_path + '/' + photo_name
        url = photos_downloader.get_photo_download_link(item)
        photo = photos_downloader.get_photo(url)
        response_status = yad_uploader.upload_file_to_disk(photo_yad_path, photo)
        if response_status == -1:
            break
        photo_info['file_name'] = photo_name
        photo_info['size'] = item['sizes']['type']
        photos_info_lst.append(photo_info)
    bar.finish()
    return photos_info_lst


if __name__ == '__main__':
    vk_user_id = 552934290
    yad_token = ''
    print(main('/photos', yad_token, vk_user_id))
