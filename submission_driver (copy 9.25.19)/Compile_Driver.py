#!/usr/bin/python3

#============== Compile_Driver.py ====================#
#                                                     #
# Authors: Mike Liddle & Stephen Leach and Dane Jo    #
# Brigham Young University                            #
#                                                     #
# Purpose: this software is to be used for the        #
#          autocompilation and grading of students'   #
#          code for CS 235 at BYU.                    #
#                                                     #
# Files:   Compile_Driver.py, ConfigFile.py           #
#                                                     #
#=====================================================#

import subprocess
import requests
import os
import shutil
import datetime
import re
import Grader
from GradedResult import GradedResult
from ConfigFile import ConfigFile
from ConfigFile import LogFile

# variables used for debugging the code
DEBUG = False
WIN_DEBUG = False

# specifies the root directory for the program to be run in.
ROOT_DIR = '/users/groups/cs235ta/submission_driver/'

# if running on a windows machine, adjust accordingly.
if WIN_DEBUG:
    ROOT_DIR = 'path'

# create the config file object from the file.
config_file_object = ConfigFile(ROOT_DIR + 'compiler_global.cfg')


#=====================================================#
# store_grade                                         #
#       ammends the given file, updating the          #
#       net_id's score, or inserting it if the first  #
#       submission.                                   #
#                                                     #
#=====================================================#
def store_grade(file_name, net_id, grade, late):
    on_time_grade = 0
    late_grade = 0
    with open(file_name, 'a+'):
        pass
    myFile = open(file_name, 'r+')
    myLines = myFile.readlines()
    myNewLines=[]
    for line in myLines:
        isDuplicate = False
        for word in line.split():
            if word == net_id + ",":
                isDuplicate = True
                temp = line.split(', ')
                on_time_grade = float(temp[1])
                late_grade = float(temp[2])

        if isDuplicate is False:
            myNewLines.append(line)
    myFile.close()
    if late:
        if late_grade < grade:
            late_grade = grade
    else:
        if on_time_grade < grade:
            on_time_grade = grade
    myNewLines.append(net_id + ', ' + str(on_time_grade) + ', ' + str(late_grade) + ', ' + str(datetime.datetime.now()) + '\n')
    myNewFile = open(file_name, 'w')
    myNewFile.writelines(myNewLines)
    return


#=====================================================#
# compile_code                                        #
#    compiles the student code and composes an info   #
#    string that reports the compilation status.      #
#                                                     #
#=====================================================#
def compile_code(lab_name, net_id, email, log_date):
    global config_file_object

    exe_name = 'run_me'
    information_string = ""
    information_string += 'compiling files:\n'

    all_files = []

    p = subprocess.run(['iconv', '-l'], stdout=subprocess.PIPE)
    with open('encodings.temp', 'w+') as temp:
        temp.writelines('\n'.join(str(p.stdout).split('\\n')))



    # include all cpp files in compilation, check file encoding.
    for f in os.listdir('.'):
        subprocess.run(['chmod', '700', f]);
        # this is what checks the extension "*.cpp"
        subprocess.run(['dos2unix', f], stdout=subprocess.PIPE)


        p = subprocess.run(['file', f], stdout=subprocess.PIPE)
        myString = str(p.stdout)
        myList = myString.split()
        myList = myList[1:]
        myString = " ".join(myList)
        myList = myString.split(',')
        index = -1
        for i in range(len(myList)):
            if myList[i].find("text") > -1:
                index = i
                break
        if index != -1:
            myString = myList[index].strip()
            myList = myString.split()
            myString = myList[0]
            encoding = myString
            p = subprocess.run(['grep', encoding, 'encodings.temp'], stdout=subprocess.PIPE)
            myString = str(p.stdout)[2:].split('\\n')[0]
            encoding = myString
            subprocess.run(['iconv', '-f', encoding, '-t', 'utf-8', f, '-o', f + 'temp'])
            subprocess.run(['mv', f + 'temp', f])

        else:
            subprocess.run(['iconv', '-t', 'utf-8', f, '-o', f + 'temp'])
            subprocess.run(['mv', f + 'temp', f])
        p = subprocess.run(['file', f], stdout=subprocess.PIPE)
        myString = str(p.stdout)
        if myString.find('UTF-8') == -1:
            Grader.log_error("Invalid File: " + myString)
            #subprocess.run(['rm', f])



        if os.path.isfile(f) and re.search('cpp', f):
            # the following process gets the file encoding.
            p = subprocess.run(['/usr/bin/file', '-i', f],
                               stdout=subprocess.PIPE)
            file_info = p.stdout.decode('utf-8').split(":")
            file_info = file_info[1].split(";")
            file_info = file_info[1].split("=")
            file_info[1] = file_info[1].strip()

            # is the file encoding one of our accepted encodings?
            if file_info[1] == "us-ascii" or file_info[1] == "utf-8":
                all_files.append(f)
            else:
                # if not, still try to compile, but report it as invalid.
                information_string += 'invalid file encoding: \"' + \
                    file_info[1] + '\" for file: ' + str(f) + '\n'
                all_files.append(f)

    # if there are no files, report that.
    if len(all_files) < 1:
        information_string += 'No valid files detected!' + '\n'

    compile_command = [config_file_object.compiler, '-g',
                       '-Wall', '-std=c++17', '-o', exe_name]
    for file in all_files:
        information_string += file + '\n'
        compile_command.append(file)

    # report the command we used to the user.
    information_string += '\ng++ -g -Wall -std=c++17 -o ' + exe_name + ' *.cpp' + '\n'

    # g++ won't work on windows, act accordingly.
    if not WIN_DEBUG:
        p = subprocess.run(
            compile_command, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        # grab the output from g++ and put it in the info string.
        compile_error = p.stderr.decode('utf-8')
        information_string += compile_error + '\n'

        # tell the user whether compilation succeeded or failed.
        if p.returncode == 0:
            information_string += 'Compilation Succeeded!'
        else:
            information_string += 'Compilation Failed!'

        # log the result as well with the student information in case of errors.
        with open(config_file_object.get_compile_log(), 'a+') as compile_log:
            compile_log.write(
                ','.join([log_date, lab_name, net_id, email, str(p.returncode)]) + '\n')
    else:
        information_string += 'Compilation Not Performed.'

    return information_string

#=====================================================#
# run_student_code                                    #
#    runs the compilation, then any other needful     #
#    actions, including emailing the student the      #
#    results of compilation.  This is where extension #
#    of functionality should happen.                  #
#                                                     #
#=====================================================#
def run_student_code(lab_name, net_id, email, log_date, late, log_line):
    global config_file_object
    os.chdir("TMP_DELETE")

    #with open('../tmp.tmp', 'a+') as error_log:
    #    error_log.write(str(datetime.datetime.now()) + "Start All\n")

    # compile the code.
    if(lab_name != "Lab12"):
        information_string = compile_code(lab_name, net_id, email, log_date)
    else:
        information_string = compile_code("Lab03", net_id, email, log_date)

    information_string += '\n\n'

    grade = 0
    message = "Compilation failed... 0 points awarded.\n"
    subject = net_id + 'Compilation failed - ' + lab_name
    #this is where we run the students' code and diff it
    result = None
    if 'Compilation Succeeded' in information_string:
        if (lab_name != "Lab12"):
            result = Grader.grade('run_me', lab_name, config_file_object.root_dir + '/LabKeyFiles', late,
                              config_file_object)
        else:
            result = Grader.grade('run_me', "Lab03", config_file_object.root_dir + '/LabKeyFiles', late,
                                  config_file_object)
        grade = result.get_score()
        message = result.get_message()
        subject = net_id + ' - ' + result.get_subject()

    grades_file_name = config_file_object.live_dir[:-9]
    grades_file_name += lab_name
    grades_file_name += "grades.csv"
    store_grade(grades_file_name, net_id, grade, late)


    individual_grades_name = '../' + net_id + '.' + lab_name + '.grade.out'
    str_late = ''
    if late:
        str_late = 'Late'
    else:
        str_late = 'On-time'
    with open(individual_grades_name, 'a+') as my_file:
        my_file.write(str(grade) + ', ' + str_late + ', ' + str(datetime.datetime.now()) + '\n')

    # write to the student compile file
    compile_file_name = net_id + '.' + lab_name + '.compile.out'
    compile_file = open(compile_file_name, 'w+')
    compile_file.write(information_string)
    compile_file.close()
    copy_command = ["cp", compile_file_name, '../' + compile_file_name]
    subprocess.run(copy_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if DEBUG:
        # don't want to pester students with debugging emails.
        email = 'test@company.com'

    # This is the body of the message.  Feel free to change and update this as needed.
    body = message
    body += '\n---------------------------------------------------------------'
    body += '<br><br>Your compilation results are as follows:\n'
    #body += truncate_compilation_resuilt(information_string)
    body += information_string

    #adding 2/22/19
    if(result != None):
        if(result.get_valgrind_message() != ""):
            body += '---------------------------------------------------------------\n\n'
            body += 'Your valgrind results are as follows:\n'
            body += result.get_valgrind_message()
            body += 'Valgrind Failed!'

    # create the email object
    # adding 2/23/19 to add the log line to the email subject
    if(late):
        emailID = " - #L" + str(log_line)
    else:
        emailID = " - #OT" + str(log_line)
    subject += emailID
    email_data = {'email': email, 'subject': subject, 'body': body}
    email_files = {'compile': open(net_id + '.' + lab_name + '.compile.out', 'rb')}

    #with open('../tmp.tmp', 'a+') as error_log:
    #    error_log.write(str(datetime.datetime.now()) + "End All\n")
    # send the HTTP request to the endpoint to send the email.
    #if(lab_name == "Lab00"):
    #	r = requests.post("https://students.cs.byu.edu/~cs235ta/emailEndpoint/dummyMatthewProofOfConcept.php", data=email_data,
    #                  files=email_files)
    #else:
    #    r = requests.post("https://students.cs.byu.edu/~cs235ta/emailEndpoint/dummy.php", data=email_data,
    #                  files=email_files)

    r = requests.post("https://students.cs.byu.edu/~cs235ta/emailEndpoint/dummy.php", data=email_data,
                      files=email_files)

    # send email and log the result.
    if not DEBUG:
        with open(config_file_object.get_email_log(), 'a+') as email_file:
            log_entry_list = (log_date, net_id, email,
                              lab_name, str(r.status_code))
            email_file.write(','.join(log_entry_list) + '\n')
    else:
        with open(config_file_object.get_email_log(), 'a+') as email_file:
            log_entry_list = (log_date, net_id, email, lab_name, 'test')
            email_file.write(','.join(log_entry_list) + '\n')

    # self-cleanup, the rm usually fails, but everything inside gets removed, which does the trick.
    os.chdir('..')
    shutil.rmtree('TMP_DELETE', True)



# adding this function to handle email body of compilation results
# 2/12/2019
def truncate_compilation_resuilt(results):
    if(results.count('\n') > 50):
        # print part of the body if the results string is super long
        mylist = results.split('\n')

        truncated_string = ""
        for i in range(0,50):
            truncated_string = truncated_string + mylist[i] + "\n"
        truncated_string += ". . . \n\n****Results were truncated**** \n\nCompilation failed!"
        return truncated_string

    return results






#=====================================================#
# submission_driver                                   #
#    this is the main driver function, it handles     #
#    logic for reading a submission from the log and  #
#    parsing the entry to run the student code.  This #
#    shouldn't need much if any maintenance for       #
#    functionality.                                   #
#                                                     #
#=====================================================#


def submission_driver():
    global config_file_object

    # this creates the log file object from the log file given in our config folder.
    log_file = LogFile(config_file_object.log_file_path)
    late_log_file = LogFile(config_file_object.late_log_file_path)
    #print(config_file_object.log_file_path)
    # run this loop indefinitely.  Cron should handle any breaking from this loop.
    while True:
        # wrap everything in a try/except to handle errors gracefully and report them.
        try:
            # we start in the root directory.
            os.chdir(config_file_object.root_dir)
            # check to see if our log file exists
            valid_log_line = log_file.check_last_line(
                config_file_object.current_line)
            if valid_log_line > 0:
                # if it exists, we get the line we are on.
                log_entry = log_file.get_line(config_file_object.current_line)

                # log information in the debuf file when debugging.
                if DEBUG:
                    with open(config_file_object.get_debug_log(), 'a+') as debug_file:
                        debug_file.write(
                            'log_entry: ' + ','.join(log_entry) + '\n')

                # increment the current line count so we know to do the next entry next.
                config_file_object.increment_current_line()

                # split and parse the log entry.
                log_date = log_entry[0]
                lab = log_entry[1]
                file_name = log_entry[5].strip('()')
                net_id = log_entry[2]
                email = log_entry[6]

                # move into the student's folder on the server.
                os.chdir(config_file_object.live_dir + net_id)

                # if they don't have a TMP_DELETE folder, create it.
                if not os.path.exists("TMP_DELETE"):
                    os.mkdir("TMP_DELETE")
                else:
                    # otherwise, remove the folder and recreate it.
                    if DEBUG:
                        with open(config_file_object.get_debug_log(), 'a+') as debug_file:
                            debug_file.write('Removing TMP_DELETE\n')
                    shutil.rmtree("TMP_DELETE")
                    os.mkdir("TMP_DELETE")

                # log the current directory when debugging.
                if DEBUG:
                    with open(config_file_object.get_debug_log(), 'a+') as debug_file:
                        debug_file.write(str(os.getcwd()) + '\n')

                # unzip the student code zip archive.
                # unzip -o -qq <file_name> -d TMP_DELETE
                if not WIN_DEBUG:  # unzip doesn't exist on Windows systems.
                    subprocess.call([config_file_object.unzip, '-o', '-qq', file_name, '-d', 'TMP_DELETE'],
                                    stdin=subprocess.DEVNULL)
                else:
                    with open(config_file_object.get_debug_log(), 'a+') as debug_file:
                        debug_file.write('Unzipping file: ' + file_name + '\n')

                # run the student code.
                run_student_code(lab, net_id, email, log_date, False, config_file_object.current_line)

            elif valid_log_line < 0:
                # if the log file has been removed, tell the config file to start over at 0.
                config_file_object.set_current_line(0)
        except KeyboardInterrupt:
            # ctrl + c SIGINT, just exit.
            exit(0)
        except Exception as error:
            # log any error messages.
            with open(config_file_object.get_error_log(), 'a+') as error_log:
                error_log.write(str(datetime.datetime.now()) +
                                ': ' + str(error) + '\n')

        #late submissions
        try:
            # we start in the root directory.
            os.chdir(config_file_object.root_dir)
            # check to see if our log file exists
            valid_log_line = late_log_file.check_last_line(
                config_file_object.current_late_line)
            if valid_log_line > 0:
                # if it exists, we get the line we are on.
                log_entry = late_log_file.get_line(config_file_object.current_late_line)

                # log information in the debuf file when debugging.
                if DEBUG:
                    with open(config_file_object.get_debug_log(), 'a+') as debug_file:
                        debug_file.write(
                            'log_entry: ' + ','.join(log_entry) + '\n')

                # increment the current line count so we know to do the next entry next.
                config_file_object.increment_current_late_line()

                # split and parse the log entry.
                log_date = log_entry[0]
                lab = log_entry[1]
                file_name = log_entry[5].strip('()')
                net_id = log_entry[2]
                email = log_entry[6]

                # move into the student's folder on the server.
                os.chdir(config_file_object.live_dir + net_id)

                # if they don't have a TMP_DELETE folder, create it.
                if not os.path.exists("TMP_DELETE"):
                    os.mkdir("TMP_DELETE")
                else:
                    # otherwise, remove the folder and recreate it.
                    if DEBUG:
                        with open(config_file_object.get_debug_log(), 'a+') as debug_file:
                            debug_file.write('Removing TMP_DELETE\n')
                    shutil.rmtree("TMP_DELETE")
                    os.mkdir("TMP_DELETE")

                # log the current directory when debugging.
                if DEBUG:
                    with open(config_file_object.get_debug_log(), 'a+') as debug_file:
                        debug_file.write(str(os.getcwd()) + '\n')

                # unzip the student code zip archive.
                # unzip -o -qq <file_name> -d TMP_DELETE
                if not WIN_DEBUG:  # unzip doesn't exist on Windows systems.
                    subprocess.call([config_file_object.unzip, '-o', '-qq', file_name, '-d', 'TMP_DELETE'],
                                    stdin=subprocess.DEVNULL)
                else:
                    with open(config_file_object.get_debug_log(), 'a+') as debug_file:
                        debug_file.write('Unzipping file: ' + file_name + '\n')

                # run the student code.
                run_student_code(lab, net_id, email, log_date, True, config_file_object.current_late_line)

            elif valid_log_line < 0:
                # if the log file has been removed, tell the config file to start over at 0.
                config_file_object.set_current_late_line(0)
        except KeyboardInterrupt:
            # ctrl + c SIGINT, just exit.
            exit(0)
        except Exception as error:
            # log any error messages.
            with open(config_file_object.get_error_log(), 'a+') as error_log:
                error_log.write(str(datetime.datetime.now()) +
                                ': ' + str(error) + '\n')


# run the driver.
submission_driver()