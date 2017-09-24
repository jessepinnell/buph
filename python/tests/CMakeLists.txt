add_test(NAME test_exercise_database COMMAND ${PYTHON_EXECUTABLE} -B ${CMAKE_CURRENT_SOURCE_DIR}/test_exercise_database.py)
set_property(TEST test_exercise_database PROPERTY ENVIRONMENT "PYTHONPATH=${CMAKE_SOURCE_DIR}/python")

add_test(NAME test_user_database COMMAND ${PYTHON_EXECUTABLE} -B ${CMAKE_CURRENT_SOURCE_DIR}/test_user_database.py)
set_property(TEST test_user_database PROPERTY ENVIRONMENT "PYTHONPATH=${CMAKE_SOURCE_DIR}/python")

add_test(NAME test_routine_generator COMMAND ${PYTHON_EXECUTABLE} -B ${CMAKE_CURRENT_SOURCE_DIR}/test_routine_generator.py)
set_property(TEST test_routine_generator PROPERTY ENVIRONMENT "PYTHONPATH=${CMAKE_SOURCE_DIR}/python")

add_test(NAME test_exercise_rendering COMMAND ${PYTHON_EXECUTABLE} -B ${CMAKE_CURRENT_SOURCE_DIR}/test_exercise_rendering.py)
set_property(TEST test_exercise_rendering PROPERTY ENVIRONMENT "PYTHONPATH=${CMAKE_SOURCE_DIR}/python")
