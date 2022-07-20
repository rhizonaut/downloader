import os
import urllib
import traceback
from yt_dlp import YoutubeDL
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import uuid
from source import Source
import requests
from item import Item
import subprocess
import magic, mimetypes
# bandcamp-dl is required

# TODO: Unify downloading process:
# 1. url parsing 2. downloading file from source 3. post-download processing
# all downloaded items to separated dir
# add archiving
class Downloader:
    downloads = os.path.join(os.path.abspath(os.getcwd()), 'downloads')

    def download(urls, is_mp3 = False):
        items = [Downloader.__get_item(url, is_mp3) for url in urls]

        for item in items:
            yield Downloader.__download(item, is_mp3)


    def __get_item(url, is_mp3):
        response = requests.get(url, allow_redirects=True)
        if response.status_code != 200:
            raise ValueError(f'Url:{url} returns error code')

        try:
            parsed_url = urllib.parse.urlparse(url)
        except:
            raise ValueError(f'An error occured while parsing url:{url} | {traceback.format_exc()}')

        if parsed_url.netloc in ['www.youtube.com', 'youtu.be']:
            return Item(url, Source.YouTube, is_mp3, response)
        elif 'bandcamp.com' in parsed_url.netloc:
            return Item(url, Source.Bandcamp, is_mp3, response)
        else:
            return Item(url, Source.UrlFile, is_mp3, response)


    def __download(item, is_mp3):
        print(f'Downloading {item.url}')

        if item.source == Source.YouTube:
            return Downloader.__download_yt(item.url, is_mp3)
        elif item.source == Source.Bandcamp:
            return Downloader.__download_bandcamp(item.url)
        elif item.source == Source.UrlFile:
            return Downloader.__download_url(item)
        else:
            raise ValueError(f'Url {item.url} was not processed')


    def __download_bandcamp(url):
        folder = os.path.join(Downloader.downloads, f'{uuid.uuid4()}')
        os.mkdir(folder)
        subprocess.run(
            [
                f'bandcamp-dl',
                '--template=%{artist}-%{album}-%{track} - %{title}',
                '-n',
                f'--base-dir={folder}',
                url
            ])

        return folder


    def __download_url(item):
        folder = os.path.join(Downloader.downloads, f'{uuid.uuid4()}')
        os.mkdir(folder)
        file_name = os.path.join(folder, f'{uuid.uuid4()}')
        open(file_name, 'wb').write(item.response.content)
        ext = mimetypes.guess_extension(magic.Magic(mime=True).from_file(file_name))
        new_file_name = f'{file_name}{ext}'
        os.rename(file_name, new_file_name)

        return folder


    def __download_yt(url, is_mp3):
        if is_mp3:
            return Downloader.__get_yt_mp3(url)
        else:
            return Downloader.__get_yt_mp4(url)


    def __get_yt_mp3(url):
        folder, info = Downloader.__get_yt_file(url, True)
        # TODO: should be working for list of files
        file_name = os.path.join(folder, os.listdir(folder)[0])
        title = info.get("title", None)
        mp3file = MP3(file_name, ID3=EasyID3)
        if '-' in title:
            mp3file['artist'] = title[:title.find('-')].strip()
            mp3file['title'] = title[title.find('-') + 1:].strip()
        else:
            mp3file['artist'] = title
        mp3file.save()

        return folder


    def __get_yt_mp4(url):
        file_name, _ = Downloader.__get_yt_file(url, False)
        return file_name

    def __get_yt_file(url, is_mp3):
        folder = os.path.join(Downloader.downloads, f'{uuid.uuid4()}')
        if is_mp3:
            ydl_opts = {
            'noplaylist': True,
            'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
            }
            with YoutubeDL(ydl_opts) as ydl:
                return folder, ydl.extract_info(url, download=True)
        else:
            ydl_opts = {
            'noplaylist': True,
            'outtmpl': os.path.join(Downloader.downloads, f'{uuid.uuid4()}', '%(title)s.%(ext)s'),
            'format': '18',
            }
            with YoutubeDL(ydl_opts) as ydl:
                return folder, ydl.extract_info(url, download=True)


def get_files(urls):
    files = []

    for folder in Downloader.download(urls, True):
        files.append([os.path.join(folder, file) for file in os.listdir(folder)])

    return files


def main():
    urls = [
        'https://tezteztez.bandcamp.com/album/a', 'https://youtu.be/1zRkbWpJ988?list=RD1zRkbWpJ988', 
    'https://sun9-85.userapi.com/impg/-FT9okSKKmYgZE566TiJ9vX4oChKboTsa4cTRw/PTyC8rNDi6s.jpg?size=964x1280&quality=96&sign=2d15eac6a9323b9231c02fcc109adbc6&type=album']
    files = get_files(urls)
    print(files)


if __name__ == '__main__':
    main()