import os
from pathlib import Path

home = str(Path.home())
root = os.path.join(home, "Desktop")
raw_file = os.path.join(root, "raw.txt")
url_file = os.path.join(root, "url.txt")

urls = set()
with open(raw_file, mode='r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        index = line.find('http')
        if index < 0:
            continue

        line = line[index:]
        url, _, _1 = line.partition(' ')
        urls.add(url)

with open(url_file, mode='w', encoding='utf-8') as f:
    for url in urls:
        print(url, file=f)
