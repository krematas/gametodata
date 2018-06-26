# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pyffi.formats.dds as pyffi
import matplotlib.pyplot as plt
import struct
from os import listdir
from os.path import isfile, join
import sys

np.set_printoptions(suppress=True)

path_to_data = 'O:\\unix\\projects\\grail\\krematas\\data\\play_for_data\\'

filenames = [f for f in listdir(join(path_to_data, 'depth')) if isfile(join(path_to_data, 'depth', f))]
dirs_to_check = ['depth']

filenames.sort()
filenames = filenames[0:27]


h, w = 1080, 1920

#filenames = ['00000.dds']

for fname in filenames:
    
    for ddir in dirs_to_check:
        fname2 = join(path_to_data, ddir, fname)
        print(ddir, fname2)
        with open(fname2, mode='rb') as file: # b is important -> binary
            fileContent = file.read()
            
            depth = np.zeros((h, w))
            for i in range(h):
                for j in range(w):
                    start = 148+i*w*8+j*8
                    end = start+4
                    byte = fileContent[start:end]
                    value = struct.unpack('f', byte)
                    depth[i, j] = value[0]
                    
            np.savez(join(path_to_data, ddir, fname.replace('.dds', '')), depth)
    
    plt.imshow(depth)
    plt.show()
sys.exit(-1)
    
print(depth)
plt.imshow(depth)





filenames = ['18291.dds']

#from PIL import Image
#dds = Image.open(join(path_to_data, 'depth', filenames[0]))


for fname in filenames:
    stream = open(join(path_to_data, 'depth', fname), 'rb')
    
    pyffi.DdsFormat.Data()
    data = pyffi.DdsFormat.Data()
    
    data.read(stream)
    
    
    h, w = data.header.height, data.header.width
    
    
    raw_data = data.pixeldata.get_value()
    depth = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            start = 0+i*w*8+j*8
            end = start+8
            byte = raw_data[start:end]
            value = struct.unpack('d', byte)
            depth[i, j] = value[0]
    
    print(depth)
    plt.imshow(depth)
    np.savez(join(path_to_data, 'depth', fname.replace('.dds', '')), depth)
    plt.imshow(depth[800:1080, 300:500])
    plt.show()
    break
        