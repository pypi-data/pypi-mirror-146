import py_starter.py_starter as ps
import dir_ops.dir_ops as do
import database_connections.sql_support_functions as ssf
from parent_class import ParentClass
import os 

default_query_filename = 'query.sql'
default_export_suffix = '_export'
default_export_extension = '.csv'

class Query( ParentClass ):

    '''
    A Python class for SQL Queries
    Query class is agnostic of engine
    '''

    def __init__( self, string = '', query_path = '', export_path = '', engine = 'teradata', query_Path = None, export_Path = None, conn_inst = None, **connection_module_params):

        ParentClass.__init__( self )

        ### make sure there is at least something to make a query
        if string == '' and query_path == '' and not do.Path.is_Path(query_Path):
            print ('Not enough info to make a Query Class')
            exit()

        ### query string takes priority over everything else
        if string != '':
            self.string = string

            if not do.Path.is_Path( query_Path ):
                if query_path != '':
                    self.query_Path = do.Path( os.path.abspath(query_path))
                else:
                    self.query_Path = do.Path ( do.Dir(do.get_cwd()).join( default_query_filename ))
                    self.get_unique_query_Path()

            else:
                self.query_Path = query_Path

        ### if no string is provided, read the contents of the .sql path
        else:
            if not do.Path.is_Path( query_Path ):
                self.query_Path = do.Path( os.path.abspath(query_path))
            else:
                self.query_Path = query_Path

            self.read_string_from_path()

        ### if no export_Path is given, make your own
        if not do.Path.is_Path( export_Path ):
            if export_path != '':
                self.export_Path = do.Path( os.path.abspath(export_path) )
            else:
                self.export_Path = do.Path ( do.Dir(self.query_Path.ascend()).join( self.query_Path.root + default_export_suffix + default_export_extension  ) )
                self.get_unique_export_Path()
        else:
            self.export_Path = export_Path

        ### Set the connection instance class
        if conn_inst == None:
            self.engine = engine
            self.conn_inst = ssf.get_DatabaseConnection(connection_module = engine, **connection_module_params)

        else:
            self.conn_inst = conn_inst
            self.engine = conn_inst.type

    def read_string_from_path( self ):

        '''read the contents of the filepath'''
        self.string = ps.read_text_file( self.query_Path.p )

    def print_imp_atts( self, print_off = True ):

        return self._print_imp_atts_helper( atts = ['string','query_Path','export_Path','engine'] )

    def print_one_line_atts( self, print_off = True, leading_string = '\t' ):

        return self._print_one_line_atts_helper( atts = ['type','query_Path','engine'], print_off = print_off, leading_string = leading_string )

    def get_unique_query_Path( self ):

        '''make sure the query Path is unique'''

        parent_Dir = self.query_Path.ascend()
        self.query_Path = parent_Dir.get_unique_Path( self.query_Path.filename ) 

    def get_unique_export_Path( self ):

        '''make sure the export Path is unique'''

        parent_Dir = self.export_Path.ascend()
        self.export_Path = parent_Dir.get_unique_Path( self.export_Path.filename ) 

    def save( self ):

        '''using the query string, export to query_Path'''
        ps.write_text_file( self.query_Path.p, string = self.string )

    def query( self, export = False, **kwargs ):

        '''run the query using the module.query(), returns pandas DataFrame'''

        print ('Executing Query: ' + self.string[: min(15, len(self.string)) ] + '...')
        self.df = self.conn_inst.query( query_string = self.string, **kwargs )

        if export:
            self.export()

        return self.df

    def execute( self ):

        '''execute a command / statement '''

        self.conn_inst.execute( self.string )

    def export( self, **kwargs ):

        '''export the df returned by the query to given export_Path'''

        print ('Exporting DataFrame to Path')
        self.export_Path.print_atts()

        if self.export_Path.ending.lower() == 'csv':

            default_kwargs = {'index': False}
            kwargs = ps.replace_default_kwargs( default_kwargs, **kwargs )
            self.df.to_csv( self.export_Path.p, **kwargs )

        elif self.export_Path.ending.lower() == 'parquet':

            self.df.to_parquet( self.export_Path.p, **kwargs )

        else:
            print ('No directions for exporting file with ending: ' + str(self.export_Path.ending))

