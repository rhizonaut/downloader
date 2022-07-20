from downloader import Downloader
import os

def get_files(urls):
    files = []

    for folder in Downloader.download(urls, True):
        files.append([os.path.join(folder, file) for file in os.listdir(folder)])

    return files


def main():
    urls = [
        'https://tezteztez.bandcamp.com/album/a', 'https://youtu.be/1zRkbWpJ988?list=RD1zRkbWpJ988', 
    'https://sun9-85.userapi.com/impg/-FT9okSKKmYgZE566TiJ9vX4oChKboTsa4cTRw/PTyC8rNDi6s.jpg?size=964x1280&quality=96&sign=2d15eac6a9323b9231c02fcc109adbc6&type=album']
    files = get_files(urls)
    print(files)


if __name__ == '__main__':
    main()