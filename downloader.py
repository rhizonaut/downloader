import os
import urllib
import traceback
import requests
from url_item  import UrlItem
from yt_item import YTItem
from bc_item import BCItem
# bandcamp-dl is required

# TODO: Unify downloading process:
# 1. url parsing 2. downloading file from source 3. post-download processing
# all downloaded items to separated dir
# add archiving
class Downloader(object):
    downloads = os.path.join(os.path.abspath(os.getcwd()), 'downloads')

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

        if parsed_url.netloc in ['www.youtube.com', 'youtu.be']:
            return YTItem(url, Downloader.downloads, is_mp3)
        elif 'bandcamp.com' in parsed_url.netloc:
            return BCItem(url, Downloader.downloads)
        else:
            return UrlItem(Downloader.downloads, response)
