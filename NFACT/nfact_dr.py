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

def nnls_func(p):
    comp, rnorm = nnls(p[0], p[1])
    return comp

import sys,os,glob,re
import numpy as np
from numpy import array, matrix
from scipy import sparse
import sklearn
import scipy
from scipy.optimize import nnls
import multiprocessing
from progressbar import progressbar

import time

# Image stuff
import nibabel as nib
from nibabel import cifti2
from fsl.data.image import Image
from fsl.data.cifti import cifti2_axes
from fsl.data.cifti import Cifti


out                     = sys.argv[1] # the output directory
group_gm_path           = sys.argv[2] # the GM components to regress from
cm_paths                = sys.argv[3] # comma separated connectivity matrices
seeds                   = sys.argv[4] # comma separated seeds
rois                    = sys.argv[5] # comma separated ROIs
waytotal                = sys.argv[6] # comma separated seed coordinates
tract_coords            = sys.argv[7] # volume coordinates
lookup                  = sys.argv[8] # volume lookup file
r_flag                  = int(sys.argv[9]) # group or subject level?
n_cores                 = int(sys.argv[10]) # the number of cores

# for testing
# out="/data/Q1200/Diffusion/group1_nfact"
# group_gm_path="/data/Q1200/Diffusion/group1_nfact/NMF_GM_100.LR.dscalar.nii"
# cm_paths="/data/Q1200/Diffusion/group2_nfact/average_matrix2.npz"
# seeds="/data/Q1200/Diffusion/group1_nfact/config/L.white.surf.gii,/data/Q1200/Diffusion/group1_nfact/config/R.white.surf.gii"
# rois="/data/Q1200/Diffusion/group1_nfact/config/L.roi.shape.gii,/data/Q1200/Diffusion/group1_nfact/config/R.roi.shape.gii"
# waytotal="x"
# tract_coords="/data/Q1200/Diffusion/group1_nfact/config/tract_space_coords_for_fdt_matrix2"
# lookup="/data/Q1200/Diffusion/group1_nfact/config/lookup_tractspace_fdt_matrix2.nii.gz"
# r_flag=0

seeds = seeds.split(",")
rois = rois.split(",")

# Load in group data - CIFTI file
group_gm = nib.load(group_gm_path)
group_gm = np.asanyarray(group_gm.dataobj).T
n_components = group_gm.shape[1]

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

# Remove medial wall from the group_gm matrix (faster than adding into the target connectivity_matrix)
group_gm = group_gm[roi == 1,:]

# load connectivity matrix that we are regressing to
print("Loading data...")
connectivity_matrix = load_connmat(cm_paths, waytotal, r_flag)
connectivity_matrix = connectivity_matrix.toarray()

n_components = group_gm.shape[1]
n_vertices, n_voxels = np.shape(connectivity_matrix)

# project group_data onto connectivity matrix
# H is the volume components
# W is the surface components
print('Calulating new components (this may take a while)')

start = time.time()

H = np.zeros((n_components, n_voxels))
W = np.zeros((n_components, n_vertices))
if n_cores == 1:
    print('WM (voxel) regression')
    # non-parallel version
    for i in progressbar(range(n_voxels)):
        H[:, i], rnorm = nnls(group_gm, connectivity_matrix[:,i])

    # find subject-specific mixing matrix
    print('GM (vertex) regression')
    for j in progressbar(range(n_vertices)):
        W[:,j], rnorm = nnls(H.T, connectivity_matrix.T[:,j])

    W = W.T
else:
    print(f'Using a pool of {n_cores} cores')
    inputlist = [[group_gm, connectivity_matrix[:,i]] for i in range(n_voxels)]
    chunksize=5

    p = multiprocessing.Pool(processes=n_cores)

    print('WM (voxel) regression')
    H_list = p.imap(nnls_func, inputlist, chunksize=chunksize)
    H_list = list(H_list)
    for i in range(n_voxels):
        H[:,i] = H_list[i]

    print('GM (vertex) regression')
    inputlist = [[H.T, connectivity_matrix.T[:,j]] for j in range(n_vertices)]
    W_list = p.imap(nnls_func, inputlist, chunksize=chunksize)

    p.close()
    p.join()
    W_list = list(W_list)
    for i in range(n_vertices):
        W[:,i] = W_list[i]

    W = W.T


end = time.time()
print(end-start)

# add in empty medial wall to surface components
full_W = np.zeros([np.shape(seed)[0], W.shape[1]])
full_W[roi == 1, :] = W
W = full_W

print(f'Output files are:')
###### Save CIFTI components
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
print(new_fname)
print('and')

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
print(new_fname)
print('Done!')
