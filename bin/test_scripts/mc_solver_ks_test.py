'''
Created on 6 May 2013
'''
import sys,os
os.chdir("..")
sys.path.append("../..")
import ForwardFinancialFramework.bin.KS_ProblemSet

def run_ks_solver(platform_name,paths,script_option,options,debug=False,threads=0):  
  option = ForwardFinancialFramework.bin.KS_ProblemSet.KS_Options(options)
 
  if(platform_name=="OpenCL_GPU"):
    from ForwardFinancialFramework.Platforms.OpenCLGPU import OpenCLGPU_MonteCarlo,OpenCLGPU
    platform = OpenCLGPU.OpenCLGPU()
    mc_solver = OpenCLGPU_MonteCarlo.OpenCLGPU_MonteCarlo(option,paths,platform)
    
  elif(platform_name=="CPU"):
    from ForwardFinancialFramework.Platforms.MulticoreCPU import MulticoreCPU_MonteCarlo,MulticoreCPU
    platform = MulticoreCPU.MulticoreCPU()
    mc_solver = MulticoreCPU_MonteCarlo.MulticoreCPU_MonteCarlo(option,paths,platform,random_number_generator="taus_boxmuller")
    
  elif(platform_name=="Maxeler_FPGA"):
    from ForwardFinancialFramework.Platforms.MaxelerFPGA import MaxelerFPGA_MonteCarlo,MaxelerFPGA
    platform = MaxelerFPGA.MaxelerFPGA()
    mc_solver = MaxelerFPGA_MonteCarlo.MaxelerFPGA_MonteCarlo(option,paths,platform)
    
  elif(platform_name=="Vivado_FPGA"):
    from ForwardFinancialFramework.Platforms.VivadoFPGA import VivadoFPGA_MonteCarlo,VivadoFPGA
    platform = VivadoFPGA.VivadoFPGA()
    mc_solver = VivadoFPGA_MonteCarlo.VivadoFPGA_MonteCarlo(option,paths,platform)
    
  else:
    print "incorrect platform type!"
    sys.exit()
    
  if("Generate" in script_option): mc_solver.generate()
  
  compile_output = [""]
  if ("Compile" in script_option): compile_output = mc_solver.compile(debug=debug)
  
  execution_output=[""]
  if ("Execute" in script_option): execution_output = mc_solver.execute(debug=debug)
 
  execution_output_dict = {}
  if("Execute" in script_option):
    for i,r in enumerate(execution_output[:-3]):
        if not(i%2): 
          execution_output_dict["Option %s"%options[i/2]] = r
	  execution_output_dict["Option %s 95%%CI"%options[i/2]] = execution_output[i+1]
      
    execution_output_dict["Total time"] = execution_output[-1]
    execution_output_dict["User time"] = execution_output[-3]
    execution_output_dict["Kernel time"] = execution_output[-2]
  
  return (compile_output,execution_output_dict)
    
if(__name__ == '__main__' and len(sys.argv)>3):
  platform_name = sys.argv[1]
  paths = int(sys.argv[3])
  script_option = sys.argv[2]
  options = sys.argv[4:]
  
  results = run_ks_solver(platform_name,paths,script_option,options,debug=True,threads=0)
  
  if(len(results[0])>0):
    print "compiler output:"
    for r in results[0]: print r
    
  if(len(results[1].keys())>3):
    for k in sorted(results[1].keys()): 
      if("time" not in k): print "%s - %s"%(k,results[1][k])
      
    print "Latency: %s uS (%s uS Setup Time + %s uS Activity Time)"%(results[1]["Total time"],results[1]["User time"],results[1]["Kernel time"])
    
elif(__name__ == '__main__'):
  print "usage: python mc_solver_ks_test_script [CPU|OpenCL_GPU|Maxeler_FPGA|Vivado_FPGA] [Generate|&Compile|&Execute] [Number of Paths] [KS Option Number 1] [KS Option Number 2] [...] [KS Option Number N]"