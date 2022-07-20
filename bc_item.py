import os
import subprocess
import uuid

class BCItem(object):
    def __init__(self, url, folder):
        self.url = url
        self.folder = folder

    def download(self):
        return self.__download(self.url)

    def __download(self, url):
        result_folder = os.path.join(self.folder, f'{uuid.uuid4()}')
        os.mkdir(result_folder)
        subprocess.run(
            [
                f'bandcamp-dl',
                '--template=%{artist} - %{title}',
                '-n',
                f'--base-dir={result_folder}',
                url
            ])

        return result_folder