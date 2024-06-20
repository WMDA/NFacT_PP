from NFACT_PP.nfactpp import main_nfact_preprocess, hcp_stream_main
from NFACT_PP.nfactpp_argument_functions import args
from NFACT_PP.nfactpp_utils_functions import error_and_exit, Signit_handler
from NFACT_PP.nfactpp_check_functions import check_fsl_is_installed, check_study_folder, does_list_of_subjects_exist, return_list_of_subjects_from_file, list_of_subjects_from_directory

if __name__ == "__main__":
    arg = args()
    handler = Signit_handler()
    error_and_exit(
        check_fsl_is_installed(),
        "FSLDIR not in path. Check FSL is installed or has been loaded correctly",
    )
    
    error_and_exit(check_study_folder(arg["study_folder"]))
    if arg["list_of_subjects"]:
        error_and_exit(
            does_list_of_subjects_exist(
                arg["list_of_subjects"]),
                "List of subjects doesn't exist.",
        )

        arg["list_of_subjects"] = return_list_of_subjects_from_file(
            arg["list_of_subjects"]
        )

        error_and_exit(arg["list_of_subjects"])

    if not arg["list_of_subjects"]:
        arg["list_of_subjects"] = list_of_subjects_from_directory(
            arg["study_folder"]
        )

        error_and_exit(
            arg["list_of_subjects"], 
            "Unable to find list of subjects from directory"
        )
    
    if arg['hcp_stream']:
        hcp_stream_main(arg)

        
    main_nfact_preprocess(arg)