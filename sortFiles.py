import os
import subprocess
import shutil
from os import path
import tkinter as tk
# from tkinter import ttk #Creates widgets (buttons and such)
import ttkbootstrap as ttk
import sqlite3 #SQLite import for Database
from datetime import datetime

def is_process_running(process_name):
    cmd = 'tasklist /fi "imagename eq {}"'.format(process_name)
    output = subprocess.check_output(cmd, shell=True).decode()
    if process_name.lower() in output.lower():
        return True
    else:
        return False
is_process_running("chrome.exe")

# Create Database that Stores Class Codes
def create_database():
    conn = sqlite3.connect("ClassCodes.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS ClassCodes (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                )""")
    conn.commit()
    conn.close()

# Add new class code when it is submitted
def on_submit():
    class_code = entry.get()
    conn = sqlite3.connect("ClassCodes.db")
    c = conn.cursor()

    c.execute("INSERT INTO ClassCodes (name) VALUES (?)", (class_code,))
    print("Class " + class_code + " added")
    conn.commit()
    conn.close()

    displayClassCodes()



def displayClassCodes():
    values = []
    param = "name"
    conn = sqlite3.connect("ClassCodes.db")
    c = conn.cursor()

    c.execute("SELECT " + param +" FROM ClassCodes")

    rows = c.fetchall()
    for element in rows:
        for i in element:
            values.append(i)

    print(values)
    conn.close()

    for i in range(0,len(values)):
        if i % 2 == 0:
            ClassCodes.insert("", "end", text = values[i])
        else:
            ClassCodes.insert("", "end", text = values[i])
    

# Add a new class code to search for
def lastRan():
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M")
    text_Str.set("Last sorted: " + dt_string)

#Find files that have the class code in the name
def findFiles(classcode):
    dir_path = r'C:\Users\chand\Desktop' #Where class Files should be when first made
    classFiles = []    #Store found classFiles
    for file_path in os.listdir(dir_path):    #Sort through desktop directory

        if os.path.isfile(os.path.join(dir_path, file_path)): #Locate all files in directory
            if classcode in file_path or classcode.lower() in file_path: #Add file that has classCode in the name to the list
                classFiles.append(file_path)


    print(classFiles)
    if len(classFiles) == 0:
        print("No Class files found")

    return classFiles
# End of findFiles function


# Move files to correct Folder in designated spot
def moveFiles(files_to_move, class_code):
    print("Start of Move Files function")
    source_folder = r'C:\Users\chand\Desktop\\'
    destination_folder = r"C:\Users\chand\OneDrive\Documents\School\EFSC\ClassAssignments\\" + class_code + "\\"

    #Folder path not created yet, make it now
    if not os.path.exists(destination_folder):
        print("Folder path not found. Creating path now...")
        os.makedirs(destination_folder)

    # iterate files
    for file in files_to_move:
        # construct full file path
        source = source_folder + file
        destination = destination_folder + file
        # move file
        shutil.move(source, destination)
        print('Moved:', file)
    print("End of Move Files Function")


# Delete Class Code function (Delete the class code from the name of the file)
def deleteCC(classcode,files_moved):
    dir_path = r"C:\Users\chand\OneDrive\Documents\School\EFSC\ClassAssignments\\" + classcode + "\\"
    print("Start of Function Deleting the Class Codes from Files")
    

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
    print("End of Function Deleting the Class Codes from Files")
#
# End of DeleteCC (Class Code) function



# Run program function (like main)    
def run():
    values = []
    param = "name"
    conn = sqlite3.connect("ClassCodes.db")
    c = conn.cursor()

    c.execute("SELECT " + param +" FROM ClassCodes")

    rows = c.fetchall()
    for element in rows:
        for i in element:
            values.append(i)

    print(values)
    conn.close()


    for i in range(0,len(values)):
        print(values[i])
        moving_files = findFiles(values[i])
        moveFiles(moving_files, values[i])
        deleteCC(values[i],moving_files)

create_database()
run()


### Start of TKinter code

# Create window
window = ttk.Window(themename= 'darkly')
window.title('File Sorter App')
window.geometry('728x318')

main_frame = tk.Frame(master=window)

# Title Text
title_frame = tk.Frame(window, highlightbackground="red", highlightthickness="2")
title_label = ttk.Label(master = title_frame, text = 'Run the App', font = 'Calibri 24 bold')

# Title layout
title_label.pack(fill= 'both')
title_label.configure(anchor='center')
title_frame.pack(anchor="n", fill="x")

# New Class Code field
newClass_Frame = tk.Frame(main_frame, highlightbackground="blue", highlightthickness=2) #div for entire entry section
entry_Frame = tk.Frame(newClass_Frame)
entry_Str = tk.StringVar()
entry_label = ttk.Label(master=newClass_Frame, text = 'Enter new Class Code Here', font = 'Calibri 12 bold')
entry = ttk.Entry(master= entry_Frame, textvariable = entry_Str, background= 'white')
button = ttk.Button(master = entry_Frame, text = 'Submit', command = on_submit)
bg1 = ttk.Label(master = newClass_Frame,text= 'Test', background = 'red'  )

# New Class Code box Layout
entry_label.pack(pady=15)
entry.pack(side="left")
button.pack(side="left")
entry_Frame.pack(padx = 60, pady= 15)
newClass_Frame.grid(row=0, column=0, sticky="NSW")

# Output Class codes fields
output_Frame = tk.Frame(master=main_frame, highlightbackground= "green", highlightthickness=2)
ClassCodes_Label = tk.Label(master=output_Frame, text = "Current Class Codes", font = 'Calibri 12 bold')
output_Classes_Frame = tk.Frame(master=output_Frame)
ClassCodes = ttk.Treeview(output_Frame, column=("c1"))

ClassCodes.column("# 0", anchor="center")

#data inserted into the ClassCodes tree for testing
displayClassCodes()


# Output Class Codes Layout
ClassCodes_Label.pack(anchor="center", pady= 15)
ClassCodes.pack(anchor="center")
output_Classes_Frame.pack()#anchor="center", fill="x")
output_Frame.grid(row= 0, column=1, sticky="NSE")

# timestamp section
timestamp_frame = ttk.Frame(master=window)
text_Str = tk.StringVar()
lastRan()
timestamp_label = ttk.Label(master= timestamp_frame,textvariable= text_Str, background='blue', font = 'Calibri 12 bold')
timestamp_label.pack(fill='both')
timestamp_label.configure(anchor='center')


main_frame.pack(fill="x",anchor="center")
timestamp_frame.pack(fill="x", anchor="s")
#run application call
window.mainloop()

### End of Tkinter code






