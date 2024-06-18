from nfactpp_utils_functions import add_file_path_for_images, write_to_file
import os
from scipy import sparse
import numpy as np


def build_xtract_arguments(arg: dict, sub: str) -> list:
    """
    Function to build out xtract arguments

    Parameters
    ----------
    arg: dict
        dictionary of arguments from
        command line
    sub: str
        subjects full path

    Returns
    -------
    list: list object
        list of xtract blueprint arguements
    """

    images = add_file_path_for_images(arg, sub)
    seeds = ",".join(images["seed"])
    rois = ",".join(images["rois"])
    gpu = "-gpu" if arg["gpu"] else ""
    bpx = os.path.join(sub, arg["bpx_suffix"])
    target_mask = os.path.join(sub, arg["target_mask"])

    xtract_Bargs = [
        "xtract_blueprint",
        "-seeds",
        seeds,
        "-bpx",
        bpx,
        "-rois",
        rois,
        "-warps",
        arg["ref"],
        images["warps"][0],
        images["warps"][1],
        gpu,
        "-stage",
        "1",
        "-tract_list",
        "null",
        "-target",
        target_mask,
        "-xtract",
    ]

    return [Bargs for Bargs in xtract_Bargs if Bargs]


def write_options_to_file(file_path: str, seed_txt: str):
    """
    Function to write seeds
    and ptx_options to file

    Parmeters
    ---------
    file_path: str
        file path for .PP_config
        directory
    seed_txt: str
        path of string to go into
        seed directory
    """
    ptx_options = write_to_file(file_path, "ptx_options.txt", "--pd")
    if not ptx_options:
        return False
    seeds = write_to_file(file_path, "seeds.txt", seed_txt)
    if not seeds:
        return False
    return True


def average_across_hemishperes(left_path: str, right_path: str) -> object:
    """
    Function to average across hemishperes

    Parameters
    ----------
    left_path: str
        path to left hemishpere
    right_path: str
        path to right hemishpere

    Returns
    -------
    sparse.vstack: object
        a sparse matrix of left
        and right averaged by waytotal

    """
    left_hemishphere = np.loadtxt(os.path.join(left_path, "fdt_matrix2.dot"))
    left_way_total = np.loadtxt(os.path.join(left_path, "waytotal"))
    left_hemishphere_normalised = left_hemishphere * (1e8 / left_way_total)
    right_hemishphere = np.loadtxt(os.path.join(right_path, "fdt_matrix2.dot"))
    right_waytotal = np.loadtxt(os.path.join(right_path, "waytotal"))
    right_hemishpere_normalised = right_hemishphere * (1e8 / right_waytotal)
    return np.vstack([left_hemishphere_normalised, right_hemishpere_normalised])
