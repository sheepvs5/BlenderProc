import subprocess
import sys
import os

# set the folder in which the run.py is located
rerun_folder = os.path.abspath(os.path.dirname(__file__))

# this sets the amount of runs, which are performed
amount_of_runs = int(sys.argv[1])
# the first one is the rerun.py script, the last is the output
used_arguments = sys.argv[2:]

for run_id in range(amount_of_runs):
    # in each run, the arguments are reused
    cmd = ["python", os.path.join(rerun_folder, "run.py")]
    cmd.extend(used_arguments)
    # the only exception is the output, which gets changed for each run, so that the examples are not overwritten
    print(" ".join(cmd))
    # execute one BlenderProc run
    subprocess.call(" ".join(cmd), shell=True)






