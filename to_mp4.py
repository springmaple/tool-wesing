import os
import subprocess
from pathlib import Path

FILE_SUFFIX = '_20191021'
home = str(Path.home())
root = os.path.join(home, "Desktop")
for subdir in [x[0] for x in os.walk(root)]:
    # master = os.path.join(subdir, "macro-output", "master.mp3")
    master = os.path.join(subdir, "master.mp3")
    source = os.path.join(subdir, "source.jpg")
    if os.path.exists(master) and os.path.exists(source):
        subprocess.check_output([
            'ffmpeg', '-loop', '1', '-i', source, '-i', master, '-c:a', 'aac', '-c:v', 'libx264', '-shortest',
            f'{os.path.basename(subdir)}{FILE_SUFFIX}.mp4'
        ], cwd=subdir)
