# import sys
# import torch.utils.data as data
# from PIL import Image
# import os.path
# from torchvision import transforms
# import os
# import time
# from typing import Iterable
# from dataclasses import dataclass
# import numpy as np
import torch
from Mini_grid import Mini_grid

from process_config import *



if __name__ == '__main__':
    
    mean=torch.tensor([0.3764, 0.5077, 0.2877])
    std = torch.tensor([0.0907, 0.0943, 0.1042])
    color_index_grel2red = {'0_5': (26, 235, 55),
               '6_15': (44, 199, 35),
               '16_25': (145, 203, 38),
               '26_35': (178, 193, 47),
               '36_50': (199, 162, 26),
               '51_65': (187, 143, 40),
               '66_80': (194, 112, 74),
              '81_110':(214, 65, 48),
              '111_above':(241, 15, 15)}

    color_index_grel2red_rep = {'0_5': (55, 235, 26),
 '6_15': (35, 199, 44),
 '16_25': (38, 203, 145),
 '26_35': (47, 193, 178),
 '36_50': (26, 162, 199),
 '51_65': (40, 143, 187),
 '66_80': (74, 112, 194),
 '81_110': (48, 65, 214),
 '111_above': (15, 15, 241)}
        
    index = {'0_5': 0,
     '6_15': 1,
     '16_25': 2,
     '26_35': 3,
     '36_50': 4,
     '51_65': 5,
     '66_80': 6,
     '81_110': 7,
     '111_above': 8}

    level_index = {'0_5': 1,
         '6_15': 10,
         '16_25': 20,
         '26_35': 30,
         '36_50': 42,
         '51_65': 58,
         '66_80': 74,
         '81_110': 95,
         '111_above': 130}

#     one = Inference(img_path=img_in,M_N=M_N,out_path=out,alpha=0.8,color_index=color_index_grel2red_rep,index=index,mean=mean,std=std,save = save)
    
#     one.scale_inference_mask(display=False,display_tile = display_tile,flip_rgb = flip_rgb)
    
#     img = r'C:\Users\urial\BG\AlphaBravo\inference\main_cut.jpg'
# out = img.split('.')[0]+'_448_90per.'+img.split('.')[1]
# one = Mini_grid(img_path=img_in,M_N=M_N,out_path=out,alpha=0.8,color_index=color_index_grel2red_rep,index=index,mean=mean,std=std,save = save)
    one = Mini_grid(img_path=img_in,M_N=M_N,out_path=out,alpha=0.8,color_index=color_index_grel2red_rep,\
                    mean=mean,std=std,index=index,level_index=level_index,save = save,stride=stride)
    one.super_inference(flip_rgb = flip_rgb,display_tile=display_tile)
    
    one.selected_heat_map(conf_out)
    
    one.cut_white_crop(path,img_in,conf_out)