import os
import subprocess
import re
import numpy as np

# NFACT functions
from NFACT_PP.nfactpp_argument_functions import args
import NFACT_PP.nfactpp_check_functions as nff
from NFACT_PP.nfactpp_utils_functions import (
    make_directory,
    error_and_exit,
    Signit_handler,
    date_for_filename,
)
from NFACT_PP.nfactpp_build_functions import (
    build_probtrackx2_arguments,
    write_options_to_file,
)


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
    handler = Signit_handler()
    arg = args()

    # Error handling section
    error_and_exit(nff.check_study_folder(arg["study_folder"]))
    if arg["list_of_subjects"]:
        error_and_exit(
            nff.does_list_of_subjects_exist(arg["list_of_subjects"]),
            "List of subjects doesn't exist.",
        )

        arg["list_of_subjects"] = nff.return_list_of_subjects_from_file(
            arg["list_of_subjects"]
        )

        error_and_exit(arg["list_of_subjects"])

    if not arg["list_of_subjects"]:
        arg["list_of_subjects"] = nff.list_of_subjects_from_directory(
            arg["study_folder"]
        )

        error_and_exit(
            arg["list_of_subjects"], "Unable to find list of subjects from directory"
        )

    error_and_exit(nff.check_subject_files(arg))
    error_and_exit(
        nff.check_fsl_is_installed(),
        "FSLDIR not in path. Check FSL is installed or has been loaded correctly",
    )

    print("Number of subjects: ", len(arg["list_of_subjects"]))
    for sub in arg["list_of_subjects"]:
        # looping over subjects and building out directories
        print("working on: ", os.path.basename(sub))
        nfactpp_diretory = os.path.join(sub, "nfact_pp")
        directory_created = make_directory(nfactpp_diretory)
        error_and_exit(directory_created)
        seed_text = "\n".join(arg["seed"])
        files_written = write_options_to_file(nfactpp_diretory, seed_text)
        command = build_probtrackx2_arguments(arg, sub, nfactpp_diretory)
        error_and_exit(files_written)

        # Running probtrackx2 blueprint
        try:
            log_name = "PP_log_" + date_for_filename()
            with open(os.path.join(nfactpp_diretory, log_name), "w") as log_file:
                run = subprocess.run(command, stdout=log_file, stderr=log_file)
        except subprocess.CalledProcessError as error:
            error_and_exit(False, f"Error in calling probtrackx blueprint: {error}")
        except KeyboardInterrupt:
            run.kill()
            return None

        # Error handling subprocess
        if run.returncode != 0:
            error_and_exit(False, f"Error in {command[0]} please check log files")

    print("Finished")


if __name__ == "__main__":
    main_nfact_preprocess()
