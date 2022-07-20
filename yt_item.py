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

    def download(self):
        return self.__download_yt(self.url, self.is_mp3)

    def __download_yt(self, url, is_mp3):
        if is_mp3:
            return self.__get_yt_mp3(url)
        else:
            return self.__get_yt_mp4(url)


    def __get_yt_mp3(self, url):
        result_folder, info = self.__get_yt_file(url, True)
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


    def __get_yt_mp4(self, url):
        file_name, _ = self.__get_yt_file(url, False)
        return file_name

    def __get_yt_file(self, url, is_mp3):
        result_folder = os.path.join(self.folder, f'{uuid.uuid4()}')
        if is_mp3:
            ydl_opts = {
            'noplaylist': True,
            'outtmpl': os.path.join(result_folder, '%(title)s.%(ext)s'),
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }],
            }
            with YoutubeDL(ydl_opts) as ydl:
                return result_folder, ydl.extract_info(url, download=True)
        else:
            ydl_opts = {
            'noplaylist': True,
            'outtmpl': os.path.join(self.folder, f'{uuid.uuid4()}', '%(title)s.%(ext)s'),
            'format': '18',
            }
            with YoutubeDL(ydl_opts) as ydl:
                return result_folder, ydl.extract_info(url, download=True)