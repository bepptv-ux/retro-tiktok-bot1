import subprocess
from pathlib import Path

AUDIO_FILE = Path("output/todays_voice.wav")
VIDEO_FILE = Path("output/todays_video.mp4")

if not AUDIO_FILE.exists():
    print("Voice file not found.")
    exit(1)

VIDEO_FILE.parent.mkdir(parents=True, exist_ok=True)

command = [
    "ffmpeg",
    "-y",
    "-f", "lavfi",
    "-i", "color=c=black:s=1080x1920:r=30",
    "-i", str(AUDIO_FILE),
    "-vf",
    "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:"
    "text='RETRO GAME OF THE DAY':"
    "fontcolor=white:"
    "fontsize=60:"
    "x=(w-text_w)/2:"
    "y=300",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-shortest",
    str(VIDEO_FILE)
]

print("Creating video...")

subprocess.run(command, check=True)

if VIDEO_FILE.exists():
    print("VIDEO CREATED SUCCESSFULLY!")
    print(VIDEO_FILE)
else:
    print("VIDEO WAS NOT CREATED.")
    exit(1)
