# 获取服务器的file_path和hash
import os

import requests
from tqdm import tqdm

from check import FileHashUtil

response = requests.get('http://1.15.138.227:8123/filehashes')
server_hashes = response.json()


# local_dir = "D:/Desktop/apex_gun"
#
# local_hashes = FileHashUtil.scan_directory(local_dir)


def check_remote_hash(local_dir):
    # 遍历本地的file_path和hash
    local_hashes = FileHashUtil.scan_directory(local_dir)
    no_match_dict = {}
    for file_path, file_hash in local_hashes.items():
        remote_file_path = ('./apex_gun' + file_path)
        # 如果本地文件的hash与服务器的hash不匹配或者在服务器的hash中不存在，打印出来
        if remote_file_path not in server_hashes:
            print(f'Not exist in remote: {remote_file_path}')
            no_match_dict[local_dir + file_path] = remote_file_path
        elif local_hashes[file_path] != server_hashes[remote_file_path]:
            print(f'Mismatch: {remote_file_path}')
            no_match_dict[local_dir + file_path] = remote_file_path
    return no_match_dict


def check_local_hash(local_dir):
    local_hashes = FileHashUtil.scan_directory(local_dir)
    # 遍历服务器的file_path和hash
    no_match_dict = {}
    for file_path, file_hash in server_hashes.items():
        local_file_path = file_path.replace("./apex_gun", '')
        # 如果服务器的文件在本地不存在，打印出来
        if local_file_path == '/config/global_config.json':
            continue
        if local_file_path not in local_hashes:
            print(f'Not exist in local: {local_file_path}')
            no_match_dict[file_path] = local_dir + local_file_path
        elif local_hashes[local_file_path] != server_hashes[file_path]:
            print(f'Mismatch: {file_path}')
            no_match_dict[file_path] = local_dir + local_file_path
    return no_match_dict


def upload_files(files_to_upload):
    try:
        with tqdm(files_to_upload.items(), desc='Uploading files', total=len(files_to_upload), unit='file') as t:
            for local_file_path, remote_file_path in t:
                # tqdm.write(f'Uploading {local_file_path} to {remote_file_path}')
                with open(local_file_path, 'rb') as f:
                    files = {'file': (remote_file_path, f)}
                    response = requests.post('http://1.15.138.227:8123/upload', files=files)
                    if response.status_code == 200:
                        tqdm.write(f'Successfully uploaded {local_file_path} to {remote_file_path}')
                    else:
                        tqdm.write(f'Failed to upload {local_file_path} to {remote_file_path}')
    except KeyboardInterrupt:
        t.close()
        raise
    t.close()


def download_files(files_to_download):
    # for remote_file_path, local_file_path in files_to_download.items():
    try:
        # for remote_file_path, local_file_path in tqdm(files_to_download.items(), desc='Downloading files',
        #                                               total=len(files_to_download), unit='file'):
        with tqdm(files_to_download.items(), desc='Downloading files',
                  total=len(files_to_download), unit='file') as t:
            for remote_file_path, local_file_path in t:
                # tqdm.write(f'Downloading {remote_file_path} to {local_file_path}')
                local_dir = os.path.dirname(local_file_path)
                if not os.path.exists(local_dir):
                    os.makedirs(local_dir)
                response = requests.post('http://1.15.138.227:8123/download', data={'path': remote_file_path},
                                         stream=True)
                # 获取文件大小
                total_size = int(response.headers.get('content-length', 0))
                # 使用tqdm显示下载进度
                with open(local_file_path, 'wb') as f:
                    try:
                        with tqdm(total=total_size, unit='B', unit_scale=True, desc=local_file_path,
                                  leave=True) as pbar:
                            for data in response.iter_content(1024 * 1024):
                                f.write(data)
                                pbar.update(len(data))
                    except KeyboardInterrupt:
                        pbar.close()
                        raise
                    pbar.close()
                t.update(1)
    except KeyboardInterrupt:
        t.close()
        raise
    t.close()
    # for data in tqdm(response.iter_content(1024), total=total_size, unit='B', unit_scale=True):
    #     f.write(data)
    # with open(local_file_path, 'wb') as f:
    #     f.write(response.content)
    # tqdm.write(f'Successfully downloaded {remote_file_path} to {local_file_path}')
