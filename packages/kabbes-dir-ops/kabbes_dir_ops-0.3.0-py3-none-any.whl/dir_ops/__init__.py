from . import dir_ops

import os
Dir = dir_ops.Dir( os.path.abspath( __file__ ) ).ascend()   #Dir that contains the package 
src_Dir = Dir.ascend()                                  #src Dir that is one above
repo_Dir = src_Dir.ascend()                    
cwd_Dir = dir_ops.Dir( dir_ops.get_cwd() )
