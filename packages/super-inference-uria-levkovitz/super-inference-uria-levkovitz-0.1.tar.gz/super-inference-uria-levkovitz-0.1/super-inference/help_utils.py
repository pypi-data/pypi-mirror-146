import numpy as np 
import cv2
import cv2 as cv
class Helper_functions():
    

    def dis_im(self,im,title='presented_image'):
#         img = transforms.functional.to_pil_image(images[i])
        cv2.imshow(f"{title}", im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    
    def get_val(self,classes,value):
        for key,val in classes.items():
            if val==value:
                return key
     
    def mean_level_accumulate(self):
    
        sum_vals = 0
        count = 0
        for key,val in self.mean_preds.items():
            sum_vals+=val[4]
            count+=1
        mean_val = sum_vals/count
        for key,val in self.index.items():
            if val ==int(np.floor(mean_val)):
                low_val = int(key.split('_')[0])
                high_val = int(key.split('_')[1])
                break
        leftover = mean_val-np.floor(mean_val)
        interval = high_val - low_val  
        ratio_add =  interval*leftover
        final_level = low_val+ratio_add

        return np.around(final_level)
    
    def logo(self,img_t):  
        x = int(img_t.shape[1]*0.20)
        y = int(0.77*x)
        x_in = int(x*0.1)
        x_in_val = int(x*0.3)
        y_in1 = int(y*0.12)
        y_in2 = int(y_in1*2)
        y_in3 = int(y_in2*2.4)
        
        values_color =  (0,0,255) if self.mean_overall_level>70 else (0,165,255) if self.mean_overall_level>40 else (0,255,0)
        text_area = np.ones((y,x,3), dtype=np.int16)*255
        cv2.putText(img=text_area, text='MEAN VALUES DETECTED', org=(x_in, y_in1), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=x*0.002, color=(0, 0, 0),thickness=1)
        cv2.putText(img=text_area, text='FOR PC:', org=(x_in, y_in2), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=x*0.002, color=(0, 0, 0),thickness=1)
        cv2.putText(img=text_area, text=str(int(self.mean_overall_level)), org=(x_in_val, y_in3), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=x*0.007, 
color=values_color,thickness=2)

        logo = cv2.imread(r'C:\Users\urial\BG\AlphaBravo\packages\full_inference\images\logo.png')
#         logoR = cv2.cvtColor(logo,cv2.COLOR_BGR2RGB)
        logo_new = cv.resize(logo, (int(text_area.shape[1]*0.6),int(text_area.shape[0]*0.26)),interpolation = cv2.INTER_AREA)

        x1 = text_area.shape[1]/2-logo_new.shape[1]/2
        x2 = text_area.shape[1]/2+logo_new.shape[1]/2
        y1 = text_area.shape[0]-logo_new.shape[0]
        y2 = text_area.shape[0]
        x1,x2,y1,y2= [int(i) for i in [x1,x2,y1,y2]]
        text_area[y1:y2,x1:x2]=logo_new


        yt = img_t.shape[0]-text_area.shape[0]
        y1t = img_t.shape[0]
        xt = img_t.shape[1]-text_area.shape[1]
        x1t = img_t.shape[1]
        img_t[yt:y1t,xt:x1t]=text_area
        return img_t

    
    def cut_white_crop(self,original_path,cropped_path,conf_path):
        
        img_original = cv.imread(original_path)
        img_cropped = cv.imread(cropped_path)
        img_inf_conf = cv.imread(conf_path)
        final_result_path = original_path.split('.')[0]+'_final.'+original_path.split('.')[1]
#         img_original[img_cropped!=255]=img_inf_conf[img_cropped!=255] 
        img_original[img_cropped<250]=img_inf_conf[img_cropped<250]
        img_original= self.logo(img_original)
        cv2.imwrite(final_result_path,img_original)