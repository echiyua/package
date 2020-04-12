import os
import shutil
import argparse
import re

parser = argparse.ArgumentParser(description='Get some msci MISIDN basefile parameters.')
parser.add_argument('--local_time', type=str, required=True, help='record the time you begin to grab BB trace')
parser.add_argument('--newest_file_counts', type=str, required=True, help='record how many newest log file you want to backup')
args = parser.parse_args()
local_time = args.local_time
newest_file_counts = args.newest_file_counts


def rm_backup(rm_path, days):
    files_list = os.listdir(rm_path)
    list = []
    dict = {}
    for i in files_list:
        all_path = os.path.join(rm_path, i)
        ctime = os.path.getctime(all_path)
        dict[all_path] = ctime
    print 'before sort , dict:',dict
    AllPathCtimeList = sorted(dict.items(), key=lambda item: item[1])   #low-high
    print 'type(AllPathCtimeList):',type(AllPathCtimeList)
    print 'after sort AllPathCtimeList:',AllPathCtimeList
    if len(AllPathCtimeList) <= days:
        print 'len(AllPathCtimeList):', len(AllPathCtimeList)
        print 'days:',days
        print 'xiaoyu' 
        pass
    else:
        for i in range(len(AllPathCtimeList) - days):  #keep newest days dir
            print 'AllPathCtimeList[i][0]:',AllPathCtimeList[i][0]
            os.remove(AllPathCtimeList[i][0])
            print 'dayu'



if __name__ == '__main__':
    str = r'cd ~ && pwd'
    s = os.popen(str)
    home_dir = re.findall(r'.+',s.read())[0]
    print ('type(home):',type(home_dir))
    print home_dir
    rm_paths = home_dir + '/DU_' + local_time  + "/"
    print 'local_time:',local_time
    print 'rm_paths:',rm_paths
    rm_backup(rm_paths, int(newest_file_counts))


#-----------------------------delete file null dir ,not null dirs----------------------------
# import os
# import shutil
#
# os.remove(r'C:\Users\echiyua\Desktop\test\test\test11\11.txt')  #delete file
# shutil.rmtree(r'C:\Users\echiyua\Desktop\test\test\test22')    #delete not null dir
# os.removedirs(r'C:\Users\echiyua\Desktop\test\test\aa')   #delete null dirs

