import numpy as np
from scipy import sparse
import os
from scipy.optimize import nnls

def nnls_func(p):
    comp, rnorm = nnls(p[0], p[1])
    return comp

def load_dot(file_path: str) -> object:
    '''
    Function to convert fdt_matrix in dot format
    to sparse matrix

    Parameters
    ----------
    file_path: str
        string of file path to fdt matrix

    Returns
    -------
    A sparse matrix in co-ordinate format
    '''
    fdt_matrix = np.loadtxt(file_path)
    n_seed = fdt_matrix[-1, 0]
    n_target = fdt_matrix[-1, 1]
    row = fdt_matrix[:-1, 0]-1
    col = fdt_matrix[:-1, 1]-1
    data = fdt_matrix[:-1, 2]
    return sparse.coo_matrix((data, (row, col)), shape=(n_seed.astype(int), n_target.astype(int)))

# load, waytotal normalise, stack and return matrix
def dotprep(dir_left: str, dir_right: str) -> object:
    """
    
    """
    con_left = load_dot(os.path.join(dir_left, 'fdt_matrix2.dot'))
    waytotal = np.loadtxt(os.path.join(dir_left, 'waytotal'))
    con_left = con_left.tocsr()
    con_left.multiply(1e8/waytotal)
    con_right = load_dot(os.path.join(dir_right, 'fdt_matrix2.dot'))
    waytotal = np.loadtxt(os.path.join(dir_right, 'waytotal'))
    con_right = con_right.tocsr()
    con_right.multiply(1e8/waytotal)
    return sparse.vstack([con_left, con_right])

# function to replace subID and sesID in paths
def replace_ids(path, id):
    new_path = path.replace("subid", str(id))
    return new_path

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