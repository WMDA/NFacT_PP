from NFACT.nfact_preproc_arguments import args
import NFACT.nfact_preprocessing_functions as npf
import os
import glob

def main_nfact_preprocess():
    arg = args()

    if not os.path.exists(arg['study_folder']):
        print("Study folder provided doesn't exist")
        print('Exiting...')
        exit(1)
    
    if arg['list_of_subjects']:
        if (not os.path.exists(arg['list_of_subjects'])) or (os.path.isdir(arg['list_of_subjects'])):
            print("List of subjects doesn't exist.")
            print('Exiting...')
            exit(1)
        if (arg['list_of_subjects'].split('.')[1] != None) or (arg['list_of_subjects'].split('.')[1] != 'txt'):
            print('List of subjects is not ascii file. Please specify a list of subject or remove flag')
            print('Exiting...')
            exit(1)
        try:
            arg['list_of_subjects'] = npf.read_file_to_list(arg['list_of_subjects'])
        except Exception as e:
            print(f'Unable to open subject list due to: {e}')

    if not arg['list_of_subjects']:
        list_of_subject = glob.glob(os.path.join(arg['study_folder'], '*'))
        arg['list_of_subjects'] = [directory for directory in list_of_subject if os.path.isdir(directory)]
        print(arg)
    
    #npf.create_paths(arg)

    #if not npf.check_directory_exists(arg['study_folder']):
    #    print('No such study directory ')


if __name__ == "__main__":
    main_nfact_preprocess()
