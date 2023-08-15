import argparse

import check_run
from update_tools import check_local_hash, download_files

if __name__ == "__main__":
    check_run.check()
    parser = argparse.ArgumentParser()
    parser.add_argument('--local_dir', type=str, default='.', help='dataset.yaml path')
    opt = parser.parse_args()
    files_to_download = check_local_hash(opt.local_dir)
    print(f'发现需要更新文件:{files_to_download}')
    download_files(files_to_download)
    print("Press any key to exit...")
    input()
