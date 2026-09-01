import json
import subprocess
from pathlib import Path

GAMES_FILE = Path("games/games.json")
USED_FILE = Path("games/used_games.json")
AUDIO_FILE = Path("output/todays_voice.wav")
VIDEO_FILE = Path("output/todays_video.mp4")

with open(GAMES_FILE, "r", encoding="utf-8") as f:
    games = json.load(f)

with open(USED_FILE, "r", encoding="utf-8") as f:
    used = json.load(f)

game_title = used[-1]

game = next(
    game for game in games
    if game["title"] == game_title
)

subprocess.run([
    "ffmpeg",
    "-y",
    "-f", "lavfi",
    "-i", "color=black:s=1080x1920:r=30",
    "-i", str(AUDIO_FILE),
    "-vf",
    "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:"
    "text='RETRO GAME OF THE DAY':"
    "fontsize=60:"
    "fontcolor=white:"
    "x=(w-text_w)/2:"
    "y=300",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-shortest",
    str(VIDEO_FILE)
], check=True)

print("Video created successfully!")
print(game["title"])
print(VIDEO_FILE)
