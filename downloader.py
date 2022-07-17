import os
import urllib
import traceback
from yt_dlp import YoutubeDL
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import uuid

class Downloader:
    def __init__():
        pass

    downloads = os.path.join(os.path.abspath(os.getcwd()), 'downloads')

    @staticmethod
    def download(urls, is_mp3 = False):
        for url in urls:
            Downloader.__download(url, is_mp3)

    def __download(url, is_mp3):
        if url == None or type(url) != str:
            raise ValueError('Passed url is None or not str')

        try:
            parsed_url = urllib.parse.urlparse(url)
        except Exception:
            raise ValueError(f'An error occured while parsing url:{url} | {traceback.format_exc()}')

        print(f'downloading {url}')

        if parsed_url.netloc in ['www.youtube.com', 'youtu.be']:
            Downloader.download_yt(url, is_mp3)

    @staticmethod
    def download_yt(url, is_mp3):
        if is_mp3:
            return Downloader.__get_yt_mp3(url)
        else:
            return Downloader.__get_yt_mp4(url)


    def __get_yt_mp3(url):
        file_name, info = Downloader.__get_yt_file(url, True)
        title = info.get("title", None)
        mp3file = MP3(file_name, ID3=EasyID3)
        if '-' in title:
            mp3file['artist'] = title[:title.find('-')].strip()
            mp3file['title'] = title[title.find('-') + 1:].strip()
        else:
            mp3file['artist'] = title
        mp3file.save()

        return file_name

    def __get_yt_mp4(url):
        file_name, _ = Downloader.__get_yt_file(url, False)
        return file_name

    def __get_yt_file(url, is_mp3):
        if is_mp3:
            file_name = os.path.join(Downloader.downloads, f'{uuid.uuid4()}' + '.mp3')
            ydl_opts = {
            'noplaylist': True,
            'outtmpl': file_name,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
            }
            with YoutubeDL(ydl_opts) as ydl:
                return file_name, ydl.extract_info(url, download=True)
        else:
            file_name = os.path.join(Downloader.downloads, f'{uuid.uuid4()}' + '.mp4')
            ydl_opts = {
            'noplaylist': True,
            'outtmpl': file_name,
            'format': '18',
            }
            with YoutubeDL(ydl_opts) as ydl:
                return file_name, ydl.extract_info(url, download=True)


def main():
    Downloader.download(['https://www.youtube.com/watch?v=PI-cESvGlKc&ab_channel=CloserToTruth'], True)


if __name__ == '__main__':
    main()