#!/usr/bin/env python                

import os

def rename():
    path = "./PAT" 

    filelist = os.listdir(path)
    for files in filelist:
    	old_dir = os.path.join(path, files)
    	filename = os.path.splitext(files)[0]
    	filetype = os.path.splitext(files)[1]
    	if filetype != '.c':
    		continue
    	# change from PAT-1001 to PAT_1001
    	fn_list = list(filename)
        fn_list[3] = '*'
        new_filename = ''.join(fn_list)
    	new_dir = os.path.join(path, new_filename + filetype)
    	os.rename(old_dir, new_dir)

rename()