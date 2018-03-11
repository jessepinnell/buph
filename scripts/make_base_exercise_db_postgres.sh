#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Usage: $0 [db username]"
	exit -1
fi
DB_USERNAME=$1

# TODO check table exists


# This requires the local user to have the following privs: CREATEDB

# Create database
echo "Dropping postgres xrsrv table..."
dropdb --if-exists xrsrv

echo "Creating postgres xrsrv table..."
createdb xrsrv

echo "Creating postgres tables..."
psql xrsrv -q ${DB_USERNAME} < tests/data/exercise_data/create.sql

echo "Generating postgres data..."
python3 python/utils/process_yaml.py --format postgres tests/data/exercise_data/*.yaml tests/data/exercise_data/exercises/*.yaml > tests/data/exercise_data/test.sql

echo "Inserting postgres data..."
psql xrsrv -q ${DB_USERNAME} < tests/data/exercise_data/test.sql
