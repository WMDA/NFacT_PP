from nfactpp_utils_functions import add_file_path_for_images, write_to_file
import os

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
    bpx = os.path.join(sub, arg['bpx_suffix'])
    target_mask = os.path.join(sub, arg['target_mask'])

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
