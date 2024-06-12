# module load fsl-img/6.0.4

# Example running NMF on a list HCP subject
code_folder=$HOME/NFACT/NFACT
StudyDir="$HOME/for_axon"
# StudyDir="/share/HCP/HCPyoung_adult"

####################################
############ run group1 processing (using downsampled data for testing here!!!!)
####################################
subject_list="$HOME/for_axon/sub_list"
ref="${FSLDIR}/data/standard/MNI152_T1_2mm_brain.nii.gz"

#rm -rf $StudyDir/Diffusion/group1_nfact
#rm -rf $StudyDir/Diffusion/group2_nfact

# downsample subject masks to speed up testing....
for subid in `cat $subject_list`; do
  echo $subid
  sub_out="$StudyDir/$subid/nfact"
  rm -rf $sub_out
  mkdir -p $sub_out

  # seed and medial wall
  # downsample the medial wall mask and the seed masks
  nvert=2000 # approx
  sph=${sub_out}/resample_sphere
  wb_command -surface-create-sphere ${nvert} ${sph}.R.surf.gii
  wb_command -surface-flip-lr ${sph}.R.surf.gii ${sph}.L.surf.gii
  wb_command -set-structure ${sph}.R.surf.gii CORTEX_RIGHT
  wb_command -set-structure ${sph}.L.surf.gii CORTEX_LEFT

  # the medial wall mask
  for side in L R; do
    wb_command -metric-resample ${StudyDir}/${subid}/${side}.atlasroi.32k_fs_LR.shape.gii \
        ${StudyDir}/${subid}/${side}.sphere.32k_fs_LR.surf.gii\
        ${sph}.${side}.surf.gii BARYCENTRIC $sub_out/${side}.atlasroi.resampled_fs_LR.shape.gii
    # threshold - actually just rounding
    wb_command -metric-math 'round(m)' $sub_out/${side}.atlasroi.resampled_fs_LR.shape.gii \
        -var m $sub_out/${side}.atlasroi.resampled_fs_LR.shape.gii
  done
  # the white seed mask
  for side in L R; do
    wb_command -surface-resample ${StudyDir}/${subid}/${side}.white.32k_fs_LR.surf.gii \
        ${StudyDir}/${subid}/${side}.sphere.32k_fs_LR.surf.gii \
        ${sph}.${side}.surf.gii BARYCENTRIC $sub_out/${side}.white.resampled_fs_LR.surf.gii
  done
done