import os
import subprocess
CWD = os.getcwd()
subprocess.call(['xterm','-e','cd ros-side & source ros-side/devel/setup.bash & roscore',""])
subprocess.call(['xterm','-e','roslaunch',"rosbridge_server rosbridge_websocket.launch"])

subprocess.call(['xterm','-e','rosrun',"node_manager worlds_manager.py"])

os.chdir(CWD+'/web-side/strl/')
os.system('source /venv/bin/activate')
subprocess.call(['xterm','-e','python3',"manage.py runserver"])
