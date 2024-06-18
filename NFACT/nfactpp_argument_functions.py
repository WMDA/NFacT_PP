import argparse


def args() -> dict:
    """
    Function to get arguements
    to run NFACT pre-processing

    Parameters
    -----------
    None

    Returns
    -------
    dict: dictionary object
        dict of arguments
    """
    option = argparse.ArgumentParser(
        description=print(splash()),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=example_usage(),
    )
    option.add_argument(
        "-f",
        "--study_folder",
        dest="study_folder",
        required=True,
        help="Study folder containing sub directories",
    )
    option.add_argument(
        "-l",
        "--list_of_subjects",
        dest="list_of_subjects",
        required=False,
        default=False,
        help="""A list of subjects in text form. If not provided NFACT PP will use all subjects in the study folder. 
        All subjects need full file path to subjects directory""",
    )
    option.add_argument(
        "-b",
        "--bpx",
        dest="bpx_suffix",
        required=False,
        default="Diffusion.bedpostX",
        help="The suffix of the bedpoxtX directory (e.g. <study>/<subid>/<bpx>)",
    )
    option.add_argument(
        "-s",
        "--seed",
        nargs="+",
        dest="seed",
        required=True,
        help="The suffixes of the paths leading to the left and right hemisphere cortical seeds (white-grey boundary GIFTI)",
    )
    option.add_argument(
        "-r",
        "--rois",
        dest="rois",
        nargs="+",
        required=True,
        help="The suffixes of the paths leading to the left and right hemisphere medial wall masks (GIFTI)",
    )
    option.add_argument(
        "-t",
        "--ref_target",
        dest="ref",
        required=True,
        help="The full path to the standard space target (e.g. MNI152 brain mask)",
    )
    option.add_argument(
        "-w",
        "--warps",
        dest="warps",
        nargs="+",
        required=True,
        help="The suffix of the path leading to the transforms between standard space and diffusion space",
    )
    option.add_argument(
        "-m",
        "--target_mask",
        dest="target_mask",
        required=True,
        help=" A whole brain/WM binary target mask in the same space as the seeds",
    )
    option.add_argument(
        "-p",
        "--prefix",
        dest="prefix",
        required=False,
        help="Designate a prefix to the group-level output directory name (default directory name: <study>/nfact_group)",
    )
    option.add_argument(
        "-o",
        "--out",
        dest="out",
        required=False,
        help="Path to output folder (default is to create subject-level output under the input subject directory and group-level under the study folder)",
    )
    option.add_argument(
        "-A",
        "--average",
        dest="average",
        required=False,
        action="store_true",
        help="Perform averagng across hemispheres. Useful for next steps in decomp if interested in whole brain tractography.",
    )
    option.add_argument(
        "-g",
        "--gpu",
        dest="gpu",
        required=False,
        action="store_true",
        help="Use GPU version",
    )
    option.add_argument(
        "-N",
        "--nsamples",
        dest="nsamples",
        required=False,
        default=1000,
        help="Number of samples per seed used in tractography (default = 1000)",
    )
    option.add_argument(
        "-R",
        "--res",
        dest="res",
        required=False,
        default=2,
        help="Resolution of NMF volume components (Default = 2 mm)",
    )
    return vars(option.parse_args())


def splash() -> str:
    """
    Function to return NFACT splash

    Parameters
    ----------
    None

    Returns
    -------
    str: splash
    """
    return """

##    ## ########    ###     ######  ########         ########  ########
###   ## ##         ## ##   ##    ##    ##            ##     ## ##     ##
####  ## ##        ##   ##  ##          ##            ##     ## ##     ##
## ## ## ######   ##     ## ##          ##            ########  ########
##  #### ##       ######### ##          ##            ##        ##
##   ### ##       ##     ## ##    ##    ##            ##        ##
##    ## ##       ##     ##  ######     ##            ##        ##

"""


def example_usage() -> str:
    """
    Function to return example usage

    Parameters
    ----------
    None

    Returns
    -------
    str: str object
    """
    return """

Example Usage:
    nfact_preprocessing -f /data/study_x -l /home/data/list
        -b Diffusion.bedpostX -s L.white.surf.gii R.white.surf.gii
        -r L.medwall.shape.gii R.medwall.shape.gii
        -w standard2acpc_dc.nii.gz acpc_dc2standard.nii.gz
        -t <FSLDIR>/data/standard/MNI152_T1_2mm_brain.nii.gz
        \n
"""
