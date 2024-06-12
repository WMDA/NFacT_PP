#! /bin/bash
ref="/usr/local/fsl/6.0.7.x/data/standard/MNI152_T1_2mm_brain.nii.gz"
code_folder=$HOME/NFacT/NFACT
StudyDir="$HOME/for_axon"
subject_list="$HOME/for_axon/sub_list"
left_seed_suff="nfact/L.white.resampled_fs_LR.surf.gii"
right_seed_suff="nfact/R.white.resampled_fs_LR.surf.gii"
seeds="$left_seed_suff $right_seed_suff"

left_roi_suff="nfact/L.atlasroi.resampled_fs_LR.shape.gii"
right_roi_suff="nfact/R.atlasroi.resampled_fs_LR.shape.gii"
rois="$left_roi_suff $right_roi_suff"

std2diff_suff="standard2acpc_dc.nii.gz"
diff2std_suff="acpc_dc2standard.nii.gz"
bpx_suff="Diffusion.bedpostX"

study_folder=$StudyDir

# NFacT pre-processing
${code_folder}/nfact_preproc -study $study_folder -subject_list $subject_list -bpx $bpx_suff \
  -seeds $seeds -rois $rois -warps $std2diff_suff $diff2std_suff -ref $ref \
  -gpu -prefix group1