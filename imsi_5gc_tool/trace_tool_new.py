#encoding:utf-8
import time
import os
import re
import configparser as ConfigParser
import subprocess

script_dir = os.getcwd()
print ('script_dir:',script_dir)   #/tmp/publichome/grabtracetool/script_dir
decode_tool_dir = script_dir + r"/../decode_tool"  #/tmp/publichome/grabtracetool/decode_tool
log_dir = script_dir + r"/../log"  #/tmp/publichome/grabtracetool/log
configure_dir = script_dir + r"/../configure"
ltng_dir = decode_tool_dir +r"/ltng"
ltng_bin_dir = ltng_dir + r"/bin/ltng-decoder"
ltng_zip_dir = decode_tool_dir + r"/ltng.zip"


stp_control_ip = ""
stp_oam_ip = ""
log_server_ip = ""
NR_L3_trcae_category =  ""
LTE_L3_trcae_category =  ""
NR_BB_trcae_category =  ""
RU_trcae_category=""
moshell_version = ""
log_server_account = ""
log_server_password = ""

def read_configure(configfile):
    global stp_control_ip, stp_oam_ip, log_server_ip, NR_L3_trcae_category, LTE_L3_trcae_category, NR_BB_trcae_category,RU_trcae_category ,moshell_version, \
        log_server_account, log_server_password
    try:
        conf = ConfigParser.SafeConfigParser()
        conf.read(configfile)
        stp_control_ip = conf.get('moshell_select', 'stp_control_ip')
        stp_oam_ip = conf.get('moshell_select', 'stp_oam_ip')
        log_server_ip = conf.get('moshell_select', 'log_server_ip')
        NR_L3_trcae_category = conf.get('trace_category', 'NR_L3_trcae_category')
        LTE_L3_trcae_category = conf.get('trace_category', 'LTE_L3_trcae_category')
        NR_BB_trcae_category = conf.get('trace_category', 'NR_BB_trcae_category')
        RU_trcae_category = conf.get('trace_category', 'RU_trcae_category')
        moshell_version = conf.get('moshell_version_dir', 'moshell_version')
        log_server_account = conf.get('moshell_select', 'log_server_account')
        log_server_password = conf.get('moshell_select', 'log_server_password')
        print ('\nstp_control_ip:', stp_control_ip)
        print ('stp_oam_ip:', stp_oam_ip)
        print ('log_server_account:', log_server_account)
        print ('log_server_password:', log_server_password)
        print ('moshell_version:', moshell_version)
        print ('NR_L3_trcae_category:', NR_L3_trcae_category)
        print ('LTE_L3_trcae_category:', LTE_L3_trcae_category)
        print ('NR_BB_trcae_category:', NR_BB_trcae_category)
        print ('RU_trcae_category:', RU_trcae_category)
        print ('\n\n')

        command = r""
        arr = NR_BB_trcae_category.split(";")
        for i in arr:
            command = command + i.strip() + r"\n"
        command = r"bbte @N_R4_0 log reset\nmtd @N_R4_0 kill -all\n" + command
        print ('command:', command)
    except Exception as error:
            print ('error:', error)

def check_moshell_version():
    global moshell_version
    print ('script_dir:',script_dir)
    p = os.popen("cd " + script_dir + " && ./check_moshell.sh")
    str = p.read()
    print ('\n\n!!!!!!!!!!!!!!!!!!!!!!!!')
    print ('str:',str)
    print ('!!!!!!!!!!!!!!!!!!!!!!!!\n\n')
    moshell_version = str.split(":")[0]
    print ('\n\n**********')
    print ('moshell_version:',moshell_version)
    print ('**********\n\n')


class Grab():
    def __init__(self, stp_control_ip):
        self.stp_control_ip = stp_control_ip

    def create_check_dir(self):
        print ('begin to create_check_dir')
        if not os.path.exists(decode_tool_dir):
            print ('decode_tool_dir not exist and will make')
            os.makedirs(decode_tool_dir)
        if not os.path.exists(log_dir):
            print ('log_dir not exist and will make')
            os.makedirs(log_dir)
        if not os.path.exists(configure_dir):
            print ('configure_dir not exist and will make')
            os.makedirs(configure_dir)
        print ('decode_tool_dir:',decode_tool_dir)
        print ('log_dir:', log_dir)
        print ('configure_dir:', configure_dir)

    def acquire_ltng_tool(self):
        print ('begin to acquire_ltng_tool')
        print ('decode_tool_dir:',decode_tool_dir)
        if os.path.exists(ltng_dir) and os.path.isfile(ltng_bin_dir):
            cmd1 = r"cd " + decode_tool_dir + r" && chmod -R 777 ltng"
            os.system(cmd1)
        elif os.path.isfile(ltng_zip_dir):
            cmd2 = r"unzip " + ltng_zip_dir + r" -d " + decode_tool_dir
            os.system(cmd2)
            cmd3 = r"cd " + decode_tool_dir + r" && chmod -R 777 ltng"
            os.system(cmd3)
        else:
            cmd4 = r"cd " + script_dir + r" && ./get_tng.sh && unzip " + ltng_zip_dir + r" -d " + decode_tool_dir
            os.system(cmd4)
            cmd5 = r"cd " + decode_tool_dir + r" && chmod -R 777 ltng"
            os.system(cmd5)

    # ********************* grab trace in local server and saved in local log dir  ***********************
    def grab_NR_L3(self):
        print ('begin to grab_NR_L3')
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
                    print (lines)
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
        print ('begin to grab_LTE_L3')
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
                    print (lines)
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

            cmd1 = r"cd " + script_dir + r" && ./login_bury_trace_LTE_L3.sh " + stp_control_ip + " " + moshell_version
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

    # ********************* grab trace in local server and saved in local log dir  ***********************
    # def grab_NR_BB(self):
    #     print 'beging to grab NR BB'
    #     print 'NR_BB_trcae_category:',NR_BB_trcae_category
    #     command = "bbte @N_R4_0 log reset\nmtd @N_R4_0 kill -all\n"
    #     try:
    #         arr = NR_BB_trcae_category.split(";")
    #         for i in arr:
    #             command = command + i.strip() + "\n"
    #         print('\n*****************')
    #         print 'command:', command
    #         print('*****************\n')
    #
    #         with open(script_dir + "/login_bury_trace_NR_BB.sh", 'r+') as f1:
    #             with open(script_dir + "/login_bury_trace_NR_BB_new.sh", 'w+') as f2:
    #                 lines = f1.read()
    #                 print lines
    #                 old_str = lines.split("\"")[1]
    #                 print 'old_str:', old_str
    #                 lines = lines.replace(old_str, command)
    #                 print '\n\n\n\n*********8\nafter*******:\n', lines
    #                 f2.write(lines)
    #                 f1.close()
    #                 f2.close()
    #             os.remove(script_dir + "/login_bury_trace_NR_BB.sh")
    #             os.system("cd " + script_dir + "&& mv login_bury_trace_NR_BB_new.sh login_bury_trace_NR_BB.sh")
    #             os.system("chmod 777 " + script_dir + "/login_bury_trace_NR_BB.sh")
    #
    #         cmd1 = "cd " + script_dir + r" && ./login_bury_trace_NR_BB.sh " + stp_control_ip + " " + moshell_version
    #         print '\n********grab NR BB cmd1:', cmd1
    #         print '**********\n'
    #         p = os.popen(cmd1)
    #         return_str = p.read()
    #         if 'fail' in return_str.lower():
    #             print 'bury trace fail, please bury trace again'
    #         else:
    #             print 'bury trace OK'
    #             # os.system(cmd1)
    #             print '\n**return_str:**', return_str
    #             return_command = re.findall(r'\$moncommand =.+', return_str)
    #             print '\nreturn_command:', return_command
    #             result_command = return_command[0].strip().split("=")[1].strip()
    #             print '\nafter split result_command:', result_command
    #
    #             log_dir_NR_BB = log_dir + "/NR_BB/NR_BB_" + time.strftime("%Y-%m-%d_%H.%M", time.localtime())
    #             print 'log_dir_NR_BB:', log_dir_NR_BB
    #             if not os.path.isdir(log_dir_NR_BB):
    #                 os.makedirs(log_dir_NR_BB)
    #             result_command = result_command + r' \
    #                            | tee ' + log_dir_NR_BB + r'/NR_BB.log'
    #             print 'after slice result_coomand:', result_command
    #             os.system(result_command)
    #     except Exception as error:
    #         print 'error:',error

    #*********************   grab and decode trace in remote logserver and decode  **********************8
    def grab_NR_BB(self):
        print ('beging to grab NR BB')
        print ('NR_BB_trcae_category:',NR_BB_trcae_category)
        command = "bbte @N_R4_0 log reset\nmtd @N_R4_0 kill -all\n"
        try:
            arr = NR_BB_trcae_category.split(";")
            for i in arr:
                command = command + i.strip() + "\n"
            print('\n*****************')
            print ('command:', command)
            print('*****************\n')
            #update login_bury_trace_NR_BB.sh file
            with open(script_dir + "/login_bury_trace_NR_BB.sh", 'r+') as f1:
                with open(script_dir + "/login_bury_trace_NR_BB_new.sh", 'w+') as f2:
                    lines = f1.read()
                    print (lines)
                    old_str = lines.split("\"")[3]
                    print ('old_str:', old_str)
                    lines = lines.replace(old_str, command)
                    print ('\n\n\n\n*********8\nafter*******:\n', lines)
                    f2.write(lines)
                    f1.close()
                    f2.close()
                os.remove(script_dir + "/login_bury_trace_NR_BB.sh")
                os.system("cd " + script_dir + "&& mv login_bury_trace_NR_BB_new.sh login_bury_trace_NR_BB.sh")
                os.system("chmod 777 " + script_dir + "/login_bury_trace_NR_BB.sh")
            #begin to carry out login_bury_trace_NR_BB.sh to accomplish grab and decode trace in remote logserver
            cmd1 = "cd " + script_dir + r" && ./login_bury_trace_NR_BB.sh " + stp_control_ip + " " + moshell_version + " " + log_server_ip + \
                " " + log_server_account + " " + log_server_password + " " + stp_oam_ip
            print ('\n********grab NR BB cmd1:', cmd1)
            print ('**********\n')
            p = os.system(cmd1)
        except Exception as error:
            print ('error:',error)


    #*******************   grab trace in local server and scp to remote logserver and decode in remote logserver**********************
    def grab_RU(self):
        print ('begin to grab_RU')
        print ('RU_trcae_category:',RU_trcae_category)
        command = "lhsh fru_2048 mtd @5EXRAT_RBLM1_0 kill -all\nlhsh fru_2048 bbte @5EXRAT_RBLM1_0 log reset\n"
        try:
            arr = RU_trcae_category.split(";")
            for i in arr:
                command = command + i.strip() + "\n"
            print('\n*****************')
            print ('command:', command)
            print('*****************\n')
            #********************  update login_bury_trace_RU.sh's  command ******************
            with open(script_dir + "/login_bury_trace_RU.sh", 'r+') as f1:
                with open(script_dir + "/login_bury_trace_RU.sh_new.sh", 'w+') as f2:
                    lines = f1.read()
                    print (lines)
                    old_str = lines.split("\"")[1]
                    # old_str1 = lines.split("\"")[3]
                    print ('old_str:', old_str)
                    lines = lines.replace(old_str, command)
                    print ('\n\n\n\n*********\nafter*******:\n', lines)
                    f2.write(lines)
                    f1.close()
                    f2.close()
                os.remove(script_dir + "/login_bury_trace_RU.sh")
                os.system("cd " + script_dir + "&& mv login_bury_trace_RU.sh_new.sh login_bury_trace_RU.sh")
                os.system("chmod 777 " + script_dir + "/login_bury_trace_RU.sh")

            remote_RU_dir = "RU_" + time.strftime("%Y-%m-%d_%H.%M", time.localtime())  # RU_2019-09-12_09.27.57
            ru_log_dir = log_dir + "/RU/" + remote_RU_dir  # /tmp/publichome/grabtracetool/log/RU/RU_2019-09-12_09.27.57
            print ('\nru_log_dir:', ru_log_dir)
            if not os.path.isdir(ru_log_dir):
                os.makedirs(ru_log_dir)
            ru_log_file = ru_log_dir + r"/RU.log"
            # ********************  begin to carry out login_bury_trace_RU.sh command: grab trace ******************
            cmd1 = "cd " + script_dir + r" && ./login_bury_trace_RU.sh " + stp_control_ip + " " + moshell_version + " " +  ru_log_file
            print ('\n********grab RU cmd1:', cmd1)
            print ('**********\n')
            os.system(cmd1)

            cmd2 = "cd " + script_dir + r" && ./ScpRemoteDecode_Ru.sh " + log_server_ip + " " +  log_server_account + " " + log_server_password + " "\
                   + ru_log_dir + " " + remote_RU_dir
            print ('\n\n****************')
            print ('cmd2:',cmd2)
            print ('****************\n\n')
            os.system(cmd2)
        except Exception as error:
            print ('error:', error)

    def scpFileToRemoteNode(user, ip, password, fileName, filePath, port=22):
        '''
        æ‹·è´è½¯ä»¶åŒ…åˆ°è¿œç¨‹èŠ‚ç‚¹ï¼Œé»˜è®¤ä½¿ç”¨rootç”¨æˆ·22å·ç«¯å£ä¼ è¾“
        :param ip:
        :param password:
        :param sourceFileName:
        :return: 0 è¡¨ç¤ºæ‰§è¡ŒæˆåŠŸ
        '''
        SCP_CMD_BASE = r"""
                expect -c "
                set timeout 2 ; 
                spawn scp -r {username}@{host}:{filePath}/{{filename}} ./  ;
                expect *yes/no* {{{{ send "yes\r"; exp_continue }}}}  ;
                expect *assword* {{{{ send {password}\r }}}}  ;
                expect *\r ;
                expect \r ;
                expect eof
                "
        """.format(username=user, password=password, host=ip, filePath=filePath, port=port)
        SCP_CMD = SCP_CMD_BASE.format(filename=fileName)
        print ("execute SCP_CMD:  ", SCP_CMD)
        p = subprocess.Popen(SCP_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        # status = os.system(SCP_CMD)
        print ("execute SCP_CMD status: ", output)
        return output


if __name__ == '__main__':
    configfile = configure_dir + r"/config.ini"
    #check_moshell_version()
    # moshell_version = check_moshell_version()
    # configfile = r"C:\Users\echiyua\Desktop\config.ini"
    read_configure(configfile)
    grab = Grab(stp_control_ip)
    while 1:
        flag = input("\033[0;32m***************************************************\n\n\033[0;31m \
    when you grab before, pls ensure your trace\n \
type and moshell ip in config.ini file and then\n \
input 1 or 2 or 3 or 4 to select which type trace you\n \
want to grab or decode, trace will be saved in this\n \
target directory(LTE_L3/NR_L3 will be saved in \n \
this moshell sever's log directory, DU/RU trace will \n \
be saved in your logserver's home directory):\n \
        \n\n\n\033[0;36m1 grab and decode NR_L3\n2 grab and decode LTE_L3\n3 grab and decode NR_BB_trace\n4 grab and decode RU\n5 quit \
        \n\n\033[0;32m***************************************************\n")
        print ('\033[m')
        flag = str(flag)
        if flag == "1":
            try:
                grab.grab_NR_L3()
            except Exception as error:
                print ('\033[7;31m?????!\033[1;31;40m')
        if flag == "2":
            try:
                grab.grab_LTE_L3()
            except Exception as error:
                print ('\033[7;31m?????!\033[1;31;40m')
        if flag == "3":
            try:
                grab.grab_NR_BB()
            except Exception as error:
                print ('\033[7;31m?????!\033[1;31;40m')
        if flag == "4":
            try:
                grab.grab_RU()
                grab.scpFileToRemoteNode()
            except Exception as error:
                print ('\033[7;31m?????!\033[1;31;40m')
        if flag == "5":
            break
    print ('\033[0;32m*********************\n\n\033[0;36myou have already quit !\n\n\033[0;32m*********************\n\n\033[m')


