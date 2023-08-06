from parent_class import ParentClass
import dir_ops as do
import py_starter as ps

import pandas as pd

class DatabaseConnection( ParentClass ):

    '''extra keyword agrugments will be set according to each SQL service's requirements
    This class should only be used as a parent class for other specific sql services
    '''

    def __init__(self, **kwargs):

        ParentClass.__init__( self )
        self.set_atts( kwargs )

        if len(kwargs) != 0: #if the user passed arguments, initialze
            self.init()

    def init( self, **kwargs ):

        '''sets attributes, gets connection, and prints attributes'''

        self.set_atts( kwargs )
        self.get_conn()
        self.get_cursor()

    def print_all_atts( self, print_off = True ):

        '''Print off all Class instance attributes'''

        atts = list(vars(self))
        to_add = ''
        if 'password' in atts:
            atts.remove( 'password' )
            to_add += 'password:\t********'

        all_atts = self.print_atts_helper( atts = atts, print_off = False, show_class_type = True ) + '\n'
        all_atts += to_add

        return self.print_string( all_atts, print_off = print_off )

    def print_imp_atts( self, **kwargs ):

        return self._print_imp_atts_helper( atts = ['type','conn'], **kwargs )

    def print_one_line_atts( self, **kwargs ):

        return self._print_one_line_atts_helper( atts = ['type','conn'], **kwargs )

    def exit( self ):

        ''' '''
        pass

    def get_cursor( self, **kwargs ):

        '''get the cursor from the connection'''

        self.cursor = self.conn.cursor( **kwargs )

    def query( self, query_string = '', query_file = None, **kwargs ):

        '''query the connection via the string or file'''

        if query_file != None and query_string == '':
            query_string = ps.read_text_file( query_file )

        df = pd.read_sql(query_string, self.conn, **kwargs )
        return df

    def execute( self, string, **kwargs ):

        '''execute the given string'''

        self.cursor.execute( string, **kwargs )

    def write( self, df, table_name, **kwargs ):

        '''given the pandas DF, table_name, and other kwargs, write to database connection '''

        default_kwargs = {
        'index': False,
        'if_exists': 'replace'}
        kwargs = ps.replace_default_kwargs( default_kwargs, **kwargs )

        df.to_sql( table_name, self.conn, **kwargs )
