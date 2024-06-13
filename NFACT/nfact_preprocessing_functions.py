import os

def read_file_to_list(filename: str) -> list:
    
    """
    Function to dump output of file to
    list format.

    Parameters
    ----------
    filename: str
        path to file
    
    Returns
    -------
    list: list of subjects
        list of path to subjects directories
    """

    with open(filename, 'r') as file:
      lines = file.readlines()
    return [sub.rstrip() for sub in lines]

def create_paths(args):
    paths = {}
    base_path = args['study_folder']
    for path in args.keys():
        print(args[path], print(type(args[path])))



def check_paths_exists(paths) -> bool:
    return os.path.exists()