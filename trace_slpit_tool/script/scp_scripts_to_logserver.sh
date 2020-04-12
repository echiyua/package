#!/usr/bin/expect

#*********scp keep_newest_fils.py******
set log_server_ip [ lindex $argv 0 ]
set log_server_account [ lindex $argv 1 ]
set log_server_password [ lindex $argv 2 ]
set local_time [ lindex $argv 3 ]
set keep_newest_logs_script_dir [ lindex $argv 4 ]
set keep_newest_logs_count [ lindex $argv 5 ]



#spawn scp -r $keep_newest_logs_script_dir $log_server_account@$log_server_ip:~/DU_${local_time}
spawn scp -r $keep_newest_logs_script_dir $log_server_account@$log_server_ip:~/
set timeout 2
expect "*yes/no*" { send "yes\r";exp_continue }
expect "*Password:*" { send "$log_server_password\r" }
expect "100%*"
expect eof


spawn ssh $log_server_account@$log_server_ip
expect "*yes/no*" { send "yes\r";exp_continue }
expect "*Password:*" {send "$log_server_password\r"}

expect "*:~>"  #DU_2019-11-22_17.31
#send "cd ~/DU_${local_time} && python keep_newest_logs_script.py --local_time=${local_time} --newest_file_counts=${keep_newest_logs_count}\r"
send "cd ~ && nohup python keep_newest_logs_script.py --local_time=${local_time} --newest_file_counts=${keep_newest_logs_count} &\r"
exec sleep 3
expect eof



