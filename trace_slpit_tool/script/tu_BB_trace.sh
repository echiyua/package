#!/usr/bin/expect
#*************login_bury_trace_NR_BB.sh************

set timeout 35
set stp_control_ip [ lindex $argv 0 ]
set moshell_version [ lindex $argv 1 ]

set command "bbte log setdest bbEqm000004 --buffer emca --ip ManagedElement=1,Transport=1,Router=OAM,InterfaceIPv4=OAM,AddressIPv4=OAM 10.163.174.12 33079 -bitrate 200000"

spawn $moshell_version $stp_control_ip

expect "Checking ip contact...OK"
send "lt all\n"

expect "*Username:"
send "muser\n"

expect "*Password:"
send "muser\n"

expect "coli>"
send "monu-\r"

expect "coli>"
send "${command}\r"
expect eof