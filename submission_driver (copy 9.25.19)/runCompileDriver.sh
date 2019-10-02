#!/bin/bash

# force the permissions of the script to be run.
chmod 777 /users/groups/cs235ta/submission_driver/Compile_Driver.py

# isRunning captures the output of a command that will check to see if the compile script is running.
# for more information about the 'ps' command, take a look at http://www.linfo.org/ps.html
isRunning=`ps auxw | grep Compile_Driver | grep python`

if [ -z "$isRunning" ]; then
  # if isRunning is empty, then the script is not running, so we need to run it.
  /users/groups/cs235ta/submission_driver/Compile_Driver.py
  # logging that we executed the Compile_Driver.py script again.
  /bin/echo "Now running script..." >> /users/groups/cs235ta/submission_driver/cronLog.txt

else
  # otherwise we log that the script is running.

  # logging result to the cronLog.
  echo "Time Stamp: (Last time the Submission Driver was online.)" > /users/groups/cs235ta/submission_driver/cronLog.txt
  echo $(date) >> /users/groups/cs235ta/submission_driver/cronLog.txt
  echo "" >> /users/groups/cs235ta/submission_driver/cronLog.txt
  echo "Process Status:" >> /users/groups/cs235ta/submission_driver/cronLog.txt
  /bin/echo "$isRunning" >> /users/groups/cs235ta/submission_driver/cronLog.txt
fi
