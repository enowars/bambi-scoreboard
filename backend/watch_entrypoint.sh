#!/bin/sh

echo "Starting scoreboard.watch ..."
python3 -c 'print("test"); import scoreboard.watch as m; print(m); from scoreboard.watch import test; import asyncio; asyncio.run(test())'
python3 -m scoreboard.watch
