#!/bin/bash

# See README.md for instructions.

# force the permissions of the script to be run.
#commenting out line #7. no need to echo. (operation not permitted when chmoding?) -danejo 2/28/19
#echo "changing permissions" 2>>/users/groups/cs235ta/submission_driver/everything_log.txt
chmod 777 /users/groups/cs235ta/submission_driver/Compile_Driver.py #2>>/users/groups/cs235ta/submission_driver/everything_log.txt

# isRunning captures the output of a command that will check to see if the compile script is running.
# for more information about the 'ps' command, take a look at http://www.linfo.org/ps.html
isRunning=`ps auxw | grep Compile_Driver | grep python`

if [ -z "$isRunning" ]; then
   # if isRunning is empty, then the script is not running, so we need to run it.
  #/bin/echo "not running" >> /users/groups/cs235ta/submission_driver/cronLog.txt
  #commenting out part of line #20 -danejo 2/28/19
  /users/groups/cs235ta/submission_driver/Compile_Driver.py #2>> /users/groups/cs235ta/submission_driver/everything_log2.txt & >> /users/groups/cs235ta/submission_driver/cronLog.txt 2>> /users/groups/cs235ta/submission_driver/cronLog.txt
  /bin/echo "Now running script..." >> /users/groups/cs235ta/submission_driver/cronLog.txt

else
  # otherwise we log that the script is running.
  #/bin/echo "running" >> /users/groups/cs235ta/submission_driver/cronLog.txt

  # log this result to the cronLog.
  echo "Time Stamp: (Last time the Submission Driver was online.)" > /users/groups/cs235ta/submission_driver/cronLog.txt
  echo $(date) >> /users/groups/cs235ta/submission_driver/cronLog.txt
  echo "" >> /users/groups/cs235ta/submission_driver/cronLog.txt
  echo "Process Status:" >> /users/groups/cs235ta/submission_driver/cronLog.txt
  /bin/echo "$isRunning" >> /users/groups/cs235ta/submission_driver/cronLog.txt
fi
