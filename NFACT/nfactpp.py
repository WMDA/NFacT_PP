from NFACT.nfactpp_argument_functions import args
import NFACT.nfactpp_check_functions as nff
from NFACT.nfactpp_utils_functions import make_directory, error_and_exit
from NFACT.nfactpp_build_functions import build_xtract_arguments, write_options_to_file
import os
import subprocess
import re


def main_nfact_preprocess() -> None:
    """
    Main function for nfact PP

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    arg = args()
    
    # Error handling section
    error_and_exit(nff.check_study_folder(arg["study_folder"]))
    
    if arg["list_of_subjects"]:
        error_and_exit(nff.does_list_of_subjects_exist(arg["list_of_subjects"]),
                             "List of subjects doesn't exist.")

        arg["list_of_subjects"] = nff.return_list_of_subjects_from_file(
            arg["list_of_subjects"]
        )
        
        error_and_exit(arg["list_of_subjects"])


    if not arg["list_of_subjects"]:
        arg["list_of_subjects"] = nff.list_of_subjects_from_directory(
            arg["study_folder"]
        )

        error_and_exit(arg["list_of_subjects"],"Unable to find list of subjects from directory")
    
    error_and_exit(nff.check_subject_files(arg))
    error_and_exit(nff.check_fsl_is_installed(), 
                   "FSLDIR not in path. Check FSL is installed or has been loaded correctly")

    # looping over subjects and building out directories
    print("Number of subjects: ", len(arg["list_of_subjects"]))
    for sub in arg["list_of_subjects"]:
        print("working on: ", os.path.basename(sub))
        config_directory_path = os.path.join(sub, ".pp_config")
        directory_created = make_directory(config_directory_path)
        #write_options_to_file()
        if not directory_created:
            print("\nExiting...\n")
            exit(1)

        command = build_xtract_arguments(arg, sub)
        command.append(config_directory_path)
        print(command)
        # Running Xtract blueprint
        try:
            run = subprocess.run(
                command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError as error:
            print("Error in calling Xtract blueprint: ", error)
            print("\nExiting...\n")
            exit(1)

        if run.returncode != 0:
            error_code = re.sub(r".rror:", "", run.stderr.decode("utf-8"))
            error_and_exit(False, f"Error in xtract blueprint: {error_code}")


if __name__ == "__main__":
    main_nfact_preprocess()
