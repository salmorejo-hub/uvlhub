#!/bin/bash

set -e
sh ./scripts/wait-for-db.sh
exec python discordbot/run.py 