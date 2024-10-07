#!/usr/bin/bash
point="/scratch/fye77278/PhoebusTesting/settings.ini"
module load java/11.0.15
/dls_sw/apps/phoebus/master/phoebus-product/phoebus.sh -settings $point "$@"

df -h
