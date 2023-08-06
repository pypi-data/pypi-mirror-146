from databricks import sql #from pypi package: databricks-sql-connector
import py_starter as ps
from database_connections.DatabaseConnection import DatabaseConnection

def get_DatabaseConnection( **kwargs ):

    '''returns the class instance of the said object'''
    return Databricks( **kwargs )

class Databricks( DatabaseConnection ):

    '''To run the Databricks module, you need to set the following attributes:

    server_hostname
    http_path
    access_token
    '''

    def __init__( self, **kwargs ):

        DatabaseConnection.__init__( self, **kwargs)

    def init( self, **kwargs ):

        self.set_atts( kwargs )
        self.get_conn()
        # skip getting cursor since Databricks doesn't have one

    def get_conn( self, **kwargs ):

        default_kwargs = {
            'server_hostname': self.server_hostname,
            'http_path': self.http_path,
            'access_token': self.access_token
        }

        joined_kwargs = ps.merge_dicts( default_kwargs, kwargs )

        self.conn = sql.connect( **joined_kwargs )





