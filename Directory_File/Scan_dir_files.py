


import os
from time import strftime, localtime


fsizedicr = {"B": 1,                        # B=Byte
             "KB": float(1)/1024,
             "MB": float(1)/(1024*1024),
             "GB": float(1)/(1024*1024*1024)
             }

path = input("Please input the directory path you want to scan: ")

for dir_path, dir_names, file_names in os.walk(path):
    
    print("Files in directory: ", dir_path)
    print('=' * 60)
    print(os.listdir(dir_path))     # list the directories and files of dir_path
    
    for file in file_names:
        file_abpath = os.path.join(dir_path, file)
        file_atime = os.path.getatime(file_abpath)  # get last access time
        file_mtime = os.path.getmtime(file_abpath)  # get last modification time
        file_ctime = os.path.getctime(file_abpath)  # get creation time for Windows, last metadata change time for Linux
        file_size = os.path.getsize(file_abpath)    # get size
        access_time = strftime("%Y/%m/%d %H:%M:%S",localtime(file_atime))
        modification_time = strftime("%Y/%m/%d %H:%M:%S",localtime(file_mtime))
        creation_time = strftime("%Y/%m/%d %H:%M:%S",localtime(file_ctime))

        if file_size>1024*1024*1024:
            sfile = str(round(fsizedicr['GB']*file_size,2))+'GB'
        elif file_size>1024*1024:
            sfile = str(round(fsizedicr['MB']*file_size,2))+'MB'
        elif file_size>1024:
            sfile = str(round(fsizedicr['KB']*file_size,2))+'KB'
        else:
            sfile = str(round(fsizedicr['B']*file_size,2))+'B'
        
#        print(file,':',sfile, ',',access_time, ',',modification_time, ',',creation_time)
        print(file,':  ',sfile, ',  ',creation_time)
#        print("-"*60)
    print('=' * 60)
