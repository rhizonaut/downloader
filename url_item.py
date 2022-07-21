import os
import magic, mimetypes
import uuid
import requests

class UrlItem(object):
    def __init__(self, folder, response):
        self.folder = folder
        self.response = response

    def download(self=None, folder=None, url = None, response = None):
        if self:
            return UrlItem.__download_url(response=self.response, folder=self.folder)
        
        if url == None and response == None:
            raise ValueError(f'Either url or response argument should be not None')
        if folder == None:
            raise ValueError(f'folder argument should be not None')

        response = response if response else requests.get(url, allow_redirects=True)
        if response.status_code != 200:
            raise ValueError(f'Url:{url} returns error code')
        return UrlItem.__download_url(response=response, folder=folder)

    def __download_url(response, folder):
        os.mkdir(folder)
        file_name = os.path.join(folder, f'{uuid.uuid4()}')
        open(file_name, 'wb').write(response.content)
        ext = mimetypes.guess_extension(magic.Magic(mime=True).from_file(file_name))
        new_file_name = f'{file_name}{ext}'
        os.rename(file_name, new_file_name)

        return folder
