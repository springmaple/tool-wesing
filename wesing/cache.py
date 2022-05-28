import hashlib
import json
import os

from wesing.dl import DlInfo

_abspath = os.path.abspath
_join = os.path.join
_dirname = os.path.dirname
cache_dir_root = _abspath(_join(_dirname(__file__), '../.dl_cache'))


def get_hash(dl_info: DlInfo) -> str:
    json_str = json.dumps([dl_info.title,
                           dl_info.music_url.partition('?')[0],
                           dl_info.img_url.partition('?')[0]])
    digest = hashlib.md5(json_str.encode('utf-8')).hexdigest()
    return str(digest[:8]).lower()


def get_cache_dir(cache_dir_name: str) -> str:
    cache_dir = _join(cache_dir_root, cache_dir_name)
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir


def delete_cache_dir():
    if os.path.isdir(cache_dir_root):
        os.system(f'RMDIR /Q /S "{cache_dir_root}"')
