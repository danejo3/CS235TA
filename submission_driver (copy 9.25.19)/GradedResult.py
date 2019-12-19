import Grader
from ConfigFile import ConfigFile
from ConfigFile import LogFile

class GradedResult:
    def __init__(self, config_object):
        self.config = config_object
        self.message = []
        self.memory_message = []
        self.points_awarded = 0
        self.bonus_points_awarded = 0
        self.points_total = 0
        self.bonus_points_total = 0
        self.valgrind_results = []
        self.in_file_names = []
        self.out_file_names = []
        self.pass_results = []
        self.final_message = ""
        self.key_file_names = []
        self.lab_name = "Lab00"
        self.late = False
        self.mem_points_awarded = 0
        self.late_message = self.config.late_message
        self.map_file_to_valgrind = {}

    def set_valgrind_message(self, file_name, message):
        self.map_file_to_valgrind[file_name] = message

    def get_valgrind_message(self):
        combined_message = ""
        for k in self.map_file_to_valgrind.keys():
            combined_message += self.map_file_to_valgrind[k]
        return combined_message

    def set_late_message(self, message):
        self.late_message = message

    def prep_message(self):
        self.final_message = '<pre>'
        if self.late is True:
            self.final_message += self.late_message
            self.final_message += '<br><br>'
        self.final_message += "You received  "
        if self.late is False:
            self.final_message += str(self.points_awarded)
            self.final_message += " points out of "
            self.final_message += str(self.points_total)
        else:
            self.final_message += str(self.points_awarded * self.config.late_ratio)
            self.final_message += " points out of "
            self.final_message += str(self.points_total)

        self.final_message += " points possible."
        self.final_message +='<br>You received '
        if self.late is False:
            self.final_message += str(self.bonus_points_awarded)
        else:
            self.final_message += str(self.bonus_points_awarded * self.config.late_ratio)
        self.final_message += ' bonus points out of '
        self.final_message += str(self.bonus_points_total)
        self.final_message += ' bonus points possible.\n<br>'
        for line in self.memory_message:
            self.final_message += line
            self.final_message += '<br>'

        self.final_message += '<br>Your total score is '
        self.final_message += str(self.get_score())
        self.final_message += ' points out of '
        self.final_message += str(self.points_total)
        self.final_message += ' points possible.<br><br>----------------------------------------------------------------<br>'
        for line in self.message:
            self.final_message += line
            self.final_message += '<br>'
        self.final_message += '</pre>'
        return self.final_message
    def get_subject(self):
        s = self.lab_name
        s += ' Score: ' 
        p = self.get_score()
        s += str(p)
        s += ' out of '
        s += str(self.points_total)
        return s

    def add_forfeited_score(self, points):
        self.points_total += points
        return

    def add_forfeited_bonus_score(self, points):
        self.bonus_points_total += points
        return

    def enter_test_result(self, in_file, out_file, key_file, point_value, bonus, passed_result, valgrind_result, partial_message):
        self.in_file_names.append(in_file)
        self.out_file_names.append(out_file)
        self.key_file_names.append(key_file)
        if bonus is False:
            self.points_total += point_value
        else:
            self.bonus_points_total += point_value
        if passed_result is None:
            if bonus is False:
                self.points_awarded += point_value
            else:
                self.bonus_points_awarded += point_value
            my_list = ['<br>Passed'] + partial_message + ['<br>' + str(point_value) + ' points awarded.']
            if bonus is True:
                my_list = ['<br>Bonus Passed'] + partial_message + ['<br>' + str(point_value) + ' points awarded.']
            self.append_message(my_list)     
        else:
            my_list = []
            if passed_result.first is 'ERROR':
                my_list = ['<br>Failed'] + partial_message + ['<br>     Error: ' + passed_result.second]
            else:
                my_list = ['<br>Failed'] + partial_message + ['<br>  Expected: ' + passed_result.first + '<br>       Got: ' + passed_result.second]
                if bonus is True: 
                    my_list = ['<br>Bonus Failed'] + partial_message + ['<br>  Expected: ' +  passed_result.first + '<br>       Got: ' + passed_result.second]
            self.append_message(my_list)
        self.pass_results.append(passed_result)
        self.valgrind_results.append(valgrind_result)
        return

    def enter_driver_test_result(self, points, command, message, passed):
        self.points_total += points
        if passed:
            self.append_message(['<br>Passed'] + message + ['<br' + str(points) + ' points awarded.'])
            self.points_awarded += points
        else:
            self.append_message(['<br>Failed'] + message)
        return
            
    def mem_check(self, point_value):
        self.mem_points_awarded += point_value
        return

    def set_message(self, my_string):
        self.final_message = ""
        self.message = []
        self.message.append(my_string)
        return

    def append_message(self, my_list):
        my_string=''
        for word in my_list:
            my_string += word
            my_string += ' '
        self.message.append(my_string)
            
        return
    
    def get_message(self):
        return self.final_message

    def get_score(self):
        total_points = self.points_awarded + self.bonus_points_awarded + self.mem_points_awarded
        if total_points < 0:
            total_points = 0
        if self.late is True:
            return total_points * self.config.late_ratio
        return total_points

    def set_lab_name(self, my_name):
        self.lab_name = my_name
        return

    def grade_mem(self, points):
        reported = []
        if points < 0:
            i = 1
            passed = True
            for result in self.valgrind_results:
                if result is False:
                    pass
                elif not result is None:
                    if not result in reported:
                        self.memory_message.append(result)
                        passed = False
                        reported.append(result)
                i += 1
            if passed is True:
                self.memory_message.append('<br>No memory leaks found!')
            else:
                self.memory_message.append(str((points * -1)) + ' points deducted. (To see Valgrind error(s), please look towards the bottom of the email.)')
                self.mem_check(points)


            return
        self.points_total += points
        i = 1
        passed = True
        for result in self.valgrind_results:
            if result is False:
                pass
            elif not result is None:
                if not result in reported:
                    self.memory_message.append(result)
                    passed = False
                    reported.append(result)
            i += 1
        if passed is True:
            self.memory_message.append('<br>No memory leaks found!')
            self.memory_message.append(str(points) + ' points  awarded.')
            self.mem_check(points)
        else:
            self.memory_message.append('0 points awarded.')
        return
        
    def set_late(self, l):
        self.late = l
        return
