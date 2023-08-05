import sys
import os
from Model_activation import Model_activation
from help_utils import Helper_functions
import cv2
from collections import defaultdict
from torchvision import datasets, transforms,models
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

from process_config import *
class Inference(Model_activation,Helper_functions):
                 
    def __init__(self,img_path,M_N,flip_rgb=flip_rgb,display_tile=display_tile,out_path=None,alpha = 0.5,color_index=None,index=None,\
                 level_index=None,mean = None,std = None,save = False):#,model
        Model_activation.__init__(self)#,model_path
        self.img = cv2.imread(img_path)# if im_from_file else img_path
        self.image_mini = cv2.imread(img_path)#self.img.copy()
        self.img4pred = cv2.imread(img_path)#self.img
        
        self.mean = mean if mean is not None else (0.4611, 0.4359, 0.3905)
        self.std = std if std is not None else (0.2193, 0.2150, 0.2109)
        
        self.flip_rgb = flip_rgb
        self.display_tile = display_tile
        
#         b,g,r = cv2.split(img) self.img = cv2.merge([r,g,b]) tile = cv2.merge([r,g,b])
#         self.model = model
        self.N = self.M = int(M_N)
        self.alpha = alpha
        self.color_index = color_index
        self.index = index
        self.out = img_path.split('.')[0]+'_out.'+img_path.split('.')[1] if out_path is None else out_path
        self.level_index = level_index

        
        self.imgheight=int(self.img.shape[0])
        self.imgwidth=int(self.img.shape[1])
        self.d = defaultdict(list)
        
        self.count_index = {}
        self.grid_index = {}
        self.save = save

        for key in color_index.keys():
            self.count_index[key]=0
            self.grid_index[key]=[]

    def prediction(self, device, batch_input):
        """Uses:   pytorch
            Used by: self.predict
        """
        # send model to cpu/cuda according to your system configuration
        self.model.to(device)
        # it is important to do model.eval() before prediction
        self.model.eval();data = batch_input.to(device);output = self.model(data)
        # Score to probability using softmax
        prob = F.softmax(output, dim=1)
        # get the max probability
        pred_prob = prob.data.max(dim=1)[0]
        # get the index of the max probability
        pred_index = prob.data.max(dim=1)[1]
        
        return pred_index.cpu().numpy(), pred_prob.cpu().numpy()    
    

         
    def predict(self,np_img):
        """Uses:    self.prediction
           Used by: self.pred_tile
           """
#         img = cv2.cvtColor(np_img, cv2.COLOR_BGR2RGB)
        img_tile_pil = transforms.functional.to_pil_image(np_img)
#         img_tile_pil = = cv2.cvtColor(img_tile_pil, cv2.COLOR_BGR2RGB)
        transform = self.image_common_transforms()
        img = transform(img_tile_pil)
        tensor_img = img.unsqueeze(0)
        cls, prob = self.prediction('cpu', batch_input=tensor_img)
        key = self.get_val(self.index,cls)
        print('cls: {}, key: {},prob: {}'.format(cls,key, prob))
        color = self.color_index[key]
        print(self.display_tile)
        if self.display_tile:
            self.dis_im(np_img,(cls,prob,key))
        return cls,key, prob,color
    
    def pred_tile(self,y,x,y1,x1,mask_im):
        """Uses: self.predict
           Used by: self.update_process
        """

        mask_im = cv2.cvtColor(mask_im, cv2.COLOR_BGR2RGB) if self.flip_rgb else mask_im
        
        cls,key, prob,color = self.predict(mask_im)
        newMat_3ch_out = self.img.copy()
#         newMat_3ch_out = cv2.cvtColor(newMat_3ch_out, cv2.COLOR_BGR2RGB)
        cv2.rectangle(self.img, (x, y), (x1, y1), color, 1)

        cv2.rectangle(self.img, (x, y), (x1, y1), color, -1)
        cv2.addWeighted(self.img, self.alpha, newMat_3ch_out, 1 - self.alpha,0, newMat_3ch_out)

        return newMat_3ch_out,cls,key, prob    
    
    def update_process(self,y,x,y1,x1):
        """Uses: self.pred_tile
           Used by: self.scale_inference_mask
        """
#         mask_im,drop_thresh = self.mask(y,x,y1,x1)
#         if drop_thresh>drop:
        tile = self.img4pred[y:y1, x:x1]#img[y:y1, x:x1]
        self.img,cls,key, prob = self.pred_tile(y,x,y1,x1,tile)
        self.grid_index[key].append([(x, y), (x1, y1)])
        self.count_index[key]+=1
            
    def scale_inference_mask(self,display = False,display_tile=display_tile,flip_rgb = flip_rgb):
        #use to flip RGB to BGR in other methodes
#         self.flip_rgb = flip_rgb
#         self.display_tile = display_tile
        
        for y in range(0, self.imgheight, self.M):
            for x in range(0, self.imgwidth, self.N):
                y1 = y + self.M
                x1 = x + self.N
                # check whether the patch width or height exceeds the image width or height
                if (x1 >= self.imgwidth) and (y1 >= self.imgheight):

                    x1 = self.imgwidth-1 #- (self.imgwidth-x)#1
                    y1 = self.imgheight-1# - (self.imgheight-y)#1
#                     print(f'both:{y,x,y1,x1}')
                    self.update_process(y,x,y1,x1)
        
                elif y1 >= self.imgheight: # when patch height exceeds the image height

                    y1 = self.imgheight - 1
#                     print(f'y:{y,x,y1,x1}')
                    self.update_process(y,x,y1,x1)

                elif x1 >= self.imgwidth: # when patch width exceeds the image width

                    x1 = self.imgwidth - 1
#                     print(f'x:{y,x,y1,x1}')
                    self.update_process(y,x,y1,x1)
                else:
                    self.update_process(y,x,y1,x1)
        
        print('process ended')
        if display:
            self.dis_im(self.img)
        if self.save:
            cv2.imwrite(self.out, self.img)
            