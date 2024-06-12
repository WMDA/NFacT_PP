
code_folder=/home/mszdjh3/NFacT/NFACT
sub_nfact2=/home/mszdjh3/for_axon/sub1/nfact
study_folder=/home/mszdjh3/for_axon/group1_nfact_group

${code_folder}/nfact_dualregress -gm_comps $study_folder/NMF_GM_100.LR.dscalar.nii -sub_dir $sub_nfact2 -seeds $sub_nfact2/L.white.resampled_fs_LR.surf.gii $sub_nfact2/R.white.resampled_fs_LR.surf.gii -rois $sub_nfact2/L.atlasroi.resampled_fs_LR.shape.gii $sub_nfact2/R.atlasroi.resampled_fs_LR.shape.gii -n_cores 10