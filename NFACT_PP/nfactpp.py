import os

# NFACT functions
from NFACT_PP.nfactpp_argument_functions import args
import NFACT_PP.nfactpp_check_functions as nff
from NFACT_PP.nfactpp_utils_functions import (
    make_directory,
    error_and_exit,
    hcp_files
)
from NFACT_PP.nfactpp_probtrackx_functions import (
    build_probtrackx2_arguments,
    write_options_to_file,
    run_probtrackx,
)


def main_nfact_preprocess(arg: dict) -> None:
    """
    Main function for nfact PP

    Parameters
    ----------
    arg: dict
       dictionary of command line
       arguments

    Returns
    -------
    None
    """

    
    nff.check_surface_arguments(arg["seed"], arg["rois"])

    # Error handling section

    error_and_exit(nff.check_subject_files(arg))

    print("Number of subjects: ", len(arg["list_of_subjects"]))
    for sub in arg["list_of_subjects"]:
        # looping over subjects and building out directories
        print("working on: ", os.path.basename(sub))
        nfactpp_diretory = os.path.join(sub, "nfact_pp")
        directory_created = make_directory(nfactpp_diretory)
        error_and_exit(directory_created)
        seeds_to_write = [os.path.join(arg['study_folder'], seed) for seed in arg["seed"]]
        seed_text = "\n".join(seeds_to_write)
        files_written = write_options_to_file(nfactpp_diretory, seed_text)
        error_and_exit(files_written)
        command = build_probtrackx2_arguments(arg, sub, nfactpp_diretory)
        
        # Running probtrackx2
        run_probtrackx(nfactpp_diretory, command)

    print("Finished")
    exit(0)


def hcp_stream_main(arg: dict) -> None:
    """
    hcp stream main function

    Parameters
    ----------
    arg: dict
       dictionary of command line
       arguments

    Returns
    ------
    None

    """

    print("HCP stream selected")
    hcpfiles = hcp_files(arg["list_of_subjects"])
    arg["seed"] = hcpfiles["seed"]
    arg["rois"] = hcpfiles["rois"]
    arg["warps"] = hcpfiles["warps"]

    print("Number of subjects: ", len(arg["list_of_subjects"]))
    for sub in arg["list_of_subjects"]:
        # looping over subjects and building out directories
        print("working on: ", os.path.basename(sub))
        nfactpp_diretory = os.path.join(sub, "nfact_pp")
        directory_created = make_directory(nfactpp_diretory)
        error_and_exit(directory_created)
        seed_text = "\n".join(arg["seed"])
        files_written = write_options_to_file(nfactpp_diretory, seed_text)
        error_and_exit(files_written)
        command = build_probtrackx2_arguments(arg, sub, nfactpp_diretory)
        print(command)






    print("Finished HCP stream")
    exit(0)
