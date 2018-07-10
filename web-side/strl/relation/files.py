import os
from pathlib import Path

cur_path = os.getcwd()
child_file = 'gravity_test.py'
# to STRLite
child_path = Path(cur_path).parents[1]
# to STRLite/ros-side
child_path = child_path.joinpath('ros-side', child_file)
