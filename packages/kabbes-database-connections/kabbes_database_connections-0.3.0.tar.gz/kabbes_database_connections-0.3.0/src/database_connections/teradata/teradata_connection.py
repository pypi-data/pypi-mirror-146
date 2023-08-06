import teradatasql
import pandas as pd
import py_starter.py_starter as ps

from database_connections.DatabaseConnection import DatabaseConnection

def get_DatabaseConnection( **kwargs ):

    '''returns the class instance of the said object'''
    return Teradata( **kwargs )

class Teradata( DatabaseConnection ):

    '''To run the teradata module, you need to set the following attributes:

    host        = 
    username    = 
    passkey_path= 'PassKey.properties'
    encpass_path= 'EncPass.properties'

    '''

    def __init__(self, **kwargs):

        DatabaseConnection.__init__( self, **kwargs)

    def init( self, **kwargs ):

        self.set_atts( kwargs )
        self.get_password()
        self.get_conn()
        self.print_atts()

    def get_conn( self, **kwargs ):

        default_kwargs = {
        'logmech' : 'LDAP',
        'log' : 8
        }
        joined_kwargs = ps.merge_dicts( default_kwargs, kwargs )

        self.conn = teradatasql.connect( host = self.host, user = self.username, password = self.sPassword, **joined_kwargs )

    def get_password( self ):

        self.sPassword = "ENCRYPTED_PASSWORD(file:{},file:{})".format (self.passkey_path, self.encpass_path)

    def query( self, query_string = '', query_file = None ):

        '''Teradata has special query method, so this class overwrites the parent class's method'''

        self.get_cursor()
        self.cursor.execute ('{fn teradata_nativesql}Driver version {fn teradata_driver_version}  Database version {fn teradata_database_version}')

        if query_file != None and query_string == '':
            query_string = ps.read_text_file( query_file )

        df = pd.read_sql(query_string, self.conn )
        return df

    def create_generic_select( self, table_name, top = None ):

        '''returns a string with a generic select'''

        string = 'SELECT '

        if top != None:
            string += str(' TOP ' + str(top) )

        string += ' * FROM ' + table_name
        return string

