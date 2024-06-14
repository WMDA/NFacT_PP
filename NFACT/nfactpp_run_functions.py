import subprocess
import os

def add_file_path_for_images(arg: dict, 
                             sub: str):
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
    keys = ['seed', 'warps', 'rois']
    image_files = {key: arg[key] for key in keys}
    for key, value in image_files.items():
        image_files[key] = [os.path.join(sub, val) for val in value]
    return image_files


def build_xtract_arguments(arg: dict, 
                           sub: str) -> list:
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
    seeds = ",".join(images['seed'])
    rois = ",".join(images['rois'])
    warps = arg['ref'] + " " + " ".join(images['warps'])
    gpu = "-gpu" if arg['gpu'] else ''

    xtract_Bargs=  ["-seeds", seeds, "-bpx", arg['bpx_suffix'], 
            "-rois", rois, "-warps", warps, gpu, '-stage', '1'
            "-tract_list", "null"  ]
    return [Bargs for Bargs in xtract_Bargs if Bargs]

def run_xtract_blueprint(arg: dict) -> None:
    """
    Function to run XTRACT blueprint

    Parameters
    ----------
    arg: dict
        dictionary of arguments from 
        command line 
    
    Returns
    -------
    None
    """
    print('Number of subjects: ', len(arg['list_of_subjects']) )
    for sub in arg['list_of_subjects']:
        print("working on: ", os.path.basename(sub))
        print(build_xtract_arguments(arg, sub))
#    
#    
#    for sub in arg['list_of_subjects']:
#        subname = os.path.basename(sub) 
#        build_xtract_arguments()