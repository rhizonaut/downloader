import os
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from yt_dlp import YoutubeDL
import uuid

class YTItem(object):
    def __init__(self, url, folder, is_mp3):
        self.url = url
        self.is_mp3 = is_mp3
        self.folder = folder


    def download(self=None, folder=None, url=None, is_mp3=None):
        if self:
            return YTItem.__download_yt(self.folder, self.url, self.is_mp3)

        if folder == None:
            raise ValueError(f'folder argument should be not None')
        
        if url == None:
            raise ValueError(f'url argument should be not None')

        if is_mp3 == None:
            raise ValueError(f'is_mp3 argument should be not None')

        return YTItem.__download_yt(folder, url, is_mp3)

    def __download_yt(folder, url, is_mp3):
        if is_mp3:
            return YTItem.__get_yt_mp3(folder, url)
        else:
            return YTItem.__get_yt_mp4(folder, url)


    def __get_yt_mp3(folder, url):
        result_folder, info = YTItem.__get_yt_file(folder, url, True)
        # TODO: should be working for list of files
        file_name = os.path.join(result_folder, os.listdir(result_folder)[0])
        title = info.get("title", None)
        mp3file = MP3(file_name, ID3=EasyID3)
        if '-' in title:
            mp3file['artist'] = title[:title.find('-')].strip()
            mp3file['title'] = title[title.find('-') + 1:].strip()
        else:
            mp3file['artist'] = title
        mp3file.save()

        return result_folder


    def __get_yt_mp4(folder, url):
        file_name, _ = YTItem.__get_yt_file(folder, url, False)
        return file_name

    def __get_yt_file(folder, url, is_mp3):
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
            'outtmpl': os.path.join(folder, f'{uuid.uuid4()}', '%(title)s.%(ext)s'),
            'format': '18',
            }
            with YoutubeDL(ydl_opts) as ydl:
                return folder, ydl.extract_info(url, download=True)