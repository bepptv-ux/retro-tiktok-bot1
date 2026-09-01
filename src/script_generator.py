import json
from pathlib import Path

GAMES_FILE = Path("games/games.json")
SCRIPT_FILE = Path("output/todays_script.txt")

with open(GAMES_FILE, "r", encoding="utf-8") as f:
    games = json.load(f)

used_file = Path("games/used_games.json")

if used_file.exists():
    with open(used_file, "r", encoding="utf-8") as f:
        used = json.load(f)
else:
    used = []

if not used:
    print("No game has been selected yet.")
    exit()

game_title = used[-1]

game = next(
    (g for g in games if g["title"] == game_title),
    None
)

if not game:
    print("Game not found.")
    exit()

script = f"""
Remember this classic?

Today we're going back to {game["year"]} with {game["title"]}!

{game["title"]} was developed by {game["developer"]}
and released for {game["system"]}.

The game is a {game["genre"]},
and it became one of the memorable games of its era.

But here's the real question...

Did you play {game["title"]} back in the day?

Let us know in the comments!

Follow for another retro game tomorrow!
""".strip()

SCRIPT_FILE.parent.mkdir(parents=True, exist_ok=True)

with open(SCRIPT_FILE, "w", encoding="utf-8") as f:
    f.write(script)

print(script)
