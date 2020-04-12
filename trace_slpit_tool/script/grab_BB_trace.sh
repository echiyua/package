#!/usr/bin/expect

set log_server_ip [ lindex $argv 0 ]
set log_server_account [ lindex $argv 1 ]
set log_server_password [ lindex $argv 2 ]
set stp_oam_ip [ lindex $argv 3 ]
set DU_length_time [ lindex $argv 4 ]
set local_time [ lindex $argv 5]
set dt [exec date "+%Y%m%d_%H.%M"]


spawn ssh ${log_server_account}@${log_server_ip}
set timeout 1
expect "*yes/no*" { send "yes\r";exp_continue }
expect "*Password:*" {send "${log_server_password}\r"}
expect "*:~>"
#set timeout 1
send "mkdir -p DU_${local_time} && viewer -m ${stp_oam_ip} -r ${log_server_ip} > DU_${local_time}/DU_${dt}.log\r"
exec sleep ${DU_length_time}
send "\003\r"
expect eof


