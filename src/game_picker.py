import json
import random
from pathlib import Path

GAMES_FILE = Path("games/games.json")
USED_FILE = Path("games/used_games.json")
OUTPUT_FILE = Path("output/todays_game.json")

games = json.loads(GAMES_FILE.read_text(encoding="utf-8"))

if USED_FILE.exists():
used = json.loads(USED_FILE.read_text(encoding="utf-8"))
else:
used = []

available = [game for game in games if game["title"] not in used]

if not available:
used = []
available = games

game = random.choice(available)
used.append(game["title"])

USED_FILE.write_text(
json.dumps(used, indent=2),
encoding="utf-8"
)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE.write_text(
json.dumps(game, indent=2),
encoding="utf-8"
)

print("Today's retro game:")
print(game["title"])
print(f'{game["year"]} | {game["system"]} | {game["developer"]}')
