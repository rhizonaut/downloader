import os
import urllib
import traceback
from yt_dlp import YoutubeDL
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import uuid
from source import Source
import requests
import mimetypes
from item import Item
from bandcamp_dl import BandcampDownloader
from bandcamp_dl import Bandcamp

class Downloader:
    downloads = os.path.join(os.path.abspath(os.getcwd()), 'downloads')

    @staticmethod
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
        elif item.source == Source.UrlFile:
            return Downloader.__download_url(item)
        else:   
            raise ValueError(f'Url {item.url} was not processed')


    # def __download_bandcamp(item):
    #     bd = BandcampDownloader(url=item.url)
    #     bd.start()


    def __download_url(item):
        content_type = item.response.headers['content-type']
        ext = mimetypes.guess_extension(content_type)
        file_name = os.path.join(Downloader.downloads, f'{uuid.uuid4()}.{ext}')
        open(file_name, 'wb').write(item.response.content)


    def __download_yt(url, is_mp3):
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
            file_name = os.path.join(Downloader.downloads, f'{uuid.uuid4()}.mp3')
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
    urls = ['https://t4.bcbits.com/stream/768defd85435ba93ba46657d6212a45e/mp3-128/2503872319?p=0&ts=1658344844&t=fd07091aca227d8e4e1e7c1863268e0e8e3184fe&token=1658344844_f86885f65f0d54a68f22194706f0454d582e0539']
    for file in Downloader.download(urls, True):
        print(file)


if __name__ == '__main__':
    main()