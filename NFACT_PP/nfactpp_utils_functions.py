import os
import signal
from datetime import datetime
import glob


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
    return {
        "reset": "\033[0;0m",
        "red": "\033[1;31m",
        "pink": "\033[1;35m",
        "purple": "\033[38;5;93m",
        "darker_pink": "\033[38;5;129m",
    }


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
        print("Exiting...\n")
        exit(1)


class Signit_handler:
    """
    A signit handler class. Will kill. Exits
    programme safely.
    """

    def __init__(
        self,
    ) -> None:
        self.register_handler()
        self.suppress_messages = False

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
        if not self.suppress_messages:
            col = colours()
            print(
                f"\n{col['darker_pink']}Recieved kill signal (Ctrl+C). Terminating..."
            )
            print(f"Exiting...{col['reset']}\n")
        exit(0)

    @property
    def get_suppress_messages(self):
        """
        Getter method for suppress_messages
        """
        return self.suppress_messages

    @get_suppress_messages.setter
    def set_suppress_messages(self, value: bool) -> None:
        """
        Setter for suppress_messages
        """
        self.suppress_messages = value


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


def hcp_get_seeds(sub: str) -> list:
    """
    Function to get HCP stream seeds

    Parameters
    ----------
    sub: str
        string of subject

    Returns
    -------
    seeds: list
       list of seeds
    """
    seeds = glob.glob(
        os.path.join(sub, f"MNINonLinear/fsaverage_LR32k/*.white.32k_fs_LR.surf.gii")
    )
    subject = os.path.basename(sub)
    error_and_exit(seeds, f"Cannot find seed files for {subject}")
    return seeds


def hcp_get_rois(sub: str) -> list:
    """
    Function to get HCP stream ROIS

    Parameters
    ----------
    sub: str
        string of subject

    Returns
    -------
    rois: list
       list of rois
    """
    rois = glob.glob(
        os.path.join(
            sub, f"MNINonLinear/fsaverage_LR32k/*.atlasroi.32k_fs_LR.shape.gii"
        )
    )
    subject = os.path.basename(sub)
    error_and_exit(rois, f"Cannot find seed files for {subject}")
    return rois


def hcp_reorder_seeds_rois(seeds: list, rois: list) -> dict:
    """
    Function to return seeds and rois
    in same order.

    Parameters
    ----------
    seeds: list
        a list of seeds
    rois: list
        a list of rois

    Returns
    -------
    dict: dict
        dictionary of left/right
        hemisphere seed and ROI

    """
    left_seed = [seed for seed in seeds if "L.white" in seed][0]
    right_seed = [seed for seed in seeds if "R.white" in seed][0]
    left_rois = [roi for roi in rois if "L.atlasroi" in roi][0]
    right_rois = [roi for roi in rois if "R.atlasroi" in roi][0]

    return {"left": [left_seed, left_rois], "right": [right_seed, right_rois]}


def update_seeds_file(file_path: str) -> None:
    """
    Function to update file extension
    in seeds.txt. Updates surface asc to
    gii.

    Parameters
    ----------
    file_path: str
        string to file path

    Returns
    -------
    None
    """
    try:
        with open(file_path, "r") as file:
            content = file.read()
            update_extensions = content.replace(".asc", ".gii")
        with open(file_path, "w") as file:
            file.write(update_extensions)
    except Exception as e:
        error_and_exit(False, f"Unable to change seeds file due to {e}")
