9/25/19

# Introduction: #

Hi! My name is Dane and I have been working on the driver for about a year. 
I hope that this README file will be helpful you. I will document the history 
of the driver, give a quick explaination of each file, and teach you how to 
run this driver.



# History of The Driver: #

The idea of an "automatic pass-off driver" began when Brother Roper started
teaching CS 235 in Winter 2018. One of the biggest problems that we had as TAs
were pass-off days. On these days, the queue to pass-off and to get help from 
the TAs were incredibly long. There were two reasons that caused this problem: 
First, all labs were graded manually, and last, students who were passing-off were 
given higher priority than those that needed help. As a result, students that 
needed help, on average, had to wait for 1+ hours in the queue. To solve this 
problem, Brother Roper hired another TA to write-up the automatic pass-off 
driver.

The first person that started working on the driver was Mike Liddle. From my 
understanding, it was Mike that decided to write the driver in Python. (I do not 
know the reason why.) Unfortunately, after a few month(s)? into the semester, I 
was told that he had stopped working as a CS 235 TA. Jason Anderson, who was the 
head TA at the time, did not have time to work on the driver. As a result, the 
implemntation of the driver was on a pause.

The next person that began working on the driver was Stephen Leech, the next head 
TA. About ~90% of code that you see today was written by Stephen. In Fall 2018, 
Stephen miraculously launched a live "automatic pass-off driver" for Brother 
Roper's Fall 2018 students. To be short and blunt, the driver had a lot of 
problems. Throughout the semester, the driver crashed constantly and had tons 
of run-time errors. Thankfully, for a year, Stephen was able to fix many of 
problems that plagued the driver and had added a lot of good key features.

Unfortunately, at the beginning of the Winter 2019, Stephen had stopped working 
and had passed the driver onto me. Although the driver had been maintained pretty 
well by Stephen, there were still a lot of problems that needed to be fixed. For 
the past year, I've been fixing and maintaining the driver. As of right now the 
driver is pretty stable and rarely crashes (if it does, 99% of the time, Brother
Roper and I have found out that it wasn't the driver's fault. For more information
about this, you can talk to Brother Roper).

As of today, Brother Roper is using the driver in tandem with his CS 235 website 
(https://students.cs.byu.edu/~cs235ta/). From my understanding, maybe in a year?, 
Brother Roper is going to replace this driver with his C++ version. Until then, 
I'll continue maintaining the driver until I graduate in April 2020.

*Cheers*

"Here, there be dragons." ~Stephen



# Files #

📁 LabKeyFiles - contains all the key files that the driver will use to compare
against the student's outputs to key files.

📁 logs - contains log files. One paraticular log file that would be of interest
is the "*_email_log.txt." This file contains who, what lab, and when a student
submitted a lab.

🐍 Compile_Driver.py - This .py file contains the function that starts the entire
driver (take a look at "submission_driver()").

⚙ compiler_global.cfg - This config file is very important. In this file, it
contains all the paths to a file or directory needed for the driver. Stephen
wanted this file so he wouldn't have to type it out multiple times each each
.py file.

🐍 ConfigFile.py - parses "compiler_global.cfg."

☰ cronLog.txt - The purpose of this .txt file is to let you know how long the
driver has been running. If the driver has stopped, it will let you know when
it stopped and how long it has stopped. About every 30 seconds, it should be
updating constantly.

🐍 GradedResult.py - The purpose of this .py file is to set up a clean text
view of the student's grade on the lab.

🐍 Grader.py - The purpose of this .py file is to compile, run (with valgrind),
and grade the student's code by comparing their outputs with the key files. 
Furthermore, this code will check and flag students if they are using code that 
shouldn't be using. For example, if vectors were not allowed, the students when 
they recieve their results will say "Illegal use of <blank>". (This feature was 
added by Brother Roper's request.) 

🐚 runCompileDriver.sh - This .sh is called by the cronjob* to make sure the
driver is running. If it isn't, it will restart the job; otherwise, continue
let it run.

\* - The cronjob command that I use is:
\* \* \* \* \* /users/groups/cs235ta/submission_driver/runCompileDriver.sh 
    &>> /users/groups/cs235ta/submission_driver/cronLog.txt
For more instructions, please see the "Instructions to Run Driver."



# Instructions to Setup Driver: #

To those that are setting up the driver,

Setting up the driver is easy; however, before you jump into setting it up, 
in a few files, you need to update a few lines of code.

First, you need to edit "Compiler_Driver.py" on line 32. Currently, as of 
December 19, 2019, Brother Roper is using 
"/users/groups/cs235ta/submission_driver/." If you are not Brother Roper,
I highly recommend that you create a different path for the driver because
if you plan on having differernt labs, the key files located in the current 
driver will we different and will therefore grade your student's output 
incorrectly. If you have plan on having the same labs as Brother Roper, for 
example, I still recommend that you create your own path because the way the 
driver is coded up. As of right now, it cannot support mutliple professors.
As a result, the solution to this problem is to create a "duplicate" driver
running seperately from other drivers.

Last, you need to edit "compiler_global.cfg." Because this contains all the
file paths for all the driver's .py files, you only need to change this once.
For each line, adjust accordingly.

Once you have edited both files, you can then read the "howto_driver_setup.pdf."

\*Remember!\* All of these things that I'm telling you is the back-end only.
To figure out how to integrate the front-end with the back-end, please contact
Brother Roper.
