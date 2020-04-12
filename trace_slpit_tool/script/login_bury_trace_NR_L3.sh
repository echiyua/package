#!/usr/bin/expect
#*************login_bury_trace_NR_L3.sh************
set timeout 47
set moshell_ip [ lindex $argv 0 ]
set moshell_version [ lindex $argv 1 ]
#set command [ lindex $argv 1 ]
set command "te e * com_ericsson_rc_cell_nr
te e * com_ericsson_rc_cell_nr_handler
te e * com_ericsson_rc_cell_nr_manager
"

#spawn moshell $moshell_ip
#spawn /usr/local/moshell/moshell $moshell_ip
spawn $moshell_version $moshell_ip
#spawn moshell 10.170.32.178

expect "Checking ip contact...OK"
send "lt all\n"


expect "*Username:"
send "muser\n"

expect "*Password:"
send "muser\n"


expect "Last MO:"
send $command

send "mon-\n"
send "mon\n"
send "exit\n"
expect eof






