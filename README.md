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
1) all labs were graded manually, and 2) students who were passing-off were 
given higher priority than those that needed help. As a result, students that 
needed help, on average, had to wait for 1+ hours in the queue. To solve this 
problem, Brother Roper hired another TA to write-up the automatic pass-off 
driver.

The first person that started working on the driver was Mike Liddle. From my 
understanding, it was Mike that decided to write the driver in Python. (I do not 
know the reason why.) Unfortunately, after a few month(s)? into the semester, I 
was told that he had stopped working as a CS 235 TA. Jason Anderson, who was the 
head TA at the time, did not have time to work on the driver. As result, the 
driver was on a pause.

The next person that began working on the driver was Stephen Leech, the next head 
TA. About ~90% of code that you see today was written by Stephen. In Fall 2018, 
Stephen was able to miraculously launch a live "automatic pass-off driver" for 
Brother Roper's Fall 2018 students. To be short and blunt, the driver had a lot 
of problems. Throughout the semester, the driver crashed constantly and had tons 
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

📁 logs - contains 

🐍 Compile_Driver.py - 

⚙ compiler_global.cfg - 

🐍 ConfigFile.py -

☰ cronLog.txt -

🐍 GradedResult.py -

🐍 Grader.py -

🐚 runCompileDriver.sh -
