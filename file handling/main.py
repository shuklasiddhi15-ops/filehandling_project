
# CRUD - File Handling
# Create
# Read
# Update
# Delete
# Rename a file.
import os
from pathlib import Path
from pathlib import Path

# create
def create_file():
 filename = input('enter your file:') #superman.txt
 path = Path(filename) #c:/users/siddhi/destop/filehandling/superman.txt
 if path.exists():
    print('file already exists')
 else:
  with open (filename, 'w') as file:
    content=input('enter your content:')
    file.write(content)
    print('file created....')

# read

def read_file():
  filename = input('enter your file:') #superman.txt
  path = Path(filename)
  if path.exists():
    with open (filename,'r') as file:
      print(file.read())
  else: 
    print('file does not exists')

# update
def update_file():
  filename = input('enter your file')
  path=Path(filename)
  if path.exists():
    with open (filename,'a') as file:
      content = input('enter your file content ')
      file.write(content)
      print('file updated sucessfully...')
  else:
    print("file does not exists!!")

# delete
def delete_file():
  filename = input("enter your file name")
  path = Path(filename)
  if path.exists():
    os.remove(path)
    print("file is deleted sucessfully")
  else:
    print("file does not exists")  

# rename
def rename_file():
    old_name = input('Enter your file name: ')
    path     = Path(old_name)

    if path.exists():
        new_name = input('Enter new name for your file: ')
        os.rename(old_name, new_name)
        print('File name changed..')

    else:
        print('File does not exists....')

# folder created 
def create_folder():
  foldername= input("enter your folder name")
  path = Path(foldername)
  if path.exists():
    print("folder is created")
  else:
    os.mkdir(foldername)
    print("folder created")

# delete folder
def delete_folder():
    foldername = input('Enter name of folder: ')
    path = Path(foldername)

    if path.exists():
        os.rmdir(foldername)
        print('Folder Created....')
    
    else:
        print('File does not exists!!')




while True:
  print("------Menu-----")
  print('Press 0 for exiting....')
  print("press 1 for creating file")
  print("press 2 for reading file")
  print("press 3 for updating file")
  print("press 4 for deleting file")
  print("press 5 for renaming file")
  print("press 6 for creating folder")
  print("press 7 for deleting folder")
  choice = int(input("enter your choice"))

  if choice ==0:
    print('exiting')
    break

  elif choice ==1:
    create_file()
    
  elif choice == 2:
    read_file()

  elif choice == 3:
    update_file()
 
  elif choice == 4:
    delete_file()

  elif choice == 5:
    rename_file()

  elif choice == 6:
    create_folder()

  elif choice == 7:
    delete_folder()
    




   