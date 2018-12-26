#!/usr/bin/Python3
# -*- coding: utf-8 -*-
# =================================================================
# File      : Scan_dir_full.py
# Author    : LinXpy
# Time      : 2018/12/21 21:29
# Function Description :
# 1) Scan the specified whole directory, calculate each subdir and
# file size, list all the subdir and files in it;
# 2) visualize/print the whole directory tree;
# =================================================================

import os
import os.path
from time import strftime, localtime

fsizedicr = {"B": 1,                        # B=Byte
             "KB": float(1)/1024,
             "MB": float(1)/(1024*1024),
             "GB": float(1)/(1024*1024*1024)
             }

scan_path = input("Please input the directory path you want to scan(like D:\somedir\somedir): ")
scan_level = input("Please input the scan level(0:current dir; 1:1st-level subDir; 2:2nd-level subDir....): ")
scan_level = int(scan_level)    # optimize: scan level的大小判断，以及彻底扫描的处理 full scan(scan_level='full')
print("Start to scan the given dir: %s ..." % scan_path)

def get_dir_size(dir_path):
    """
    Description: get the whole size of specified directory dir_path
    """
    dir_size = 0
    for sub_dir_path, sub_dir_names, sub_file_names in os.walk(dir_path):
        for sub_file_name in sub_file_names:
            try:
                sub_file = os.path.join(dir_path, sub_dir_path, sub_file_name)
                dir_size += os.path.getsize(sub_file)
            except:
                print("Hit exception when deal with file %s" % sub_file)
                continue
    return dir_size

def get_dir_file_info(item_path):
    """
    Description: get detail information about the specified dir/file
    item_path: the absolute path of the specified dir or file
    """
    try:
        item_atime = os.path.getatime(item_path)  # get last access time
        item_mtime = os.path.getmtime(item_path)  # get last modification time
        item_ctime = os.path.getctime(item_path)  # get creation time for Windows, last metadata change time for Linux
        access_time = strftime("%Y/%m/%d %H:%M:%S", localtime(item_atime))
        modification_time = strftime("%Y/%m/%d %H:%M:%S", localtime(item_mtime))
        creation_time = strftime("%Y/%m/%d %H:%M:%S", localtime(item_ctime))
    except:
        modification_time = None
        print("Item %s is not dir, nor file" % item_path)

    if os.path.isfile(item_path):
        item_size = os.path.getsize(item_path)  # get file size
    elif os.path.isdir(item_path):
        item_size = get_dir_size(item_path)
    else:
        item_size = 0
        print("Item %s is not dir, nor file" % item_path)

    return item_size, modification_time

def size_transform(size):
    """
    Description: transform the int size(byte) into string size with specified unit(GB, MB, KB, B)
    """
    if size > 1024 * 1024 * 1024:
        size_str = str(round(fsizedicr['GB'] * size, 2)) + 'GB'
    elif size > 1024 * 1024:
        size_str = str(round(fsizedicr['MB'] * size, 2)) + 'MB'
    elif size > 1024:
        size_str = str(round(fsizedicr['KB'] * size, 2)) + 'KB'
    else:
        size_str = str(round(fsizedicr['B'] * size, 2)) + 'B'
    return size_str

base_path_list = scan_path.split('\\')   # D:\Doc_Test -> ['D:', 'Doc_Test']
base_path_len = len(base_path_list)

# dir_list_dict:
# key: dirname of level0 + '-level' + level_flag(offset)(like "test-level1")
# value: list of dirs & files in current dir
dir_list_dict = {}      # store the list of files & dirs in each scan dir
dir_info_dict = {}      # store the info(size, mtime) of dirs in each scan dir
file_info_dict = {}     # store the info(size, mtime) of files in each scan dir

def scan_dir(scan_path, scan_level):
    """
    Description: 
        list the dirs & files in the scan dir of each scan level;
        calculate the size of dirs & files in the scan dirl
        store the scan dirs & files info into dict(info: size, modification time);
    """
    size = 0                        # size of current scan dir scan_path
    print("Dir scan path: %s" % scan_path)
    path_list = scan_path.split('\\')
    path_len = len(path_list)
    level_flag = path_len - base_path_len   # current scan path level based on the base scan path
    print("Dirs scan level: %d" % level_flag)
    dir_file_list = os.listdir(scan_path)
    print("Dirs or files list: %s" % dir_file_list)

    # if level_flag == 0:     # reserve the name of dirs in root scan path to form the key of dir_list_dict
    #     root_subdir_list = dir_file_list
    if level_flag == 0:     # scan the initial base path
        key_name = os.path.basename(scan_path)
        dir_list_dict[key_name] = dir_file_list
    elif level_flag == 1:   # extract root subdir(level 0) name from path_list for current scan dir
        root_subdir_name = path_list[base_path_len]     # list index is 0 base
        key_name = root_subdir_name
        dir_list_dict[key_name] = dir_file_list
    else:
        root_subdir_name = path_list[base_path_len]
        key_name = root_subdir_name + "@level" + str(level_flag - 1) + '@' + path_list[-1]    # construct special key_name with root subdir
        dir_list_dict[key_name] = dir_file_list

    # calculate the size of directory scan_path
    for item in os.listdir(scan_path):
        item_full = os.path.join(scan_path, item)
        item_size, mtime = get_dir_file_info(item_full)
        size += item_size

        # if file, store file info into dict according to current level_flag for latter usage
        if os.path.isfile(item_full):
            if level_flag == 0:     # files in initial base path
                file_size_str = size_transform(item_size)
                key_name = item
                file_info_dict[key_name] = "size:%s mtime:%s" % (file_size_str, mtime)
            else:
                file_size_str = size_transform(item_size)
                root_subdir_name = path_list[base_path_len]  # list index is 0 base
                key_name = root_subdir_name + "@level" + str(level_flag) + '@' + item
                file_info_dict[key_name] = "size:%s mtime:%s" % (file_size_str, mtime)
        # if dir, store dir info into dict later in outside of for cycle
        if os.path.isdir(item_full):
            if level_flag == 0:  # dirs in initial base path
                dir_size_str = size_transform(item_size)
                key_name = item
                dir_info_dict[key_name] = "size:%s mtime:%s" % (dir_size_str, mtime)
            else:
                dir_size_str = size_transform(item_size)
                root_subdir_name = path_list[base_path_len]
                key_name = root_subdir_name + "@level" + str(level_flag) + '@' + item
                dir_info_dict[key_name] = "size:%s mtime:%s" % (dir_size_str, mtime)

    #     if os.path.isdir(item_full) and scan_level > 0:  # recursively scan next level dir
    #         scan_dir(item_full, scan_level - 1)
    size_str = size_transform(size)
    print("Current dir %s size is: %s" % (scan_path, size_str))

    # store the base scan dir info into dict
    if level_flag == 0:
        # base_dir_size_str = size_transform(size)
        base_dir_size_str = size_str
        key_name = os.path.basename(scan_path)
        base_dir_atime = os.path.getatime(scan_path)
        base_dir_mtime = os.path.getmtime(scan_path)
        base_dir_ctime = os.path.getctime(scan_path)
        access_time = strftime("%Y/%m/%d %H:%M:%S", localtime(base_dir_atime))
        modification_time = strftime("%Y/%m/%d %H:%M:%S", localtime(base_dir_mtime))
        creation_time = strftime("%Y/%m/%d %H:%M:%S", localtime(base_dir_ctime))
        dir_info_dict[key_name] = "size:%s mtime:%s" % (base_dir_size_str, modification_time)

    # According to scan_level to decide whether need to scan deeper
    for item in os.listdir(scan_path):
        item_full = os.path.join(scan_path, item)
        if os.path.isdir(item_full) and scan_level > 0:  # recursively scan next level dir
            scan_dir(item_full, scan_level - 1)

def create_show_dir_tree(scan_path, scan_level):
    """
    Description: create and print the whole dir tree
    """
    node_icon = {"BRANCH": '├─',
                 "LAST_BRANCH": '└─',
                 "TAB": '│  ',
                 "EMPTY_TAB": '   '}
    # BRANCH = '├─'
    # LAST_BRANCH = '└─'
    # TAB = '│  '
    # EMPTY_TAB = '   '

    level_flag = 0
    base_dir_name = os.path.basename(scan_path)     # root dir name of scan_path
    root_node = base_dir_name
    print(root_node)
    for item in dir_list_dict[base_dir_name]:   # item: root subdir name or file name, level 0
        if item not in dir_info_dict.keys():  # a file
            root_subfile_node = node_icon["LAST_BRANCH"] + item
            root_subfile_info = file_info_dict[item]
            print(root_subfile_node)
        else:
            root_subdir_node = node_icon["BRANCH"] + item
            root_subdir_info = dir_info_dict[item]
            print(root_subdir_node)
            level_flag += 1
            parse_dict_create_tree(level_flag, item, item, node_icon)   # for root subdir, key_name==root_subdir_name
            level_flag = 0

def parse_dict_create_tree(level_flag, key_name, root_subdir_name, node_icon):
    """
    Description: recursively create and print subdir tree
    key_name: the specially constructed name for subdir, files
    root_subdir_name: the subdir & file name in root scan dir, use to construct the key_name
    """
    if level_flag <= scan_level and len(dir_list_dict[key_name]) > 0:   # dir key_name not empty
        for sub_item in dir_list_dict[key_name]:
            key_name = root_subdir_name + "@level" + str(level_flag) + '@' + sub_item   # construct special key for subdir/file
            if key_name not in dir_info_dict.keys():  # a file
                level_subfile_node = node_icon["TAB"] * level_flag + node_icon["LAST_BRANCH"] + sub_item
                level_subfile_info = file_info_dict[key_name]
                print(level_subfile_node)
            else:   # a dir
                level_subdir_node = node_icon["TAB"] * level_flag + node_icon["BRANCH"] + sub_item
                level_subdir_info = dir_info_dict[key_name]
                print(level_subdir_node)
                parse_dict_create_tree(level_flag + 1, key_name, root_subdir_name, node_icon)


if __name__ == "__main__":
    scan_dir(scan_path, scan_level)
    print(dir_list_dict)
    print(file_info_dict)
    print(dir_info_dict)
    create_show_dir_tree(scan_path, scan_level)
