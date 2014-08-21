'''
Created on 1 April 2014

'''
import os,time,subprocess,sys,time,math,pyopencl
import platform as plat
from ForwardFinancialFramework.Platforms.MulticoreCPU import MulticoreCPU_MonteCarlo
from ForwardFinancialFramework.Platforms.OpenCLGPU import OpenCLGPU_MonteCarlo
from ForwardFinancialFramework.Solvers.MonteCarlo import MonteCarlo

class OpenCLAlteraFPGA_MonteCarlo(OpenCLGPU_MonteCarlo.OpenCLGPU_MonteCarlo):
  instance_paths = 1
  instances = 1
  pipelining = 1
  cslow = False
  simulation = False
    
  def __init__(self,derivative,paths,platform,reduce_uNderlyings=True,kernel_path_max=1,random_number_generator="taus_boxmuller",floating_point_format="float",instance_paths=1000,instances=1,pipelining=1,cslow=False,simulation=False,default_points=4096,reduce_underlyings=True):
    self.instance_paths = instance_paths
    self.pipelining = pipelining
    self.simulation = simulation
    self.cslow = cslow
    self.instances = instances
    
    OpenCLGPU_MonteCarlo.OpenCLGPU_MonteCarlo.__init__(self,derivative,paths,platform,reduce_underlyings=reduce_underlyings,kernel_path_max=kernel_path_max,random_number_generator=random_number_generator,floating_point_format=floating_point_format,default_points=default_points)
    
    #self.utility_libraries.remove("CL/cl.hpp")
    #self.utility_libraries.append("CL/opencl.h") #Because the one thing that people wont standardise on is the name and location of the API header file...
    self.solver_metadata["local_work_items"] = self.instances
    
    if("CL/cl.hpp" in self.utility_libraries): self.utility_libraries.remove("CL/cl.hpp")
    if("CL/opencl.h" not in self.utility_libraries): self.utility_libraries.append("CL/opencl.h")
    
  def generate_name(self):
      MonteCarlo.MonteCarlo.generate_name(self)  
      self.output_file_name = ("%s_cslow_%s_pipe_%d_insts_%d"%(self.output_file_name,str(self.cslow),self.pipelining,self.instances))
  
  def generate_activity_thread(self):
    output_list = OpenCLGPU_MonteCarlo.OpenCLGPU_MonteCarlo.generate_activity_thread(self)
    
    #Looking for an aocx file instead of a clbin file
    index = output_list.index("FILE *fp=fopen(\"%s.clbin\", \"r\");"%self.output_file_name)
    output_list.insert(index,"FILE *fp=fopen(\"%s_kernel.aocx\", \"r\");"%self.output_file_name)
    output_list.remove("FILE *fp=fopen(\"%s.clbin\", \"r\");"%self.output_file_name)

    index = output_list.index("const size_t local_kernel_paths = local_work_items;")
    output_list.insert(index,"const size_t local_kernel_paths = 1;") #TODO I should rather be getting the OpenCL runtime to do this
    output_list.remove("const size_t local_kernel_paths = local_work_items;")
    
    #Creating attribute struct buffers as Altera OpenCL doesn't support passing structs as kernel arguments directly
    for u_index,u in enumerate(self.underlying):
      index = output_list.index("%s_attributes u_a_%d;" % (u.name,u_index))
      output_list.insert(index+1,"cl_mem u_a_%d_buff = clCreateBuffer(context, CL_MEM_READ_ONLY,sizeof(%s_attributes),NULL,&ret);" % (u_index,u.name))
      output_list.insert(index+2,"assert(ret==CL_SUCCESS);")
    
    for d_index,d in enumerate(self.derivative):
      index = output_list.index("%s_attributes o_a_%d;" % (d.name,d_index))
      output_list.insert(index+1,"cl_mem o_a_%d_buff = clCreateBuffer(context, CL_MEM_READ_ONLY,sizeof(%s_attributes),NULL,&ret);" % (d_index,d.name))
      output_list.insert(index+2,"assert(ret==CL_SUCCESS);")
    
    #Setting attribute struct buffers as the kernel arguments 
    for u_index,u in enumerate(self.underlying):
      index = output_list.index("ret = clSetKernelArg(%s_kernel, %d, sizeof(%s_attributes), &u_a_%d);"%(self.output_file_name,4 + u_index,u.name,u_index))
      output_list.insert(index,"ret = clSetKernelArg(%s_kernel, %d, sizeof(cl_mem), (void *)&u_a_%d_buff);"%(self.output_file_name,4 + u_index,u_index))
      output_list.remove("ret = clSetKernelArg(%s_kernel, %d, sizeof(%s_attributes), &u_a_%d);"%(self.output_file_name,4 + u_index,u.name,u_index))
      
    for d_index,d in enumerate(self.derivative):
      index = output_list.index("ret = clSetKernelArg(%s_kernel, %d, sizeof(%s_attributes), &o_a_%d);"%(self.output_file_name,4 + len(self.underlying) + d_index,d.name,d_index))
      output_list.insert(index,"ret = clSetKernelArg(%s_kernel, %d, sizeof(cl_mem), (void *)&o_a_%d_buff);"%(self.output_file_name,4 + len(self.underlying) + d_index,d_index))
      output_list.remove("ret = clSetKernelArg(%s_kernel, %d, sizeof(%s_attributes), &o_a_%d);"%(self.output_file_name,4 + len(self.underlying) + d_index,d.name,d_index))
    
    #Writing to the attribute struct buffers
    index = output_list.index("double temp_total_0=0;")
    output_list.insert(index,"cl_event write_events[%d];"%(len(self.underlying)+len(self.derivative)))
    index += 1
    
    for u_index,u in enumerate(self.underlying):
        output_list.insert(index,"ret = clEnqueueWriteBuffer(command_queue, u_a_%d_buff, CL_TRUE, 0, sizeof(%s_attributes), &u_a_%d, 0, NULL, &write_events[%d]);"%(u_index,u.name,u_index,u_index))
        output_list.insert(index+1,"assert(ret==CL_SUCCESS);")
        index += 2
    
    for d_index,d in enumerate(self.derivative):
        output_list.insert(index,"ret = clEnqueueWriteBuffer(command_queue, o_a_%d_buff, CL_TRUE, 0, sizeof(%s_attributes), &o_a_%d, 0, NULL, &write_events[%d]);"%(d_index,d.name,d_index,len(self.underlying)+d_index))
        output_list.insert(index+1,"assert(ret==CL_SUCCESS);")
        index += 2
        
        
    #Changing 1st kernel call to be dependent on the option and underlying write events. Also, the number of work items per work group is left up to the compiler
    index = output_list.index("ret = clEnqueueNDRangeKernel(command_queue, %s_kernel, (cl_uint) 1, NULL, &kernel_paths, &local_kernel_paths, 0, NULL, kernel_event);"%(self.output_file_name))
    output_list.insert(index,"ret = clEnqueueNDRangeKernel(command_queue, %s_kernel, (cl_uint) 1, NULL, &kernel_paths, NULL, %d, write_events, kernel_event);"%(self.output_file_name,len(self.underlying)+len(self.derivative)))
    output_list.remove("ret = clEnqueueNDRangeKernel(command_queue, %s_kernel, (cl_uint) 1, NULL, &kernel_paths, &local_kernel_paths, 0, NULL, kernel_event);"%(self.output_file_name))
    
    #Changing the following kernel calls to let the compiler determine the number of work items per work group is left up to the compiler
    index  = output_list.index("ret = clEnqueueNDRangeKernel(command_queue, %s_kernel, (cl_uint) 1, NULL, &kernel_paths, &local_kernel_paths, %d, read_events, kernel_event);"%(self.output_file_name,len(self.derivative)))
    output_list.insert(index,"ret = clEnqueueNDRangeKernel(command_queue, %s_kernel, (cl_uint) 1, NULL, &kernel_paths, NULL, %d, read_events, kernel_event);"%(self.output_file_name,len(self.derivative)))
    output_list.remove("ret = clEnqueueNDRangeKernel(command_queue, %s_kernel, (cl_uint) 1, NULL, &kernel_paths, &local_kernel_paths, %d, read_events, kernel_event);"%(self.output_file_name,len(self.derivative)))
    
    return output_list

  def generate_kernel(self):
    output_list = OpenCLGPU_MonteCarlo.OpenCLGPU_MonteCarlo.generate_kernel(self)
    
    #Adding Compile time loop bounds, and removing the kernel arguments
    output_list.insert(0,"#define PATHS %d"%self.solver_metadata["kernel_loops"])
    output_list.insert(1,"#define PATH_POINTS %d"%self.solver_metadata["path_points"])
    
    #output_list.remove("\tconstant int *path_points,")
    #output_list.remove("\tglobal uint *chunk_size,")
    
    if(self.cslow):
        for index,u in enumerate(self.underlying):
            lindex = output_list.index("%s_variables temp_u_v_%d;"%(u.name,index))
            output_list.insert(lindex,"%s_variables u_v_%d_array[PATHS];"%(u.name,index))
            output_list.insert(lindex,"FP_t spot_price_%d_array[PATHS],time_%d_array[PATHS];"%(index,index))
                               
        for index,d in enumerate(self.derivative):
            lindex = output_list.index("%s_variables temp_o_v_%d;"%(d.name,index))
            output_list.insert(lindex,"%s_variables o_v_%d_array[PATHS];"%(d.name,index))
    
    index = output_list.index("uint local_path_points = path_points;")
    output_list.insert(index,"const uint local_path_points = PATH_POINTS;")
    output_list.remove("uint local_path_points = path_points;")
    
    #Modifying the outer, path loop
    lindex = output_list.index("for(int k=0;k<%d;++k){"%self.kernel_loops)
    if not(self.cslow):
        #output_list.insert(lindex,"for(int j=0;j<PATH_POINTS;++j){");
        output_list.insert(lindex,"for(int k=0;k<PATHS;++k){")
    output_list.remove("for(int k=0;k<%d;++k){"%self.kernel_loops)
    
    #Modifying the inner, path simulation loop
    lindex = output_list.index("for(int j=0;j<local_path_points;++j){")
    if(self.cslow):
        for index,u in enumerate(self.underlying):
            output_list.insert(lindex,"temp_u_v_%d = u_v_%d_array[k];"%(index,index))
            output_list.insert(lindex,"spot_price_%d = spot_price_%d;"%(index,index))
            output_list.insert(lindex,"time_%d = time_%d_array[k];"%(index,index))
        for index,d in enumerate(self.derivative):
            output_list.insert(lindex,"temp_o_v_%d = o_v_%d_array[k];"%(index,index))
        
        output_list.insert(lindex,"for(int k=0;k<PATHS;++k){")
        output_list.insert(lindex,"for(int j=0;j<PATH_POINTS;++j){")
        
        
        """or index,u in enumerate(self.underlying):
            output_list.insert(lindex,"u_v_%d_array[k] = temp_u_v_%d;"%(index,index))
            output_list.insert(lindex,"spot_price_%d_array[k] = spot_price_%d;"%(index,index))
            output_list.insert(lindex,"time_%d_array[k] = time_%d;"%(index,index))
        for index,d in enumerate(self.derivative):
            output_list.insert(lindex,"o_v_%d_array[k] = temp_o_v_%d;"%(index,index))"""
            
        output_list.insert(lindex,"}") #end off the initialisation loop
        
        for index,u in enumerate(self.underlying):
            output_list.insert(lindex,"u_v_%d_array[k] = temp_u_v_%d;"%(index,index))
            output_list.insert(lindex,"spot_price_%d_array[k] = spot_price_%d;"%(index,index))
            output_list.insert(lindex,"time_%d_array[k] = time_%d;"%(index,index))
        for index,d in enumerate(self.derivative):
            output_list.insert(lindex,"o_v_%d_array[k] = temp_o_v_%d;"%(index,index))
        
    else:
        output_list.insert(lindex,"for(int j=0;j<PATH_POINTS;++j){")
        
    output_list.remove("for(int j=0;j<local_path_points;++j){")
    
    if(self.cslow):
        #Creating the seperate initiation loop
        lindex = output_list.index("%s_underlying_path_init(&temp_u_v_0,&temp_u_a_0);"%self.underlying[0].name)
        output_list.insert(lindex,"for(int k=0;k<PATHS;++k){")
        
        #copying the state at the end of the path step into the array variables
        lindex = output_list.index("time_%d = temp_u_v_%d.time;"%(len(self.underlying)-1,len(self.underlying)-1)) + 1
        lindex = output_list[lindex:].index("time_%d = temp_u_v_%d.time;"%(len(self.underlying)-1,len(self.underlying)-1)) + lindex + 1
        
        for index,u in enumerate(self.underlying):
            output_list.insert(lindex,"u_v_%d_array[k] = temp_u_v_%d;"%(index,index))
            output_list.insert(lindex,"spot_price_%d_array[k] = spot_price_%d;"%(index,index))
            output_list.insert(lindex,"time_%d_array[k] = time_%d;"%(index,index))
        for index,d in enumerate(self.derivative):
            output_list.insert(lindex,"o_v_%d_array[k] = temp_o_v_%d;"%(index,index))
        
        #Creating the separate payoff loop
        lindex = output_list.index("temp_value_0 += temp_o_v_0.value;") - 1 #this should always work, but doesn't feel right
        
        for index,u in enumerate(self.underlying):
            output_list.insert(lindex,"spot_price_%d = spot_price_%d;"%(index,index))
        for index,d in enumerate(self.derivative):
            output_list.insert(lindex,"temp_o_v_%d = o_v_%d_array[k];"%(index,index))
        
        output_list.insert(lindex,"for(int k=0;k<PATHS;++k){")
        output_list.insert(lindex,"}")
    
    """index = output_list.index("uint local_chunk_size = chunk_size[0];")
    output_list.insert(index,"uint local_chunk_size = PATHS;")
    output_list.remove("uint local_chunk_size = chunk_size[0];")"""
    
    
    #Making struct arguments into memory operations. Also, adding the restrict keyword to arguments
    for index,u in enumerate(self.underlying):
      temp_index = output_list.index("\tconst %s_attributes u_a_%d,"%(u.name,index))
      output_list.insert(temp_index,"\tglobal %s_attributes *restrict u_a_%d,"%(u.name,index))
      output_list.remove("\tconst %s_attributes u_a_%d,"%(u.name,index))
      
      temp_index = output_list.index("%s_attributes temp_u_a_%d = u_a_%d;"%(u.name,index,index))
      output_list.insert(temp_index,"%s_attributes temp_u_a_%d = *u_a_%d;"%(u.name,index,index))
      output_list.remove("%s_attributes temp_u_a_%d = u_a_%d;"%(u.name,index,index))
      
      #temp_index = output_list.index("\tglobal const rng_state_t *seed_%d,"%index)
      #output_list.insert(temp_index,"\tglobal const rng_state_t *restrict seed_%d,"%index)
      #output_list.remove("\tglobal const rng_state_t *seed_%d,"%index)
      
    for index,d in enumerate(self.derivative):
      temp_index = output_list.index("\tconst %s_attributes o_a_%d,"%(d.name,index))
      output_list.insert(temp_index,"\tglobal %s_attributes *restrict o_a_%d,"%(d.name,index))
      output_list.remove("\tconst %s_attributes o_a_%d,"%(d.name,index))
      
      temp_index = output_list.index("%s_attributes temp_o_a_%d = o_a_%d;"%(d.name,index,index))
      output_list.insert(temp_index,"%s_attributes temp_o_a_%d = *o_a_%d;"%(d.name,index,index))
      output_list.remove("%s_attributes temp_o_a_%d = o_a_%d;"%(d.name,index,index))
      
      temp_index = 0
      if(index<(len(self.derivative)-1)):
        temp_index = output_list.index("\tglobal FP_t *value_%d,"%(index))
        output_list.insert(temp_index,"\tglobal FP_t *restrict value_%d,"%(index))
        output_list.remove("\tglobal FP_t *value_%d,"%(index))
      
      else:
        temp_index = output_list.index("\tglobal FP_t *value_%d){"%(index))
        output_list.insert(temp_index,"\tglobal FP_t *restrict value_%d){"%(index))
        output_list.remove("\tglobal FP_t *value_%d){"%(index))
    
    #Controlling the amount of pipeline parallelism
    #if(self.pipelining>1):
    index = output_list.index("for(int j=0;j<PATH_POINTS;++j){")
    output_list.insert(index,"#pragma unroll UNROLL_FACTOR")
    
    #Controlling the degree of task parallelism
    index = output_list.index("kernel void %s_kernel("%self.output_file_name)
    output_list.insert(index,"__attribute__((num_compute_units(COMPUTE_UNITS)))")
    
    #Pointing to a NULL value
    #index = output_list.index("clEnqueueNDRangeKernel(command_queue, %s_kernel, (cl_uint) 1, NULL, &kernel_paths, &local_kernel_paths, %d, write_events, kernel_event);"%(self.output_file_name,4+len(self.underlying)+len(self.derivative)))
    #output_list.insert(index,"clEnqueueNDRangeKernel(command_queue, %s_kernel, (cl_uint) 1, NULL, &kernel_paths, NULL, 1, write_events, kernel_event);")
    #output_list.remove("clEnqueueNDRangeKernel(command_queue, %s_kernel, (cl_uint) 1, NULL, &kernel_paths, &local_kernel_paths, %d, write_events, kernel_event);"%(self.output_file_name,4+len(self.underlying)+len(self.derivative)))

    #index = output_list.index("clEnqueueNDRangeKernel(command_queue, %s_kernel, (cl_uint) 1, NULL, &kernel_paths, &local_kernel_paths, 1, write_events, kernel_event);"%self.output_file_name)
    #output_list.insert(index,"clEnqueueNDRangeKernel(command_queue, %s_kernel, (cl_uint) 1, NULL, &kernel_paths, NULL, 1, write_events, kernel_event);")
    #output_list.remove("clEnqueueNDRangeKernel(command_queue, %s_kernel, (cl_uint) 1, NULL, &kernel_paths, &local_kernel_paths, 1, write_events, kernel_event);")
    
    #if(self.instances>1):
        #output_list.insert(index,"__attribute__((reqd_work_group_size(%d,1,1)))"%self.instances)
        #output_list.insert(index,"__attribute__((num_simd_work_items(%d)))"%self.instances)
        #self.solver_metadata["local_work_items"] = self.instances #just in case this has changed
       
    #Designating each kernel as a task
    index = output_list.index("kernel void %s_kernel("%self.output_file_name)
    output_list.insert(index,"__attribute__((task))")
    output_list.insert(index,"__attribute__((reqd_work_group_size(1,1,1)))")
    
    #Ammending the seeding operation
    """for index,u in enumerate(self.underlying):
        if("black_scholes" in u.name or "heston" in u.name):
            temp_index = output_list.index("temp_u_v_%d.rng_state.s1 = %d + local_chunk_number*local_chunk_size + 2;"%(index,index))
            output_list.insert(temp_index,"temp_u_v_%d.rng_state.s1 = local_seed + %d + local_chunk_number*local_chunk_size + 2;"%(index,index))
            output_list.remove("temp_u_v_%d.rng_state.s1 = %d + local_chunk_number*local_chunk_size + 2;"%(index,index))
            
            temp_index = output_list.index("temp_u_v_%d.rng_state.s2 = %d + local_chunk_number*local_chunk_size + 8;"%(index,index))
            output_list.insert(temp_index,"temp_u_v_%d.rng_state.s2 = local_seed + %d + local_chunk_number*local_chunk_size + 8;"%(index,index))
            output_list.remove("temp_u_v_%d.rng_state.s2 = %d + local_chunk_number*local_chunk_size + 8;"%(index,index))"""
    
    return output_list

  def compile(self,override=True,debug=False,simulation=False):
    #compile_flags = ["-lOpenCL","-I/usr/include","-fpermissive"]
    
    start_directory = os.getcwd()
    
    os.chdir("..")
    os.chdir(self.platform.platform_directory())
    
    opencl_compile_flags = ["-v","--report"]
    opencl_compile_flags.extend(["--board",self.platform.board])
    
    path_string = ""
    if(self.random_number_generator=="mwc64x_boxmuller"):
      #path_string = ""
      opencl_compile_flags.append("-DMWC64X_BOXMULLER")
    
    elif(self.random_number_generator=="taus_boxmuller" or self.random_number_generator=="taus_ziggurat"):
      #path_string = ""
      opencl_compile_flags.append("-DTAUS_BOXMULLER")
    
    #if("darwin" in sys.platform): path_string = "%s/%s"%(os.getcwd(),path_string)
    path_string = os.getcwd()
    #else: path_string = "%s/%s"%(os.getcwd(),path_string)
    
    opencl_compile_flags.extend(["-DOPENCL_GPU","-I%s"%path_string,"-DCOMPUTE_UNITS=%d"%self.instances,"-DUNROLL_FACTOR=%d"%self.pipelining])
    if(simulation): opencl_compile_flags.append("-march=emulator")
    
    compile_cmd = ["aoc"]
    compile_cmd.extend(opencl_compile_flags)
    compile_cmd.append("%s.cl"%self.output_file_name)
    compile_cmd.extend(["-o","%s_kernel.aocx"%self.output_file_name])
    
    compile_string = ""
    for c_c in compile_cmd: compile_string = "%s %s"%(compile_string,c_c)
    if(debug): print compile_string
    
    result = [subprocess.check_output(compile_cmd)]
    
    #subprocess.call(["rm","-rf","%s"%self.output_file_name])
    
    os.chdir(start_directory)
    
    compile_flags = subprocess.check_output(["aocl","compile-config"]).strip("\n").split(" ")
    compile_flags.extend(subprocess.check_output(["aocl","ldflags"]).strip("\n").split(" "))
    compile_flags.extend(subprocess.check_output(["aocl","ldlibs"]).strip("\n").split(" "))
    
    compile_flags.extend(["-fpermissive", "-DCOMPUTE_UNITS=%d"%self.instances,"-DUNROLL_FACTOR=%d"%self.pipelining])
    if(debug): compile_flags.append("-ggdb")
    while('' in compile_flags): compile_flags.remove('')
    
    result.append(MulticoreCPU_MonteCarlo.MulticoreCPU_MonteCarlo.compile(self,override,compile_flags,debug)) #Compiling Host C Code

    
    return result
    
    #os.chdir("..")
    #os.chdir(self.platform.platform_directory())
  
  #def execute(self): pass
  """
  ./mc_solver_opencl_gpu_un_1_op_1Run 1000 10 10 1 8 1 2 4253708855 0.1 100 1.0 1.0 100
  """
    
  def set_chunk_paths(self):
    self.solver_metadata["chunk_paths"] = self.instance_paths
    self.chunk_paths = self.instance_paths
    
