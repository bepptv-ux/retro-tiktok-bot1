import subprocess
from pathlib import Path

SCRIPT_FILE = Path("output/todays_script.txt")
AUDIO_FILE = Path("output/todays_voice.wav")

if not SCRIPT_FILE.exists():
    print("Script not found.")
    exit(1)

AUDIO_FILE.parent.mkdir(parents=True, exist_ok=True)

subprocess.run([
    "kokoro-tts",
    str(SCRIPT_FILE),
    str(AUDIO_FILE),
    "--voice",
    "am_michael"
], check=True)

print("Natural male AI voice created!")
print(AUDIO_FILE)
