###########################################!/usr/bin/python3
##########################################import subprocess
##########################################import os
##########################################import requests
##########################################
##########################################def get_days_in_month(M, Y):
##########################################    if M == 'Jan' or M == 'Mar' or M == 'May' or M == 'Jul' or M == 'Aug' or M == 'Oct' or M == 'Dec':
##########################################        return 31
##########################################    if M == 'Feb':
##########################################        if Y % 4 == 0 and Y % 100 != 0:
##########################################            return 29
##########################################        else:
##########################################            return 28
##########################################    if M == 'Apr' or M == 'Jun' or M == 'Sep' or M == 'Nov':
##########################################        return 30
##########################################    
##########################################
##########################################def get_difference(M, D, h, m, M1, D1, h1, m1, Y):
##########################################    file_sum = get_days_in_month(M, Y) * 24 * 60 + (D - 1) * 24 * 60 + h * 60 + m
##########################################    current_sum = get_days_in_month(M1, Y) * 24 * 60 + (D1 - 1) * 24 * 60 + h1 * 60 + m1
##########################################    return file_sum - current_sum
##########################################
##########################################def comment_out():
##########################################    my_file = open('DriverChecker.py', 'r+')
##########################################    my_lines = my_file.readlines()
##########################################    my_file.close()
##########################################    my_file = open('DriverChecker.py', 'w+')
##########################################    for line in my_lines:
##########################################        my_file.write('#' + line)
##########################################    my_file.close()
##########################################
##########################################os.chdir('/users/groups/cs235ta/submission_driver/')
##########################################file_info = subprocess.run(['ls', '-l', 'cronLog.txt'], stdout=subprocess.PIPE).stdout.decode('utf-8').split()
##########################################date_info = subprocess.run(['date'], stdout=subprocess.PIPE).stdout.decode('utf-8').split()
##########################################file_month = file_info[5]
##########################################file_day = int(file_info[6])
##########################################file_hour = int(file_info[7].split(':')[0])
##########################################file_minutes = int(file_info[7].split(':')[1] )
##########################################current_month = date_info[1]
##########################################current_day = int(date_info[2])
##########################################current_hour = int(date_info[3].split(':')[0])
##########################################current_minutes = int(date_info[3].split(':')[1])
##########################################year = int(date_info[5])
##########################################difference = get_difference(file_month, file_day, file_hour, file_minutes, current_month, current_day, current_hour,
##########################################        current_minutes, year) 
##########################################if difference < -10:
##########################################    #Email Roper here, and then open the current file and comment out every line
##########################################    email_data = {'email':'danejo3@outlook.com', 'subject':'TEST DRIVER ALERT!', 'body':'The driver has been down for more than ten minutes!!!<br>-Stephen Leach<br>(I may be contacted at stephenpleach@outlook.com)<br>'}
##########################################    email_files = None
##########################################    r = requests.post("https://students.cs.byu.edu/~cs235ta/emailEndpoint/dummy.php", data=email_data, files=email_files)
##########################################    email_data = {'email':'proper@cs.byu.edu', 'subject':'TEST DRIVER ALERT!', 'body':'The driver has been down for more than ten minutes!!!<br>-Stephen Leach<br>(I may be contacted at stephenpleach@outlook.com)<br>'}
##########################################    r = requests.post("https://students.cs.byu.edu/~cs235ta/emailEndpoint/dummy.php", data=email_data, files=email_files)
##########################################    comment_out()
##########################################else:
##########################################    pass
###########################################    if current_minutes % 30 == 0:
###########################################        email_data = {'email':'test@company.com', 'subject':'Test Driver Status: Good', 'body':'The driver is currently working<br>-Stephen Leach<br>(I may be contacted at stephenpleach@outlook.com)<br>'}
###########################################        email_files = None
###########################################        r = requests.post("https://students.cs.byu.edu/~cs235ta/emailEndpoint/dummy.php", data=email_data, files=email_files)
