'''
Created on 30 October 2012

'''
import os,time,subprocess,sys,time,math
from ForwardFinancialFramework.Solvers.MonteCarlo import MonteCarlo

class MulticoreCPU_MonteCarlo(MonteCarlo.MonteCarlo):
  def __init__(self,derivative,paths,platform,reduce_underlyings=True):
    MonteCarlo.MonteCarlo.__init__(self,derivative,paths,platform,reduce_underlyings)
    self.solver_metadata["threads"] = self.platform.threads #Number of threads set by the platform
    
    self.utility_libraries = ["math.h","pthread.h","stdint.h","stdlib.h","stdio.h","sys/time.h","sys/resource.h","unistd.h","string.h"]
    self.activity_thread_name = "multicore_montecarlo_activity_thread"
    
  def generate(self,name_extension=".c",override=True,verbose=False):
    #os.chdir("..")
    #os.chdir(self.platform.platform_directory())
    
    if(override or not os.path.exists("%s.c"%self.output_file_name)):
        #os.chdir(self.platform.root_directory())
        #os.chdir("bin")
      
        code_string = []
        code_string.extend(self.generate_identifier())
        code_string.extend(self.generate_libraries())
        code_string.extend(self.generate_variable_declaration())
        code_string.extend(self.generate_activity_thread())
        code_string.extend(self.generate_main_thread())
        
        #Actually writing to the file
        self.generate_source(code_string,name_extension,verbose)
        
    #os.chdir(self.platform.root_directory())
    #os.chdir("bin")
  
  def generate_identifier(self): return ["//%s.c Generated by Monte Carlo MulticoreCPU Solver"%self.output_file_name]
    
  def generate_libraries(self):
    #Checking that the platform source code for the derivatives and underlyings required are present
    os.chdir("..")
    os.chdir(self.platform.platform_directory())
    
    underlying_libraries = []
    for u in self.underlying: 
      if(not(os.path.exists("%s.c"%u.name)) or not(os.path.exists("%s.h"%u.name))): raise IOError, ("missing the source code for the underlying - %s.c or %s.h" % (u.name,u.name))
      else: underlying_libraries.append("%s.h"%u.name)
        
    derivative_libraries = []    
    for d in self.derivative:
      if(not(os.path.exists("%s.c"%d.name)) or not(os.path.exists("%s.h"%d.name))): raise IOError, ("missing the source code for the derivative - %s.c or %s.h" %  (d.name,d.name))
      else: derivative_libraries.append("%s.h"%d.name)
      
    os.chdir(self.platform.root_directory())
    os.chdir("bin")
    
    output_list = ["//Libraries"]
    for u in self.utility_libraries: output_list.append("#include \"%s\";"%u)
    for u in underlying_libraries: output_list.append("#include \"%s\";"%u)
    for d in derivative_libraries: output_list.append("#include \"%s\";"%d)
  
    return output_list
  
  def generate_variable_declaration(self):
    #Generate Intermediate and Communication Variables
      output_list = []
      output_list.append("//*Intermediate and Communication Variables*")
      
      for d in self.derivative:
          index = self.derivative.index(d)
          for u in d.underlying:
              u_index = self.underlying.index(u)
              output_list.append("double discount_%d_%d;"%(index,u_index))
              
          output_list.append("double option_price_%d;"%index)
          
      index = 0
      for u_a in self.underlying_attributes:
          for a in u_a: output_list.append("static double %s_%d_%s;"%(self.underlying[index].name,index,a)) #execution code must mirror this ordering
          index += 1
      
      index = 0
      for o_a in self.derivative_attributes:
          for o in o_a: output_list.append("static double %s_%d_%s;"%(self.derivative[index].name,index,o)) #execution code must mirror this ordering
          index += 1
          
      for k in self.solver_metadata.keys(): output_list.append("static int %s;"%k) 
          
      output_list.append("int thread_paths,i,j;")
      
      output_list.append("struct thread_data{")
      output_list.append("int thread_paths;")
      output_list.append("double *thread_result;")
      output_list.append("};")
      
      #Performance Monitoring Variables
      output_list.append("//*Performance Monitoring Variables*")
      output_list.append("double system_time,user_time,cpu_time,wall_time;")
      output_list.append("struct timeval start, end;")
      output_list.append("int ret,ret_2;")
      output_list.append("struct rusage usage,usage_2;")
      
      return output_list
  
  def generate_main_thread(self):
    output_list = []
	
    #Declare Main Function
    output_list.append("//*Main Function*")
    output_list.append("int main(int argc,char* argv[]){")
    ##Commented out diagnostic tool
    #output_file.write("/*for(i=0;i<argc;i++){//For diagnostic Purposes\nprintf(\"%s \",argv[i]);\n}*/\n")
    
    ##Convert command line arguments to static variables
    output_list.append("//**Unpacking Command Line Variables**")
    temp = 1
    output_list.append("//***Solver Metadata***")
    for k in self.solver_metadata.keys(): 
        output_list.append("%s = atoi(argv[%d]);"%(k,temp))
        temp += 1
    
    output_list.append("//***Underlying Attributes***")
    index = 0
    for u_a in self.underlying_attributes:
        for a in u_a:
            output_list.append("%s_%d_%s = strtod(argv[%d],NULL);"%(self.underlying[index].name,index,a,temp))
            temp += 1
        index += 1
    
    output_list.append("//***Derivative Attributes***")
    index = 0
    for o_a in self.derivative_attributes:
        for a in o_a:
            output_list.append("%s_%d_%s = strtod(argv[%d],NULL);"%(self.derivative[index].name,index,a,temp))
            temp += 1
        index += 1
        
    output_list.append("//**Starting Timers**")
    output_list.append("int who = RUSAGE_SELF;")
    output_list.append("gettimeofday(&start,NULL);")
    output_list.append("ret=getrusage(who,&usage);")
    
    ##Calculate Discount Factor
    output_list.append("//**Calculating Discount Factor**")
    
    for d in self.derivative:
        index = self.derivative.index(d)
        for u in d.underlying:
            u_index = self.underlying.index(u)
            output_list.append("discount_%d_%d = exp(-%s_%d_rfir*%s_%d_time_period);"%(index,u_index,u.name,u_index,d.name,index))
            
    
    ##Create Thread Support Structure
    output_list.append("//**Creating Thread Variables**")
    output_list.append("thread_paths = paths/threads;")
    output_list.append("pthread_t pthreads[threads];")
    output_list.append("double thread_results[threads][%d];"%len(self.derivative))
    output_list.append("struct thread_data temp_data[threads];")
    
    output_list.append("pthread_attr_t attr;")
    output_list.append("pthread_attr_init(&attr);")
    output_list.append("pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);")
    
    ##Pack up data and pass to threads
    output_list.append("//**Packing up data and passing to threads**")
    output_list.append("int i;");
    output_list.append("for(i=0;i<threads;i++){ //Generating Threads");
    output_list.append("temp_data[i].thread_paths = thread_paths;")
    output_list.append("if(i==(threads-1)){ //If final thread, allocating any remaining paths to it (i.e. PATHS%THREADS!=0)")
    output_list.append("temp_data[i].thread_paths += paths%threads;")
    output_list.append("}")
    output_list.append("temp_data[i].thread_result = thread_results[i];")
    output_list.append("pthread_create(&pthreads[i],&attr,%s,&temp_data[i]);"%self.activity_thread_name)
    output_list.append("}")
    ##Join Threads, aggregate results
    output_list.append("//**Waiting for threads to join**")
    output_list.append("void *status;")
    for d in self.derivative: output_list.append("option_price_%d = 0;"%self.derivative.index(d))
    output_list.append("for(i=0;i<threads;i++){ //Waiting for Threads");
    output_list.append("pthread_join(pthreads[i],&status);");
    
    for d in self.derivative:
        index = self.derivative.index(d)
        for u in d.underlying:
            u_index = self.underlying.index(u)
            output_list.append("option_price_%d += discount_%d_%d*thread_results[i][%d];"%(index,index,u_index,index));
            #output_file.write("option_price_%d = thread_results[i][%d];"%(index,index));
    
    output_list.append("}")
    
    ##Calculate final value and return value
    output_list.append("//**Calculating Final Option Value and Return**")
    for d in self.derivative:
        output_list.append("option_price_%d = option_price_%d/paths;//Calculate final value and return value as well as timing"%(self.derivative.index(d),self.derivative.index(d)))
        output_list.append("printf(\"\%f\\n\"")
        output_list.append(",option_price_%d);"%self.derivative.index(d))
    
    ##Return Performance evaluation
    output_list.append("//**Performance Monitoring Calculation and Return**")
    output_list.append("gettimeofday(&end,NULL);")
    output_list.append("ret_2=getrusage(who,&usage_2);")
    
    output_list.append("user_time = usage_2.ru_utime.tv_sec*1000000+usage_2.ru_utime.tv_usec-(usage.ru_utime.tv_sec*1000000+usage.ru_utime.tv_usec);")
    output_list.append("system_time = usage_2.ru_stime.tv_sec*1000000+usage_2.ru_stime.tv_usec-(usage.ru_stime.tv_sec*1000000+usage.ru_stime.tv_usec);")
    output_list.append("cpu_time = (user_time + system_time);")
    output_list.append("wall_time = 1000000*(end.tv_sec-start.tv_sec)+end.tv_usec-start.tv_usec;")
    
    output_list.append("printf(\"\%f\\n\",cpu_time);")
    output_list.append("printf(\"\%f\\n\",wall_time);")
    #output_list.append("printf(\"\%d\\n\",(MemoryUsed()));")
    output_list.append("}")
    
    return output_list
  
  def generate_activity_thread(self):
    #Generate Path Loop Function
    output_list = []
    output_list.append("//*MC Multicore Activity Thread Function*")
    output_list.append("void * %s(void* thread_arg){"%self.activity_thread_name)
    
    ##Declare Loop Data Structures
    output_list.append("//**Loop Data Structures**")
    output_list.append("struct thread_data* temp_data;")
    output_list.append("temp_data = (struct thread_data*) thread_arg;")
    
    for u in self.underlying:
        index = self.underlying.index(u)
        output_list.append("%s_under_attr u_a_%d;" % (u.name,index))
        output_list.append("%s_under_var u_v_%d;" % (u.name,index))
    
    for d in self.derivative:
        index = self.derivative.index(d)
        output_list.append("%s_opt_attr o_a_%d;" % (d.name,index))
        output_list.append("%s_opt_var o_v_%d;" % (d.name,index))
    
    
    output_list.append("//**Initialising Loop Attributes*")
    
    ##Calling Init Functions
    for u in self.underlying:
        u_index = self.underlying.index(u)
        
        temp = ("%s_underlying_init("%u.name)
        for u_a in self.underlying_attributes[u_index][:-1]: temp=("%s%s_%d_%s,"%(temp,u.name,u_index,u_a))
        temp=("%s%s_%d_%s,&u_a_%d);"%(temp,u.name,u_index,self.underlying_attributes[u_index][-1],u_index))
        output_list.append(temp)
    
    for d in self.derivative:
        index = self.derivative.index(d)
        
        temp = ("%s_derivative_init("%d.name)
        for o_a in self.derivative_attributes[index][:-1]: temp=("%s%s_%d_%s,"%(temp,d.name,index,o_a))
        temp=("%s%s_%d_%s,&o_a_%d);"%(temp,d.name,index,self.derivative_attributes[index][-1],index))
        output_list.append(temp)
    
    ##Thread calculation loop
    output_list.append("//**Thread Calculation Loop**")
    
    for r in range(len(self.derivative)):
        output_list.append("double temp_total_%d=0;"%r)
    
    temp="double dummy_2"
    for d in self.derivative:
        index = self.derivative.index(d)
        for u in d.underlying:
            u_index = self.underlying.index(u)
            temp=("%s,price_%d_%d,next_time_%d_%d"%(temp,index,u_index,index,u_index))
            
    for u in self.underlying:
        u_index = self.underlying.index(u)
        temp=("%s,very_next_time_%d"%(temp,u_index))
            
    temp = "%s;"%temp
    output_list.append(temp)
    
    output_list.append("int l,k,done;")
    output_list.append("double ")
    for d in self.derivative:
      index = self.derivative.index(d)
      if(index<(len(self.derivative)-1)): output_list[-1] = ("%stemp_value_sqrd_%d,"%(output_list[-1],index))
      elif(index==(len(self.derivative)-1)): output_list[-1] = ("%stemp_value_sqrd_%d;"%(output_list[-1],index))
    output_list.append("for(l=0;l<temp_data->thread_paths;l++){")
    
    output_list.append("//***Underlying and Derivative Path Initiation***")
    for u in self.underlying: 
        index = self.underlying.index(u)
        output_list.append("%s_underlying_path_init(&u_v_%d,&u_a_%d);" % (u.name,index,index))
    
    
    for d in self.derivative:
        index = self.derivative.index(d)
        output_list.append("%s_derivative_path_init(&o_v_%d,&o_a_%d);" % (d.name,index,index))
        for u in d.underlying:
            u_index = self.underlying.index(u)
            output_list.append("next_time_%d_%d = 0;"%(index,u_index))
            output_list.append("price_%d_%d = u_a_%d.current_price*exp(u_v_%d.gamma);"%(index,u_index,u_index,u_index))
    
    
    output_list.append("done=1;")
    output_list.append("while(done){")
    output_list.append("//***Derivative Path Function Calls***")
    for d in self.derivative: #calling the derivative path function
        index = self.derivative.index(d)
        output_list.append("if(")
        for u in d.underlying:
            u_index = self.underlying.index(u)
            output_list.append("(next_time_%d_%d==u_v_%d.time) && (u_v_%d.time<=o_a_%d.time_period) &&"%(index,u_index,u_index,u_index,index))
        output_list.append(" 1){")
        
        for u in d.underlying:
            u_index = self.underlying.index(u)
            output_list.append("price_%d_%d = u_a_%d.current_price*exp(u_v_%d.gamma);"%(index,u_index,u_index,u_index))
           
        output_list.append("%s_derivative_path(price_%d_%d,u_v_%d.time,&o_v_%d,&o_a_%d);" % (d.name,index,u_index,u_index,index,index)) #TODO - Some clever introspection to determine the composition of the call
        
        for u in d.underlying:
            u_index = self.underlying.index(u)
            output_list.append("next_time_%d_%d = u_v_%d.time + o_v_%d.delta_time;" % (index,u_index,u_index,index))
        output_list.append("}")
    
    
    output_list.append("//***Determining Next Times for Underlyings***")
    for u in self.underlying: 
        u_index = self.underlying.index(u)
        output_list.append("if((u_v_%d.time<o_a_%d.time_period)){"%(u_index,self.underlying_dependencies[u_index][0])) #setting very next time to the first active next time point
        output_list.append("very_next_time_%d=next_time_%d_%d;"%(u_index,self.underlying_dependencies[u_index][0],u_index))
        output_list.append("}")
        if(len(self.underlying_dependencies[u_index])>1): 
            for u_l in self.underlying_dependencies[u_index][1:]:
                output_list.append("if((u_v_%d.time<o_a_%d.time_period)&&(next_time_%d_%d<very_next_time_%d)){"%(u_index,u_l,u_l,u_index,u_index))
                output_list.append("very_next_time_%d=next_time_%d_%d;"%(u_index,u_l,u_index))
                output_list.append("}")
        
    output_list.append("//***Assesing whether loop is complete or not***")
    output_list.append("if(1")
    for d in self.derivative:
        index = self.derivative.index(d)
        for u in d.underlying:
            u_index = self.underlying.index(u)
            output_list.append(" && (u_v_%d.time>=o_a_%d.time_period)"%(u_index,index)) 
    output_list.append("){") #ending the loop if all underlyings are passed the time required by the derivatives
    output_list.append("done=0;")
    output_list.append("}")
    
    output_list.append("//***Calling Underlying Path Functions***")
    for u in self.underlying: #Calling the underlying path function
        u_index = self.underlying.index(u)
        output_list.append("if(u_v_%d.time<very_next_time_%d){"%(u_index,u_index))
        
        output_list.append("%s_underlying_path((very_next_time_%d-u_v_%d.time),&u_v_%d,&u_a_%d);" % (u.name,u_index,u_index,u_index,u_index))
        
        output_list.append("}")
    
    output_list.append("}") #End of Path Generation Loop
    
    output_list.append("//**Post path-generation calculations**")
    
    for d in self.derivative: #Post path-generation calculations
        index = self.derivative.index(d)
        for u in d.underlying:
            u_index = self.underlying.index(u)
            
            output_list.append("%s_derivative_payoff(price_%d_%d,&o_v_%d,&o_a_%d);"%(d.name,index,u_index,index,index))
            output_list.append("temp_total_%d += o_v_%d.value;"%(index,index))
            output_list.append("temp_value_sqrd_%d += pow(o_v_%d.value,2);"%(index,index))
            
    output_list.append("}")
    ##Calculating standard error
    for d in self.derivative:
      index = self.derivative.index(d)
      output_list.append("double temp_sample_std_dev_%d = pow((temp_value_sqrd_%d/temp_data->thread_paths-pow(temp_total_%d/temp_data->thread_paths,2))/(temp_data->thread_paths-1),0.5);"%(index,index,index))
      output_list.append("double temp_sample_std_error_%d = 1.96*temp_sample_std_dev_%d/pow(temp_data->thread_paths,0.5);"%(index,index))
      output_list.append("printf(\"%%f\\n\",temp_sample_std_error_%d);"%(index))
    ##Return result to main loop
    output_list.append("//**Returning Result**")
    for d in self.derivative: output_list.append("temp_data->thread_result[%d] = temp_total_%d;"%(self.derivative.index(d),self.derivative.index(d)))
    output_list.append("}")
    
      
    return output_list
  
  def compile(self,overide=True):
    try:
      os.chdir("..")
      os.chdir(self.platform.platform_directory())
      
    except:
      os.chdir("bin")
      return "Multicore C directory doesn't exist!"
    
    if(overide or not os.path.exists("%s"%self.output_file_name)):
        compile_cmd = ["g++","%s.c"%self.output_file_name]
        
        #Including all of the derivative and option classes that are used
        temp = []
        for u in self.underlying:
            if(not(u.name in temp)):
                compile_cmd.append(("%s.c" % u.name))
                temp.append(u.name)
            
            base_list = []
            self.generate_base_class_names(u.__class__,base_list)
            base_list.remove("underlying")
        
            for b in base_list:
                if(b not in temp):
                    compile_cmd.append(("%s.c" % b))
                    temp.append(b)
            
        for d in self.derivative:
            if(not(d.name in temp)):
                compile_cmd.append(("%s.c" % d.name))
                temp.append(d.name)
                
            base_list = []
            self.generate_base_class_names(d.__class__,base_list)
            base_list.remove("option")
                
            for b in base_list:
                if(b not in temp):
                    compile_cmd.append(("%s.c" % b))
                    temp.append(b) 
        
        #Including all of the non system libraries used
        #for u_l in self.non_system_libraries:
            #if(not(("%s.c" % u_l) in compile_cmd)): compile_cmd.append(("%s.c" % u_l))
            
        #Output flag
        compile_cmd.append("-o")
        compile_cmd.append(self.output_file_name)
        
        #Linking pthread library
        compile_cmd.append("-lpthread")
        
        #Optimisation Level 3
        compile_cmd.append("-O3")
        compile_cmd.append("-w")
        
        #SSE
        compile_cmd.append("-msse3")
        
        #Fast Math
        compile_cmd.append("-ffast-math")
        
        #print compile_cmd
        result = subprocess.check_output(compile_cmd)
        #print subprocess.check_output("pwd")
        os.chdir(self.platform.root_directory())
        os.chdir("bin")
        
        return result
      
    else:
      print "multicore binary already exists, using previous version. Set overide to True if you would like to force the code to be recompiled"
      os.chdir(self.platform.root_directory)
      os.chdir("bin")
          
  def execute(self,cleanup=False):
    try:
      os.chdir("..")
      os.chdir(self.platform.platform_directory())
    except:
      os.chdir("bin")
      return "Multicore C directory doesn't exist!"

    run_cmd = ["./%s"%self.output_file_name]
    for k in self.solver_metadata.keys(): run_cmd.append(str(self.solver_metadata[k])) 
    
    index = 0
    for u_a in self.underlying_attributes:
        for a in u_a: run_cmd.append(str(self.underlying[index].__dict__[a])) #mirrors generation code to preserve order of variable loading
        index += 1
    
    index = 0
    for o_a in self.derivative_attributes: 
        for a in o_a: run_cmd.append(str(self.derivative[index].__dict__[a]))
        index +=1
    
    start = time.time() #Wall-time is measured by framework, not the generated application to measure overhead in calling code
    results = subprocess.check_output(run_cmd)
    finish = time.time()
    
    results = results.split("\n")[:-1]
    results.append((finish-start)*1000000)
    
    os.chdir(self.platform.root_directory())
    os.chdir("bin")
    
    if(cleanup): self.cleanup()
    
    return results
  
  def cleanup(self):
    os.chdir("..")
    os.chdir(self.platform.platform_directory())
    
    subprocess.call(["rm","%s.c"%self.output_file_name])
    subprocess.call(["rm","%s"%self.output_file_name])
  
  def generate_source(self,code_string,name_extension=".c",verbose=False):
    os.chdir("..")
    os.chdir(self.platform.platform_directory())
    
    output_file = open("%s%s"%(self.output_file_name,name_extension),"w")
    tab_count = 0;
    for c_s in code_string:
        if("*" in c_s and "//" in c_s):
          output_file.write("\n") #Insert a blank line if the line is a comment section
          
          if(verbose and "**" in c_s):
            for i in range(tab_count): output_file.write("\t")	#Tabify the code
            output_file.write("printf(\"%s\\n\");\n"%c_s.strip("/")) #If verbose, print out comment to help locate errors
        
        for i in range(tab_count): output_file.write("\t")	#Tabify the code
        output_file.write("%s\n"%c_s)
            
        if("{" in c_s): tab_count = tab_count+1
        if("}" in c_s): tab_count = max(tab_count-1,0)
    output_file.close()
    
    os.chdir(self.platform.root_directory())
    os.chdir("bin")
  
  def generate_base_class_names(self,tempclass,templist):
    """Another Helper Method, uses to help pull in various super classes during compilation """
    if(tempclass.name not in templist): templist.append(tempclass.name)
    for b in tempclass.__bases__: self.generate_base_class_names(b,templist)