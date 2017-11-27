#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Usage: $0 [db filename]"
	exit -1
fi
SCRIPT_DIR=tests/database/exercise_db
DB_FILENAME=$1

function source_sql
{
	sqlite3 ${DB_FILENAME} < ${SCRIPT_DIR}/${1} || { echo "Error in ${1}"; exit -1; }
}

# need to preserve order here or foreign keys will die
rm -f $1

source_sql create.sqlite
source_sql muscle_groups.sqlite
source_sql muscles.sqlite
source_sql stretches.sqlite
source_sql fixtures.sqlite
source_sql rigs.sqlite
source_sql exercises.sqlite
source_sql muscles_exercised.sqlite
source_sql muscle_antagonists.sqlite
source_sql exercise_rigs.sqlite
source_sql exercise_fixtures.sqlite
