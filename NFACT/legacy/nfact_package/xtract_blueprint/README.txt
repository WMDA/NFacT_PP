## Generating Connectivity Blueprints with xtract_blueprint

xtract_blueprint is a flexible yet simple way to calculate the "connectivity blueprint" (Mars et al. 2018 eLife, Warrington et al. 2020 NeuroImage): a vertex by tract matrix where each row describes how each cortical location is connected to major white matter fibre bundles, and each column describes the cortical terminations of each of the white matter fibre bundles. xtract_blueprint can, in principle, build a connectivity blueprint for any brain (e.g. different species), at any resolution (i.e. number of vertices) and for any region (whole whole or a given ROI, a lobe for example).

The script was written by Shaun Warrington (University of Nottingham), Saad Jbabdi (Oxford University) and Stamatios Sotiropoulos (University of Nottingham).

---------------------------------------------------------------------

## Citations:

Mars R, Sotiropoulos SN, Passingham RE, Sallet J, Verhagen L, Khrapitchev AA, Sibson N, Jbabdi S (2018) Whole brain comparative anatomy using connectivity blueprints. eLife. DOI: 10.7554/eLife.35237

Warrington S, Bryant K, Khrapitchev A, Sallet J, Charquero-Ballester M, Douaud G, Jbabdi S*, Mars R*, Sotiropoulos SN* (2020) XTRACT - Standardised protocols for automated tractography in the human and macaque brain. NeuroImage. DOI: 10.1016/j.neuroimage.2020.116923

---------------------------------------------------------------------
## Usage:
```

__  _______ ____      _    ____ _____ _     _                       _       _
\ \/ /_   _|  _ \    / \  / ___|_   _| |__ | |_   _  ___ _ __  _ __(_)_ __ | |_
 \  /  | | | |_) |  / _ \| |     | | | '_ \| | | | |/ _ \ '_ \| '__| | '_ \| __|
 /  \  | | |  _ <  / ___ \ |___  | | | |_) | | |_| |  __/ |_) | |  | | | | | |_
/_/\_\ |_| |_| \_\/_/   \_\____| |_| |_.__/|_|\__,_|\___| .__/|_|  |_|_| |_|\__|
                                                        |_|


Usage:
    xtract_blueprint -bpx <folder> -xtract <folder> -seeds <list> -warps <ref> <xtract2diff> <diff2xtract> -out <folder> [options]

    Compulsory arguments:

       -bpx       <folder>                          Path to bedpostx folder
       -out       <folder>                          Path to output folder
       -xtract    <folder>                          Path to xtract folder
       -seeds     <list>                            Comma separated list of seeds for which a blueprint is requested (e.g. left and right cortex in standard space)
       -warps     <ref> <xtract2diff> <diff2xtract> Standard space reference image and transforms between xtract space and diffusion space

    Optional arguments:
       -stage                                       What to run. 1:matrix2, 2:blueprint, all:everythng (default)
       -gpu                                         Use GPU version
       -savetxt                                     Save blueprint as txt file (nseed by ntracts) instead of CIFTI
       -prefix    <string>                          Specify a prefix for the final blueprint filename (e.g. <prefix>_BP.LR.dscalar.nii)

       -rois  <list>                                Comma separated list (1 per seed): ROIs (gifti) to restrict seeding (e.g. medial wall masks)
       -stops     <stop.txt>                        Text file containing line separated list
       -wtstops   <wtstop.txt>                      Text file containing line separated list
       -tract_list                                  Comma separated list of tracts to include (default = all found under -xtract <folder>)

       -thr                                         Threshold applied to XTRACT tracts prior to blueprint calculation (default = 0.001, i.e. 0.1% probability).
       -nsamples                                    Number of samples per seed used in tractography (default = 1000)
       -res       <mm>                              Resolution of matrix2 output (Default = 3 mm)
       -ptx_options <options.txt>                   Pass extra probtrackx2 options as a text file to override defaults

   Example (recommended) usage:
      xtract_blueprint -bpx sub001/dMRI.bedpostx -out sub001/blueprint -xtract sub001/xtract -seeds sub001/l.white.surf.gii,sub001/r.white.surf.gii \
           -rois sub001/l.medwall.shape.gii,sub001/r.medwall.shape.gii -warps MNI152_brain.nii.gz sub001/xtract2diff.nii.gz sub001/diff2xtract.nii.gz -gpu \


```

---------------------------------------------------------------------

## Running xtract_blueprint:

In order to use xtract_blueprint, you need to have run xtract first. To construct the connectivity blueprints, xtract_blueprint expects the same warp fields as used in the running of xtract.

xtract_blueprint currently supports the construction of connectivity blueprints using surface (GIFTI) files only. As such, you must provide GIFTI surface files containing the white-grey matter boundary surface data. (We plan to extend this to support volume seeding in the future.)

Required input:
	bedpostx folder 		- crossing fibre modelled diffusion data (expects to find nodif_brain_mask)
	xtract folder 		- xtract tract folder (the output from xtract)
	seed 			- the comma separated seed masks to use in tractography (e.g. the white-grey matter boundary surfaces), e.g. `L.white.surf.gii,R.white.surf.gii`
	warps			- a reference standard space image and warps to and from the native diffusion and standard spaces, e.g. `MNI152.nii.gz standard2diff.nii.gz diff2standard.nii.gz`

Note: if running whole-brain (recommended), you must provide the left seed first, as exampled.


Running modes:
- Stage 1 only		- only run seed-based tractography
- Stage 2 only		- only run blueprint processing (requires xtract output and tractography from stage 1)
- All			        - runs both stage 1 and stage 2 processing

xtract_blueprint is capable of GPU acceleration (`'-gpu'` flag) and detects $SGE_ROOT to work with fsl_sub. If using the CPU version, expect tractography to take many hours.


**Tractography details and options:**

Tractography is performed for each seed separately. The resultant connectivity matrices (fdt_matrix) are stacked in order to construct a whole-brain connectivity blueprint. You may also provide a single hemisphere if you wish.

Optionally, you may also provide stop (stop tracking at locations given by this mask file) and wtstop (allow propagation within mask but terminate on exit) masks. Stop is typically the pial surface. wtstop is typically subcortical structures and/or the white surface. These should be specified as line separated text files. e.g. `-seeds <l.white.surf.gii,r.white.surf.gii> -stop stop.txt -wtstop wtstop.txt`

Spatial resolution: by default tractography will be ran and stored using a resolution of 3 mm. This may be adjusted using the `'-res'` argument. Note: if required, xtract_blueprint will resample the xtract tracts. Warning: connectivity matrices are very large and require a lot of memory to handle - 3 mm is usually sufficient for the adult human brain.

Additional probtrackx options may also be supplied. Simply add the probtrackx arguments to a text file and direct xtract_blueprint to this using the `'-ptx_options'` argument.

Connectivity blueprints are primarily concerned with the connectivity of the cortex to white matter tracts. As such, we offer the option the mask out the medial wall. To do so, provide a single medial wall mask per supplied seed: e.g. `-seeds l.white.surf.gii,r.white.surf.gii -rois l.roi,r.roi`. By default, the medial wall is included in the calculation of the connectivity blueprint: we recommend the use of the medial wall mask to prevent this.

The '-roi' argument may be used to restrict the blueprint to any region of interest, not just to exclude the medial wall. For example, you may provide an ROI restricting the blueprint to the temporal or frontal lobe.

If you wish to use a stop/wtstop surface mask, you must ensure that the number of vertices matches the seed mask. This means that, if you are providing a seed mask and medial wall mask to xtract_blueprint, and wish to provide a surface stop mask, you must convert the stop mask to asc, restricting the data points to the medial wall mask, e.g.:

	${FSLDIR}/bin/surf2surf -i stop.L.surf.gii -o stop.L.asc --outputtype=ASCII --values=l.roi.shape.gii
	${FSLDIR}/bin/surf2surf -i stop.R.surf.gii -o stop.R.asc --outputtype=ASCII --values=r.roi.shape.gii

Then supply "stop.L.asc" and "stop.R.asc" in a text file to xtract_blueprint using the `'-stop'` argument. This conversion is automatically performed for the seed mask in xtract_blueprint if a medial wall mask is supplied.


**Which tracts are included?**

Connectivity blueprints may be constructed using the provided XTRACT tracts or using your own. By default, xtract_blueprint will use all tracts it finds under the xtract folder. You can specify a subset, or you own tracts, by providing a comma separated list of tracts using the `'-tracts <str,str,str>'` argument.

Certain tracts, e.g. the Middle Cerebellar Peduncle (MCP), do not project to the cortex. As such, they should be disregarded when interpreting the connectivity blueprint, or excluded from its construction.


**Only interested in the connectivity of a specific area?**
In many cases, the connectivity to a particular lobe, e.g. temporal or frontal, is of interest. You can use xtract_blueprint to obtain a connectivity blueprint for such a region:

1. Define a binary mask which contains the region of interest as a shape.gii or func.gii file
2. Select the tracts of interest: in all likelihood, only a subset of XTRACT's tracts will project to the ROI
3. Supply the whole white matter surface file along with the ROI to xtract_blueprint, e.g. for the temporal lobe

  xtract_blueprint -bpx sub001/dMRI.bedpostx -out sub001/blueprint -xtract sub001/xtract \
  -warps MNI152_brain.nii.gz sub001/xtract2diff.nii.gz sub001/diff2xtract.nii.gz -gpu \
  -seeds sub001/l.white.surf.gii -rois sub001/l.temporal_lobe.shape.gii -tract_list af_l,ilf_l,ifo_l,mdlf_l,slf3_l


**Outputs of xtract_blueprint**

xtract_blueprint will create an output directory specified by the `'-out'` argument. This will contain any log and command files along with a sub-directory per seed. Each sub-directory contains the resultant connectivity matrix from stage 1. The connectivity blueprint will be saved in the parent output directory (a CIFTI dscalar.nii file).

Under outputDir:
- Stage 1 (matrix2 tractography) output
    - omatrix2:
        - "ptx_commands.txt" - the probtrackx commands for tractography
        - "`<seed>`" - sub-directory containing tractography results for each seed supplied, each containing:
            - "coords_fdt_matrix2" - the coordinates of the seed mask
            - "lookup_tractspace_fdt_matrix.nii.gz" - the target lookup space
            - "tract_space_coords_for_fdt_matrix2" - the coordinates of the target mask
            - "probtrackx.log" - the probtrackx log file
            - "fdt_paths.nii.gz" - a NIFTI file containing the generated streamlines
            - "fdt_matrix.dot" - the sparse format connectivity matrix (used to calculated the blueprint)
            - "waytotal" - txt file continaing the number of valid streamlines
- Stage 2 (blueprint calculation) output
    - "bp_commands.txt" - the blueprint calculation commands
    - "BP.`<L,R,LR>`.dscalar.nii" - CIFTI file containing the whole-brain connectivity blueprint - if running both hemispheres
- "logs" - sub-directory containing job scheduler log files for both stages

Alternatively, the `'-savetxt'` option may be used to override this. In this case, two txt files will be saved: the first (BP.<L,R,LR>.txt) will be an n_seed by n_tracts array containing the blueprint; the second (tract_order.`<L,R,LR>`.txt) is an n_tracts by 1 array containing the tract order in which the blueprint is structured. Note: no CIFTI file will be generated.
