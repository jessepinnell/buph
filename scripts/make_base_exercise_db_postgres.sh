#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Usage: $0 [db username]"
	exit -1
fi
DB_USERNAME=$1

# TODO check table exists


# This requires the local user to have the following privs: CREATEDB

# Create database
dropdb --if-exists xrsrv
createdb xrsrv
psql xrsrv ${DB_USERNAME} < tests/data/exercise_data/create.sql

#python3 python/utils/process_yaml.py --format postgres tests/data/exercise_data/*.yaml tests/data/exercise_data/exercises/*.yaml > tests/data/exercise_data/test.sql

#psql ${DB_FILENAME} < tests/data/exercise_data/test.sql
