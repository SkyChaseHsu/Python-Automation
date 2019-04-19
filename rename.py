#!/usr/bin/env python                

import os

def rename():
    path = "./PAT" 

    filelist = os.listdir(path)
    for files in filelist:
        # file's old location
    	old_dir = os.path.join(path, files)
        # Split the file name and type
    	filename = os.path.splitext(files)[0]
    	filetype = os.path.splitext(files)[1]

        # Pass other files
    	if filetype != '.c':
    		continue
    	# change from PAT-1001 to PAT_1001
        # - We cannot change the char in the string directly
        # - So we turn it in a list, in which we change the certain element
        # - and them turn it into string
    	fn_list = list(filename)
        fn_list[3] = '_'
        new_filename = ''.join(fn_list)

        # file's new location
    	new_dir = os.path.join(path, new_filename + filetype)

    	os.rename(old_dir, new_dir)

rename()

