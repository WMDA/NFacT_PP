import os
import subprocess

from NFACT_PP.nfactpp_utils_functions import (
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

    bpx_path = os.path.join(sub, "T1w/Diffusion.bedpostX")
    error_and_exit(
        os.path.exists(bpx_path[0]), "Cannot find Diffusion.bedpostX directory"
    )
    warp = [
        os.path.join(sub, "MNINonLinear/xfms/standard2acpc_dc.nii.gz"),
        os.path.join(sub, "MNINonLinear/xfms/acpc_dc2standard.nii.gz"),
    ]
    [error_and_exit(os.path.exists(path), f"Unable to find {path}") for path in warp]
    return {
        "seed": os.path.join(sub, "nfact_pp", "seeds.txt"),
        "warps": warp,
        "bpx_path": bpx_path,
    }


def process_command_arguments(arg: dict, sub: str):
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

    Returns
    -------
    dict: dictonary oject
        dict of processed
        command line arguments
    """
    return {
        "warps": [os.path.join(sub, warp) for warp in arg["warps"]],
        "seed": os.path.join(sub, "nfact_pp", "seeds.txt"),
        "bpx_path": os.path.join(sub, arg["bpx_path"]),
    }


def build_probtrackx2_arguments(
    arg: dict, sub: str, hcp_stream=False, ptx_options=False
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
        print("HCP arguments")
        command_arguments = hcp_files(sub)
    if not hcp_stream:
        command_arguments = process_command_arguments(arg, sub)

    binary = "probtrackx2_gpu" if arg["gpu"] else "probtrackx2"
    warps = command_arguments["warps"]
    seeds = command_arguments["seed"]
    mask = os.path.join(command_arguments["bpx_path"], "nodif_brain_mask")
    target_mask = os.path.join(sub, "nfact_pp", "target2.nii.gz")
    bpx = os.path.join(command_arguments["bpx_path"], "merged")
    output_dir = os.path.join(sub, "nfact_pp", "omatrxi2")

    command = [
        binary,
        "-x",
        seeds,
        "-s",
        bpx,
        f"--mask={mask}",
        f"--xfm={warps[0]}",
        f"--invxfm={warps[1]}",
        f"--seedref={arg['ref']}",
        "--omatrix2",
        f"--target2={target_mask}",
        "--loopcheck",
        "--forcedir",
        "--opd",
        f"--nsamples={arg['nsamples']}",
        f"--dir={output_dir}",
        "--pd",
    ]
    if ptx_options:
        command = command + ptx_options
    return command


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

    print("Running", command[0])
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
    interpolation_strategy: str,
) -> None:
    """
    Function to create target2 image

    Parameters
    ----------
    target_img: str
        string to target image
    output: str
        string to output directory
    resolution: str
        resolution of target2
    reference_img: str
        reference input
    interpolation_strategy: str
        interpolation, either
        trilinear,
        nearestneighbour,
        sinc,
        spline

    Returns
    -------
    None
    """
    print("Creating target2 image")
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
                interpolation_strategy,
            ],
            capture_output=True,
        )

    except subprocess.CalledProcessError as error:
        error_and_exit(False, f"Error in calling FSL flirt: {error}")
    except KeyboardInterrupt:
        run.kill()

    if run.returncode != 0:
        error_and_exit(
            False, f"FSL FLIRT failure due to {run.stderr}. Unable to build target2"
        )


def seeds_to_ascii(surfin: str, roi: str, surfout: str) -> None:
    """
    Function to create seeds from
    surfaces.

    Parameters
    ----------
    surfin: str
        input surface
    roi: str,
        medial wall surface
    surfout: str
        name of output surface.
        Needs to be full path
    """
    print(f"Converting seed surface {os.path.basename(surfin)} to ASC")
    try:
        run = subprocess.run(
            [
                "surf2surf",
                "-i",
                surfin,
                "-o",
                surfout,
                f"--values={roi}",
                "--outputtype=ASCII",
            ],
            capture_output=True,
        )

    except subprocess.CalledProcessError as error:
        error_and_exit(False, f"Error in calling surf2surf: {error}")
    except KeyboardInterrupt:
        run.kill()

    if run.returncode != 0:
        error_and_exit(
            False,
            f"FSL surf2surf failure due to {run.stderr}. Unable to create asc surface",
        )


def get_probtrack2_arguments():
    """
    Function to get probtrack2
    arguments to check that user input
    is valid

    Parameters
    ----------
    None

    Returns
    -------
    help_arguments: str
        string of help arguments
    """
    import subprocess

    try:
        help_arguments = subprocess.run(["probtrackx2", "--help"], capture_output=True)
    except subprocess.CalledProcessError as error:
        error_and_exit(False, f"Error in calling surf2surf: {error}")

    return help_arguments.stderr.decode("utf-8")
