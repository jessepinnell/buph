#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Usage: $0 [db fliename]"
	exit -1
fi
SCRIPT_DIR=tests/database/user_db
DB_FILENAME=$1

function source_sql
{
	sqlite3 ${DB_FILENAME} < ${SCRIPT_DIR}/${1} || { echo "Error in ${1}"; exit -1; }
}

# need to preserve order here or foreign keys will die
rm -f $1

source_sql create.sqlite
source_sql user_profiles.sqlite
source_sql user_fixtures.sqlite
source_sql user_rigs.sqlite
source_sql exercise_set_history.sqlite
