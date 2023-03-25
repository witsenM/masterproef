import subprocess
import os
from datetime import datetime

def uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
    return uptime_seconds

take_picture = False

if uptime() <= 5*60:
    take_picture = True

now = datetime.now()

if now.time().hour % 4 == 0 and now.time().minute == 30:
    take_picture = True

if take_picture:
    folder = '/home/pi/masterproef'
    subfolder = 'fotos'

    os.chdir(folder)

    if not os.path.exists(subfolder):
        os.mkdir(subfolder)

    small_fp = now.strftime(f"{subfolder}/small-%Y-%m-%d-%H-%M.jpg")
    large_fp = now.strftime(f"{subfolder}/large-%Y-%m-%d-%H-%M.jpg")

    def run(cmd):
        print(f"Running {cmd}")
        subprocess.run(cmd, shell=True)

    run(f"raspistill -t 1 -w 820 -h 616 -o {small_fp}")
    run(f"raspistill -t 1 -o {large_fp}")
    run(f"git add {small_fp}")
    run(f"git commit -m {small_fp}")
    run(f"git pull")
    run(f"git push")

