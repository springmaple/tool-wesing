import json
import os
import shutil
import urllib.request
from pathlib import Path

home = str(Path.home())
root = os.path.join(home, "Desktop")


def get_wesing(url):
    with urllib.request.urlopen(url) as resp:
        data = resp.read().decode('utf-8')
    _, _1, part = data.partition('"playurl":"')
    media_url, _, _1 = part.partition('"')

    _, _1, part = data.partition('"song_name":"')
    title, _, _1 = part.partition('"')

    _, _1, part = data.partition('"cover":"')
    img_url, _, _1 = part.partition('"')

    return title, media_url, img_url


def get_starmaker(url):
    _, _1, part = url.partition('recording_id=')
    recording_id, _, _1 = part.partition('&')

    detail_url = f'https://m.starmakerstudios.com/api/recordings/{recording_id}/share/detail'
    with urllib.request.urlopen(detail_url) as resp:
        data = json.loads(resp.read().decode('utf-8'))

    title = data['song']['title']
    media_url = data['recording']['media_url']
    img_url = data['recording']['cover_image']
    return title, media_url, img_url


def download_all(title, media_url, img_url):
    print([title, media_url, img_url])

    def create_folder():
        for i in range(100):
            folder_name = title if i == 0 else f'{title}_{i}'
            save_to = os.path.join(root, folder_name)
            if not os.path.exists(save_to):
                os.makedirs(save_to)
                return save_to
        raise Exception('failed to create folder after 100 loop')

    def download_to(source_url, target_path):
        with urllib.request.urlopen(source_url) as response, open(target_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

    save_to_dir = create_folder()
    download_to(media_url, os.path.join(save_to_dir, 'master.mp4'))
    download_to(img_url, os.path.join(save_to_dir, 'source.jiff'))


def start():
    url_file = os.path.join(root, 'url.txt')
    with open(url_file, mode='r', encoding='utf-8') as f:
        for url in f:
            url = url.strip()
            print('parsing url - ' + url)
            if 'wesingapp' in url:
                obj = get_wesing(url)
            elif 'starmaker' in url:
                obj = get_starmaker(url)
            else:
                raise Exception('unsupported url ' + url)

            download_all(*obj)


start()
