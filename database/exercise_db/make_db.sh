#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Usage: $0 [db fliename]"
	exit -1
fi
SCRIPT_DIR=tests/database/exercise_db

# need to preserve order here or foreign keys will die
rm -f $1
sqlite3 $1 < ${SCRIPT_DIR}/create.sqlite && \
sqlite3 $1 < ${SCRIPT_DIR}/muscle_groups.sqlite && \
sqlite3 $1 < ${SCRIPT_DIR}/muscles.sqlite && \
sqlite3 $1 < ${SCRIPT_DIR}/stretches.sqlite && \
sqlite3 $1 < ${SCRIPT_DIR}/fixtures.sqlite && \
sqlite3 $1 < ${SCRIPT_DIR}/equipment_rigs.sqlite && \
sqlite3 $1 < ${SCRIPT_DIR}/exercises.sqlite && \
sqlite3 $1 < ${SCRIPT_DIR}/muscles_exercised.sqlite
