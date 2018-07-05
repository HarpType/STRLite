import os
from pathlib import Path

cur_path = os.getcwd()
child_file = 'gravity_test.py'
# to STRLite
child_path = Path(cur_path).parents[1]
# to STRLite/ros-side
child_path = child_path.joinpath('ros-side', child_file)

#for child proccess
proc = None

#for queue
q = None


#for reading thread
def enqueue_output(out, queue):
    while True:
        line = out.readline()
        if line == 'Stop\n':
            out.close()
            return
        queue.put(line)

