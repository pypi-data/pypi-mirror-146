import sys
import os
from Inference import Inference
import cv2
from collections import defaultdict
import numpy as np
# M_N = sys.argv[1]
# save = bool(int(sys.argv[2]))
# display_tile = bool(int(sys.argv[3]))
# flip_rgb = bool(int(sys.argv[4]))
# stride = sys.argv[5]
# img_in = sys.argv[6]
# stride = 64 if stride is None else stride
# out = img_in.split('.')[0]+'_inference.'+img_in.split('.')[1]
# conf_out = out.split('.')[0]+'_conf_thresh.'+out.split('.')[1]
from process_config import *
class Mini_grid(Inference):
    def __init__(self,img_path,M_N,out_path,alpha,save,color_index,index,\
                 level_index,stride,mean,std):
        
        self.stride = int(stride)
        Inference.__init__(self,img_path,M_N,out_path,alpha,color_index=color_index,\
                           index=index,level_index=level_index,mean=mean,std=std,save=save)
        
        self.img4pred = self.img.copy()
        self.img4heat = self.img.copy()

        
    def super_inference(self,thresh = 0.2,display = False,display_tile=display_tile,flip_rgb = flip_rgb):
        self.flip_rgb = flip_rgb
        self.display_tile = display_tile
        grid_num = 0            
        self.di = defaultdict(list)
  
        def inner_process(y,x,y1,x1,thresh):
            tile = self.img4pred[y:y1, x:x1]#img[y:y1, x:x1]
            self.img,cls,key, prob = self.pred_tile(y,x,y1,x1,tile)
 
            percent_not_white = len(tile[tile!=255])/(tile.shape[0]*tile.shape[1]*tile.shape[2])
    
            if prob>thresh and percent_not_white>0.7:
                key_val = self.mini_grid(y,x,y1,x1)
                print(key_val)
                [self.di[key_val[i]].append(cls[0]) for i in range(len(key_val))]
                
        for y in range(0, self.imgheight, self.stride):
            for x in range(0, self.imgwidth, self.stride):
                
                grid_num+=1 
                y1 = y + self.M
                x1 = x + self.N
                    
                # check whether the patch width or height exceeds the image width or height
                if x1 >= self.imgwidth and y1 >= self.imgheight:
                    x1 = self.imgwidth - 1
                    y1 = self.imgheight - 1
                        
#                     tile = self.img4pred[y:y1, x:x1]#img[y:y1, x:x1]
#                     self.img,cls,key, prob = self.pred_tile(y,x,y1,x1,tile)
#                     if prob>thresh:
#                         key_val = self.mini_grid(y,x,y1,x1)
#                         [di[key_val[i]].append(cls[0]) for i in range(len(key_val))]
                        
                    inner_process(y,x,y1,x1,thresh)

                elif y1 >= self.imgheight: # when patch height exceeds the image height
                    y1 = self.imgheight - 1
                    
#                     code cut is here
                    inner_process(y,x,y1,x1,thresh)   
    
                elif x1 >= self.imgwidth: # when patch width exceeds the image width
                    x1 = self.imgwidth - 1
                    
#                     code cut is here
                    inner_process(y,x,y1,x1,thresh)

                else:
#                     code cut is here
                    inner_process(y,x,y1,x1,thresh)

        self.mini_grid_vals = self.di
        
        self.calculate_mini_grid()
        print('process ended')
        
        if display:
            self.dis_im(self.img)
        if self.save:
            cv2.imwrite(self.out, self.img) 
            print('img saved')
        return self.mini_grid_vals
            
    def mini_grid(self,y,x,y1,x1):
#     grid_num = 0
        val_list = []
        for y_ in range(y, y1, self.stride):
            for x_ in range(x, x1, self.stride):

                y1_ = y_ + self.stride
                x1_ = x_ + self.stride
                # check whether the patch width or height exceeds the image width or height
                if x1_ >= x1 and y1_ >= y1:
                    x1_ = x1
                    y1_ = y1
                    val_list.append(f'{y_,x_,y1_,x1_}')

                elif y1_ >= y1: # when patch height exceeds the image height
                    y1_ = y1
                    val_list.append(f'{y_,x_,y1_,x1_}')
                elif x1_ >= x1: # when patch width exceeds the image width
                    x1_ = x1
                    val_list.append(f'{y_,x_,y1_,x1_}')
                else:
                    val_list.append(f'{y_,x_,y1_,x1_}')
        return val_list
    
    def calculate_mini_grid(self):
        mean_preds = defaultdict(list)
        for key,val in self.mini_grid_vals.items():
            mini_grid = key.replace('(','').replace(')','').split(',')
            [mean_preds[key].append(int(coordinate)) for coordinate in mini_grid]
            if len(val)>1:
                mean_val = int(np.around(np.mean(val)))
        #         print(key,val,)
                mean_preds[key].append(mean_val)
            else:
                mean_preds[key].append(val[0])
        self.mean_preds = mean_preds
        self.mean_overall_level = self.mean_level_accumulate()
        print(f'{"-"*20}\nProcess ended!\nThe overall level detected is {int(self.mean_overall_level)}\n{"-"*20}\n')
        
    def selected_heat_map(self,out_path):

        
        for key,val in self.mean_preds.items():
            heat_img_out = self.img4heat.copy()
            key = self.get_val(self.index,val[4])
            color = self.color_index[key]
            cv2.rectangle(self.img4heat, (val[1], val[0]), (val[3], val[2]), color, 1)
            cv2.rectangle(self.img4heat, (val[1], val[0]), (val[3], val[2]), color, -1)
            self.img4heat= cv2.addWeighted(self.img4heat, self.alpha, heat_img_out, 1 - self.alpha,0, heat_img_out)
#             self.img4heat = bla(val[1], val[0],val[2], val[3],color)
        cv2.imwrite(out_path, self.img4heat) 
        print('img saved')
        
     