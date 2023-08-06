import pyathena
import pandas as pd
from database_connections.DatabaseConnection import DatabaseConnection


def get_DatabaseConnection( **kwargs ):

    '''returns the class instance of the said object'''
    return Athena( **kwargs )

class Athena( DatabaseConnection ):

    '''Need the following attributes to be stored:
    aws_conn_params = { 'aws_access_key_id'     : 'XXXXXX',
                        'aws_secret_access_key' : 'XXXXXX',
                        'aws_session_token'     : 'XXXXXX',
                        'N # of other params'   : 'XXXXXX',
                        'region_name'           : 'us-east-1',
                        'work_group'            : 
                        's3_staging_dir'        : 
                        }'''

    def __init__( self, **kwargs ):

        DatabaseConnection.__init__( self, **kwargs)

    def get_conn( self, **kwargs ):

        self.conn = pyathena.connect( **self.aws_conn_params )

    def write( self, **kwargs ):

        print ('Writing to S3 is not possible through Athena')

