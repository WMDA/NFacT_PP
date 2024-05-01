import argparse


def nfact_averaging_args() -> dict:
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


def nfact_nmf_args() ->dict:
    """
    """
    opts = argparse.ArgumentParser()
    opts.add_argument('-o', '--output_directory', 
                      dest='output_directory',
                      help='Path to the output_directory')
    opts.add_argument('-n', '--n_components', 
                      dest='n_components',
                      help='Number of components',
                      type=int)
    opts.add_argument('-c', '--cm_paths', 
                      dest='ptx_folder',
                      help="""The path to a comma sperated 
                      connectivity matrices""")
    opts.add_argument('-s', '--seeds', 
                      dest='seeds',
                      help="""The path to a comma sperated 
                      seeds. First left then right""")

    return vars(opts.parse_args())


seeds = sys.argv[4] # comma separated seeds
rois = sys.argv[5] # comma separated ROIs
waytotal = sys.argv[6] # comma separated seed coordinates
tract_coords = sys.argv[7] # volume coordinates
lookup = sys.argv[8] # volume lookup file
r_flag = int(sys.argv[9]) # volume lookup file