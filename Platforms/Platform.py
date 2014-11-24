'''
Created on 23 November 2014
'''
import os,sys

class Platform:
    name = "platform"
    platform_directory_string = ""
    root_directory_string = ""
    
    def __init__(self,platform_directory_string=None,root_directory_string=None):
        self.platform_directory_string = platform_directory_string
        self.root_directory_string = root_directory_string
        
        #incase the environmental variable isn't set
        if not(self.root_directory_string):
            try: self.root_directory_string = os.environ["F3_ROOT"]
            except KeyError:
                print("F3_ROOT environmental variable not set")
                sys.exit(1)
        
    def platform_directory(self):
        return self.platform_directory_string
  
    def root_directory(self):
        return self.root_directory_string