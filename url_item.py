import os
import magic, mimetypes
import uuid

class UrlItem(object):
    def __init__(self, folder, response):
        self.folder = folder
        self.response = response

    def download(self):
        return self.__download_url(self.response)

    def __download_url(self, response):
        result_folder = os.path.join(self.folder, f'{uuid.uuid4()}')
        os.mkdir(result_folder)
        file_name = os.path.join(result_folder, f'{uuid.uuid4()}')
        open(file_name, 'wb').write(response.content)
        ext = mimetypes.guess_extension(magic.Magic(mime=True).from_file(file_name))
        new_file_name = f'{file_name}{ext}'
        os.rename(file_name, new_file_name)

        return result_folder
