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
    def chdir(folder):
        os.chdir(folder)
        if not os.path.exists('original'):
            os.mkdir('original')
        
    def run(cmd):
        print(f"Running {cmd}")
        subprocess.run(cmd, shell=True)

    chdir('/home/pi')
    large_fp = now.strftime(f"original/large-%Y-%m-%d-%H-%M.jpg")
    run(f"raspistill -t 1 -o {large_fp}")
    
    chdir('/home/pi/masterproef')
    small_fp = now.strftime(f"original/small-%Y-%m-%d-%H-%M.jpg")
    run(f"raspistill -t 1 -w 820 -h 616 -o {small_fp}")
    run(f"git add {small_fp}")
    run(f"git commit -m {small_fp}")
    run(f"git pull")
    run(f"git push")

