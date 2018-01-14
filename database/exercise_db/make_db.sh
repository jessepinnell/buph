#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Usage: $0 [db filename]"
	exit -1
fi
DB_FILENAME=$1

rm -f $1

sqlite3 ${DB_FILENAME} < tests/database/exercise_db/create.sqlite
python3 scripts/process_yaml.py --format sqlite3 tests/data/exercise_data/*.yaml > tests/data/exercise_data/test.sqlite
sqlite3 ${DB_FILENAME} < tests/data/exercise_data/test.sqlite
