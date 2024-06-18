import os
import subprocess
import re
import numpy as np

# NFACT functions
from NFACT.nfactpp_argument_functions import args
import NFACT.nfactpp_check_functions as nff
from NFACT.nfactpp_utils_functions import (
    make_directory,
    error_and_exit,
    Signit_handler,
    date_for_filename,
)
from NFACT.nfactpp_build_functions import (
    build_xtract_arguments,
    write_options_to_file,
    average_across_hemishperes,
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
        command = build_xtract_arguments(arg, sub)
        command.append(nfactpp_diretory)
        seed_text = re.sub(",", "\n", command[2])
        files_written = write_options_to_file(nfactpp_diretory, seed_text)
        error_and_exit(files_written)
        command.append("-ptx_options")
        command.append(os.path.join(nfactpp_diretory, "ptx_options.txt"))
        # Running Xtract blueprint
        try:
            log_name = "PP_log_" + date_for_filename()
            with open(os.path.join(nfactpp_diretory, log_name), "w") as log_file:
                run = subprocess.run(command, stdout=log_file, stderr=log_file)
        except subprocess.CalledProcessError as error:
            error_and_exit(False, f"Error in calling Xtract blueprint: {error}")
        except KeyboardInterrupt:
            run.kill()
            return None

        # Error handling subprocess
        if run.returncode != 0:
            error_code = re.sub(r".rror:", "", run.stderr.decode("utf-8"))
            error_and_exit(False, f"Error in xtract blueprint: {error_code}")

        if arg["average"]:
            left_path = os.path.join(
                nfactpp_diretory, "blueprint", "omatrix2", "omatrix2_L.white.32k_fs_LR"
            )
            right_path = os.path.join(
                nfactpp_diretory, "blueprint", "omatrix2", "omatrix2_R.white.32k_fs_LR"
            )
            matrix = average_across_hemishperes(left_path, right_path)
            save_path_for_matrix = os.path.join(nfactpp_diretory, "average_matrix2.dot")
            print(f"Saving matrix to:", save_path_for_matrix)
            np.savetxt(save_path_for_matrix, matrix)
    print("Finished")


if __name__ == "__main__":
    main_nfact_preprocess()
