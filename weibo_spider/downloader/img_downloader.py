import os

from .downloader import Downloader
from ..uploader.upload_file import UploadFile

class ImgDownloader(Downloader):
    def __init__(self, file_dir):
        self.file_dir = file_dir
        self.describe = u'图片'
        self.key = 'original_pictures'
        self.uploader = UploadFile()

    def handle_download(self, urls, w):
        local_paths = []
        """处理下载相关操作"""
        file_prefix = w.publish_time[:11].replace('-', '') + '_' + w.id
        if ',' in urls:
            url_list = urls.split(',')
            for i, url in enumerate(url_list):
                index = url.rfind('.')
                if len(url) - index >= 5:
                    file_suffix = '.jpg'
                else:
                    file_suffix = url[index:]
                file_name = file_prefix + '_' + str(i + 1) + file_suffix
                file_path = self.file_dir + os.sep + file_name
                self.download_one_file(url, file_path, w.id)
                local_paths.append(file_path)
        else:
            index = urls.rfind('.')
            if len(urls) - index > 5:
                file_suffix = '.jpg'
            else:
                file_suffix = urls[index:]
            file_name = file_prefix + file_suffix
            file_path = self.file_dir + os.sep + file_name
            self.download_one_file(urls, file_path, w.id)
            local_paths.append(file_path)

        cdn_paths = self.uploader.batch_upload(local_paths)
        w.uploaded_pictures = cdn_paths
