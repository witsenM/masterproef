import subprocess
from datetime import datetime

folder = "/home/pi/masterproef/fotos/"

now = datetime.now()
filename = now.strftime(f"{folder}foto-%Y-%m-%d-%Hu.jpg")

cmd = f"raspistill -t 1 -o {filename}"
subprocess.run(cmd, shell=True)

subprocess.run(f"git add {filename}")
subprocess.run(f"git commit -m {filename}")
subprocess.run(f"git pull")
subprocess.run(f"git push")

