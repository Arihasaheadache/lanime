import subprocess

subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
subprocess.run(["playwright", "install", "chromium"], check=True)

print("Everything has been downloaded! Now run scrape.py >:3")
