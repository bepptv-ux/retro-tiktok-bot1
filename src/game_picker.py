import json
import random
from pathlib import Path

GAMES_FILE = Path("games/games.json")
USED_FILE = Path("games/used_games.json")

with open(GAMES_FILE, "r", encoding="utf-8") as f:
    games = json.load(f)

if USED_FILE.exists():
    with open(USED_FILE, "r", encoding="utf-8") as f:
        used = json.load(f)
else:
    used = []

available = [game for game in games if game["title"] not in used]

if not available:
    used = []
    available = games

game = random.choice(available)

used.append(game["title"])

with open(USED_FILE, "w", encoding="utf-8") as f:
    json.dump(used, f, indent=2)

print("Today's retro game:")
print(game["title"])
print(f'{game["year"]} | {game["system"]} | {game["developer"]}')
