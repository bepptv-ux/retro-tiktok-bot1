import subprocess
from pathlib import Path

AUDIO = Path("output/todays_voice.wav")
VIDEO = Path("output/todays_video.mp4")

if not AUDIO.exists():
    print("Voice file not found.")
    exit(1)

duration = subprocess.check_output([
    "ffprobe",
    "-v", "error",
    "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1",
    str(AUDIO)
]).decode().strip()

subprocess.run([
    "ffmpeg",
    "-y",
    "-f", "lavfi",
    "-i", "color=c=black:s=1080x1920:r=30",
    "-i", str(AUDIO),
    "-t", duration,
    "-vf",
    "drawtext=text='RETRO GAME OF THE DAY':"
    "fontcolor=white:fontsize=64:"
    "x=(w-text_w)/2:y=500",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-shortest",
    str(VIDEO)
], check=True)

print("Video created successfully:")
print(VIDEO)
