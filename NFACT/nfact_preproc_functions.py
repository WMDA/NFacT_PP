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
    option = argparse.ArgumentParser(description=print(splash()))
    option.add_argument("-f" ,
                        "--study_folder",
                        dest='study_folder',
                        required=True,
                        help='Study folder containing sub directories'
                        )
    option.add_argument('-l', 
                        '--list_of_sujects',
                        dest='list_of_sujects',
                        required=True,
                        help='A list of subjects in text form')
    option.add_argument('-b', '--bpx', 
                        dest='path_to_bpx_folder', 
                        required=True, 
                        help='The suffix of the bedpoxtX directory (e.g. <study>/<subid>/<bpx>)'
                        )
    option.add_argument('-s', 
                        '--seed', 
                        dest='path to bpx folder', 
                        required=True, 
                        help='The suffixes of the paths leading to the left and right hemisphere cortical seeds (white-grey boundary GIFTI)')
    option.add_argument('-r', 
                        '--rois', 
                        dest='rois', 
                        required=True, 
                        help='The suffixes of the paths leading to the left and right hemisphere medial wall masks (GIFTI)')
    option.add_argument('-t', 
                        '--ref_target', 
                        dest='ref', 
                        required=True, 
                        help='The full path to the standard space target (e.g. MNI152 brain mask)')
    option.add_argument('-p', 
                        '--prefix', 
                        dest='prefix', 
                        required=False, 
                        help='Designate a prefix to the group-level output directory name (default directory name: <study>/nfact_group)')
    option.add_argument('-o', 
                        '--out', 
                        dest='out', 
                        required=False, 
                        help='Path to output folder (default is to create subject-level output under the input subject directory and group-level under the study folder)')
    
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
