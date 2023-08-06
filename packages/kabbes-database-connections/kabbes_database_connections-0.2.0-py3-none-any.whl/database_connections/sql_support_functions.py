import dir_ops.dir_ops as do
import py_starter.py_starter as ps
import os
import database_connections.Query as Query

script_Path = do.Path( os.path.abspath(__file__) )
sql_Dir = script_Path.ascend() 

def get_DatabaseConnection( connection_module = 'teradata', **kwargs ):

    '''returns a class object from the given SQL connection module'''

    # list out the options available in the SQL folder: Oracle, Redshift, SQLite, Teradata
    module_options_Dirs = sql_Dir.list_contents_Paths( block_dirs = False, block_paths = True )

    for module_options_Dir in module_options_Dirs:
        if module_options_Dir.dirs[-1].lower() == connection_module.lower():
            module = ps.import_module_from_path( module_options_Dir.join( module_options_Dir.dirs[-1] + '_connection.py' ))
            return module.get_DatabaseConnection( **kwargs )

    return None

def list_to_string( iterable, sep = ',', quotes = "'" ):

    """Given a list [ 'meter1', 'meter2', 'meter3' ] spits out  '1234','2345','3456'"""

    item_separator = quotes + sep + quotes
    string = quotes + item_separator.join( iterable ) + quotes

    return string

def run_queries_in_folder( queries_Dir, export_Dir, engine = 'teradata', export_type = 'csv', ask_to_run = True, print_df = True, parquet_engine = 'fastparquet', conn_inst = None, **connection_module_params ):

    sql_types = ['sql']
    sql_Paths = queries_Dir.list_contents_Paths( block_dirs = True )

    if conn_inst == None:
        conn_inst = get_DatabaseConnection( connection_module = engine, **connection_module_params )
    conn_inst.init()

    ### only select queries which have correct endings
    for i in range(len(sql_Paths)-1,-1,-1):
        sql_Path = sql_Paths[i]
        if sql_Path.ending.lower() not in sql_types:
            del sql_Paths[i]

    sql_paths = [ i.path for i in sql_Paths ]

    ### Ask the users which queries which they want to run
    inds_to_run = list(range(len(sql_Paths)))
    if ask_to_run:
        inds_to_run = ps.get_user_selection_for_list_items(sql_paths, prompt = 'Select which queries to run - enter to exit', print_off = True)

    ### Execute the queries
    for i in inds_to_run:
        sql_Path = sql_Paths[i]
        export_Path = do.Path( export_Dir.join( sql_Path.root + '.' + export_type ) )

        export_kwargs = {}
        if export_Path.ending == 'parquet':
            export_kwargs['engine'] = parquet_engine

        sql_Query = Query.Query( query_Path = sql_Path, export_Path = export_Path, conn_inst = conn_inst )
        sql_Query.query()
        sql_Query.export( **export_kwargs )

        if print_df:
            sql_Query.df

    # close out of the connection
    conn_inst.exit()
