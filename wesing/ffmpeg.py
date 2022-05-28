import os
import subprocess

_abspath = os.path.abspath
_join = os.path.join
_dirname = os.path.dirname
ffmpeg_exe = _abspath(_join(_dirname(__file__), '../bin/ffmpeg.exe'))


def convert_media(source_path: str, dest_path: str):
    subprocess.check_call([
        ffmpeg_exe, '-i', source_path, dest_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def compile_final_mp3(title: str,
                      album_name: str,
                      artist_name: str,
                      genre: str,
                      mp3_path: str,
                      jpg_path: str,
                      dest_dir: str) -> str:
    output_path = _get_unique_path(dest_dir, title, 'mp3')
    subprocess.check_call([
        ffmpeg_exe, '-i', mp3_path, '-i', jpg_path,
        '-metadata', f'title={title}',
        '-metadata', f'artist={artist_name}',
        '-metadata', f'album_artist={artist_name}',
        '-metadata', f'album={album_name}',
        '-metadata', f'genre={genre}',
        '-metadata:s:v', 'comment="Cover (front)"',
        '-map', '0:0', '-map', '1:0', '-id3v2_version', '3',
        '-codec', 'copy', '-y',
        output_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path


def _get_unique_path(dest_dir: str, file_name: str, file_ext: str) -> str:
    output_path = os.path.join(dest_dir, f'{file_name}.{file_ext}')
    increment_id = 0
    while os.path.exists(output_path):
        increment_id += 1
        output_path = os.path.join(dest_dir, f'{file_name}_{increment_id}.{file_ext}')
    return output_path
