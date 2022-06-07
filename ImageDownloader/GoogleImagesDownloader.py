# pip install git+https://github.com/Joeclinton1/google-images-download.git

from google_images_download import google_images_download

downloader = google_images_download.googleimagesdownload()

search_queries = [
    'hand'
]


def download_images(query):
    arguments = {"keywords": query,
                 "format": "png",
                 "limit": 10,
                 "print_urls": True,
                 # "size": "medium", # large, medium, icon
                 # "aspect_ratio": "panoramic" # tall, square, wide, panoramic
                 }
    downloader.download(arguments)


if __name__ == '__main__':
    for query in search_queries:
        download_images(query)
        print()
