import subprocess
from pathlib import Path

SCRIPT_FILE = Path("output/todays_script.txt")
AUDIO_FILE = Path("output/todays_voice.wav")

if not SCRIPT_FILE.exists():
    print("Script not found.")
    exit(1)

text = SCRIPT_FILE.read_text(encoding="utf-8")

subprocess.run([
    "espeak-ng",
    "-w",
    str(AUDIO_FILE),
    "-s", "175",
    "-p", "35",
    "-a", "180",
    text
], check=True)

print("Male energetic voice created successfully!")
print(AUDIO_FILE)
