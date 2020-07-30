import os
import requests
import hashlib
import time

class UploadFile:
    def __init__(self):
        self.upload_path_prefix = 'http://upload1.file.market.miui.srv/upload?channel=Oebjfre'
        self.download_path_prefix = 'http://t1.market.xiaomi.com/download/{}/{}'

    def single_upload(self, path):
        url = self.upload_path_prefix
        md5_val = self.get_file_sha1(path)
        t = time.time()
        n = int(round(t * 1000))
        size = os.path.getsize(path)
        f = open(path, 'rb')
        dir, file = os.path.split(path)
        header = {
            'Content-Range': "bytes {0}-{1}/{2}".format(0, size-1, size),
            'Session-ID': md5_val + '-' + str(n),
            'Content-Disposition': "attachment; filename=\"" + file + "\"",
            'Content-Type': "application/octet-stream"
        }  # 上传文件请求的头信息
        res = requests.post(url=url, headers=header, data=f.read(), verify=False)
        if res.status_code == 200:
            response = res.json()
            return self.download_path_prefix.format(response[0]['exloc'], file)
        else:
            return ''

    def batch_upload(self, paths):
        cdn_paths = []
        for path in paths:
            cdn_paths.append(self.single_upload(path))
        return cdn_paths

    def get_file_sha1(self, file_path):
        with open(file_path, 'rb') as f:
            md5obj = hashlib.sha1()
            md5obj.update(f.read())
            _hash = md5obj.hexdigest()
        return str(_hash).upper()
