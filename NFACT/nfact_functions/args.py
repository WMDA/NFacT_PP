import argparse


def get_nfact_averaging_args() -> dict:
    """
    Function to get arguments for the 
    nfact_averaging script.

    Parameters
    ----------
    None

    Returns
    -------
    dict: dictionary
        dictionary of arguments
        of subject_list_path

    """
    opts = argparse.ArgumentParser()
    opts.add_argument('-s', '--subject_list_path', 
                      dest='subject_list_path',
                      help='Path to the subject list')
    opts.add_argument('-p', '--ptx_folder', 
                      dest='ptx_folder',
                      help="""The path to a ptx_folder 
                      example comma separated ptx_folders""")
    opts.add_argument('-o', '--output_directory', 
                      dest='output_directory',
                      help='Path to the output_directory')
    return vars(opts.parse_args())

