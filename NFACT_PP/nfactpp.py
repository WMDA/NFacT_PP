import os
import re
import numpy as np
import glob

# NFACT functions
from NFACT_PP.nfactpp_argument_functions import args
import NFACT_PP.nfactpp_check_functions as nff
from NFACT_PP.nfactpp_utils_functions import (
    make_directory,
    error_and_exit,
   

)
from NFACT_PP.nfactpp_probtrackx_functions import (
    build_probtrackx2_arguments,
    write_options_to_file,
    hcp_files,
    run_probtrackx
)

def main_nfact_preprocess(arg: dict) -> None:
    """
    Main function for nfact PP

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    
    nff.check_arguments(arg)
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
        seed_text = "\n".join(arg["seed"])
        files_written = write_options_to_file(nfactpp_diretory, seed_text)
        command = build_probtrackx2_arguments(arg, sub, nfactpp_diretory)
        error_and_exit(files_written)
        # Running probtrackx2 
        run_probtrackx(nfactpp_diretory, command)

    print("Finished")


def hcp_stream_main(arg: dict):
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

    print('HCP stream selected')
    hcpfiles = hcp_files()
    arg['seed'] = hcpfiles['seed']
    arg['rois'] = hcpfiles['rois']
    arg['warps'] = hcpfiles['warps']
    print('Finished HCP stream')
    exit(0)


