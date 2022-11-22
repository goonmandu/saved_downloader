# Source: https://stackoverflow.com/a/22058673

import hashlib

BUF_SIZE = 65536  # 64kB chunks to save memory


def chunk_md5(path):
    md5 = hashlib.md5()
    with open(path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


# print(f"MD5: {md5.hexdigest()}")
