#!/usr/bin/expect

set dt [exec date "+%Y%m%d_%H.%M"]

spawn ssh echiyua@10.163.174.48
set timeout 1
expect "*yes/no*" { send "yes\r";exp_continue }
expect "*Password:*" {send "echiyua123!\r"}
expect "*:~>"
#set timeout 1
send "mkdir DU_${dt} && viewer -m 10.164.133.225 -r 10.163.174.48 > DU_${dt}/DU.log\r"
exec sleep 60
send "\003\r"
expect eof
