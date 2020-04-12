#!/usr/bin/expect
#*************login_bury_trace_NR_BB.sh************

set timeout 45
set stp_control_ip [ lindex $argv 0 ]
set moshell_version [ lindex $argv 1 ]
set log_server_ip [ lindex $argv 2 ]
set command "bbte @N_R4_0 log reset
mtd @N_R4_0 kill -all
bbte @N_R4_0 log enable bbEqm000004 NR_UPC_golden_traces
"

spawn $moshell_version $stp_control_ip

expect "Checking ip contact...OK"
send "lt all\n"

expect "*Username:"
send "muser\n"

expect "*Password:"
send "muser\n"


expect "Last MO:"
send "${command}\n"

expect "*ok"
exec sleep 3
send "monu all\n"
expect eof