import json
import sys

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} path/to/scoreboard.json")
    sys.exit(1)

out = {"standings": []}

sb = json.load(open(sys.argv[1], "r"))
for (pos, team) in enumerate(sb["Teams"]):
    out["standings"].append({
        "pos": pos + 1,
        "team": team["Name"],
        "score": team["TotalPoints"],
    })

print(json.dumps(out))
