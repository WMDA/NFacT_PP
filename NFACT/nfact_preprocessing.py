from NFACT.nfact_preproc_arguments import args
import NFACT.nfact_file_checking_functions as nff
from NFACT.nfactpp_run_functions import make_directory, build_xtract_arguments
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
    if not nff.check_study_folder(arg["study_folder"]):
        exit(1)

    if arg["list_of_subjects"]:
        if not nff.does_list_of_subjects_exist(arg["list_of_subjects"]):
            exit(1)
        arg["list_of_subjects"] = nff.return_list_of_subjects_from_file(
            arg["list_of_subjects"]
        )
        if not arg["list_of_subjects"]:
            exit(1)

    if not arg["list_of_subjects"]:
        arg["list_of_subjects"] = nff.list_of_subjects_from_directory(
            arg["study_folder"]
        )
        if not arg["list_of_subjects"]:
            print("Unable to find list of subjects from directory")
            print("Exiting...")
            exit(1)

    if not nff.check_subject_files(arg):
        print("\nExiting...\n")
        exit(1)
    
    if not nff.check_fsl_is_installed():
        print("\nExiting...\n")
        exit(1)
    
    print("Number of subjects: ", len(arg["list_of_subjects"]))
    for sub in arg["list_of_subjects"]:
        print("working on: ", os.path.basename(sub))
        config_directory_path = os.path.join(sub, '.pp_config')
        directory_created = make_directory(config_directory_path)
        
        if not directory_created:
            print("\nExiting...\n")
            exit(1)

        command = build_xtract_arguments(arg, sub)
        command.append(config_directory_path)
        print(command)

        try:
            run = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as error:
            print('Error in calling Xtract blueprint: ', error)
            print("\nExiting...\n")
            exit(1)

        if run.returncode != 0:
            col = nff.colours()
            error_code = re.sub(r'.rror:', '', run.stderr.decode("utf-8"))
            print(f'{col["red"]}Error in xtract blueprint: {error_code}{col["reset"]}')
            print("\nExiting...\n")
            exit(1)


if __name__ == "__main__":
    main_nfact_preprocess()
