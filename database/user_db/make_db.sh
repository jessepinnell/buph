#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Usage: $0 [db fliename]"
	exit -1
fi
SCRIPT_DIR=tests/database/user_db

# need to preserve order here or foreign keys will die
rm -f $1
sqlite3 $1 < ${SCRIPT_DIR}/create.sqlite
sqlite3 $1 < ${SCRIPT_DIR}/fixtures.sqlite
sqlite3 $1 < ${SCRIPT_DIR}/equipment_accessories.sqlite
