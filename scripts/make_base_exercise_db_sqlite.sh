#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Usage: $0 [db filename]"
	exit -1
fi
DB_FILENAME=$1

rm -f $1

echo "Creating sqlite tables..."
sqlite3 ${DB_FILENAME} < tests/data/exercise_data/create.sqlite

echo "Generating sqlite data..."
python3 python/utils/process_yaml.py --format sqlite3 tests/data/exercise_data/*.yaml tests/data/exercise_data/exercises/*.yaml > tests/data/exercise_data/test.sqlite

echo "Inserting sqlite data..."
sqlite3 ${DB_FILENAME} < tests/data/exercise_data/test.sqlite
