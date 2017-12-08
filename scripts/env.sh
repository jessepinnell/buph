#!/bin/bash
# Set the path so python apps can be run from build directory like:
# ../xrsrv/python/apps/exercise_renderer.py python/tests/exercise.db 20 > /tmp/test.html
export PYTHONPATH="$PYTHONPATH:$(dirname `pwd`)/xrsrv/python"
