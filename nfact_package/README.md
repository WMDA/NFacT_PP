## Performing data-driven tractography using NFacT

NFacT (Non-negative matrix Factorisation of Tractography data) uses NMF (non-negative matrix factorisation) to perform data-driven tractography and may to be applied to a structural connectivity matrix derived from any brain in principle.

The script was written by Ellie Thompson, Shaun Warrington and Stamatios Sotiropoulos.

---------------------------------------------------------------------

## Citations:

# for NMF routines:

Thompson E, Mohammadi-Nejad AR, Robinson EC, Andersson JLR, Jbabdi S, Glasser MF, Bastiani M, Sotiropoulos SN (2020) Non-negative data-driven mapping of structural connections with application to the neonatal brain. NeuroImage. DOI: 10.1016/j.neuroimage.2020.117273

---------------------------------------------------------------------
## Usage:
```

##    ## ########    ###     ######  ########
###   ## ##         ## ##   ##    ##    ##
####  ## ##        ##   ##  ##          ##
## ## ## ######   ##     ## ##          ##
##  #### ##       ######### ##          ##
##   ### ##       ##     ## ##    ##    ##
##    ## ##       ##     ##  ######     ##


Usage:
    nfact -nfact_dir <folder> [options]

    Compulsory arguments:

    EITHER:
       -nfact_dir    <folder>                     Directory containing the group-level NFacT connectivity matrix

    OR:
       -sub_dir      <folder>                     An individual subject's NFacT results folder
       -seeds        <left> <right>               Paths to the left and right cortical seeds (white-grey boundary GIFTI)
       -rois         <left> <right>               Paths to the left and right medial wall masks (GIFTI)

    Optional arguments:
       -n_comp                                    Number of components used in the NMF decomposition (default = 100)


Example call:

  To call nfact for group-level analysis (from nfact_preproc):

    nfact -nfact_dir /home/nfact

  To call nfact for subject-level analysis (from nfact_preproc):

    nfact -sub_dir /home/sub-01/nfact -seeds /home/sub-01/L.white.surf.gii /home/sub-01/R.white.surf.gii
        -rois /home/sub-01/L.roi.shape.gii /home/sub-01/R.roi.shape.gii

```

---------------------------------------------------------------------

## Running NFacT:

NFacT requires a tractography-derived brain connectivity matrix (.dot or .npz) in which each row corresponds to a surface-based (vertex) seed and each column to a volume-based (voxel) target. Further, in order to obtain human-readable results (CIFTI and NIFTI files), a set of seed and target coordinate files are required.

**Input**

NFacT may be performed at a single-subject level or at the group-level. The input required to use NFacT may be obtained using nfact_preproc (see below).

The required input may take one of two formats: either a whole-brain connectivity matrix in Python's .npz file format, or two connectivity matrices (one left and one right hemisphere), and their associated coordinates files.

To call nfact for group-level decomposition:

  nfact -nfact_dir /home/nfact

Where /home/nfact
        ├── average_matrix2.npz                      - the whole-brain connectivity matrix
        └── config                                   - config directory containing coordinate, seed and target files
            ├── L.white.surf.gii                     - the surface seed for the left hemisphere
            ├── R.white.surf.gii                     - the surface seed for the right hemisphere
            ├── L.roi.shape.gii                      - the medial wall surface mask for the left hemisphere
            ├── R.roi.shape.gii                      - the medial wall surface mask for the right hemisphere
            ├── L.coords_for_fdt_matrix2             - the surface coordinates for the left hemisphere seed
            ├── R.coords_for_fdt_matrix2             - the surface coordinates for the right hemisphere seed
            ├── lookup_tractspace_fdt_matrix2.nii.gz - the volume space target lookup file
            └── tract_space_coords_for_fdt_matrix2   - the volume space coordinates file


To call nfact for subject-level decomposition:

    nfact -sub_dir /home/sub-01/nfact -seeds /home/sub-01/L.white.surf.gii /home/sub-01/R.white.surf.gii
        -rois /home/sub-01/L.roi.shape.gii /home/sub-01/R.roi.shape.gii

Where /home/sub-01/nfact
        └── omatrix2
            ├── omatrix2_L.white
            │   ├── coords_for_fdt_matrix2
            │   ├── fdt_matrix2.dot
            │   ├── lookup_tractspace_fdt_matrix2.nii.gz
            │   ├── tract_space_coords_for_fdt_matrix2
            │   └── waytotal
            └── omatrix2_R.white
                ├── coords_for_fdt_matrix2
                ├── fdt_matrix2.dot
                ├── lookup_tractspace_fdt_matrix2.nii.gz
                ├── tract_space_coords_for_fdt_matrix2
                └── waytotal


Take the hard work out of it.... it's easiest to use nfact_preproc!

**Output of NFacT**

NFacT will generate a GM component surface file (CIFTI) and a WM component volume file (NIFTI). By default, 100 components will be used in the decomposition. This may be adjusted using the 'n_comps' argument. The output files will be stored under the input directory: 'nfact_dir' or 'sub_dir', depending on your options.



## NFacT Pre-Processing:

The required input for NFacT may be obtained using nfact_preproc. Here, whole-brain probabilistic tractography connectivity matrices are derived for a set of subjects (or a single subject) and an average connectivity matrix is derived.

---------------------------------------------------------------------
## Usage:
```


##    ## ########    ###     ######  ########         ########  ########
###   ## ##         ## ##   ##    ##    ##            ##     ## ##     ##
####  ## ##        ##   ##  ##          ##            ##     ## ##     ##
## ## ## ######   ##     ## ##          ##            ########  ########
##  #### ##       ######### ##          ##            ##        ##
##   ### ##       ##     ## ##    ##    ##            ##        ##
##    ## ##       ##     ##  ######     ##    ####### ##        ##


Usage:
    nfact_preproc -study <path> -subject_list <txt> -bpx <path> -seeds <left> <right> -rois <left> <right> -warps <std2diff> <diff2std> -ref <mask> [options]

    Compulsory arguments:

       -study        <folder>                       Study folder containing subject sub-directories - should lead to the subject folder
       -subject_list <txt>                          Line separated list of subject IDs in text file

       -bpx          <path>                         The suffix of the bedpoxtX directory (e.g. <study>/<subid>/<bpx>)
       -seeds        <left> <right>                 The suffixes of the paths leading to the left and right hemisphere cortical seeds (white-grey boundary GIFTI)
       -rois         <left> <right>                 The suffixes of the paths leading to the left and right hemisphere medial wall masks (GIFTI)
       -warps        <std2diff> <diff2std>          The suffix of the path leading to the transforms between standard space and diffusion space

       -ref          <path>                         The full path to the standard space target (e.g. MNI152 brain mask)

    Optional arguments:
       -prefix       <str>                          Designate a prefix to the group-level output directory name (default directory name: <study>/nfact)
       -out          <folder>                       Path to output folder (default is to create subject-level output under the input subject directory and group-level under the study folder)
       -no_average                                  Do not perform connectivity matrix averaging - required for NMF (default averages across all subjects)

       -gpu                                         Use GPU version
       -nsamples                                    Number of samples per seed used in tractography (default = 1000)
       -res          <mm>                           Resolution of NMF volume components (Default = 2 mm)
       -ptx_options  <options.txt>                  Pass extra probtrackx2 options as a text file to override defaults


Example call:

  To call nfact_preproc for the subject 'sub-01':

    nfact_preproc -study /data/study_x -subject_list /home/data/list
        -bpx Diffusion.bedpostX -seeds L.white.surf.gii R.white.surf.gii
        -rois L.medwall.shape.gii R.medwall.shape.gii
        -warps std2diff.nii.gz diff2std.nii.gz
        -ref <FSLDIR>/data/standard/MNI152_T1_2mm_brain.nii.gz

    The bedpostX directory path would then be /data/study_x/sub-01/Diffusion.bedpostX and the path to the left seed would be /data/study_x/sub-01/L.white.surf.gii, for example.
    All path suffixes should be generic and consistent across subjects (i.e. not contain any subject IDs).


```

---------------------------------------------------------------------


**Input for nfact_preproc**

nfact_preproc requires crossing-fibre diffusion modelled data (bedpostX), surface white-grey matter boundary surface files (seeds), medial wall surface masks (the 'ROIs'), diffusion space to standard space warp fields and a standard space reference brain mask. These files are specified relative to a parent 'study' directory.

'''Note: in group-analysis, surfaces must maintain vertex correspondence across subjects to ensure proper averaging! This may be achieved two ways. 1) use the same seed and medial wall surfaces for all subjects. 2) use MSM to register surfaces for each subject to a standard space.'''

A set of subject IDs should be provided as a line separated text file (i.e. a subject ID per line) using the 'subject_list' argument.

To run nfact_preproc for a set of subjects, file names and directory structure must be consistent across subjects (i.e. file names should not contain any reference to subject IDs). The 'study' path should lead to a directory containing a set of subject directories. Each subject directory should then contain the input files required. For example:

/home/study1
    ├── subject-01
    │       ├── dmri.bedpostx                            - the bedpostx directory          
    │       ├── std2diff.nii.gz diff2std.nii.gz          - standard to diffusion warp (and visa versa)
    │       ├── L.white.surf.gii R.white.surf.gii        - the left and right seed files
    │       └── L.medwall.shape.gii R.medwall.shape.gii  - the left and right medial wall files
    ├── subject-02
    │       ├── dmri.bedpostx                                   
    │       ├── std2diff.nii.gz diff2std.nii.gz         
    │       ├── L.white.surf.gii R.white.surf.gii      
    │       └── L.medwall.shape.gii R.medwall.shape.gii
    └── subject-03                 
            ├── dmri.bedpostx                                 
            ├── std2diff.nii.gz diff2std.nii.gz        
            ├── L.white.surf.gii R.white.surf.gii      
            └── L.medwall.shape.gii R.medwall.shape.gii

These data could then be processed using nfact_preproc with the command call:

      nfact_preproc -study /home/study1 -subject_list /home/study1/subject_list
          -bpx dmri.bedpostx -seeds L.white.surf.gii R.white.surf.gii
          -rois L.medwall.shape.gii R.medwall.shape.gii
          -warps std2diff.nii.gz diff2std.nii.gz
          -ref <FSLDIR>/data/standard/MNI152_T1_2mm_brain.nii.gz


**Output from nfact_preproc**

The output from nfact_preproc follows the format required as input for nfact. For each subject, a sub-directory called 'nfact' is generated (e.g. /home/study1/subject-01/nfact). If data are being averaged, an additional 'nfact_group' directory is created under 'study' (e.g. /home/study1/nfact_group) containing the average connectivity matrix and the config files required for NFacT decomposition.



## NFacT Dual Regression:

Following decomposition, nfact_dr may be used to regress to subject-level or group-level data. This regression may be; from group to subject, from subject to subject or from group to group.

---------------------------------------------------------------------
## Usage:
```

##    ## ########    ###     ######  ########         ########  ########
###   ## ##         ## ##   ##    ##    ##            ##     ## ##     ##
####  ## ##        ##   ##  ##          ##            ##     ## ##     ##
## ## ## ######   ##     ## ##          ##            ##     ## ########
##  #### ##       ######### ##          ##            ##     ## ##   ##
##   ### ##       ##     ## ##    ##    ##            ##     ## ##    ##
##    ## ##       ##     ##  ######     ##    ####### ########  ##     ##

Usage:
    nfact_dualregress -gm_comps <path> [options]

    Compulsory arguments:
       -gm_comps     <path>                       Path to NFacT GM components (CIFTI) to use in regression

    AND EITHER:
       -sub_dir      <folder>                     Directory containing target subject's NFacT results folder
       -seeds        <left> <right>               Paths to the left and right cortical seeds (white-grey boundary GIFTI)
       -rois         <left> <right>               Paths to the left and right medial wall masks (GIFTI)

    OR:
       -nfact_dir    <folder>                     Directory containing the target group-level NFacT connectivity matrix

    Optional arguments:
       -out          <path>                       Output directory for dual regression results (default <nfact_dir>)

Example call:

  nfact_dualregress may be use to regress to a single subject's data or to group-level data.

  To call nfact for subject-level analysis (from nfact_preproc):

    nfact_dualregress -gm_comps /home/nfact_group/NMF_GM_100.LR.dscalar.nii -sub_dir /home/sub-01/nfact \
        -seeds /home/sub-01/L.white.surf.gii /home/sub-01/R.white.surf.gii \
        -rois /home/sub-01/L.roi.shape.gii /home/sub-01/R.roi.shape.gii

  For group-level regression:

    nfact_dualregress -gm_comps /home/group1_nfact_group/NMF_GM_100.LR.dscalar.nii -nfact_dir /home/group2_nfact_group

```

---------------------------------------------------------------------

**Input for nfact_dualregress**

In order to regress from a decomposition to a new connectivity matrix, the GM (surface) decomposition and the new set of connectivity matrices are required. As with nfact, the new (target) connectivity data may take the form a group-averaged dataset (whole-brain .npz) structure or single-subject dataset (left and right sub-directories containing .dot files).

 - To call nfact for group-level to subject-level regression:

  nfact_dualregress -gm_comps /home/nfact_group/NMF_GM_100.LR.dscalar.nii -sub_dir /home/sub-01/nfact
      -seeds /home/sub-01/L.white.surf.gii /home/sub-01/R.white.surf.gii
      -rois /home/sub-01/L.roi.shape.gii /home/sub-01/R.roi.shape.gii

Where 'sub_dir' (/home/sub-01/nfact) follows the structure of the subject-level connectivity data from nfact_preproc. /home/nfact_group/NMF_GM_100.LR.dscalar.nii is the decomposition and sub-01 is the target.

 - To call nfact for subject-level to subject-level regression (from nfact_preproc):

  nfact_dualregress -gm_comps /home/sub-01/nfact/NMF_GM_100.LR.dscalar.nii -sub_dir /home/sub-02/nfact
      -seeds /home/sub-02/L.white.surf.gii /home/sub-02/R.white.surf.gii
      -rois /home/sub-02/L.roi.shape.gii /home/sub-02/R.roi.shape.gii

/home/sub-01/nfact/NMF_GM_100.LR.dscalar.nii is the decomposition and sub-02 is the target.

 - You may also regress from one group to another:

  nfact_dualregress -gm_comps /home/group1_nfact_group/NMF_GM_100.LR.dscalar.nii -nfact_dir /home/group2_nfact_group

Where 'nfact_dir' (/home/group2_nfact_group) follows the structure of the group-level average from nfact_preproc. /home/group1_nfact_group/NMF_GM_100.LR.dscalar.nii is the decomposition and /home/group2_nfact_group is the target.


Regression may also be performed from a group-level decomposition to new subjects (i.e. those not included in group averaging, for example). First, create brain connectivity data for these subjects using nfact_preproc (use the '-no_average' flag as we do not require an addition group average). Next, call nfact_dualregress for each new subject, regressing from the group decomposition.

Note: dual regression only works between data of equal dimensions - you must use the same target ('ref') file, same resolution and maintain vertex correspondence for the seed and ROI surfaces during nfact_preproc!

**Output from nfact_dualregress**

The output of nfact_dualregress follows the format of nfact: a CIFTI and NIFTI file are generated under either 'nfact_dir' or 'sub_dir'.
