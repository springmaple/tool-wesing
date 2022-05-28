import json
import os
import re
import urllib.request
from collections import namedtuple
from pathlib import Path
from typing import Any, List, Callable

home = str(Path.home())
root = os.path.join(home, "Desktop")

DlInfo = namedtuple('DlInfo', ['title', 'music_url', 'img_url'])


def _get_wesing(url: str) -> DlInfo:
    def _get_first_non_empty(elements: List[Any], getter: Callable[[Any], str]):
        for element in elements:
            string = getter(element)
            if string:
                return string

    with urllib.request.urlopen(url) as resp:
        data = resp.read().decode('utf-8')

    matches = re.findall(r'"(playurl|playurl_video)":"(.*?)"', data, re.IGNORECASE | re.MULTILINE)
    media_url = _get_first_non_empty(matches, lambda e: e[1].strip())

    matches = re.findall(r'"song_name":"(.*?)"', data, re.IGNORECASE | re.MULTILINE)
    title = _get_first_non_empty(matches, lambda e: e.strip())

    matches = re.findall(r'"cover":"(.*?)"', data, re.IGNORECASE | re.MULTILINE)
    img_url = _get_first_non_empty(matches, lambda e: e.strip())

    # For 全民K歌 only:
    # `bsy` is too slow and always fail, manually replace to `ws`.
    media_url = media_url.replace('bsy.stream.kg.qq.com', 'ws.stream.kg.qq.com')

    # For 全民K歌 only:
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
