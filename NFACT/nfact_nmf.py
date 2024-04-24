#!/usr/bin/env fslpython

# Run pre-NMF processing, including zipping, stacking, conversion to sparse, and averaging
#
# Author: Shaun Warrington <shaun.warrington1@nottingham.ac.uk> and Ellie Thompson

# function to load fdt_matrix in dot format and convert to sparse
def load_dot(f):
    x = np.loadtxt(f)
    n_seed=x[-1,0]
    n_target=x[-1,1]
    row=x[:-1,0]-1
    col=x[:-1,1]-1
    data=x[:-1,2]
    return sparse.coo_matrix((data, (row, col)), shape=(n_seed.astype(int), n_target.astype(int)))

# load, waytotal normalise, stack and return matrix
def dotprep(con_left_path, con_right_path, wt_left_path, wt_right_path):
    con_left = load_dot(con_left_path)
    waytotal = np.loadtxt(wt_left_path)
    con_left = con_left.tocsr()
    con_left.multiply(1e8/waytotal)
    con_right = load_dot(con_right_path)
    waytotal = np.loadtxt(wt_right_path)
    con_right = con_right.tocsr()
    con_right.multiply(1e8/waytotal)
    return sparse.vstack([con_left, con_right])

def load_connmat(cm_paths, wt_paths, r_flag):
    cm_paths = cm_paths.split(",")
    extension = os.path.splitext(cm_paths[0])[1]
    wt_paths = wt_paths.split(",")
    # either .dot with two hemispheres (single-subject)
    # OR .npz because it is averaged using this package
    if r_flag == 1:
        cmat = dotprep(cm_paths[0], cm_paths[1], wt_paths[0], wt_paths[1])
    elif r_flag == 0:
        cmat = sparse.load_npz(cm_paths[0])
    return cmat

import numpy as np
import sys,os,glob
from scipy import sparse
from numpy import array, matrix
from sklearn.decomposition import NMF as nmf
import pandas as pd

# Image stuff
import nibabel as nib
from nibabel import cifti2
from fsl.data.image import Image
from fsl.data.cifti import cifti2_axes
from fsl.data.cifti import Cifti

out                     = sys.argv[1] # the output directory
n_components            = int(sys.argv[2]) # model order for the decomposition
cm_paths                = sys.argv[3] # comma separated connectivity matrices
seeds                   = sys.argv[4] # comma separated seeds
rois                    = sys.argv[5] # comma separated ROIs
waytotal                = sys.argv[6] # comma separated seed coordinates
tract_coords            = sys.argv[7] # volume coordinates
lookup                  = sys.argv[8] # volume lookup file
r_flag                  = int(sys.argv[9]) # volume lookup file

# for testing
# out="/data/Q1200/Diffusion/nfact"
# n_components=100
# cm_paths="/data/Q1200/Diffusion/nfact/average_matrix2.npz"
# seeds="/data/Q1200/Diffusion/nfact/config/L.white.surf.gii,/data/Q1200/Diffusion/nfact/config/R.white.surf.gii"
# rois="/data/Q1200/Diffusion/nfact/config/L.roi.shape.gii,/data/Q1200/Diffusion/nfact/config/R.roi.shape.gii"
# waytotal="x"
# tract_coords="/data/Q1200/Diffusion/nfact/config/tract_space_coords_for_fdt_matrix2"
# lookup="/data/Q1200/Diffusion/nfact/config/lookup_tractspace_fdt_matrix2.nii.gz"
# r_flag=0

seeds = seeds.split(",")
rois = rois.split(",")
# surf_coords = surf_coords.split(",")

########## NMF
# alpha - the regularisation parameter - original is 0.1
alpha = 0.1

# regularisation parameters
l1_ratio=1

# load connectivity matrix
print("Loading data...")
connectivity_matrix = load_connmat(cm_paths, waytotal, r_flag)
connectivity_matrix = connectivity_matrix.toarray()

# apply NMF to connectivity matrix
print("Running decomposition...")
model = nmf(n_components=n_components, alpha=alpha, l1_ratio=l1_ratio, init="nndsvd", random_state=1)
W = model.fit_transform(connectivity_matrix) # the GM surface data
H = model.components_ # the WM volume data

print("Saving component data...")
########## the reference coordinates, surface and volume data for conversion
# load in gifti metric files
# seeds
seed_l = nib.load(seeds[0]).darrays[0].data != 0
seed_l = seed_l[:,0]
seed_r = nib.load(seeds[1]).darrays[0].data != 0
seed_r = seed_r[:,0]
seed = np.concatenate((seed_l,seed_r))

# ROIs
roi_l = nib.load(rois[0]).darrays[0].data != 0
roi_r = nib.load(rois[1]).darrays[0].data != 0
roi = np.concatenate((roi_l,roi_r))

###### Save CIFTI components
# add in empty medial wall
full_W = np.zeros([np.shape(seed)[0], n_components])
full_W[roi == 1, :] = W
W = full_W

# build CIFTI brain model and save
bm_l      = cifti2_axes.BrainModelAxis.from_mask(seed_l, name=f'CortexLeft')
bm_r      = cifti2_axes.BrainModelAxis.from_mask(seed_r, name=f'CortexRight')
bm        = bm_l + bm_r
new_fname = os.path.join(out, f'NMF_GM_{n_components}.LR.dscalar.nii')
# save cifti
sc        = cifti2_axes.ScalarAxis(np.linspace(0, n_components, n_components, dtype='int'))
hdr       = cifti2.Cifti2Header.from_axes((sc, bm))
img       = cifti2.Cifti2Image(W.T, hdr)
nib.save(img, new_fname)

print(f'Output files are:')
print(new_fname)

###### Save NIFTI components
# target space coordinates and reference image
coords = np.loadtxt(tract_coords, dtype='int')
ref_img = nib.load(lookup)

(xdim, ydim, zdim)=ref_img.shape
ref_affine =ref_img.affine
n_target = H.shape[1]

# fill image matrix
comps_mat = np.zeros((xdim, ydim, zdim, n_components))
for j in range(0, n_components):
	for i in range(0, int(n_target)):
		comps_mat[coords[i,0], coords[i,1], coords[i,2], j]=H[j,i]

# save NIFTI
img = nib.Nifti1Image(comps_mat, ref_affine)
new_fname = os.path.join(out, f'NMF_WM_{n_components}.nii.gz')
nib.save(img, new_fname)

print('and')
print(new_fname)
print('Done!')
