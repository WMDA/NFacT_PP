import os
import re
# NFACT functions
import NFACT_PP.nfactpp_check_functions as nff
from NFACT_PP.nfactpp_utils_functions import make_directory, error_and_exit, hcp_get_seeds, hcp_get_target_image, hcp_get_rois, hcp_reorder_seeds_rois
from NFACT_PP.nfactpp_probtrackx_functions import (
    build_probtrackx2_arguments,
    write_options_to_file,
    run_probtrackx,
    get_target2,
    seeds_to_ascii
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
        seeds_to_write = [
            os.path.join(arg["study_folder"], seed) for seed in arg["seed"]
        ]
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

    print("Number of subjects: ", len(arg["list_of_subjects"]))
    for sub in arg["list_of_subjects"]:
        # looping over subjects and building out directories
        print("\nworking on: ", os.path.basename(sub))
        nfactpp_diretory = os.path.join(sub, "nfact_pp")
        directory_created = make_directory(nfactpp_diretory)
        error_and_exit(directory_created)
        seeds = hcp_get_seeds(sub)
        seed_text = "\n".join(seeds)
        files_written = write_options_to_file(nfactpp_diretory, seed_text)
        error_and_exit(files_written)
        arg['rois'] = hcp_get_rois(sub)
        arg['ref'] = hcp_get_target_image(sub)
        
        ordered_by_hemisphere = hcp_reorder_seeds_rois(seeds,arg['rois'])
        for hemishphere, img in ordered_by_hemisphere.items():
            seeds_to_ascii(img[0], 
                      img[1],
                      os.path.join(nfactpp_diretory, 
                                   f'{hemishphere}white.32k_fs_LR.surf.asc'))
        get_target2(arg['ref'], 
                    os.path.join(nfactpp_diretory, 'target2'),  
                    arg['res'], 
                    arg['ref'], 
                    'nearestneighbour')
        command = build_probtrackx2_arguments(
            arg, sub, nfactpp_diretory, hcp_stream=True
        )
        print(command)

    print("\nFinished HCP stream")
    exit(0)
