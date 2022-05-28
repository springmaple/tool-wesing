import argparse
import os
from typing import List

from wesing.cache import get_cache_dir, get_hash, delete_cache_dir
from wesing.dl import dl_media, get_dl_info, DlInfo
from wesing.ffmpeg import convert_media, compile_final_mp3
from wesing.find_url import find_urls


def _get_urls_from_file(raw_file: str) -> List[str]:
    with open(raw_file, mode='r', encoding='utf-8') as f:
        content = f.read()
    return find_urls(content)


def _dl_media_to_cache(cache_dir: str, media_file_name: str, media_url: str) -> str:
    media_path = os.path.join(cache_dir, media_file_name)
    if not os.path.isfile(media_path):
        media_data = dl_media(media_url)
        with open(media_path, 'wb') as f:
            f.write(media_data)
    return media_path


def _convert_media_to_cache(source_path: str, dest_path: str):
    if not os.path.isfile(dest_path):
        convert_media(source_path, dest_path)


def _write_dl_info_to_cache(cache_dir: str, dl_info: DlInfo):
    with open(os.path.join(cache_dir, 'info.txt'), mode='w', encoding='utf-8') as f:
        print('Title:', dl_info.title, file=f)
        print('Music:', dl_info.music_url, file=f)
        print('Cover:', dl_info.img_url, file=f)


def _change_file_ext(source_path: str, new_ext: str) -> str:
    def _get_file_name_no_ext(path: str) -> str:
        return os.path.splitext(os.path.basename(path))[0]

    filename = _get_file_name_no_ext(source_path)
    return os.path.join(os.path.dirname(source_path), f'{filename}.{new_ext}')


def main(raw_urls_file_path: str,
         dest_dir_path: str,
         album_name: str,
         artist_name: str,
         genre: str):
    urls = _get_urls_from_file(raw_urls_file_path)
    os.makedirs(dest_dir_path, exist_ok=True)
    print(f'Found {len(urls)} URLs, retrieving metadata... ', end='', flush=True)

    dl_infos = [get_dl_info(url) for url in urls]
    print('[OK]', flush=True)
    for index, dl_info in enumerate(dl_infos, start=1):
        if not all([dl_info.title, dl_info.music_url, dl_info.img_url]):
            print(f'[{index}/{len(dl_infos)}] Metadata missing! [FAILED]', flush=True)
            continue
           
        print(f'[{index}/{len(dl_infos)}] {dl_info.title} ', end='', flush=True)

        cache_dir = get_cache_dir(get_hash(dl_info))
        _write_dl_info_to_cache(cache_dir, dl_info)
        print(f'({os.path.basename(cache_dir)}) -> ', end='', flush=True)

        mp4_path = _dl_media_to_cache(cache_dir, 'raw.mp4', dl_info.music_url)
        jfif_path = _dl_media_to_cache(cache_dir, 'raw.jfif', dl_info.img_url)

        mp3_path = _change_file_ext(mp4_path, 'mp3')
        jpg_path = _change_file_ext(jfif_path, 'jpg')

        _convert_media_to_cache(mp4_path, mp3_path)
        _convert_media_to_cache(jfif_path, jpg_path)

        final_mp3_path = compile_final_mp3(dl_info.title,
                                           album_name,
                                           artist_name,
                                           genre,
                                           mp3_path,
                                           jpg_path,
                                           dest_dir_path)
        print(f'{final_mp3_path} [OK]', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='wesing', add_help=True)
    parser.add_argument('urls_file', type=str, help='A file that contains list of URLs')
    parser.add_argument('dest_dir', type=str, help='Destination directory')
    parser.add_argument('-album', type=str, required=False, default='', help='Album')
    parser.add_argument('-artist', type=str, required=False, default='', help='Artist')
    parser.add_argument('-genre', type=str, required=False, default='', help='Genre')
    parser.add_argument('-d', required=False, default=False, action='store_true', help='Delete cache folder')
    args = parser.parse_args()

    if args.d:
        delete_cache_dir()

    main(os.path.abspath(args.urls_file),
         os.path.abspath(args.dest_dir),
         args.album,
         args.artist,
         args.genre)
