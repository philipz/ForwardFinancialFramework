
set TopModule "vivado_activity_thread"
set ClockPeriod "10.000000"
set ClockList {ap_clk}
set multiClockList {}
set PortClockMap {}
set CombLogicFlag 0
set PipelineFlag 0
set DataflowTaskPipelineFlag  1
set TrivialPipelineFlag 0
set noPortSwitchingFlag 0
set FloatingPointFlag 1
set ResetLevelFlag 1
set ResetStyle "control"
set ResetSyncFlag 1
set ResetVariableFlag 0
set fsmEncStyle "auto"
set RtlPrefix ""
set ExtraCCFlags ""
set ExtraCLdFlags ""
set SynCheckOptions ""
set PresynOptions ""
set PreprocOptions ""
set SchedOptions ""
set BindOptions ""
set RtlGenOptions ""
set RtlWriterOptions ""
set CbcGenFlag ""
set CasGenFlag ""
set CasMonitorFlag ""
set AutoSimOptions {}
set ExportMCPathFlag "0"
set SCTraceFileName "mytrace"
set SCTraceFileFormat "vcd"
set SCTraceOption "all"
set TargetInfo "xc7z045:ffg900:-2"
set SourceFiles {sc {} c {../../srcs/option.c ../../srcs/underlying.c ../../srcs/asian_option.c ../../srcs/barrier_option.c ../../srcs/black_scholes_underlying.c ../../srcs/digital_double_barrier_option.c ../../srcs/double_barrier_option.c ../../srcs/european_option.c ../../srcs/gauss.c ../../srcs/heston_underlying.c ../../srcs/vivado_core.c}}
set SourceFlags {sc {} c {-DFP_t=float -DFP_t=float -DFP_t=float -DFP_t=float {-DFP_t=float -DTAUS_BOXMULLER -Dpow=powr -Dsqrt=rsqrt -Dsin=sinf -Dcos=cosf -DVIVADOHLS} -DFP_t=float -DFP_t=float -DFP_t=float {-DFP_t=float -Dpow=powr -Dsqrt=rsqrt -Dsin=sinf -Dcos=cosf -DVIVADOHLS} {-DFP_t=float -DTAUS_BOXMULLER -Dpow=powr -Dsqrt=rsqrt -Dsin=sinf -Dcos=cosf -DVIVADOHLS} -DFP_t=float}}
set DirectiveFile {/home/sf306/phd_codebase/FPL2014/FFF/ForwardFinancialFramework/Platforms/VivadoFPGA/vivadohls_code/hls_prj/F3_VivadoHLS_core/F3_VivadoHLS_core.directive}
set TBFiles {bc {} c {} sc {} cas {} vhdl {} verilog {}}
set TVInFiles {bc {} c {} sc {} cas {} vhdl {} verilog {}}
set TVOutFiles {bc {} c {} sc {} cas {} vhdl {} verilog {}}
set TBTops {bc "" c "" sc "" cas "" vhdl "" verilog ""}
set TBInstNames {bc "" c "" sc "" cas "" vhdl "" verilog ""}
set ExtraGlobalOptions {"area_timing" 1 "clock_gate" 1 "impl_flow" map "power_gate" 0}
set PlatformFiles {{DefaultPlatform {xilinx/zynq/zynq xilinx/zynq/zynq_fpv6}}}
set DefaultPlatform "DefaultPlatform"
set TBTVFileNotFound ""
set AppFile "../vivado_hls.app"
set ApsFile "F3_VivadoHLS_core.aps"
set AvePath "../.."