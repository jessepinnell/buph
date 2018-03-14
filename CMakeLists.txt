cmake_minimum_required(VERSION 3.3)
project(xrsrv)
enable_testing()
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/modules/")

find_package(PythonInterp 3.6 REQUIRED)
find_package(SQLite3 REQUIRED)

# XXX remove this
set(PostgreSQL_TYPE_INCLUDE_DIR /usr/lib/x86_64-linux-gnu/libpq.so)
find_package(PostgreSQL REQUIRED)
# TODO(jessepinnell) Add find for psycopg2
# TODO(jessepinnell) Add check for postgres user with createdb privileges
# TODO(jessepinnell) Add check for pylint3
# TODO(jessepinnell) Add check for pip3?
# TODO(jessepinnell) Add check for pyyaml (installed via pip3)
# TODO(jessepinnell) Add check for psycopg2-binary (installed via pip3)


# Set up linting
add_custom_target(lint)
set(PYLINT pylint3 -f colorized --rcfile=${CMAKE_CURRENT_SOURCE_DIR}/python/.pylintrc)
add_custom_command(TARGET lint COMMAND ${PYLINT} ${CMAKE_CURRENT_SOURCE_DIR}/python/setup.py VERBATIM)
add_custom_command(TARGET lint COMMAND ${PYLINT} ${CMAKE_CURRENT_SOURCE_DIR}/python/xrsrv VERBATIM)
add_custom_command(TARGET lint COMMAND ${PYLINT} ${CMAKE_CURRENT_SOURCE_DIR}/python/tests VERBATIM)
add_custom_command(TARGET lint COMMAND ${PYLINT} ${CMAKE_CURRENT_SOURCE_DIR}/python/apps VERBATIM)
add_custom_command(TARGET lint COMMAND ${PYLINT} ${CMAKE_CURRENT_SOURCE_DIR}/python/utils VERBATIM)

# Set up testing environment in bulid directory
# TODO(jessepinnell) this is crude
# TODO(jessepinnell) this is not platform-independent

set(TEST_EXERCISE_SQLITE_DB_NAME "exercise.db")
add_custom_target(create_testing_environment ALL)
add_custom_command(
   TARGET create_testing_environment PRE_BUILD
   COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/tests
   COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/tests/database
   COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/database ${CMAKE_BINARY_DIR}/tests/database
   COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/tests/data
   COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/data ${CMAKE_BINARY_DIR}/tests/data
   COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/python
   COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/python ${CMAKE_BINARY_DIR}/python
   COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_BINARY_DIR}/scripts
   COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/scripts ${CMAKE_BINARY_DIR}/scripts)

add_custom_command(TARGET create_testing_environment
   COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/scripts/make_base_exercise_db_sqlite.sh ${CMAKE_BINARY_DIR}/python/tests/${TEST_EXERCISE_SQLITE_DB_NAME}
   COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/scripts/make_base_exercise_db_postgres.sh $ENV{USER})

add_subdirectory(python)
