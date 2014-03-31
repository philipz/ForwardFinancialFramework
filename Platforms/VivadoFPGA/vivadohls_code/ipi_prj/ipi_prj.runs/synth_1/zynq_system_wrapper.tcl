# 
# Synthesis run script generated by Vivado
# 

set_msg_config -id {HDL 9-1061} -limit 100000
set_msg_config -id {HDL 9-1654} -limit 100000
create_project -in_memory -part xc7z020clg484-1
set_property target_language VHDL [current_project]
set_property board xilinx.com:zynq:zc702:1.0 [current_project]
set_param project.compositeFile.enableAutoGeneration 0
set_property ip_repo_paths /home/ee/g/gi11/workspace/ForwardFinancialFramework/Platforms/VivadoFPGA/vivadohls_code/hls_prj/F3_VivadoHLS_core [current_fileset]

add_files /home/ee/g/gi11/workspace/ForwardFinancialFramework/Platforms/VivadoFPGA/vivadohls_code/ipi_prj/ipi_prj.srcs/sources_1/bd/zynq_system/zynq_system.bd
set_property used_in_implementation false [get_files -all /home/ee/g/gi11/workspace/ForwardFinancialFramework/Platforms/VivadoFPGA/vivadohls_code/ipi_prj/ipi_prj.srcs/sources_1/bd/zynq_system/ip/zynq_system_processing_system7_0_0/zynq_system_processing_system7_0_0.xdc]
set_property used_in_implementation false [get_files -all /home/ee/g/gi11/workspace/ForwardFinancialFramework/Platforms/VivadoFPGA/vivadohls_code/ipi_prj/ipi_prj.srcs/sources_1/bd/zynq_system/ip/zynq_system_vivado_activity_thread_0_0/constraints/vivado_activity_thread_ooc.xdc]
set_property used_in_implementation false [get_files -all /home/ee/g/gi11/workspace/ForwardFinancialFramework/Platforms/VivadoFPGA/vivadohls_code/ipi_prj/ipi_prj.srcs/sources_1/bd/zynq_system/ip/zynq_system_proc_sys_reset_0/zynq_system_proc_sys_reset_0.xdc]
set_property used_in_implementation false [get_files -all /home/ee/g/gi11/workspace/ForwardFinancialFramework/Platforms/VivadoFPGA/vivadohls_code/ipi_prj/ipi_prj.srcs/sources_1/bd/zynq_system/ip/zynq_system_proc_sys_reset_0/zynq_system_proc_sys_reset_0_ooc.xdc]
set_property used_in_implementation false [get_files -all /home/ee/g/gi11/workspace/ForwardFinancialFramework/Platforms/VivadoFPGA/vivadohls_code/ipi_prj/ipi_prj.srcs/sources_1/bd/zynq_system/ip/zynq_system_proc_sys_reset_0/zynq_system_proc_sys_reset_0_board.xdc]
set_property used_in_implementation false [get_files -all /home/ee/g/gi11/workspace/ForwardFinancialFramework/Platforms/VivadoFPGA/vivadohls_code/ipi_prj/ipi_prj.srcs/sources_1/bd/zynq_system/ip/zynq_system_auto_pc_12/zynq_system_auto_pc_12_ooc.xdc]
set_property used_in_implementation false [get_files -all /home/ee/g/gi11/workspace/ForwardFinancialFramework/Platforms/VivadoFPGA/vivadohls_code/ipi_prj/ipi_prj.srcs/sources_1/bd/zynq_system/zynq_system_ooc.xdc]
set_msg_config -id {IP_Flow 19-2162} -severity warning -new_severity info
set_property is_locked true [get_files /home/ee/g/gi11/workspace/ForwardFinancialFramework/Platforms/VivadoFPGA/vivadohls_code/ipi_prj/ipi_prj.srcs/sources_1/bd/zynq_system/zynq_system.bd]

read_vhdl /home/ee/g/gi11/workspace/ForwardFinancialFramework/Platforms/VivadoFPGA/vivadohls_code/ipi_prj/ipi_prj.srcs/sources_1/bd/zynq_system/hdl/zynq_system_wrapper.vhd
read_xdc dont_touch.xdc
set_property used_in_implementation false [get_files dont_touch.xdc]
set_param synth.vivado.isSynthRun true
set_property webtalk.parent_dir /home/ee/g/gi11/workspace/ForwardFinancialFramework/Platforms/VivadoFPGA/vivadohls_code/ipi_prj/ipi_prj.data/wt [current_project]
set_property parent.project_dir /home/ee/g/gi11/workspace/ForwardFinancialFramework/Platforms/VivadoFPGA/vivadohls_code/ipi_prj [current_project]
synth_design -top zynq_system_wrapper -part xc7z020clg484-1
write_checkpoint zynq_system_wrapper.dcp
report_utilization -file zynq_system_wrapper_utilization_synth.rpt -pb zynq_system_wrapper_utilization_synth.pb
