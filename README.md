## Performing data-driven tractography using NFacT

NFacT (Non-negative matrix Factorisation of Tractography data) uses NMF (non-negative matrix factorisation) to perform data-driven tractography and may to be applied to a structural connectivity matrix derived from any brain in principle.


---------------------------------------------------------------------

## Citations:

Thompson E, Mohammadi-Nejad AR, Robinson EC, Andersson JLR, Jbabdi S, Glasser MF, Bastiani M, Sotiropoulos SN (2020) Non-negative data-driven mapping of structural connections with application to the neonatal brain. NeuroImage. DOI: 10.1016/j.neuroimage.2020.117273

NFacT uses XTRACT tools (xtract_blueprint) in its pipeline, please also cite:

Warrington S, Bryant K, Khrapitchev A, Sallet J, Charquero-Ballester M, Douaud G, Jbabdi S*, Mars R*, Sotiropoulos SN* (2020) XTRACT - Standardised protocols for automated tractography and connectivity blueprints in the human and macaque brain. NeuroImage, 217(116923). DOI: 10.1016/j.neuroimage.2020.116923


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

'''Note: in group-analysis, surfaces must maintain vertex correspondence across subjects to ensure proper averaging! This may be achieved two ways. 1) use the same seed and medial wall surfaces for all subjects (likely to introduce inaccuracies, particularly in human tractography). 2) use MSM to register surfaces for each subject to a standard space.'''

A set of subject IDs should be provided as a line separated text file (i.e. a subject ID per line) using the 'subject_list' argument.

To run nfact_preproc for a set of subjects, file names and directory structure must be consistent across subjects (i.e. file names should not contain any reference to subject IDs). The 'study' path should lead to a directory containing a set of subject directories. Each subject directory should then contain the input files required. For example:

```
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
```

These data could then be processed using nfact_preproc with the command call:

      nfact_preproc -study /home/study1 -subject_list /home/study1/subject_list
          -bpx dmri.bedpostx -seeds L.white.surf.gii R.white.surf.gii
          -rois L.medwall.shape.gii R.medwall.shape.gii
          -warps std2diff.nii.gz diff2std.nii.gz
          -ref <FSLDIR>/data/standard/MNI152_T1_2mm_brain.nii.gz

'''Note: the directory structure may be built using symbolic links (soft links) using the `ln -s` command in bash.'''

**Output from nfact_preproc**

The output from nfact_preproc follows the format required as input for nfact. For each subject, a sub-directory called 'nfact' is generated (e.g. /home/study1/subject-01/nfact). If data are being averaged, an additional 'nfact_group' directory is created under 'study' (e.g. /home/study1/nfact_group) containing the average connectivity matrix and the config files required for NFacT decomposition.

and ROI surfaces during nfact_preproc!

**Output from nfact_dualregress**

The output of nfact_dualregress follows the format of nfact: a CIFTI and NIFTI file are generated under either 'nfact_dir' or 'sub_dir'.
