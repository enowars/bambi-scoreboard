import asyncio
import json
import os

import aredis
from watchgod import Change, awatch

from .common import current_round, redis
from .models import JsonScoreboard

DATA_DIR = os.getenv("DATA_DIR", "/services/data")


class RestartedException(Exception):
    pass


async def main() -> None:
    while True:
        try:
            if not await parse_info(os.path.join(DATA_DIR, "scoreboardInfo.json")):
                await asyncio.sleep(1)
                continue

            base_path = os.path.join(DATA_DIR, "scoreboard.json")
            await parse_base_scoreboard(base_path)
            if not await current_round():
                print("no pre-existing scoreboard files found")

            print(f"watching {base_path}")
            async for changes in awatch(base_path):
                for c in changes:
                    if c[0] == Change.added or c[0] == Change.modified:
                        await parse_base_scoreboard(base_path)
        except aredis.exceptions.ConnectionError:
            print("Failed to connect to redis...")
            await asyncio.sleep(1)


async def parse_info(file_: str) -> bool:
    basename = os.path.basename(file_)
    if basename != "scoreboardInfo.json":
        print(f"skipping scoreboardInfo.json: {file_}")
        return False
    print(f"parsing scoreboardInfo.json: {file_}")
    try:
        obj = json.load(open(file_, "r"))

        team_info = {}
        for t in obj["teams"]:
            team_info[t["id"]] = {
                "id": t["id"],
                "name": t["name"],
                "logoUrl": t["logoUrl"] if "logoUrl" in t else None,
                "flagUrl": t["flagUrl"] if "flagUrl" in t else None,
            }

        config = {
            "dnsSuffix": obj["dnsSuffix"] if "dnsSuffix" in obj else None,
            "title": obj["title"] if "title" in obj else None,
            "teams": team_info,
        }

        await redis.set("config", json.dumps(config).encode())
        return True
    except FileNotFoundError as e:
        print(f"Failed to load scoreboardInfo.json: {file_}, {str(e)}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse scoreboardInfo.json: {file_}, {str(e)}")
    return False


async def parse_base_scoreboard(base_path: str) -> None:
    try:
        prev_max = (await current_round()) or 0
        await parse_scoreboard(base_path)
    except RestartedException:
        print("CTF was restarted, flushing Redis")
        await redis.flushall()
        await parse_info(os.path.join(DATA_DIR, "scoreboardInfo.json"))
        await parse_scoreboard(base_path)
        prev_max = 0

    new_max = (await current_round()) or 0
    for i in range(prev_max, new_max):
        sb_path = os.path.join(DATA_DIR, f"scoreboard{i}.json")
        await parse_scoreboard(sb_path)


async def parse_scoreboard(file_: str) -> None:
    basename = os.path.basename(file_)
    if not basename.startswith("scoreboard") or not basename.endswith(".json"):
        print(f"skipping {file_}")
        return
    print(f"parsing {file_}")
    try:
        obj = json.load(open(file_, "r"))
        sb = JsonScoreboard(**obj)
        print(f"Loading scoreboard for round {sb.currentRound}")

        if not sb.currentRound:
            return

        entry = await redis.get(f"sb_{sb.currentRound}")
        if not entry:
            await redis.set(f"sb_{sb.currentRound}", sb.json())

        entry = await redis.get("max_round")
        print(f"previous: max_round: {entry}")
        if not entry or int(entry.decode()) < sb.currentRound:
            await redis.set("max_round", sb.currentRound)
            await redis.publish("notifications", sb.currentRound)
        elif (
            entry
            and int(entry.decode()) > sb.currentRound
            and basename == "scoreboard.json"
        ):
            raise RestartedException()

        for t in sb.teams:
            await redis.set(f"team_exists_${t.teamId}", True)
    except FileNotFoundError as e:
        print(f"Failed to load scoreboard: {file_}, {str(e)}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse scoreboard: {file_}, {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
