import subprocess
import os
from datetime import datetime

folder = "/home/pi/masterproef"

os.chdir(folder)

now = datetime.now()
small_fp = now.strftime(f"fotos/small-%Y-%m-%d-%H:%M.jpg")
large_fp = now.strftime(f"fotos/large-%Y-%m-%d-%H:%M.jpg")

def run(cmd):
    print(f"Running {cmd}")
    subprocess.run(cmd, shell=True)

run(f"raspistill -t 1 -w 820 -h 616 -o {small_fp}")
run(f"raspistill -t 1 -o {large_fp}")
run(f"git add {small_fp}")
run(f"git commit -m {small_fp}")
run(f"git pull")
run(f"git push")

