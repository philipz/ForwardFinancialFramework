#!/bin/sh
lli=${LLVMINTERP-lli}
exec $lli \
    /home/ee/g/gi11/workspace/ForwardFinancialFramework/Platforms/VivadoFPGA/vivadohls_code/hls_prj/F3_VivadoHLS_core/.autopilot/db/a.g.bc ${1+"$@"}
