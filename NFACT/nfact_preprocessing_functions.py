import os
import glob

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

    with open(filename, "r") as file:
        lines = file.readlines()
    return [sub.rstrip() for sub in lines]


def create_paths(args):
    paths = {}
    base_path = args["study_folder"]
    for path in args.keys():
        print(args[path], print(type(args[path])))


def check_paths_exists(paths) -> bool:
    return os.path.exists()

def directory_contains_subjects(study_folder_path: str) -> bool:
    """
    Function to check that study directory contains
    subjects

    Parameters
    ---------
    study_folder_path: str
        study folder path
    
    Returns
    -------
    bool: boolean
       True if it does else
       False and error messages
    """
    content = [direct for direct in 
               os.listdir(study_folder_path) 
               if os.path.isdir(
                   os.path.join(study_folder_path, 
                                direct))]
    if not content:
        print('Study folder is empty')
        print("Exiting...")
        return False
    return True

def check_study_folder_is_dir(study_folder_path: str) -> bool:
    """
    Function to check that study folder is a
    direcotry

    Parameters
    ----------
    study_folder_path: str
        Study folder path
    
    Returns
    -------
    bool: boolean
       True if is 
       else prints error message and
       returns false
    """
    if not os.path.isdir(study_folder_path):
        print("Study folder provided is not a directory")
        print("Exiting...")
        return False

    return True

def check_study_folder_exists(study_folder_path: str) -> bool:
    """
    Function to check that study folder exists

    Parameters
    ----------
    study_folder_path: str
        Study folder path
    
    Returns
    -------
    bool: boolean
       True if does exist
       else prints error message and
       returns false
    """
    if not os.path.exists(study_folder_path):
        print("Study folder provided doesn't exist")
        print("Exiting...")
        return False

    return True

def check_study_folder(study_folder_path: str) ->bool:
    """
    Check that the study directory exists,
    is a directory and contains subjects

    Parameters
    ----------
    study_folder_path: str
        path to study directory
    
    Returns
    -------
    bool: boolean
       True if study folder passes 
       else prints error message and
       returns false
    """
    if not check_study_folder_exists(study_folder_path):
        return False
    if not check_study_folder_is_dir(study_folder_path):
        return False
    if not directory_contains_subjects(study_folder_path):
        return False
    return True

def does_list_of_subjects_exist(path_to_list: str) -> bool:
    """
    Function to check if list of subjects
    exists and isn't a directory.

    Parameters
    ----------
    path_to_list: str
        file path to list of subjects
    
    Returns
    -------
    bool: boolean
       True if list of subjects exists 
       else prints error message and
       returns false
    """

    if (not os.path.exists(path_to_list)) or (
        os.path.isdir(path_to_list)
    ):
        print("List of subjects doesn't exist.")
        print("Exiting...")
        return False 
        
    return True

def return_list_of_subjects_from_file(path_to_list: str) -> list:
    """
    Function to return list of subjects from a file

    Parameters
    ----------
    path_to_list: str
        path to subject directory

    Returns
    -------
    list_of_subjects: list
        list of subjects
    """
    # First check that list of subjects is a txt file.
    try: 
        if path_to_list.split(".")[1] != "txt":
            print("""List of subjects is not ascii file. 
                  Please specify a list of subject or remove flag""")
            print("Exiting...")
            return None
    # Hacky way to allow sub list not to have an extension
    except IndexError: 
         pass
        
    try:
        list_of_subjects = read_file_to_list(path_to_list)
    except Exception as e:
        print(f"Unable to open subject list due to: {e}")
    
    return list_of_subjects
    

def list_of_subjects_from_directory(study_folder: str) -> list: 
    """
    Function to get list of subjects from a directory
    if a list of subjects is not given

    Parameters
    ---------
    study_folder: str
       path to study folder
    
    Returns
    -------
    list: list object
        list of subjects
    """
    list_of_subject = glob.glob(os.path.join(study_folder, "*"))
    return [direct for direct in list_of_subject if os.path.isdir(direct)]