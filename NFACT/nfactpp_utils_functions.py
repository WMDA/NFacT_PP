import os


def add_file_path_for_images(arg: dict, sub: str) -> dict:
    """
    Function to add file path to
    images.

    Parameters
    ----------
    arg: dict
        dictionary of arguments from
        command line
    sub: str
        subjects full path
    """
    keys = ["seed", "warps", "rois"]
    image_files = {key: arg[key] for key in keys}
    for key, value in image_files.items():
        image_files[key] = [os.path.join(sub, val) for val in value]
    return image_files


def write_to_file(file_path: str, name: str, text: str) -> bool:
    """
    Function to write to file.

    Parameters
    ----------
    file_path: str
        abosulte file path to
        where file is created
    name: str
        name of file
    text: str
        string to add to file
    """
    try:
        with open(f"{file_path}/{name}", "w") as file:
            file.write(text)
    except Exception as e:
        print(f"Unable to write to {file_path}/{name} due to :", e)
        return False
    return True



def colours():
    """
    Function to print out text in colors

    Parameters
    ----------
    None

    Returns
    -------
    dict: dictionary object
        dictionary of color strings
    """
    return {"reset": "\033[0;0m", "red": "\033[1;31m"}

def make_directory(path: str) -> None:
    """
    Function to make a directory

    Parameters
    ----------
    path: str
        string to directory path

    Returns
    -------
    None
    """
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except Exception as e:
            print(e)
        return False
    return True

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

def error_and_exit(bool_statement: bool, 
          error_message=None):
    """
    Function to exit out of script
    with error message if bool statement
    is false
    """
    if not bool_statement:
        if error_message:
            col = colours()
            print(col['red']+ error_message + col['reset'])
        print("Exiting...")
        exit(1)
