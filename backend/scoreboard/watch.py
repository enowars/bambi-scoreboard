import asyncio
import json
import os

import aredis
from watchgod import Change, awatch

from .common import current_round, redis
from .models import JsonScoreboard

DATA_DIR = os.getenv("DATA_DIR", "/services/data")
CTF_JSON_DIR = os.getenv("CTF_JSON_DIR", "/services/EnoEngine")
CTF_JSON_PATH = os.path.join(CTF_JSON_DIR, "ctf.json")


class RestartedException(Exception):
    pass


async def main() -> None:
    while True:
        try:
            await parse_ctf(CTF_JSON_PATH)

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


async def parse_ctf(file_: str) -> None:
    basename = os.path.basename(file_)
    if basename != "ctf.json":
        print(f"skipping ctf.json: {file_}")
        return
    print(f"parsing ctf.json: {file_}")
    try:
        obj = json.load(open(file_, "r"))

        team_info = {}
        for t in obj["Teams"]:
            team_info[t["Id"]] = {
                "Id": t["Id"],
                "Name": t["Name"],
                "LogoUrl": t["LogoUrl"] if "LogoUrl" in t else None,
                "FlagUrl": t["FlagUrl"] if "FlagUrl" in t else None,
            }

        config = {
            "DnsSuffix": obj["DnsSuffix"] if "DnsSuffix" in obj else None,
            "Title": obj["Title"] if "Title" in obj else None,
            "Teams": team_info,
        }

        await redis.set("config", json.dumps(config).encode())
    except FileNotFoundError as e:
        print(f"Failed to load ctf.json: {file_}, {str(e)}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse ctf.json: {file_}, {str(e)}")


async def parse_base_scoreboard(base_path: str) -> None:
    try:
        prev_max = (await current_round()) or 0
        await parse_scoreboard(base_path)
    except RestartedException:
        print("CTF was restarted, flushing Redis")
        await redis.flushall()
        await parse_ctf(CTF_JSON_PATH)
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
        elif (
            entry
            and int(entry.decode()) > sb.CurrentRound
            and basename == "scoreboard.json"
        ):
            raise RestartedException()

        for t in sb.Teams:
            await redis.set(f"team_exists_${t.TeamId}", True)
    except FileNotFoundError as e:
        print(f"Failed to load scoreboard: {file_}, {str(e)}")
    except json.JSONDecodeError as e:
        print(f"Failed to parse scoreboard: {file_}, {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())
