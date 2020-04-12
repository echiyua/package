# encoding:utf-8
import os
import time
import threading
import ConfigParser
import re

script_dir = os.getcwd()
print ('script_dir:', script_dir)  # /tmp/publichome/grabtracetool/script_dir
decode_tool_dir = script_dir + r"/../decode_tool"  # /tmp/publichome/grabtracetool/decode_tool
log_dir = script_dir + r"/../log"  # /tmp/publichome/grabtracetool/log
configure_dir = script_dir + r"/../configure"
ltng_dir = decode_tool_dir + r"/ltng"
ltng_bin_dir = ltng_dir + r"/bin/ltng-decoder"
ltng_zip_dir = decode_tool_dir + r"/ltng.zip"

stp_control_ip = ""
stp_lte_control_ip = ""
stp_oam_ip = ""
log_server_ip = ""
NR_L3_trcae_category = ""
LTE_L3_trcae_category = ""
NR_BB_trcae_category = ""
RU_trcae_category = ""
moshell_version = ""
log_server_account = ""
log_server_password = ""
DU_length_time = ""
RU_length_time = ""
local_time = ""
keep_newest_logs_count = ""
keep_newest_logs_script_dir = script_dir + "/keep_newest_logs_script.py"
decode_file_dir = script_dir + "/traverse_decode_BB_trace.sh"
lock = threading.RLock()


def read_configure(configfile):
    global stp_control_ip, stp_lte_control_ip, stp_oam_ip, log_server_ip, NR_L3_trcae_category, LTE_L3_trcae_category, NR_BB_trcae_category, RU_trcae_category, moshell_version, DU_length_time, RU_length_time, \
        log_server_account, log_server_password, keep_newest_logs_count, DU_length_time
    try:
        conf = ConfigParser.SafeConfigParser()
        conf.read(configfile)
        stp_control_ip = conf.get('moshell_select', 'stp_control_ip').strip()
        stp_lte_control_ip = conf.get('moshell_select', 'stp_lte_control_ip').strip()
        stp_oam_ip = conf.get('moshell_select', 'stp_oam_ip').strip()
        log_server_ip = conf.get('moshell_select', 'log_server_ip').strip()
        NR_L3_trcae_category = conf.get('trace_category', 'NR_L3_trcae_category').strip()
        LTE_L3_trcae_category = conf.get('trace_category', 'LTE_L3_trcae_category').strip()
        NR_BB_trcae_category = conf.get('trace_category', 'NR_BB_trcae_category').strip()
        moshell_version = conf.get('moshell_version_dir', 'moshell_version').strip()
        log_server_account = conf.get('moshell_select', 'log_server_account').strip()
        log_server_password = conf.get('moshell_select', 'log_server_password').strip()
        DU_length_time = conf.get('moshell_select', 'DU_length_time').strip()
        keep_newest_logs_count = conf.get('moshell_select', 'keep_newest_logs_count').strip()
        DU_length_time = int(DU_length_time)

        print ('\nstp_control_ip:', stp_control_ip)
        print ('stp_oam_ip:', stp_oam_ip)
        print ('log_server_account:', log_server_account)
        print ('log_server_password:', log_server_password)
        print ('moshell_version:', moshell_version)
        print ('NR_L3_trcae_category:', NR_L3_trcae_category)
        print ('NR_BB_trcae_category:', NR_BB_trcae_category)
        print ('keep_newest_logs_script_dir:', keep_newest_logs_script_dir)
        print ('decode_file_dir:', decode_file_dir)
        print ('keep_newest_logs_count:', keep_newest_logs_count)
        print ('DU_length_time:', DU_length_time)
        print ('type(DU_length_time):', type(DU_length_time))
        print ('\n\n')

        command = r""
        arr = NR_BB_trcae_category.split(";")
        for i in arr:
            command = command + i.strip() + r"\n"
        command = r"bbte @N_R4_0 log reset\nmtd @N_R4_0 kill -all\n" + command
        print ('command:', command)
    except Exception as error:
        print ('error:', error)


class Grab():
    def __init__(self, stp_control_ip):
        self.stp_control_ip = stp_control_ip

    def grab_NR_L3(self):
        print  ('**************begin to grab_NR_L3****************')
        print ('NR_L3_trcae_category:',NR_L3_trcae_category)
        try:
            arr = NR_L3_trcae_category.split(";")
            print ('arr:', arr)
            command = r""
            for i in arr:
                command = command + i.strip() + "\n"
            print('\n*****************')
            print('command:', command)
            print('*****************\n\n')

            with open(script_dir + "/login_bury_trace_NR_L3.sh", 'r+') as f1:
                with open(script_dir + "/login_bury_trace_NR_L3_new.sh", 'w+') as f2:
                    lines = f1.read()
                    print lines
                    old_str = lines.split("\"")[1]
                    print ('old_str:', old_str)
                    lines = lines.replace(old_str, command)
                    print ('\n\n\n\n*********\nafter*******:\n', lines)
                    f2.write(lines)
                    f1.close()
                    f2.close()
                os.remove(script_dir + "/login_bury_trace_NR_L3.sh")
                os.system("cd " + script_dir + "&& mv login_bury_trace_NR_L3_new.sh login_bury_trace_NR_L3.sh")
                os.system("chmod 777 " + script_dir + "/login_bury_trace_NR_L3.sh")

            cmd1 = r"cd " + script_dir + r" && ./login_bury_trace_NR_L3.sh " + stp_control_ip + " " + moshell_version
            print ('\n\ngrab NR L3 cmd1:',cmd1)
            p = os.popen(cmd1)
            return_str = p.read()
            #os.system(cmd1)
            print ('\n\n**return_str:**\n',return_str)
            return_command = re.findall(r'\$moncommand =.+',return_str)
            print ('\n\nreturn_command:',return_command)
            result_command = return_command[0].strip().split("=")[1].strip()
            print ('\nafter split result_command:',result_command)

            log_dir_NR_L3 = log_dir + "/NR_L3/NR_L3_" + time.strftime("%Y-%m-%d_%H.%M", time.localtime())
            print ('log_dir_NR_L3:',log_dir_NR_L3)
            if not os.path.isdir(log_dir_NR_L3):
                os.makedirs(log_dir_NR_L3)
            result_command = result_command + r' \
                            | tee -a ' + log_dir_NR_L3 + r'/NR_L3.raw \
                            | ' + decode_tool_dir + r'/ltng/bin/ltng-decoder -s --3gpp 15.3 \
                            | tee ' + log_dir_NR_L3 + r'/NR_L3.dec \
                            | ' + decode_tool_dir + r'/ltng/bin/ltng-flow -s --3gpp 15.3 \
                            | tee ' + log_dir_NR_L3 + r'/NR_L3.fl'
            print ('\nafter slice result_coomand:',result_command)
            os.system(result_command)
        except Exception as error:
            print ('error:', error)

    #********************* grab trace in local server and saved in local log dir  ***********************
    def grab_LTE_L3(self):
        print ('**********begin to grab_LTE_L3********')
        command = r""
        print ('LTE_L3_trcae_category:',LTE_L3_trcae_category)
        try:
            arr = LTE_L3_trcae_category.split(";")
            for i in arr:
                command = command + i.strip() + "\n"
            print('\n*****************')
            print ('command:', command)
            print('*****************\n\n')

            with open(script_dir + "/login_bury_trace_LTE_L3.sh", 'r+') as f1:
                with open(script_dir + "/login_bury_trace_LTE_L3_new.sh", 'w+') as f2:
                    lines = f1.read()
                    print lines
                    old_str = lines.split("\"")[1]
                    print ('old_str:', old_str)
                    lines = lines.replace(old_str, command)
                    print ('\n\n\n\n*********8\nafter*******:\n', lines)
                    f2.write(lines)
                    f1.close()
                    f2.close()
                os.remove(script_dir + "/login_bury_trace_LTE_L3.sh")
                os.system("cd " + script_dir + "&& mv login_bury_trace_LTE_L3_new.sh login_bury_trace_LTE_L3.sh")
                os.system("chmod 777 " + script_dir + "/login_bury_trace_LTE_L3.sh")

            cmd1 = r"cd " + script_dir + r" && ./login_bury_trace_LTE_L3.sh " + stp_lte_control_ip + " " + moshell_version
            print ('\n*******grab LTE L3 cmd1:', cmd1)
            print ('**********\n')
            p = os.popen(cmd1)
            return_str = p.read()
            # os.system(cmd1)
            print ('\n\n**return_str:**\n', return_str)
            return_command = re.findall(r'\$moncommand =.+', return_str)
            print ('\n\nreturn_command:', return_command)
            result_command = return_command[0].strip().split("=")[1].strip()
            print ('\nafter split result_command:', result_command)

            log_dir_LTE_L3 = log_dir + "/LTE_L3/LTE_L3_" + time.strftime("%Y-%m-%d_%H.%M", time.localtime())
            print ('log_dir_LTEL3:', log_dir_LTE_L3)
            if not os.path.isdir(log_dir_LTE_L3):
                os.makedirs(log_dir_LTE_L3)
            result_command = result_command + r' \
                           | tee -a ' + log_dir_LTE_L3 + r'/LTE_L3.raw \
                           | ' + decode_tool_dir + r'/ltng/bin/ltng-decoder -s --3gpp 15.3 \
                           | tee ' + log_dir_LTE_L3 + r'/LTE_L3.dec \
                           | ' + decode_tool_dir + r'/ltng/bin/ltng-flow -s --3gpp 15.3 \
                           | tee ' + log_dir_LTE_L3 + r'/LTE_L3.fl'
            print ('\nafter slice result_coomand:', result_command)
            os.system(result_command)
        except Exception as error:
            print ('error:', error)

    def login_bury_BB_trace(self):
        print ('beging to grab NR BB')
        print ('NR_BB_trcae_category:', NR_BB_trcae_category)
        command = "bbte @N_R4_0 log reset\nmtd @N_R4_0 kill -all\n"
        try:
            arr = NR_BB_trcae_category.split(";")
            for i in arr:
                command = command + i.strip() + "\n"
            print('\n*****************')
            print ('command:', command)
            print('*****************\n')
            # update login_bury_BB_trace.sh file and acquire return command
            with open(script_dir + "/login_bury_BB_trace.sh", 'r+') as f1:
                with open(script_dir + "/login_bury_BB_trace_new.sh", 'w+') as f2:
                    lines = f1.read()
                    print lines
                    old_str = lines.split("\"")[1]
                    print ('old_str:', old_str)
                    lines = lines.replace(old_str, command)
                    print ('\n\n\n\n*********\nafter*******:\n', lines)
                    f2.write(lines)
                    f1.close()
                    f2.close()
                os.remove(script_dir + "/login_bury_BB_trace.sh")
                os.system("cd " + script_dir + "&& mv login_bury_BB_trace_new.sh login_bury_BB_trace.sh")
                os.system("chmod 777 " + script_dir + "/login_bury_BB_trace.sh")
            # begin to carry out login_bury_trace_NR_BB.sh to accomplish grab and decode trace in remote logserver
            cmd1 = "cd " + script_dir + r" && ./login_bury_BB_trace.sh " + stp_control_ip + " " + moshell_version + " " + log_server_ip
            print ('\n********grab NR BB cmd1:', cmd1)
            print ('**********\n')
            p = os.popen(cmd1)
            return_str = p.read()
            tu_trace = re.findall(r"coli>/fruacc/lhsh 000100 /diagm/(.+)", return_str)[0]
            print ('~~~~~tu_trace~~~~~',tu_trace)
            tu_trace_command = re.sub(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", log_server_ip, tu_trace, 0, flags=re.I)
            print ('~~~~~~tu_trace_command~~~~~',tu_trace_command)

            # update tu_BB_trace.sh file and excute this scripts
            with open(script_dir + "/tu_BB_trace.sh", 'r+') as f1:
                with open(script_dir + "/tu_BB_trace_new.sh", 'w+') as f2:
                    lines = f1.read()
                    print lines
                    old_str = lines.split("\"")[1]
                    print ('old_str:', old_str)
                    lines = lines.replace(old_str, command)
                    print ('\n\n\n\n*********\nafter*******:\n', lines)
                    f2.write(lines)
                    f1.close()
                    f2.close()
                os.remove(script_dir + "/tu_BB_trace.sh")
                os.system("cd " + script_dir + "&& mv tu_BB_trace_new.sh tu_BB_trace.sh")
                os.system("chmod 777 " + script_dir + "/tu_BB_trace.sh")
            cmd2 = "cd " + script_dir + r" && ./tu_BB_trace.sh " + stp_control_ip + " " + moshell_version
            print ('~~~~~~~~~~~~~~`cmd2~~~~~~~~~~~~~',cmd2)
            os.system(cmd2)
        except Exception as error:
            print ('error:', error)


    def grab_NR_BB(self):
        print ('**************begin to grab BB trace***************')
        try:
            cmd1 = "cd " + script_dir + r" && ./grab_BB_trace.sh " + log_server_ip + " " + log_server_account + " " + log_server_password + " " + stp_oam_ip + " " + str(
                DU_length_time) \
                   + " " + local_time
            print ('\n********grab NR BB cmd1:', cmd1)
            print ('**********\n')
            p = os.system(cmd1)
        except Exception as error:
            print ('error:', error)

    def rm_backup(self):
        print ('*****************begin to rm_backup*****************')
        print ('****************begin to login and scp scripts to remote log server******************')
        rm_path = r"~/DU_" + local_time
        cmd = r'cd ' + script_dir + "&& ./scp_scripts_to_logserver.sh " + log_server_ip + " " + log_server_account + " " + log_server_password + " " + \
              local_time + " " + keep_newest_logs_script_dir + " " + keep_newest_logs_count
        print ('cmd:', cmd)
        os.system(cmd)

    def stop_grab_trace(self):
        lock.acquire()
        c1.stop()
        c2.stop()
        k1.stop()
        lock.release()


    def decode_NR_BB_trace(self):
        print ('****************begin to decode NR BB tarce******************')
        cmd = r"cd " + script_dir + " && ./scp_decode_BB_trace.sh " + log_server_ip + " " + log_server_account + " " +\
              log_server_password + " " + local_time + " " + decode_file_dir
        print ('cmd:',cmd)
        os.system(cmd)


    def kill_all_process(self):
        lock.acquire()
        print('********************')
        os.system("ps aux|grep python")
        str1 = r"kill -s 9 `ps ef | grep grab_BB_trace.sh | awk '{print $1}'`"
        str2 = r"kill -s 9 `ps ef | grep python | awk '{print $1}'`"
        print ('str:', str1)
        os.system(str1)
        os.system(str2)
        os.system("ps aux|grep python")
        lock.release()


class keep_newest_logs(threading.Thread):

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        # super(Producer,self).__init__(self)
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()
        self.__running.set()

    def stop(self):
        self.__flag.set()
        self.__running.clear()

    def run(self):
        global count_screenshot, count_analyze, thread_start, each_test_path, local_time
        while self.__running.isSet():
            grab.rm_backup()
            # time.sleep(DU_length_time)
            # rm_paths = (r'C:\Users\echiyua\Desktop\test\test')
            # rm_backup(rm_paths, 1)


class collect1(threading.Thread):

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        # super(Producer,self).__init__(self)
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()
        self.__running.set()

    def stop(self):
        self.__flag.set()
        self.__running.clear()

    def run(self):
        global count_screenshot, count_analyze, thread_start, each_test_path, local_time
        while self.__running.isSet():
            self.__flag.wait()
            # for i in range(2):   #login need 2 s
            #     print '111 logging'
            #     time.sleep(1)
            # for i in range(10):      #grab need 10 s
            #     print '111 now grabing '
            #     time.sleep(1)
            # time.sleep(8)   #this time is waiting for 222 to grab
            print ('begin to collect 1111')
            # c1.resume()
            grab.grab_NR_BB()
            # c1.pause()
            time.sleep(DU_length_time - 2)


class collect2(threading.Thread):

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        # super(Producer,self).__init__(self)
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()
        self.__running.set()

    def stop(self):
        self.__flag.set()
        self.__running.clear()

    def run(self):
        global count_screenshot, count_analyze, thread_start, each_test_path
        while self.__running.isSet():
            self.__flag.wait()
            # for i in range(2):
            #     print '222n logging '
            #     time.sleep(1)
            # for i in range(10):
            #     print '222 now grabbing'
            #     time.sleep(1)
            # time.sleep(8)    #this time need to wait 1 to grab
            print ('begin to collect 2222')
            # c2.resume()
            grab.grab_NR_BB()
            # c2.pause()
            time.sleep(DU_length_time - 2)


if __name__ == '__main__':
    global local_time
    configfile = configure_dir + r"/config.ini"
    read_configure(configfile)
    grab = Grab(stp_control_ip)
    while 1:
        flag = raw_input("\033[0;32m\n***************************************************\n\n\033[0;31m \
    when you grab before, pls ensure your trace\n \
type and moshell ip in config.ini file and then\n \
input 1 or 2 or 3 or 4 or 5 to select which type trace you\n \
want to grab or decode, trace will be saved in this\n \
target directory(LTE_L3/NR_L3 will be saved in \n \
this moshell sever's log directory, DU trace will \n \
be saved in your logserver's home directory):\n \
        \n\n\n\033[0;36m1 grab and decode NR_L3\n2 grab and decode LTE_L3\n3 begin to bury BB trace(no using, please bury trace by yourself)\n4 grab NR_BB_trace\n5 stop grab BB trace and decode BB trace\n6 quit \
        \n\n\033[0;32m***************************************************\n\033[m")
        print ('\033[m')
        flag = str(flag)
        if flag == "1":
            try:
                grab.grab_NR_L3()
            except Exception as error:
                print ('\033[7;31mplease input number!\033[1;31;40m')
        if flag == "2":
            try:
                grab.grab_LTE_L3()
            except Exception as error:
                print ('\033[7;31mplease input number!\033[1;31;40m')
        if flag == "3":
            try:
                grab.login_bury_BB_trace()
            except Exception as error:
                print ('\033[7;31mplease input number!\033[1;31;40m')
        if flag == "4":
            try:
                c1 = collect1()
                c2 = collect2()
                k1 = keep_newest_logs()
                local_time = time.strftime("%Y-%m-%d_%H.%M", time.localtime())
                c1.start()
                time.sleep(DU_length_time)
                c2.start()
                k1.start()

            except Exception as error:
                print ('\033[7;31mplease input number!\033[1;31;40m')
        if flag == "5":
            try:
                grab.stop_grab_trace()
                lock.acquire()
                grab.decode_NR_BB_trace()
                lock.release()
            except Exception as error:
                print ('\033[7;31mplease input number!\033[1;31;40m')
        if flag == "6":
            grab.kill_all_process()
            break
    # grab.stop_grab_trace()
    print (
        '\033[0;32m*********************\n\n\033[0;36myou have already quit !\n\n\033[0;32m*********************\n\n\033[m')