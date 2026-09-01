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
    text
], check=True)

print("Voice created successfully:")
print(AUDIO_FILE)
