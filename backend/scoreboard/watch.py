import asyncio
import json
import os

from watchgod import Change, awatch

from .common import current_round, redis
from .models import JsonScoreboard

DATA_DIR = os.getenv("DATA_DIR", "../data")


async def test() -> None:
    base_path = os.path.join(DATA_DIR, "scoreboard.json")
    await parse_scoreboard(base_path)
    r = await current_round()
    if r is not None:
        for i in range(0, r + 1):
            sb_path = os.path.join(DATA_DIR, f"scoreboard{i}.json")
            await parse_scoreboard(sb_path)
    else:
        print("no pre-existing scoreboard files found")

    print(f"watching {DATA_DIR}")
    async for changes in awatch(DATA_DIR):
        for c in changes:
            if c[0] == Change.added or c[0] == Change.modified:
                await parse_scoreboard(c[1])
            else:
                print(f"ignoring change: {c}")


async def parse_scoreboard(file_: str) -> None:
    basename = os.path.basename(file_)
    if not basename.startswith("scoreboard") or not basename.endswith(".json"):
        print(f"skipping {file_}")
        return
    print(f"parsing {file_}")
    try:
        obj = json.load(open(file_, "r"))
        sb = JsonScoreboard(**obj)
        print(f"Loading scoreboard for round {sb.CurrentRound}")

        if not sb.CurrentRound:
            return

        entry = await redis.get(f"sb_{sb.CurrentRound}")
        if not entry:
            await redis.set(f"sb_{sb.CurrentRound}", sb.json())

        entry = await redis.get("max_round")
        print(f"previous: max_round: {entry}")
        if not entry or int(entry.decode()) < sb.CurrentRound:
            await redis.set("max_round", sb.CurrentRound)
            await redis.publish("notifications", sb.CurrentRound)

        for t in sb.Teams:
            await redis.set(f"team_exists_${t.TeamId}", True)
    except FileNotFoundError as e:
        print(f"Failed to load scoreboard: {file_}, {str(e)}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse scoreboard: {file_}, {str(e)}")


if __name__ == "__main__":
    asyncio.run(test())
