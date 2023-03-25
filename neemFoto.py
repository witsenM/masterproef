import subprocess
from datetime import datetime

folder = "/home/pi/masterproef/fotos/"

now = datetime.now()
small_fp = now.strftime(f"{folder}small-%Y-%m-%d-%Hu.jpg")
large_fp = now.strftime(f"{folder}large-%Y-%m-%d-%Hu.jpg")

def run(cmd):
    print(f"Running {cmd}")
    subprocess.run(cmd, shell=True)

run(f"raspistill -t 1 -w 820 -h 616 -o {small_fp}")
run(f"raspistill -t 1 -o {large_fp}")
run(f"git add {small_fp}")
run(f"git commit -m {small_fp}")
run(f"git pull")
run(f"git push")

