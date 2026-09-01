import json
import subprocess
from pathlib import Path

GAMES_FILE = Path("games/games.json")
USED_FILE = Path("games/used_games.json")
SCRIPT_FILE = Path("output/todays_script.txt")
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

duration = subprocess.check_output([
    "ffprobe",
    "-v", "error",
    "-show_entries", "format=duration",
    "-of", "default=noprint_wrappers=1:nokey=1",
    str(AUDIO_FILE)
]).decode().strip()

title = game["title"].replace(":", "\\:")
year = str(game["year"])
system = game["system"].replace(":", "\\:")
genre = game["genre"].replace(":", "\\:")

filter_text = (
    "drawtext=text='RETRO GAME OF THE DAY':"
    "fontcolor=white:fontsize=64:"
    "x=(w-text_w)/2:y=250,"
    f"drawtext=text='{title}':"
    "fontcolor=white:fontsize=82:"
    "x=(w-text_w)/2:y=600,"
    f"drawtext=text='{year}':"
    "fontcolor=white:fontsize=58:"
    "x=(w-text_w)/2:y=750,"
    f"drawtext=text='{system}':"
    "fontcolor=white:fontsize=48:"
    "x=(w-text_w)/2:y=900,"
    f"drawtext=text='{genre}':"
    "fontcolor=white:fontsize=48:"
    "x=(w-text_w)/2:y=1000,"
    "drawtext=text='FOLLOW FOR MORE RETRO HISTORY':"
    "fontcolor=white:fontsize=42:"
    "x=(w-text_w)/2:y=1650"
)

subprocess.run([
    "ffmpeg",
    "-y",
    "-f", "lavfi",
    "-i", "color=c=black:s=1080x1920:r=30",
    "-i", str(AUDIO_FILE),
    "-t", duration,
    "-vf", filter_text,
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-shortest",
    str(VIDEO_FILE)
], check=True)

print("TikTok video created:")
print(VIDEO_FILE)
