import os
import subprocess
from pathlib import Path

home = str(Path.home())
root = os.path.join(home, "Desktop")
for subdir in [x[0] for x in os.walk(root)]:
    # master = os.path.join(subdir, "macro-output", "master.mp3")
    master = os.path.join(subdir, "master.mp3")
    source = os.path.join(subdir, "source.jpg")
    if os.path.exists(master) and os.path.exists(source):
        title = os.path.basename(subdir)
        subprocess.check_output([
            'ffmpeg', '-i', master, '-i', source,
            '-metadata', f'title={title}',
            '-metadata:s:v', 'comment="Cover (front)"',
            '-map', '0:0', '-map', '1:0', '-id3v2_version', '3',
            '-codec', 'copy', '-y', f'{title}.mp3'
        ], cwd=subdir)
