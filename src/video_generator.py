import json
import math
import re
import subprocess
from pathlib import Path

AUDIO_FILE = Path("output/todays_voice.wav")
SCRIPT_FILE = Path("output/todays_script.txt")
GAMES_FILE = Path("games/games.json")
VIDEO_FILE = Path("output/todays_video.mp4")

WIDTH = 1080
HEIGHT = 1920
FPS = 30
MIN_DURATION = 60

if not AUDIO_FILE.exists():
    print("ERROR: Voice file not found.")
    raise SystemExit(1)

if not SCRIPT_FILE.exists():
    print("ERROR: Script file not found.")
    raise SystemExit(1)

if not GAMES_FILE.exists():
    print("ERROR: Games file not found.")
    raise SystemExit(1)


def ffmpeg_escape(text):
    text = str(text)
    text = text.replace("\\", "\\\\")
    text = text.replace(":", "\\:")
    text = text.replace("'", "\\'")
    text = text.replace(",", "\\,")
    text = text.replace("[", "\\[")
    text = text.replace("]", "\\]")
    text = text.replace("%", "\\%")
    return text


with open(GAMES_FILE, "r", encoding="utf-8") as f:
    games = json.load(f)


used_file = Path("games/used_games.json")

if used_file.exists():
    with open(used_file, "r", encoding="utf-8") as f:
        used_games = json.load(f)
else:
    used_games = []


if used_games:
    selected_title = used_games[-1]
else:
    selected_title = games[0]["title"]


game = next(
    (g for g in games if g["title"] == selected_title),
    games[0]
)


title = game["title"]
year = game["year"]
system = game["system"]
developer = game["developer"]
genre = game["genre"]


script = SCRIPT_FILE.read_text(encoding="utf-8").strip()

word_count = len(re.findall(r"\b[\w'-]+\b", script))

# Estimate narration duration.
# 130 words per minute gives the video enough breathing room.
estimated_duration = math.ceil((word_count / 130) * 60)

# Never make a short video.
duration = max(MIN_DURATION, estimated_duration + 4)

print("")
print("========================================")
print("        RETRO VIDEO GENERATOR")
print("========================================")
print(f"Game:       {title}")
print(f"Year:       {year}")
print(f"System:     {system}")
print(f"Developer:  {developer}")
print(f"Genre:      {genre}")
print(f"Words:      {word_count}")
print(f"Duration:   {duration} seconds")
print("========================================")
print("")


VIDEO_FILE.parent.mkdir(parents=True, exist_ok=True)


font_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font_regular = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


safe_title = ffmpeg_escape(title)
safe_system = ffmpeg_escape(system)
safe_developer = ffmpeg_escape(developer)
safe_genre = ffmpeg_escape(genre)


# ---------------------------------------------------------
# Animated retro visual background
# ---------------------------------------------------------

background = (
    f"color=c=0x080812:s={WIDTH}x{HEIGHT}:r={FPS},"
    f"format=yuv420p,"
    
    # Slow moving grid
    f"drawgrid="
    f"w=90:"
    f"h=90:"
    f"t=2:"
    f"c=white@0.10,"
    
    # Large arcade panels
    f"drawbox="
    f"x=55:"
    f"y=55:"
    f"w=970:"
    f"h=1810:"
    f"t=8:"
    f"c=white@0.18,"
    
    f"drawbox="
    f"x=90:"
    f"y=260:"
    f"w=900:"
    f"h=1120:"
    f"t=6:"
    f"c=white@0.15,"
    
    # Moving horizontal scanlines
    f"drawbox="
    f"x=0:"
    f"y='mod(t*160,1920)':"
    f"w=1080:"
    f"h=8:"
    f"t=fill:"
    f"c=white@0.10"
)


# ---------------------------------------------------------
# Hook screen
# ---------------------------------------------------------

hook_start = 0
hook_end = min(8, duration)

hook = (
    f"drawtext="
    f"fontfile='{font_bold}':"
    f"text='RETRO GAME':"
    f"fontsize=55:"
    f"fontcolor=white:"
    f"x=(w-text_w)/2:"
    f"y=420:"
    f"enable='between(t,{hook_start},{hook_end})',"
    
    f"drawtext="
    f"fontfile='{font_bold}':"
    f"text='{safe_title}':"
    f"fontsize=100:"
    f"fontcolor=white:"
    f"x=(w-text_w)/2:"
    f"y=530:"
    f"enable='between(t,{hook_start},{hook_end})',"
    
    f"drawtext="
    f"fontfile='{font_regular}':"
    f"text='THE STORY BEHIND THE GAME':"
    f"fontsize=43:"
    f"fontcolor=white:"
    f"x=(w-text_w)/2:"
    f"y=690:"
    f"enable='between(t,{hook_start},{hook_end})',"
    
    f"drawbox="
    f"x=190:"
    f"y=780:"
    f"w=700:"
    f"h=14:"
    f"t=fill:"
    f"c=white@0.8:"
    f"enable='between(t,{hook_start},{hook_end})'"
)


# ---------------------------------------------------------
# Information cards
# ---------------------------------------------------------

card1_start = 8
card1_end = min(20, duration)

card1 = (
    f"drawtext="
    f"fontfile='{font_bold}':"
    f"text='RELEASED':"
    f"fontsize=45:"
    f"fontcolor=white:"
    f"x=130:"
    f"y=440:"
    f"enable='between(t,{card1_start},{card1_end})',"
    
    f"drawtext="
    f"fontfile='{font_bold}':"
    f"text='{year}':"
    f"fontsize=100:"
    f"fontcolor=white:"
    f"x=130:"
    f"y=510:"
    f"enable='between(t,{card1_start},{card1_end})',"
    
    f"drawtext="
    f"fontfile='{font_bold}':"
    f"text='SYSTEM':"
    f"fontsize=45:"
    f"fontcolor=white:"
    f"x=130:"
    f"y=700:"
    f"enable='between(t,{card1_start},{card1_end})',"
    
    f"drawtext="
    f"fontfile='{font_bold}':"
    f"text='{safe_system}':"
    f"fontsize=68:"
    f"fontcolor=white:"
    f"x=130:"
    f"y=770:"
    f"enable='between(t,{card1_start},{card1_end})'"
)


card2_start = 20
card2_end = min(34, duration)

card2 = (
    f"drawtext="
    f"fontfile='{font_bold}':"
    f"text='DEVELOPER':"
    f"fontsize=45:"
    f"fontcolor=white:"
    f"x=130:"
    f"y=440:"
    f"enable='between(t,{card2_start},{card2_end})',"
    
    f"drawtext="
    f"fontfile='{font_bold}':"
    f"text='{safe_developer}':"
    f"fontsize=75:"
    f"fontcolor=white:"
    f"x=130:"
    f"y=520:"
    f"enable='between(t,{card2_start},{card2_end})',"
    
    f"drawtext="
    f"fontfile='{font_bold}':"
    f"text='GENRE':"
    f"fontsize=45:"
    f"fontcolor=white:"
    f"x=130:"
    f"y=710:"
    f"enable='between(t,{card2_start},{card2_end})',"
    
    f"drawtext="
    f"fontfile='{font_bold}':"
    f"text='{safe_genre}':"
    f"fontsize=72:"
    f"fontcolor=white:"
    f"x=130:"
    f"y=790:"
    f"enable='between(t,{card2_start},{card2_end})'"
)


# ---------------------------------------------------------
# Retro fact screen
# ---------------------------------------------------------

card3_start = 34
card3_end = min(48, duration)

card3 = (
    f"drawtext="
    f"fontfile='{font_bold}':"
    f"text='WHY IT MATTERED':"
    f"fontsize=50:"
    f"fontcolor=white:"
    f"x=(w-text_w)/2:"
    f"y=410:"
    f"enable='between(t,{card3_start},{card3_end})',"
    
    f"drawtext="
    f"fontfile='{font_regular}':"
    f"text='A RETRO GAMING STORY':"
    f"fontsize=58:"
    f"fontcolor=white:"
    f"x=(w-text_w)/2:"
    f"y=570:"
    f"enable='between(t,{card3_start},{card3_end})',"
    
    f"drawtext="
    f"fontfile='{font_regular}':"
    f"text='THAT DESERVES TO BE REMEMBERED':"
    f"fontsize=48:"
    f"fontcolor=white:"
    f"x=(w-text_w)/2:"
    f"y=680:"
    f"enable='between(t,{card3_start},{card3_end})',"
    
    f"drawbox="
    f"x=160:"
    f"y=810:"
    f"w=760:"
    f"h=10:"
    f"t=fill:"
    f"c=white@0.7:"
    f"enable='between(t,{card3_start},{card3_end})'"
)


# ---------------------------------------------------------
# Closing screen
# ---------------------------------------------------------

card4_start = 48
card4_end = duration

card4 = (
    f"drawtext="
    f"fontfile='{font_bold}':"
    f"text='REMEMBER THIS ONE?':"
    f"fontsize=58:"
    f"fontcolor=white:"
    f"x=(w-text_w)/2:"
    f"y=520:"
    f"enable='gte(t,{card4_start})',"
    
    f"drawtext="
    f"fontfile='{font_bold}':"
    f"text='{safe_title}':"
    f"fontsize=90:"
    f"fontcolor=white:"
    f"x=(w-text_w)/2:"
    f"y=650:"
    f"enable='gte(t,{card4_start})',"
    
    f"drawtext="
    f"fontfile='{font_regular}':"
    f"text='FOLLOW FOR MORE RETRO GAMING':"
    f"fontsize=43:"
    f"fontcolor=white:"
    f"x=(w-text_w)/2:"
    f"y=820:"
    f"enable='gte(t,{card4_start})'"
)


# ---------------------------------------------------------
# Combine everything
# ---------------------------------------------------------

filter_complex = (
    background
    + ","
    + hook
    + ","
    + card1
    + ","
    + card2
    + ","
    + card3
    + ","
    + card4
)


command = [
    "ffmpeg",
    "-y",

    "-f",
    "lavfi",

    "-i",
    f"color=c=0x080812:s={WIDTH}x{HEIGHT}:r={FPS}",

    "-i",
    str(AUDIO_FILE),

    "-t",
    str(duration),

    "-vf",
    filter_complex,

    "-map",
    "0:v:0",

    "-map",
    "1:a:0",

    "-c:v",
    "libx264",

    "-preset",
    "veryfast",

    "-crf",
    "22",

    "-pix_fmt",
    "yuv420p",

    "-c:a",
    "aac",

    "-b:a",
    "192k",

    "-movflags",
    "+faststart",

    str(VIDEO_FILE),
]


print("Rendering the complete vertical video...")
print("Please wait...")

subprocess.run(command, check=True)


if not VIDEO_FILE.exists():
    print("ERROR: Video was not created.")
    raise SystemExit(1)


file_size = VIDEO_FILE.stat().st_size

if file_size < 100000:
    print("ERROR: Video file is suspiciously small.")
    raise SystemExit(1)


print("")
print("========================================")
print("       VIDEO CREATED SUCCESSFULLY")
print("========================================")
print(f"File: {VIDEO_FILE}")
print(f"Size: {file_size:,} bytes")
print(f"Duration target: {duration} seconds")
print(f"Resolution: {WIDTH}x{HEIGHT}")
print("========================================")
