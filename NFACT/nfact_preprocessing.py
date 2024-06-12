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
    option = argparse.ArgumentParser()
    option.add_argument(
        "-s"
        "--study_folder"
        "helllllllllllllllldfdfdfdfdfdfdfdflldfdfdfddfdfdfdfdfdfdfdfddfdfll"
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
