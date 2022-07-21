import os
import urllib
import traceback
import requests
from url_item  import UrlItem
from yt_item import YTItem
from bc_item import BCItem
import uuid
# bandcamp-dl is required

# TODO
# add archiving
# add set_options() which sets them only if idle
# pass file name into items
class Downloader(object):
    __downloads = os.path.join(os.path.abspath(os.getcwd()), 'downloads')

    # TODO someday make public after making download() return filepaths
    __is_create_subdirs = False

    def download(urls, is_mp3 = False):
        items = [Downloader.__get_item(url, is_mp3) for url in urls]

        for item in items:
            yield item.download()


    def __get_item(url, is_mp3):
        response = requests.get(url, allow_redirects=True)
        if response.status_code != 200:
            raise ValueError(f'Url:{url} returns error code')

        try:
            parsed_url = urllib.parse.urlparse(url)
        except:
            raise ValueError(f'An error occured while parsing url:{url} | {traceback.format_exc()}')

        folder = os.path.join(Downloader.downloads, f'{uuid.uuid4()}') if Downloader.__is_create_subdirs else folder
        if parsed_url.netloc in ['www.youtube.com', 'youtu.be']:
            return YTItem(url, folder, is_mp3)
        elif 'bandcamp.com' in parsed_url.netloc:
            return BCItem(url, folder)
        else:
            return UrlItem(folder, response)
