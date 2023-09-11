import os
import shutil
from os import path

FILE_DIR_PATTERN = ["COP2500", "COP1000"]    #Class codes in file name



def findFiles(classcode):
    dir_path = r'C:\Users\chand\OneDrive\Desktop' #Where class Files should be when first made
    classFiles = []    #Store found classFiles
    for file_path in os.listdir(dir_path):    #Sort through desktop directory

        if os.path.isfile(os.path.join(dir_path, file_path)): #Locate all files in directory
            if classcode in file_path or classcode.lower() in file_path: #Add file that has classCode in the name to the list
                classFiles.append(file_path)


    print(classFiles)
    return classFiles


def moveFiles(files_to_move):
    source_folder = r'C:\Users\chand\OneDrive\Desktop\\'
    destination_folder = r"C:\Users\chand\OneDrive\Documents\School\EFSC\ClassAssignments\\" + FILE_DIR_PATTERN[i] + "\\"

    # iterate files
    for file in files_to_move:
        # construct full file path
        source = source_folder + file
        destination = destination_folder + file
        # move file
        shutil.move(source, destination)
        print('Moved:', file)

    return 0

def deleteCC(classcode,files_moved):
    dir_path = r"C:\Users\chand\OneDrive\Documents\School\EFSC\ClassAssignments\\" + classcode + "\\"
    print("Delete Class Code from Files")

    #Search through the class folder for files with the class code
    for file_path in os.listdir(dir_path):
        #If it does have class code upper cased remove it
        if classcode in file_path:
            print("file path: " + file_path)
            new_file_name = file_path.replace(classcode,'')
            os.rename(os.path.join(dir_path,file_path),os.path.join(dir_path,new_file_name))
            print("file name changed to: " + new_file_name)
        #If it does have class code lower cased remove it
        if classcode.lower() in file_path:
            print("file path: " + file_path)
            new_file_name = file_path.replace(classcode.lower(),'')
            os.rename(os.path.join(dir_path,file_path),os.path.join(dir_path,new_file_name))
    return 0

for i in range(0,len(FILE_DIR_PATTERN)):
    print(FILE_DIR_PATTERN[i])
    moving_files = findFiles(FILE_DIR_PATTERN[i])
    moveFiles(moving_files)
    deleteCC(FILE_DIR_PATTERN[i],moving_files)