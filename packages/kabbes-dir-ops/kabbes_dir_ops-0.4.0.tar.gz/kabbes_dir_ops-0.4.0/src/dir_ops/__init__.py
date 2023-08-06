from .dir_ops import *
import os

_Dir = Dir( os.path.abspath( __file__ ) ).ascend()   #Dir that contains the package 
_src_Dir = _Dir.ascend()                                  #src Dir that is one above
_repo_Dir = _src_Dir.ascend()                    
_cwd_Dir = dir_ops.Dir( dir_ops.get_cwd() )

