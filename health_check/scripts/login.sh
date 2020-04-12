#!/usr/bin/expect
set timeout 69
set moshell_ip [ lindex $argv 0 ]

#spawn moshell $moshell_ip
spawn /usr/local/moshell/moshell $moshell_ip

expect "$moshell_ip"
send "lt all\n"


expect "*Username:"
send "muser\n"

expect "*Password:"
send "muser\n"


expect "Last MO:"
send "cvcu\n"

expect "BrmFailSafe:"
#send "pget NRCellDU pmRadioP.*McsDistr|pmRadioUeRepCqi*|pmRadioUeRepRankDistr|pmRadioSinr*|pmRadioRecInterferencePwrDistr|pmRadioRaAttTaDistr\n"
send "pget .  pmRadioRecInterferencePwrDistr\r"

expect "Total:"
send "exit\n"

expect eof

