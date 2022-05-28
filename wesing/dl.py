import json
import os
import urllib.request
from collections import namedtuple
from pathlib import Path
from typing import Any

home = str(Path.home())
root = os.path.join(home, "Desktop")

DlInfo = namedtuple('DlInfo', ['title', 'music_url', 'img_url'])


def _get_wesing(url: str) -> DlInfo:
    with urllib.request.urlopen(url) as resp:
        data = resp.read().decode('utf-8')
    _, _1, part = data.partition('"playurl":"')
    media_url, _, _1 = part.partition('"')
    if not media_url:
        _, _1, part = data.partition('"playurl_video":"')
        media_url, _, _1 = part.partition('"')

    _, _1, part = data.partition('"song_name":"')
    title, _, _1 = part.partition('"')

    _, _1, part = data.partition('"cover":"')
    img_url, _, _1 = part.partition('"')

    # For Quan Ming K Ge only:
    # `bsy` is too slow and always fail, manually replace to `ws`.
    media_url = media_url.replace('bsy.stream.kg.qq.com', 'ws.stream.kg.qq.com')

    # For Quan Ming K Ge only:
    # Replace invalid characters for folder name.
    title = title.replace(':', '-')

    return DlInfo(title, media_url, img_url)


def _get_starmaker(url: str) -> DlInfo:
    _, _1, part = url.partition('recording_id=')
    recording_id, _, _1 = part.partition('&')

    detail_url = f'https://m.starmakerstudios.com/api/recordings/{recording_id}/share/detail'
    with urllib.request.urlopen(detail_url) as resp:
        data = json.loads(resp.read().decode('utf-8'))

    title = data['song']['title']
    media_url = data['recording']['media_url']
    img_url = data['recording']['cover_image']
    return DlInfo(title, media_url, img_url)


def get_dl_info(url: str) -> DlInfo:
    if 'wesingapp' in url:
        dl_info = _get_wesing(url)
    elif 'starmaker' in url:
        dl_info = _get_starmaker(url)
    elif 'kg.qq.com' in url:
        dl_info = _get_wesing(url)
    elif 'kg2.qq.com' in url:
        dl_info = _get_wesing(url)
    elif 'kg3.qq.com' in url:
        dl_info = _get_wesing(url)
    else:
        raise Exception('unsupported url ' + url)
    return dl_info


def dl_media(url: str) -> Any:
    with urllib.request.urlopen(url) as response:
        return response.read()
