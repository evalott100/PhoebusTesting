#!/usr/bin/bash
point="/scratch/fye77278/Code/PhoebusTesting/settings.ini"
#export EPICS_CA_SERVER_PORT=6064
#export EPICS_CA_REPEATER_PORT=6065
module load java/11.0.15
/dls_sw/apps/phoebus/master/phoebus-product/phoebus.sh -settings $point "$@"

df -h
