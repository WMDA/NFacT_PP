import os
import numpy as np
from NFACT_PP.nfactpp_utils_functions import add_file_path_for_images, write_to_file


def build_probtrackx2_arguments(arg: dict, sub: str, output_dir: str) -> list:
    """
    Function to build out xtract arguments

    Parameters
    ----------
    arg: dict
        dictionary of arguments from
        command line
    sub: str
        subjects full path
    output_dir: str
        path to output directory

    Returns
    -------
    list: list object
        list of probtrackx2 arguements
    """

    images = add_file_path_for_images(arg, sub)
    seeds = os.path.join(output_dir, 'seeds.txt')
    rois = ",".join(images["rois"])
    binary = "probtrackx2_gpu" if arg["gpu"] else "probtrackx2"
    #bpx = os.path.join(sub, arg["bpx_suffix"])
    target_mask = os.path.join(sub, arg["target_mask"])
    mask = os.path.join()

    return [
        binary,
        "-x",
        seeds,
        "-s",
        "merged",
        f"--mask={mask}",
        f"--xfm={images['warps'][0]}",
        f"--invxfm={images['warps'][1]}",
        f"--seedref={arg['ref']}",
        "--omatrix2",
        f"--target2={target_mask}" 
        "--loopcheck",
        "--forcedir",
        "--opd",
        "--nsamples=1000",
        "-o",
        output_dir
    ]

     


def write_options_to_file(file_path: str, seed_txt: str):
    """
    Function to write seeds
    and ptx_options to file

    Parmeters
    ---------
    file_path: str
        file path for nfact_PP
        directory
    seed_txt: str
        path of string to go into
        seed directory
    """
    seeds = write_to_file(file_path, "seeds.txt", seed_txt)
    if not seeds:
        return False
    return True
