import cx_Oracle
from database_connections import password_encryption
from database_connections.DatabaseConnection import DatabaseConnection

def get_DatabaseConnection( **kwargs ):

    '''returns the class instance of the said object'''
    return Oracle( **kwargs )

class Oracle( DatabaseConnection ):

    '''To run the Oracle module, you need to set the following attributes:

    dsn 
    username 
    passkey_path
    encpass_path

    or

    host 
    port 
    sid  
    username 
    passkey_path
    encpass_path

    '''

    def __init__( self, **kwargs ):

        DatabaseConnection.__init__( self, **kwargs)

    def init(self, **kwargs):

        self.set_atts( kwargs )
        self.get_password()
        self.get_dsn()
        self.get_conn()
        self.get_cursor()
        self.print_atts()

    def get_password(self):

        '''get password by custom decrypting '''

        if not self.has_attr( 'password' ):
            self.password = password_encryption.custom_decrypt( self.passkey_path, self.encpass_path )

    def get_conn( self, **kwargs ):

        '''get the connection to cx_Oracle'''

        self.conn = cx_Oracle.connect( user = self.username, password = self.password, dsn=self.dsn, **kwargs )
        #(user=None, password=None, dsn=None, mode=None, handle=None, pool=None, threaded=False, events=False, cclass=None, purity=None, newpassword=None, encoding=None, nencoding=None, edition=None, appcontext=[], tag=None, matchanytag=None, shardingkey=[], supershardingkey=[])

    def get_dsn( self ):

        '''make a dsn connection if one doesnt exist'''

        if 'dsn' not in vars(self):

            possible_kwargs = ['sid','service_name','region','sharding_key','super_sharding_key']
            dsn_kwargs = {}
            for att in vars(self):
                if att in possible_kwargs:
                    dsn_kwargs[att] = vars(self)[att]

            self.dsn = cx_Oracle.makedsn( self.host, self.port, **dsn_kwargs )

    def get_all_tables( self ):

        '''returns a list of all available table names'''

        string = """select * from all_tables"""

        df = self.query( query_string = string )
        return list( df['TABLE_NAME'] )

    def create_generic_select( self, table_name, top = None ):

        '''returns a string with a generic select'''

        string = 'SELECT * FROM ' + str(table_name)

        if top != None:
            string += 'WHERE ROWNUM <= ' + str(top)

        return string

