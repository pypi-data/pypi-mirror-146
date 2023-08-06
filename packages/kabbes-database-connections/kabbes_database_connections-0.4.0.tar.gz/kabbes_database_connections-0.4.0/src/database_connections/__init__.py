from . import TJEncryptPassword
from . import password_encryption
from .Query import Query
from .DatabaseConnection import DatabaseConnection
from . import sql_support_functions

import dir_ops as do
import os

_Dir = do.Dir( os.path.abspath( __file__ ) ).ascend()   #Dir that contains the package 
_src_Dir = _Dir.ascend()                                  #src Dir that is one above
_repo_Dir = _src_Dir.ascend()                    
_cwd_Dir = do.Dir( do.get_cwd() )
