import os
import subprocess

class BCItem(object):
    def __init__(self, url, folder):
        self.url = url
        self.folder = folder

    def download(self=None, folder=None, url=None):
        if self:
            return BCItem.__download(self.url, self.folder)
        
        if folder == None:
            raise ValueError(f'folder argument should be not None')
        
        if url == None:
            raise ValueError(f'url argument should be not None')

        return BCItem.__download(url, folder)


    def __download(url, folder):
        os.mkdir(folder)
        subprocess.run(
            [
                f'bandcamp-dl',
                '--template=%{artist} - %{title}',
                '-n',
                f'--base-dir={folder}',
                url
            ])

        return folder