#!/usr/bin/python3


class ConfigFile(object):
    def __init__(self, file_path):
        # define all members.
        self.file_path = file_path
        self.file_object = open(file_path, 'r+')
        self.current_line = 0
        self.current_late_line = 0
        self.log_file_path = ""
        self.late_log_file_path = ""
        self.live_dir = 0
        self.grade_log_file = 0
        self.out_file = 0
        self.semester = ''
        self.root_dir = ''
        self.log_dir = ''
        self.email_log = ''
        self.grade_log = ''
        self.error_log = ''
        self.debug_log = ''
        self.compile_log = ''
        self.compiler = 'g++'
        self.unzip = 'unzip'
        self.late_ratio = 1.0
        self.late_message = 'Assignment Late! Points will be deducted!'
        self.file_contents = self.file_object.readline(10000)

        # initialize file.
        self.parse_config_file()
        self.file_object.close()

    # end __init__

    def parse_config_file(self):
        self.file_object.seek(0)
        current_line = self.file_object.readline()[13:].strip('\n')
        self.current_line = int(current_line)
        current_late_line = self.file_object.readline()[18:].strip('\n')
        self.current_late_line = int(current_late_line)
        self.log_file_path = self.file_object.readline()[9:].strip('\n')
        self.late_log_file_path = self.file_object.readline()[14:].strip('\n')
        self.live_dir = self.file_object.readline()[9:].strip('\n')
        self.out_file = self.file_object.readline()[9:].strip('\n')
        self.semester = self.file_object.readline()[9:].strip('\n')
        self.root_dir = self.file_object.readline()[9:].strip('\n')
        self.log_dir = self.file_object.readline()[8:].strip('\n')
        self.email_log = self.file_object.readline()[15:].strip('\n')
        self.grade_log = self.file_object.readline()[10:].strip('\n')
        self.error_log = self.file_object.readline()[15:].strip('\n')
        self.debug_log = self.file_object.readline()[15:].strip('\n')
        self.compile_log = self.file_object.readline()[17:].strip('\n')
        self.compiler = self.file_object.readline()[9:].strip('\n')
        self.unzip = self.file_object.readline()[6:].strip('\n')
        self.late_ratio = float(self.file_object.readline()[11:].strip('\n'))
        self.late_message = self.file_object.readline()[13:].strip('\n')

    # end parse_config_file

    def closed(self):
        self.file_object = open(self.file_path, 'r+')
        if self.file_object.closed:
            return True
        else:
            self.file_object.close()
            return False

    # end closed

    def set_current_line(self, new_line):
        self.current_line = new_line
        self.write_file()

    def set_current_late_line(self, new_line):
        self.current_late_line = new_line
        self.write_file()

    # set current_line

    def increment_current_line(self):
        self.current_line = self.current_line + 1
        self.write_file()

    # end increment_current_line

    def increment_current_late_line(self):
        self.current_late_line = self.current_late_line + 1
        self.write_file()



    def write_file(self):
        self.file_object = open(self.file_path, 'w')

        str_current_line = 'CURRENT_LINE:' + str(self.current_line)
        str_current_late_line = 'CURRENT_LATE_LINE:' + str(self.current_late_line)
        str_log_file = 'LOG_FILE:' + str(self.log_file_path)
        str_late_log_file = 'LATE_LOG_FILE:' + str(self.late_log_file_path)
        str_live_dir = 'LIVE_DIR:' + str(self.live_dir)
        str_out_file = 'OUT_FILE:' + str(self.out_file)
        str_semester = 'SEMESTER:' + str(self.semester)
        str_root_dir = 'ROOT_DIR:' + str(self.root_dir)
        str_log_dir = 'LOG_DIR:' + str(self.log_dir)
        str_email_log = 'EMAIL_LOG_FILE:' + str(self.email_log)
        str_grade_log = 'GRADE_LOG:' + str(self.grade_log)
        str_error_log = 'error_LOG_FILE:' + str(self.error_log)
        str_debug_log = 'debug_LOG_FILE:' + str(self.debug_log)
        str_compile_log = 'COMPILE_LOG_FILE:' + str(self.email_log)
        str_compiler = 'COMPILER:' + str(self.compiler)
        str_unzip = 'UNZIP:' + str(self.unzip)
        str_late_ratio = 'LATE_RATIO:' + str(self.late_ratio)
        str_late_message = 'LATE_MESSAGE:' + str(self.late_message)

        string_to_write = "\n".join([str_current_line, str_current_late_line, str_log_file, str_late_log_file, str_live_dir, str_out_file, str_semester, str_root_dir,
                                     str_log_dir, str_email_log, str_grade_log, str_error_log, str_debug_log, str_compile_log, str_compiler, str_unzip, str_late_ratio, str_late_message])

        self.file_object.write(string_to_write)

        self.file_object.close()

    # end write_file

    def __del__(self):
        self.write_file()

    # end __del__

    def __delete__(self, instance):
        self.write_file()

    # end __delete__

    def get_email_log(self):
        return self.root_dir + self.log_dir + self.semester + self.email_log

    def get_grade_log(self):
        return self.root_dir + self.log_dir + self.semester + self.grade_log

    def get_error_log(self):
        return self.root_dir + self.log_dir + self.semester + self.error_log

    def get_debug_log(self):
        return self.root_dir + self.log_dir + self.semester + self.debug_log

    def get_compile_log(self):
        return self.root_dir + self.log_dir + self.semester + self.compile_log


class LogFile(object):
    def __init__(self, file_name):
        self.file_path = file_name
        self.file_contents = []
        self.refresh()

    # end __init__

    def refresh(self):
        try:
            self.file_contents = list(open(self.file_path, 'r'))
            return 0
        except:
            self.file_contents = list()
            return -1

    # end refresh

    def get_line(self, index):
        if self.refresh() >= 0:
            return self.file_contents[index].split(',')
        else:
            return -1

    # end get_last_line

    def check_last_line(self, compare_index):
        if self.refresh() >= 0:
            if compare_index < len(self.file_contents):
                return len(self.file_contents)
            else:
                return 0
        return -1

    # end check_last_line
