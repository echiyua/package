#!/usr/bin/expect
#*************login_bury_trace_LTE_L3.sh************
set timeout 55
set moshell_ip [ lindex $argv 0 ]
#set command [ lindex $argv 1 ]
set moshell_version [ lindex $argv 1 ]
set command "te e all uehNwIfCtxtC
te e all uehNwIfBl_CtxtSwU
te e all Ft_CONN_COORD
te e all Ft_ENDC
te e all Ft_S1_X2_ENB_ID
te e all Ft_ENDC_SETUP
te e all Ft_INCOMING_HANDOVER
te e all Ft_OUTGOING_HANDOVER
te e all uehBearerBl_HandlingSwU
te e all Ft_UE_RAC_MEASUREMENTS
te e all uehRrcSigBl_CtxtSwU
te e all Ft_RRC_ASN
te e all Ft_S1AP_ASN
te e all Ft_X2AP_ASN
te e all uehMeasBl_CtxtSwU
te e all uehUeBl_SCellEvalSwU
te e all uehUeBl_CtxtSwU
te e all uehBearerBl_HandlingSwU
te e all Ft_ENDC_RELEASE
ue enable -allcell -allUe
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





