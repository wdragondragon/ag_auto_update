import argparse

import requests

import check_run
from update_tools import check_remote_hash, upload_files

if __name__ == "__main__":
    check_run.check()
    parser = argparse.ArgumentParser()
    parser.add_argument('--local_dir', type=str, default='.', help='dataset.yaml path')
    opt = parser.parse_args()
    files_to_upload = check_remote_hash(opt.local_dir)
    print(f'发现需要更新文件:{files_to_upload}')
    upload_files(files_to_upload)
    if len(files_to_upload) > 0:
        response = requests.get('http://1.15.138.227:8123/refresh_files')
        print(response.text)
    print("Press any key to exit...")
    input()
