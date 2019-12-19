from GradedResult import GradedResult
from ConfigFile import ConfigFile
from ConfigFile import LogFile
import subprocess
import os
import re
import datetime

def decomment_word(word):
    if len(word) < 2:
        return word
    newWord = ''
    for i  in range(len(word)):
        char = word[i]
        if char == '/':
            if (len(word) - 1) == i:
                return word
            if word[i + 1] == '/':
                return newWord
        newWord += char
    return word

def decomment(list_of_words):
    command = []
    for word in list_of_words:
        new_word = decomment_word(word)
        command.append(new_word)
        if not len(new_word) == len(word):
            break
    return command
        
def grade(executable, lab_name, key_dir, late, config):
    lab_config_file_name = key_dir + '/' +  lab_name + '/' + "setup.ini"
    my_grader = open(lab_config_file_name, 'r+')
    my_commands = my_grader.readlines()
    result = GradedResult(config)
    result.set_late(late)
    squash_h = False
    squash_v = False
    order = True
    abort = False
    stl = False
    failed_flag = False
    mem_check = False
    test_count = 0
    used_stl = False
    cache = {}
    result.set_lab_name(lab_name)
    #with open("../tmp.tmp","a+") as f:
    #    f.write(str(datetime.datetime.now()) + ' begin tests\n')
    for line in my_commands:
        if len(line) == 0:
            continue
        command = line.split()
        command = decomment(command)
        if len(command) == 0:
            continue
        elif command[0] == "SQUASH:":
            cache = {}
            if command[1] == "0":
                squash_h = False
                squash_v = False
            else:
                squash_h = True
                squash_v = True
        elif command[0] == "SQUASH_H:":
            cache = {}
            if command[1] == "0":
                squash_h = False
            else:
                squash_h = True
        elif command[0] == "SQUASH_V:":
            cache = {}
            if command[1] == "0":
                squash_v = False
            else:
                squash_v = True
        elif command[0] == "IGNORE_ORDER:":
            cache = {}
            if command[1] == "0":
                order = True
            else:
                order = False
        elif command[0] == "STL_ALLOWED:":
            cache = {}
            stl_use = None
            if command[1] == "0":
                if len(command) == 2:
                    stl_use = uses_stl(True, [])
                elif len(command) > 2:
                    if command[2] == 'EXCEPT:':
                        stl_use = uses_stl(True, command[3:])
            else:
                if len(command) == 2:
                    stl = True
                    used_stl = False
                elif len(command) > 2:
                    stl_use = uses_stl(False, command[3:])
            if not stl_use is None:
                result.append_message(["You illegally used: " + stl_use])
                used_stl = True

        elif command[0] == "ABORT:":
            cache = {}
            if command[1] == "0":
                abort = False
            else:
                abort = True
                failed_flag = False
        elif command[0] == "MEMCHECK:":
            cache = {}
            if command[1] == "0":
                mem_check = False
            else:
                mem_check = True
        elif command[0] == "MEMPOINTS:":
            cache = {}
            if used_stl is False:
                result.grade_mem(int(command[1]))
            else:
                result.add_forfeited_score(int(command[1]))
        elif command[0] == "TEST:":
            if (abort is False or failed_flag is False) and used_stl is False:
                test = execute(executable, key_dir, lab_name, command[1], command[2], squash_h, squash_v, order, mem_check, cache)
                #added 2/22/19
                result.set_valgrind_message(test.valgrind_passed, test.valgrind_output)
                result.enter_test_result(command[1], test.out_file_name, command[2], int(command[3]), False, test.test_result, test.valgrind_passed, command[4:])
                if not test.test_result is None:
                    failed_flag = True
            else:
                result.add_forfeited_score(int(command[3]))
        elif command[0] == "BONUS:":
            if (abort is False or failed_flag is False) and used_stl is False:
                test = execute(executable, key_dir, lab_name, command[1], command[2], squash_h, squash_v, order, mem_check, cache)
                #added 2/22/19
                result.set_valgrind_message(test.valgrind_passed, test.valgrind_output)
                result.enter_test_result(command[1], test.out_file_name, command[2], int(command[3]), True, test.test_result, test.valgrind_passed, command[4:])
                if not test.test_result is None:
                    failed_flag = True
            else:
                result.add_forfeited_bonus_score(int(command[3]))
        elif command[0] == 'RUN:':
            if (abort is False or failed_flag is False) and used_stl is False:
                test_passed = run_driver_test(get_driver_command(command[2:]), key_dir, lab_name, get_driver_key_word(command[2:]))
                result.enter_driver_test_result(int(command[1]), get_driver_command(command[2:]), get_driver_message(command[2:]), test_passed)
            else:
                result.add_forfeited_score(int(command[1]))
        elif command [0] == 'RUN_LINUX:':
            linux_command = command[1:]
            subprocess.run(linux_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result.prep_message()
    return result

def run_driver_test(files, key_dir, lab_name, key_word):
    root_dir = key_dir + '/' + lab_name + '/driver_files/'
    for name in files:
        command = ['cp', root_dir + name, '.']
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    command = ['g++', '-std=c++17']
    for name in files:
        command.append(name)
    command.append('-o')
    command.append('driver_test')
    p = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode == 0:
        command = ['./driver_test']
        p = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = str(p.stdout)
        if key_word in result:
            return True
    return False



def execute(executable, key_dir, lab_name, in_file_name, key_file_name, squash_h, squash_v, order, mem_check, cache):
    cached_result = get_cached_result(in_file_name, key_dir, lab_name, mem_check, cache, executable, key_file_name)
    try:
        if order is False:
            cached_result.test_result = out_file_contains_key(cached_result.out_file_name, key_file_name, squash_h)
        else:
            cached_result.test_result = out_file_contains_key_in_order(cached_result.out_file_name, key_file_name, squash_h, squash_v)
    except Exception as error:
        #cached_result.test_result = Pair('ERROR', str(error))
        cached_result.test_result = Pair('ERROR', "Check your spelling and punctuation to ensure it exactly matches the key file.")
    return cached_result

def get_cached_result(in_file_name, key_dir, lab_name, mem_check, cache, executable, key_file_name):
    with open(key_dir + '/' + lab_name + '/key_files/' + key_file_name, 'r+') as f:
        with open(key_file_name, 'w+') as f1:
            lines = f.readlines()
            for line in lines:
                if len(line.split()) > 0:
                    f1.write(line)

    if in_file_name in cache.keys():
        return cache[in_file_name]

    command = ['cp', key_dir + '/' + lab_name + '/in_files/' + in_file_name, '.']
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    command = ['dos2unix', in_file_name]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    valgrind_result = False
    test_result = False
    out_file_name = in_file_name + '_student.out'
    with open(out_file_name, 'a+') as file:
        pass
    command = ['timeout', '5', 'valgrind', '--leak-check=full', '--show-leak-kinds=all', './' + executable, in_file_name, out_file_name]
    process_result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = str(process_result.stderr)
    if mem_check is True:
        valgrind_result = get_valgrind_message(result, in_file_name, out_file_name)
    cache[in_file_name] = Trio(None, valgrind_result[0], out_file_name, valgrind_result[1])
    return cache[in_file_name]







# adding a function to truncate the memory leak errors
def truncate_valgrind_resuilt(results):
    if(results.count('\n') > 20):
        # print part of the body if the results string is super long
        mylist = results.split('\n')

        truncated_string = ""
        for i in range(0,20):
            truncated_string = truncated_string + mylist[i] + "\n"
        truncated_string += ". . . \n****Results were truncated****"
        return truncated_string

    return results














def get_valgrind_message(result, file_name, out_file_name):
    # adding valgrind error notes <----------------------------------------------------------------- 2/14/19
    replaced_newlines = result.replace('\\n', '\n')

    s = ' with input file: ' + file_name
    #vo = 'valgrind --leak-check=full --show-leak-kinds=all ./run_me ' + file_name + ' ' + out_file_name + '\n' + truncate_valgrind_resuilt(replaced_newlines) + '\n\n'
    vo = 'valgrind --leak-check=full --show-leak-kinds=all ./run_me ' + file_name + ' ' + out_file_name + '\n' + replaced_newlines + '\n\n'
    if 'Invalid read of size' in result:
        return 'Attempted to access out of bounds data' + s, vo
    if 'terminate called after throwing an instance of \'std::out_of_range\'' in result:
        return 'Out of bounds on STL Container' + s, vo
    if 'Invalid free() / delete / delete[] / realloc()' in result or 'Mismatched free() / delete / delete []' in result:
        return 'Invalid use of delete or free()' + s, vo
    if 'Process terminating with default action of signal 15' in result:
        return 'Program timed out' + s, vo
    if 'Conditional jump or move depends on uninitialised value' in result:
        return 'Uninitialized value used' + s, vo
    if 'terminate called after throwing an instance of' in result:
        return 'Unknown run-time error detected' + s, vo
    if 'in use at exit: 0 bytes in 0 blocks' in result or 'in use at exit: 72,704 bytes in 1 blocks' in result:
        return None, ""
    else:
        return 'Memory leaks or run-time errors detected' + s, vo

def out_file_contains_key_in_order(out_file_name, key_file_name, squash_h, squash_v):
    key_file = open(key_file_name, 'r+')
    with open(out_file_name, 'a+') as f:
        pass
    out_file = open(out_file_name, 'r+')
    key_lines = key_file.readlines()
    out_lines = out_file.readlines()
    key_file.close()
    out_file.close()
    i = 0
    start = 0
    for j in range(len(out_lines)):
        if i >= len(out_lines):
            break
        line = out_lines[i].strip()
        key_line = key_lines[start].strip()
        if squash_v is True:
            while len(line) == 0:
                i += 1
                if i == len(out_lines):
                    break
                line = out_lines[i].strip()
            while len(key_line) == 0:
                start += 1
                if start == len(key_lines):
                    break
                line = key_lines[i].strip()
        if squash_h is True:
            line = ''.join(line.split())
            key_line = ''.join(key_line.split())
        if line == key_line:
            break
        i += 1
    if i >= len(out_lines):
        return Pair( key_lines[0].strip(), 'Unable to find expected line. Reached end of file...')
    previous_line = key_lines[0].strip()
    previous_out_line = key_lines[0].strip()
    for line in key_lines:
        if i == len(out_lines):
            return Pair(previous_line + '<br>            ' + line.strip(), previous_out_line + '<br>            Unable to find expected line. Reached end of file...')
        key_line = line.strip()
        out_line = out_lines[i].strip()
        if squash_h is True:
            key_line = ''.join(key_line.split())
            out_line = ''.join(out_line.split())
        if squash_v is True:
            while len(out_line) == 0:
                i += 1
                if i == len(out_lines):
                    return Pair(previous_line + '<br>            ' + line.strip(), previous_out_line + '<br>            Unable to find expected line. Reached end of file...')
                out_line = out_lines[i].strip()
                if squash_h is True:
                    out_line = ''.join(out_line.split())
        if not key_line == out_line:
            return_line = previous_line + '<br>            ' + line.strip()
            return_out_line = previous_out_line + '<br>            ' + out_lines[i].strip()
            return Pair(return_line, return_out_line)
        previous_line = line.strip()
        previous_out_line = out_lines[i].strip()
        i += 1
    return None #This is the equivalent of True

def out_file_contains_key(out_file_name, key_file_name, squash_h):
    key_file = open(key_file_name, 'r+')
    with open(out_file_name, 'a+') as f:
        pass
    out_file = open(out_file_name, 'r+')
    key_lines = key_file.readlines()
    out_lines = out_file.readlines()
    key_file.close()
    out_file.close()
    for l in key_lines:
        line = l
        if squash_h is True:
            line = ''.join(line.split())
        if in_array(line, out_lines, squash_h) is False:
            return Pair(l, 'Unable to find expected line. Reached end of file...')
    return None

def in_array(key_line, array, squash_h):
    for l in array:
        line = l
        if squash_h is True:
            line = ''.join(line.split())
        if key_line == line:
            return True
    return False

def log_error(myString):
    with open('/users/groups/cs235ta/submission_driver/logs/W2019_errors.txt', 'a+') as f:
        f.write(str(datetime.datetime.now()) + ' ' + myString + '\n')

def uses_stl(restricted, exceptions):
    stl = ['vector', 'map', 'set', 'queue', 'deque', 'stack', 'list', 'unordered_map', 'unordered_set', 'forward_list', 'array']
    myDict = {}
    for container in stl:
        myDict[container] = restricted
    for e in exceptions:
        myDict[e] = not restricted
    for f in os.listdir('.'):
        if (os.path.isfile(f) and re.search('cpp', f)) or (os.path.isfile(f) and re.search('h', f)):
            #log_error("Valid File");
            my_file = open(f)
            try:
                my_lines = my_file.readlines()
            except:
                log_error('Invalid File: ' + str(f))
                return 'Error encountered. Please remove unidentifiable symbol. (Most likely in one of your comments)'
            my_file.close()
            #log_error("Done");
            for line in my_lines:
                l = line.replace(" ", "")
                for container in stl:
                    if 'include<' + container + '>' in l and myDict[container]:
                        return '#include &lt' + container + '&gt;'
        else:
            #log_error("Invalid File")
            pass
    return None

class Trio:
    def __init__(self, t, v, o, vo = ""):
        self.test_result = t
        self.valgrind_passed = v
        self.out_file_name = o
        self.valgrind_output = vo

class Pair:
    def __init__(self, f, s):
        self.first = f
        self.second = s

def get_driver_message(my_array):
    new_array = []
    message = False
    for line in my_array:
        if message:
            new_array.append(line)
        if line[:2] == '$:':
            message = True
            new_array.append(line[2:])
    return new_array

def get_driver_command(my_array):
    new_array = [] 
    for line in my_array:
        if line[:1] == '\"':
            break
        new_array.append(line)
    return new_array

def get_driver_key_word(my_array):
    new_string = ''
    string = False
    for line in my_array:
        if string:
            if line[-1:] == '\"':
                new_string += line[:-1]
                break
            else:
                new_string += line
                new_string += ' '
        elif line[:1] == '\"':
            new_string += line[1:]
            new_string += ' '
            string = True
    return new_string

