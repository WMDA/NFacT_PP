import os
import glob
import subprocess

from NFACT_PP.nfactpp_utils_functions import (
    add_file_path_for_images,
    write_to_file,
    date_for_filename,
    error_and_exit,
)


def hcp_files(sub: str) -> dict:
    """
    Function to return
    HCP standard seed, ROI
    and warps. Also checks that they exist

    Parameters
    ----------
    sub: str
        string to subjects
        files

    Returns
    -------
    dict: dictionary object
        dict of seeds, ROIS and warps
    """
    

    subject = os.path.basename(sub)

    rois = glob.glob(
         os.path.join(sub, f"MNINonLinear/fsaverage_LR32k/*.atlasroi.32k_fs_LR.shape.gii"
         )
     )
    rois = [rois[0], rois[1]]
    if not rois:
        error_and_exit(False, f"Cannot find ROI files for {subject}")
    
    bpx_path = os.path.join(sub, 'T1w/Diffusion.bedpostX')
    print(bpx_path)
    error_and_exit(os.path.exists(bpx_path[0]), "Cannot find Diffusion.bedpostX directory")
    warp = [
        os.path.join(sub, "MNINonLinear/xfms/standard2acpc_dc.nii.gz"),
        os.path.join(sub, "MNINonLinear/xfms/acpc_dc2standard.nii.gz"),
    ]
    [
        error_and_exit(os.path.exists(path), f"Unable to find {path}")
        for path in warp
    ]
    return {
        "seed": os.path.join(sub, 'nfact_pp', "seeds.txt"),
        "rois": rois,
        "warps": warp,
        "bpx_path": bpx_path,
        'target_mask': None
    }


def process_command_arguments(arg: dict, sub: str, output_dir: str):
    """
    Function to process command line
    arguments

    Parameters
    -----------
        arg: dict
        dictionary of arguments from
        command line
    sub: str
        subjects full path
    output_dir: str
        path to output directory

    Returns
    -------
    dict: dictonary oject
        dict of processed
        command line arguments
    """
    images = add_file_path_for_images(arg, sub)
    return {
        "rois" : images['rois'],
        "warps": images['warps'],
        "seed": os.path.join(output_dir, "seeds.txt"),
        "rois": ",".join(images["rois"]),
        'bpx_path': os.path.join(sub, arg['bpx_path']), 
        #"target_mask": os.path.join(sub, arg["target_mask"]),
    }


def build_probtrackx2_arguments(
    arg: dict, sub: str, output_dir: str, hcp_stream=False
) -> list:
    """
    Function to build out probtrackx2 arguments

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
    if hcp_stream:
        command_arguments = hcp_files(sub)
    if not hcp_stream:
        command_arguments = process_command_arguments(arg, sub, output_dir)

    binary = "probtrackx2_gpu" if arg["gpu"] else "probtrackx2"
    warps = command_arguments["warps"]
    seeds = command_arguments["seed"]
    mask = os.path.join(command_arguments["bpx_path"], 'nodif_brain_mask')
    target_mask = command_arguments["target_mask"]

    return [
        binary,
        "-x", seeds,
        "-s", command_arguments["bpx_path"],
        f"--mask={mask}",
        f"--xfm={warps[0]}",
        f"--invxfm={warps[1]}",
        f"--seedref={arg['ref']}",
        "--omatrix2",
        f"--target2={target_mask}",
        "--loopcheck",
        "--forcedir",
        "--opd",
        "--nsamples=1000",
        f"--dir={output_dir}",
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


def run_probtrackx(nfactpp_diretory: str, command: list) -> None:
    """
    Function to run probtrackx

    Parameters
    ----------
    nfactpp_diretory: str
        path to nfactpp_diretory

    command: list
        command in list form to run

    Returns
    -------
    None
    """

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


def get_target2(
    target_img: str,
    output_dir: str,
    resolution: str,
    reference_img: str,
    interpolation_straety: str,
) -> None:
    """
    Function to create target image

    Parameters
    ----------

    Returns
    -------
    None
    """
    try:
        run = subprocess.run(
            [
                "flirt",
                "-in",
                target_img,
                "-out",
                output_dir,
                "-applyisoxfm",
                str(resolution),
                "-ref",
                reference_img,
                "-interp",
                interpolation_straety,
            ],
            capture_output=True,
        )

    except subprocess.CalledProcessError as error:
        error_and_exit(False, f"Error in calling probtrackx blueprint: {error}")
    except KeyboardInterrupt:
        run.kill()

    if run.returncode != 0:
        error_and_exit(
            False, f"FSL FLIRT failure due to {run.stderr}. Unable to build target2"
        )
