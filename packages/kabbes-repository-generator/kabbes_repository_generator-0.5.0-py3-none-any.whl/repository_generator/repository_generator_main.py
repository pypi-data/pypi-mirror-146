import dir_ops as do
import py_starter as ps
import repository_generator

def get_template():

    #list_contents_Paths()
    module_Dirs = repository_generator.templates_Dir.list_contents_Paths( block_paths=True,block_dirs=False )
    module_Dir = ps.get_selection_from_list( module_Dirs )
    module_Path = do.Path( module_Dir.join( module_Dir.dirs[-1] + '.py' ) )

    module = module_Path.import_module()
    return module.Repository

def generate( *args ):
    
    Repo_template = get_template()
    R = Repo_template( repository_generator._cwd_Dir )
    R.generate( overwrite = "overwrite" in args )

