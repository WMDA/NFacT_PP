import os


def add_file_path_for_images(arg: dict, sub: str) -> dict:
    """
    Function to add file path to
    images.

    Parameters
    ----------
    arg: dict
        dictionary of arguments from
        command line
    sub: str
        subjects full path
    """
    keys = ["seed", "warps", "rois"]
    image_files = {key: arg[key] for key in keys}
    for key, value in image_files.items():
        image_files[key] = [os.path.join(sub, val) for val in value]
    return image_files


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

    xtract_Bargs = [
        "xtract_blueprint",
        "-seeds",
        seeds,
        "-bpx",
        arg["bpx_suffix"],
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
        "-xtract",
    ]

    return [Bargs for Bargs in xtract_Bargs if Bargs]


def write_to_file(file_path: str, name: str, text: str) -> bool:
    """
    Function to write to file.

    Parameters
    ----------
    file_path: str
        abosulte file path to
        where file is created
    name: str
        name of file
    text: str
        string to add to file
    """
    try:
        with open(f"{file_path}/{name}", "w") as file:
            file.write(text)
    except Exception as e:
        print(f"Unable to write to {file_path}/{name} due to :", e)
        return False
    return True


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

def colours():
    """
    Function to print out text in colors

    Parameters
    ----------
    None

    Returns
    -------
    dict: dictionary object
        dictionary of color strings
    """
    return {"reset": "\033[0;0m", "red": "\033[1;31m"}