from NFACT.nfact_preproc_arguments import args
import NFACT.nfact_file_checking_functions as nff
from NFACT.nfactpp_run_functions import run_xtract_blueprint

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
    run_xtract_blueprint(arg)

if __name__ == "__main__":
    main_nfact_preprocess()
