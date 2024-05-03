#!/bin/bash

# Example running NMF on a list of HCP subjects
code_folder=$HOME/nfact_code
StudyDir="/data/Q1200"

####################################
############ run group processing
####################################
subject_list="${code_folder}/../subject_list"
ref="${FSLDIR}/data/standard/MNI152_T1_2mm_brain.nii.gz"

rm -rf $StudyDir/Diffusion/nfact_group

for subid in `cat $subject_list`; do
  echo $subid
  sub_out="$StudyDir/Diffusion/$subid/nfact"
  rm -rf $sub_out
  mkdir -p $sub_out

  # soft link other files
  for side in L R; do
    ln -s ${StudyDir}/Structural/${subid}/MNINonLinear/fsaverage_LR32k/${subid}.${side}.atlasroi.32k_fs_LR.shape.gii ${sub_out}/${side}.atlasroi.32k_fs_LR.shape.gii
    ln -s ${StudyDir}/Structural/${subid}/MNINonLinear/fsaverage_LR32k/${subid}.${side}.white.32k_fs_LR.surf.gii ${sub_out}/${side}.white.32k_fs_LR.surf.gii
  done

  ln -s ${StudyDir}/Structural/${subid}/MNINonLinear/xfms/acpc_dc2standard.nii.gz ${sub_out}/
  ln -s ${StudyDir}/Structural/${subid}/MNINonLinear/xfms/standard2acpc_dc.nii.gz ${sub_out}/
  ln -s ${StudyDir}/Diffusion/${subid}/T1w/Diffusion.bedpostX ${sub_out}/
done

# set paths
left_seed_suff="nfact/L.white.32k_fs_LR.surf.gii"
right_seed_suff="nfact/R.white.32k_fs_LR.surf.gii"
seeds="$left_seed_suff $right_seed_suff"

left_roi_suff="nfact/L.atlasroi.32k_fs_LR.shape.gii"
right_roi_suff="nfact/R.atlasroi.32k_fs_LR.shape.gii"
rois="$left_roi_suff $right_roi_suff"

std2diff_suff="nfact/standard2acpc_dc.nii.gz"
diff2std_suff="nfact/acpc_dc2standard.nii.gz"
bpx_suff="nfact/Diffusion.bedpostX"

study_folder=$StudyDir/Diffusion

# NFacT pre-processing
${code_folder}/nfact_preproc -study $study_folder -subject_list $subject_list -bpx $bpx_suff\
  -seeds $seeds -rois $rois -warps $std2diff_suff $diff2std_suff -ref $ref -gpu

# group-level NFacT
${code_folder}/nfact -nfact_dir $study_folder/nfact_group

# group-average to single-subject NFacT dual regression
subid=100307 # the target subject
sub_nfact2=$study_folder/${subid}/nfact
${code_folder}/nfact_dualregress -gm_comps $study_folder/nfact_group/NMF_GM_100.LR.dscalar.nii\
    -sub_dir $sub_nfact2 -seeds $sub_nfact2/L.white.32k_fs_LR.surf.gii $sub_nfact2/R.white.32k_fs_LR.surf.gii\
    -rois $sub_nfact2/L.atlasroi.32k_fs_LR.shape.gii $sub_nfact2/R.atlasroi.32k_fs_LR.shape.gii -n_cores 5
