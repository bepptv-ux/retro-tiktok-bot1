import json
import subprocess
from pathlib import Path

AUDIO_FILE = Path("output/todays_voice.wav")
SCRIPT_FILE = Path("output/todays_script.txt")
GAMES_FILE = Path("games/games.json")
VIDEO_FILE = Path("output/todays_video.mp4")

WIDTH = 1080
HEIGHT = 1920
FPS = 30

if not AUDIO_FILE.exists():
    print("Voice file not found.")
    raise SystemExit(1)

if not SCRIPT_FILE.exists():
    print("Script file not found.")
    raise SystemExit(1)

if not GAMES_FILE.exists():
    print("Games file not found.")
    raise SystemExit(1)

with open(GAMES_FILE, "r", encoding="utf-8") as f:
    games = json.load(f)

used_file = Path("games/used_games.json")

if used_file.exists():
    with open(used_file, "r", encoding="utf-8") as f:
        used_games = json.load(f)
else:
    used_games = []

if used_games:
    current_title = used_games[-1]
else:
    current_title = games[0]["title"]

current_game = next(
    (game for game in games if game["title"] == current_title),
    games[0]
)

title = current_game["title"]
year = current_game["year"]
system = current_game["system"]
developer = current_game["developer"]
genre = current_game["genre"]

VIDEO_FILE.parent.mkdir(parents=True, exist_ok=True)

print(f"Creating visual video for: {title}")
print(f"Year: {year}")
print(f"System: {system}")
print(f"Developer: {developer}")
print(f"Genre: {genre}")

# Read the script to estimate a useful minimum video length.
script_text = SCRIPT_FILE.read_text(encoding="utf-8").strip()

word_count = len(script_text.split())

# Approximately 150 words per minute.
estimated_seconds = max(35, int((word_count / 150) * 60) + 5)

# Give short scripts enough visual time.
duration = max(estimated_seconds, 35)

# Escape text for FFmpeg drawtext.
def escape_text(value):
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace(":", "\\:")
        .replace("'", "\\'")
        .replace(",", "\\,")
        .replace("[", "\\[")
        .replace("]", "\\]")
    )

safe_title = escape_text(title)
safe_system = escape_text(system)
safe_developer = escape_text(developer)
safe_genre = escape_text(genre)

font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Animated retro-style background.
# This is generated directly by FFmpeg, so the workflow does not depend
# on an asset being manually uploaded to the repository.
filter_complex = (
    f"drawbox=x=0:y=0:w=iw:h=ih:color=black:t=fill,"
    f"drawbox=x=55:y=55:w=iw-110:h=ih-110:color=white@0.08:t=8,"
    f"drawbox=x=95:y=300:w=iw-190:h=900:color=black@0.55:t=fill,"
    f"drawbox=x=95:y=300:w=iw-190:h=900:color=white@0.15:t=6,"
    
    # Moving horizontal scan lines
    f"drawgrid=w=1080:h=80:t=2:c=white@0.06,"
    
    # Main title
    f"drawtext=fontfile='{font}':"
    f"text='{safe_title}':"
    f"fontcolor=white:"
    f"fontsize=92:"
    f"x=(w-text_w)/2:"
    f"y=410,"
    
    # RETRO GAME label
    f"drawtext=fontfile='{font}':"
    f"text='RETRO GAME':"
    f"fontcolor=white:"
    f"fontsize=46:"
    f"x=(w-text_w)/2:"
    f"y=330,"
    
    # Metadata
    f"drawtext=fontfile='{font}':"
    f"text='YEAR  {year}':"
    f"fontcolor=white:"
    f"fontsize=50:"
    f"x=(w-text_w)/2:"
    f"y=610,"
    
    f"drawtext=fontfile='{font}':"
    f"text='SYSTEM  {safe_system}':"
    f"fontcolor=white:"
    f"fontsize=50:"
    f"x=(w-text_w)/2:"
    f"y=700,"
    
    f"drawtext=fontfile='{font}':"
    f"text='DEVELOPER  {safe_developer}':"
    f"fontcolor=white:"
    f"fontsize=50:"
    f"x=(w-text_w)/2:"
    f"y=790,"
    
    f"drawtext=fontfile='{font}':"
    f"text='GENRE  {safe_genre}':"
    f"fontcolor=white:"
    f"fontsize=50:"
    f"x=(w-text_w)/2:"
    f"y=880,"
    
    # Decorative arcade-style blocks
    f"drawbox=x=160:y=1320:w=760:h=12:color=white@0.65:t=fill,"
    f"drawbox=x=250:y=1380:w=580:h=12:color=white@0.45:t=fill,"
    f"drawbox=x=340:y=1440:w=400:h=12:color=white@0.30:t=fill,"
    
    # Animated progress bar
    f"drawbox=x=120:y=1630:w=840:h=22:color=white@0.15:t=fill,"
    f"drawbox=x=120:y=1630:w='840*(t/{duration})':h=22:color=white@0.8:t=fill,"
    
    # Footer
    f"drawtext=fontfile='{font}':"
    f"text='RETRO GAMING HISTORY':"
    f"fontcolor=white@0.8:"
    f"fontsize=38:"
    f"x=(w-text_w)/2:"
    f"y=1730,"
    
    f"format=yuv420p"
)

command = [
    "ffmpeg",
    "-y",
    "-f",
    "lavfi",
    "-i",
    f"color=c=0x101018:s={WIDTH}x{HEIGHT}:r={FPS}",
    "-i",
    str(AUDIO_FILE),
    "-t",
    str(duration),
    "-filter_complex",
    filter_complex,
    "-map",
    "0:v",
    "-map",
    "1:a",
    "-c:v",
    "libx264",
    "-preset",
    "veryfast",
    "-crf",
    "23",
    "-pix_fmt",
    "yuv420p",
    "-c:a",
    "aac",
    "-b:a",
    "192k",
    "-shortest",
    str(VIDEO_FILE),
]

print(f"Target duration: {duration} seconds")
print("Rendering video...")

subprocess.run(command, check=True)

if VIDEO_FILE.exists() and VIDEO_FILE.stat().st_size > 10000:
    print("VIDEO CREATED SUCCESSFULLY!")
    print(f"File: {VIDEO_FILE}")
    print(f"Size: {VIDEO_FILE.stat().st_size} bytes")
else:
    print("VIDEO WAS NOT CREATED CORRECTLY.")
    raise SystemExit(1)
