from NFACT.nfact_preproc_arguments import args
import NFACT.nfact_preprocessing_functions as npf
import os
import glob


def main_nfact_preprocess():
    arg = args()
    if not npf.check_study_folder(arg["study_folder"]):
        exit(1)

    if arg["list_of_subjects"]:
        if not npf.does_list_of_subjects_exist(arg["list_of_subjects"]):
            exit(1)
        arg["list_of_subjects"] = npf.return_list_of_subjects_from_file(
            arg["list_of_subjects"]
        )
        if not arg["list_of_subjects"]:
            exit(1)

    if not arg["list_of_subjects"]:
        arg["list_of_subjects"] = npf.list_of_subjects_from_directory(
            arg["study_folder"]
        )
        if not arg["list_of_subjects"]:
            print("Unable to find list of subjects from directory")
            print("Exiting...")
            exit(1)
    
    if not npf.check_subject_files(arg):
        print('\nExiting...\n')
        exit(1)
    #print(arg)
    

if __name__ == "__main__":
    main_nfact_preprocess()
