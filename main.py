import subprocess
from urllib import request
import os
from music import WeSing
from music import Meta
import shutil


class Network:
    @staticmethod
    def download_source(url):
        with request.urlopen(url) as resp:
            return resp.read().decode('utf-8')

    @staticmethod
    def download_music(music_url, target_file):
        with request.urlopen(music_url) as resp:
            with open(target_file, mode='wb') as file:
                file.write(resp.read())

    @staticmethod
    def download_image(url, target_file):
        with request.urlopen(url) as resp:
            with open(target_file, mode='wb') as file:
                file.write(resp.read())


class Converter:
    @staticmethod
    def to_mp3(input_file, output_name, meta=None):
        args = ['ffmpeg', '-i', input_file]
        if meta:
            for key, value in meta.items():
                args += ['-metadata', '%s="%s"' % (key, value)]

        output_file = output_name + '.mp3'
        args += [output_file]

        subprocess.run(args, stdout=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        return output_file


def download_wesing_music(url, output_dir):
    src = Network.download_source(url)
    wesing = WeSing(src)
    meta = wesing.get_meta()

    tmp_file = 'original.m4a'
    play_url = wesing.get_music_url()
    Network.download_music(play_url, tmp_file)

    title = meta.get(Meta.Title, 'Untitled')
    output_file = Converter.to_mp3(tmp_file, title, meta)

    image_file = 'cover.jpg'
    Network.download_image(wesing.get_cover(), image_file)

    shutil.move(output_file, os.path.join(output_dir, output_file))
    shutil.move(tmp_file, os.path.join(output_dir, tmp_file))
    shutil.move(image_file, os.path.join(output_dir, image_file))


if __name__ == '__main__':
    SONG_URL = r'https://wesingapp.com/play?s=5kx5CaH515XNDH5x&lang=en'
    OUTPUT_DIR = r'C:\Users\wilson.ong\Desktop'
    download_wesing_music(SONG_URL, OUTPUT_DIR)
