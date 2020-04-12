#coding:utf-8
import os
import time
import re

# moshell_list = ["10.164.133.81"]
# moshell_list = ["10.164.133.95", "10.164.133.84", "10.164.133.107", "10.164.133.95"]

# moshell_list = ['10.170.32.169', '10.170.32.175', '10.170.32.176', '10.170.32.178', '10.170.32.179', '10.170.32.180',
#                '10.164.133.12', '10.164.133.14', '10.164.133.16', '10.164.133.18', '10.164.133.20', '10.164.133.25',
#                '10.164.133.26', '10.164.133.33', '10.164.133.34', '10.164.133.36', '10.164.133.44', '10.164.133.46',
#                '10.164.133.52', '10.164.133.58', '10.164.133.59', '10.164.133.61', '10.164.133.63', '10.164.133.64',
#                '10.164.133.65', '10.164.133.66', '10.164.133.69', '10.164.133.75', '10.164.133.79', '10.164.133.85',
#                '10.164.133.86', '10.164.133.87', '10.164.133.92', '10.164.133.93', '10.164.133.95', '10.164.133.97',
#                '10.164.133.99', '10.164.133.100', '10.164.133.101', '10.164.133.105', '10.164.133.107',
#                '10.164.133.108', '10.164.133.110', '10.164.133.113', '10.164.133.114', '10.164.133.115',
#                '10.164.133.116', '10.164.133.120', '10.164.133.123', '10.164.133.124', '10.166.184.12',
#                '10.166.184.13', '10.166.184.15', '10.166.184.16', '10.166.184.17', '10.166.184.20', '10.166.184.21',
#                '10.166.184.22', '10.166.184.23', '10.166.184.26', '10.166.184.27', '10.166.184.29', '10.166.184.30',
#                '10.166.184.33', '10.166.184.35', '10.166.184.37', '10.166.184.38', '10.166.184.42', '10.166.184.44',
#                '10.166.184.46', '10.166.184.47', '10.166.184.48', '10.166.184.49', '10.166.184.50', '10.166.184.51',
#                '10.166.184.52', '10.166.184.54', '10.166.184.56', '10.166.184.58', '10.166.184.60']


##         ----------when debugging use following code-------
# moshell_list = []
# localDir = os.getcwd()
# Date = str(time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime()))
# ss = r"mkdir ./../log/" + Date
# os.system(ss)
# file1 = localDir + r"/../" + r"log/" + Date + r"/" + r"result.txt"
# file2 = localDir + r"/../" + r"log/" + Date + r"/" + r"serous_result.txt"
# moshellfile = localDir + r"/../" + r"configure/" + r"moshell_ip.txt"


infomation = ["N+I less than or equals to -121","-121 less than N+I less than or equals to -120","-120 less than N+I less than or equals to -119",
        " -119 less than N+I less than or equals to -118","-118 less than N+I less than or equals to -117","-117 less than N+I less than or equals to -116",
        "-116 less than N+I less than or equals to -115","-115 less than N+I less than or equals to -114"," -114less than N+I less than or equals to -113",
        "-113 less than N+I less than or equals to -112","-112 less than N+I less than or equals to -108","-108 less than N+I less than or equals to -104",
        " UL Interference power is more than -104dbm","UL Interference power is more than -100dbm","UL Interference power is more than -96dbm",
        "UL Interference power is more than -92dbm"]

#         w----------hen trigging time to run use absolute dir-----------
moshell_list = []
localDir = os.getcwd()
Date = str(time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime()))
ss = r"mkdir -p /tmp/echiyua/log/" + Date
os.system(ss)
file1 = r"/tmp/echiyua/log/" + Date + "/result.txt"
file2 = r"/tmp/echiyua/log/" + Date + "/no_param_result.txt"
file3 = r"/tmp/echiyua/log/" + Date + "/serious_result.txt"
moshellfile = r"/tmp/echiyua/" + r"configure/" + r"moshell_ip_bak.txt"


def readfile():
    try:
        with open(moshellfile, 'r') as ff:
            lines = ff.readlines()
            for line in lines:
                line = line.strip()
                moshell_list.append(line)
    except Exception as error:
        print error
    finally:
        ff.close()
    print 'moshell_list:', moshell_list


def analysis(result, version_result, moshell):
    print 'begin to analysis'
    global file1, file2, file3
    line_later = result.split("=")[1]
    print 'line_later', line_later
    str = re.findall('\d+.*\d+', line_later)
    # ['0 0 0 0 0 0 0 48000 0 0 0 0 0 0 0 0']
    print 'str:', str
    pmRadioUeRepCqi256QamRank1Distr = str[0].split(" ")
    print 'pmRadioUeRepCqi256QamRank1Distr[12]:', pmRadioUeRepCqi256QamRank1Distr[12]
    print 'pmRadioUeRepCqi256QamRank1Distr[12]:', pmRadioUeRepCqi256QamRank1Distr[12]
    print 'pmRadioUeRepCqi256QamRank1Distr[13]:', pmRadioUeRepCqi256QamRank1Distr[13]
    print 'pmRadioUeRepCqi256QamRank1Distr[14]:', pmRadioUeRepCqi256QamRank1Distr[14]
    print 'pmRadioUeRepCqi256QamRank1Distr[15]:', pmRadioUeRepCqi256QamRank1Distr[15]
    if int(pmRadioUeRepCqi256QamRank1Distr[12]) > 20 or int(pmRadioUeRepCqi256QamRank1Distr[13]) or int(pmRadioUeRepCqi256QamRank1Distr[14]) \
            or int(pmRadioUeRepCqi256QamRank1Distr[15]):
        try:
            with open(file3, "a+") as f3:
                string = "FATAL:moshell:%s\t%s\t" % (moshell,version_result)
                if int(pmRadioUeRepCqi256QamRank1Distr[15]):
                    string = string + "%s" % (infomation[15])
                elif int(pmRadioUeRepCqi256QamRank1Distr[14]):
                    string = string + "%s" % (infomation[14])
                elif int(pmRadioUeRepCqi256QamRank1Distr[13]):
                    string = string + "%s" % (infomation[13])
                elif int(pmRadioUeRepCqi256QamRank1Distr[12]) > 20:
                    string = string + "%s" % (infomation[12])
                string = string + "\t%s\n" %(result)
                f3.write(string)
        except Exception as error:
            print 'error in open file in %s' % (time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime()))
            print error
        finally:
            f3.close()
    else:
        print 'pmRadioUeRepCqi256QamRank1Distr is in range'
        

def recordAll(moshell, status_list, result_list):
    print 'begin to recordAll'
    try:
        # status_list = [isConnect,isHaveVersion,isHaveTargetParam]
        # result_list = [regex2,result]
        print 'status_list:',status_list
        print 'result_list:',result_list
        print 'result_list[0]:',result_list[0]
        with open(file1, "a+") as f1:
            if not status_list[0]:
                str0 = "moshell:%s\tconnected FAIL!\n" %(moshell)
                f1.write(str0)
            else:
                if status_list[1] and status_list[2]:  # have version and para
                    str1 = "moshell:%s\t%s\t%s\n" % (moshell, result_list[0], result_list[1])
                    f1.write(str1)
                if status_list[1] and not status_list[2]:  # have version but no para
                    str2 = "moshell:%s\t%s\t%s\n" % (moshell, result_list[0], result_list[1])
                    f1.write(str2)
                    with open(file2, "a+") as ff:
                        ff.write(str2)
                    ff.close()
                if not status_list[1] and status_list[2]:  # have no version but have para
                    str3 = "moshell:%s\t%s\t%s\n" % (moshell, result_list[0], result_list[1])
                    f1.write(str3)
                if not status_list[1] and not status_list[2]:  # have no version and no para
                    str4 = "moshell:%s\t%s\t%s\n" % (moshell,result_list[0],result_list[1])
                    f1.write(str4)
                    with open(file2, "a+") as ff:
                        ff.write(str4)
                    ff.close()
    except Exception as error:
        print 'error in open file in %s' % (time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime()))
        print error
    finally:
        f1.close()


def monitor(moshell_list):
    for moshell in moshell_list:
        try:
            # set every moshell is safe
            haspParam = 0
            result = ""
            isConnect = 0
            isHaveTargetParam = 0
            isHaveVersion = 0
            result_list = [0,0]
            version_result = "no version"
            interface_result = "have no target parameter"
            command = r'cd /tmp/echiyua/scripts/ && ./login.sh ' + moshell
            print 'command:', command
            print '*********************\n********************\n'
            p = os.popen(command)
            print 'type(p)', type(p)
            # return type is string
            return_string = p.read()
            print 'return_string:',return_string
            if r"Connected to" in return_string and "Checking ip contact...OK" in return_string:
                print '~~~~~~~~~~~~~~~~'
                isConnect = 1
                if r"Current SwVersion:" in return_string:
                    print '********************'
                    isHaveVersion = 1
                    regex1 = re.findall(r"Current SwVersion:.+.+", return_string)
                    print 'regex1:',regex1
                    if len(regex1) != 0:
                        print '??????????????????'
                        # regex2 = re.findall(r"CX.+", regex1[0])
                        try:
                            regex2 = regex1[0].strip().split(":")[1]
                            print 'before regex2:', regex2
                            regex2 = regex2.strip()
                            print 'after regex2:', regex2
                            version_result = regex2
                        except Exception as error:
                            print error
                        finally:
                            print 'version_result:',version_result
                if r"pmRadioRecInterferencePwrDistr l[16]" in return_string:
                    print '!!!!!!!!!!!!!!!!!!!!'
                    isHaveTargetParam = 1
                    pa = re.findall(r"pmRadioRecInterferencePwrDistr.l\[.+\d+", return_string)
                    if len(pa) != 0:
                        result = pa[0]
                        # result: pmRadioRecInterferencePwrDistr l[16] = 0 0 0 0 0 0 0 1736000 0 0 0 0 0 0 0 0
                        print 'result:', result
                        analysis(result, version_result, moshell)
                        interface_result = result
                    else:
                        print 'have pmRadioUeRepCqi256QamRank1Distr but no result'
            else:
                if "Cannot connect to MO server, exiting.. ":
                    print 'can not connect to moshell:%s' %(moshell)
                else:
                    print 'another situations'
            status_list = [isConnect,isHaveVersion,isHaveTargetParam]
            result_list = [version_result,interface_result]
            recordAll(moshell, status_list, result_list)
        except Exception as error:
            print 'check Fail in moshell:%s' % (moshell)
            print error

if __name__ == '__main__':
    readfile()
    #moshell_list = ["10.164.133.95","10.164.133.84","10.164.133.105","10.164.133.104","10.164.133.95","10.166.133.95"]
    #moshell_list = ["10.164.133.95","10.164.133.84"]
    monitor(moshell_list)




