#!/usr/bin/env fslpython

# Run pre-NMF processing, including zipping, stacking, conversion to sparse, and averaging
# Author: Shaun Warrington <shaun.warrington1@nottingham.ac.uk> and Ellie Thompson

import os
import sys
import shutil
import numpy as np
from scipy import sparse
from progressbar import progressbar
import nfact_functions as nf

def get_args() -> dict:
    '''
    Function to assign input into a dictionary

    Parameters
    ----------
    None

    Returns
    -------
    dict: dictionary obj
       dictionary of subject_list_path,
       ptx_folder and output_directory
    '''
    
    return {
    'subject_list_path': sys.argv[1],  # the subject list
    'ptx_folder': sys.argv[2], # the example comma separated ptx_folders
    'output_directory': sys.argv[3] # the output directory
    }

print('Averaging connectivity matrices')

args = get_args()

subject_list_nmf = np.loadtxt(args['subject_list_path'], dtype='str')
ptx_folder = args['ptx_folder'].split(",")

# loop through subjects:
#               prep fdt_matrices
#               average across subjects
COUNTER=0
for id in progressbar(subject_list_nmf):
    ptx_path_l = ptx_folder[0].replace("subid", str(id))
    ptx_path_r = ptx_folder[1].replace("subid", str(id))
    # the sudjects waytotal normalised whole-brain connectivity matrix in sparse format
    cm_csr = nf.dotprep(ptx_path_l, ptx_path_r)
    # initialise average matrix from first dataset
    if COUNTER == 0:
        average_cm = cm_csr
        # also, for 1 example subject copy files for building CIFTI/NIFTI later
        target = os.path.join(args['output_directory'], 'config')
        tmp = shutil.copyfile(os.path.join(ptx_path_l, 'lookup_tractspace_fdt_matrix2.nii.gz'), os.path.join(target, 'lookup_tractspace_fdt_matrix2.nii.gz'))
        tmp = shutil.copyfile(os.path.join(ptx_path_l, 'tract_space_coords_for_fdt_matrix2'), os.path.join(target, 'tract_space_coords_for_fdt_matrix2'))
        tmp = shutil.copyfile(os.path.join(ptx_path_l, 'coords_for_fdt_matrix2'), os.path.join(target, 'L.coords_for_fdt_matrix2'))
        tmp = shutil.copyfile(os.path.join(ptx_path_r, 'coords_for_fdt_matrix2'), os.path.join(target, 'R.coords_for_fdt_matrix2'))
    else:
    # sum each sum with previous average
        average_cm += (cm_csr)
    COUNTER+=1

# divide summed connectivity matrix by number of subjects and save
average_cm = average_cm.multiply(1/COUNTER)
average_cm_coo = average_cm.tocoo()
print('Saving average connectivity matrix:')
fname = os.path.join(args['output_directory'], 'average_matrix2')
sparse.save_npz(fname, average_cm.tocoo())
print(fname)
