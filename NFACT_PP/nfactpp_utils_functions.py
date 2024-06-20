import os
import signal
from datetime import datetime
import glob

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


def error_and_exit(bool_statement: bool, error_message=None):
    """
    Function to exit out of script
    with error message if bool statement
    is false
    """
    if not bool_statement:
        if error_message:
            col = colours()
            print(col["red"] + error_message + col["reset"])
        print("Exiting...")
        exit(1)


class Signit_handler:
    """
    A signit handler class. Will kill. Exits
    programme safely.
    """

    def __init__(self) -> None:
        self.register_handler()

    def register_handler(self) -> None:
        """
        Method to registers the SIGINT handler.
        """
        signal.signal(signal.SIGINT, self.handle_sigint)

    def handle_sigint(self, sig, frame) -> None:
        """
        Method that handles the SIGINT signal (Ctrl+C)

        Parameters
        -----------
        sig: The signal number
        frame: The current stack frame
        """
        print("\nUser killed script (Ctrl+C). Terminating...")
        print("Exiting...")
        exit(0)


def date_for_filename() -> str:
    """
    Function to get the
    date and time in format
    useful for a file name.

    Parameters
    ----------
    None

    Returns
    -------
    str: string
        string of datetime object
    """
    now = datetime.now()
    return now.strftime("%Y_%m_%d_%H_%M_%S")

def hcp_files(list_of_subjects: list) -> dict:
    """
    Function to return
    HCP standard seed, ROI
    and warps. Also checks that they exist

    Parameters
    ----------
    None

    Returns
    -------
    dict: dictionary object
        dict of seeds, ROIS and warps
    """
    

    for sub in list_of_subjects:
        subject = os.path.basename(sub)
        seeds = glob.glob(os.path.join(sub, f'MNINonLinear/fsaverage_LR32k/*.white.32k_fs_LR.surf.gii'))
        seed = [seeds[0], seeds[1]]
        if not seed:
            error_and_exit(False, f"Cannot find seed files for {subject}")
        
        rois = glob.glob(os.path.join(sub, f'MNINonLinear/fsaverage_LR32k/*.atlasroi.32k_fs_LR.shape.gii'))
        rois = [rois[0], rois[1]]
        if not rois:
            error_and_exit(False, f"Cannot find ROI files for {subject}")
        
        warp = [os.path.join(sub, 'MNINonLinear/xfms/standard2acpc_dc.nii.gz'), 
                os.path.join(sub, 'MNINonLinear/xfms/acpc_dc2standard.nii.gz')]
        [error_and_exit(os.path.exists(path), f"Unable to find {path}") for path in warp]
    return {
        "seed": seed,
        "rois": rois,
        "warps": warp,
    }