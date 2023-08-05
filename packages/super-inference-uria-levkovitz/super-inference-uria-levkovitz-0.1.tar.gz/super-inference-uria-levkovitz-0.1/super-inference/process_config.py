import tkinter as tk
from tkinter import filedialog
import numpy as np
import cv2 as cv
import cv2


def pick_img():
    root = tk.Tk()
    root.withdraw()

    file = filedialog.askopenfilenames(title='Open an inference image', filetypes=[("image files", ".jpeg .jpg .tif")])[0]
    return file


# def pick_model():
#     root = tk.Tk()
#     root.withdraw()
#
#     model = filedialog.askopenfilenames(title='Open a model file', filetypes=[("model files", ".pt .onnx")])[0]
#     return model


def crop_img(path):
    # load the image, clone it, and setup the mouse callback function
    image_window = cv.imread(path)
    original_size_img = image_window.copy()

    size_original = (image_window.shape[1], image_window.shape[0])
    size_sub = (int(image_window.shape[1] / 4), int(image_window.shape[0] / 4))
    image_window = cv.resize(image_window, size_sub)
    clone = image_window.copy()
    clean = image_window.copy()
    global draw
    draw = False
    list_cor = []
    clone = image_window.copy()
    clean = image_window.copy()

    def poly_shape(event, x, y, flagval, par):
        global draw

        if event == cv.EVENT_LBUTTONDOWN:
            draw = True

        elif event == cv.EVENT_MOUSEMOVE:
            if draw == True:
                cv.circle(image_window, (x, y), 1, (255, 0, 0,), 1)
                list_cor.append((x, y))

        elif event == cv.EVENT_LBUTTONUP:
            draw = False
            cv.circle(image_window, (x, y), 1, (255, 0, 0,), 1)
            list_cor.append((x, y))

    cv.namedWindow('image_window')

    cv.setMouseCallback('image_window', poly_shape)  # rectangle_shape)
    while True:
        cv.imshow('image_window', image_window)
        key = cv2.waitKey(1) & 0xFF
        # if the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
            list_cor = []
            image_window = clone.copy()
        elif key == ord("c"):
            cv.polylines(clean, np.array([list_cor]), True, (255, 255, 255), 1)
            cv.fillPoly(clean, pts=np.array([list_cor]), color=(255, 255, 255))
            list_cor = []
            image_window = clean.copy()

        elif key == ord("b"):
            break
    clean = cv.resize(clean, size_original)
    original_size_img[clean == 255] = 255
    cv.destroyAllWindows()
    out = path.split('.')[0] + '_cropped.' + path.split('.')[1]
    cv2.imwrite(out, original_size_img)
    return out


def allow_user_input():
    decide = input('Would you like to choose parameters? [YES/NO]')
    if decide.lower() == 'yes':
        M_N = int(input('Choose grid size in number'))
        save = bool(int(input('Would you like to save the result in image? [1 for yes, 0 for no]')))
        display_tile = bool(int(input('Would you like to display tiles? [1 for yes, 0 for no]')))
        flip_rgb = bool(int(input('Would you like to replace red with blue band? [1 for yes, 0 for no]')))
        stride = M_N / 4
        return M_N, save, display_tile, flip_rgb, stride
    else:
        M_N = 256
        save = False
        display_tile = False
        flip_rgb = False
        stride = M_N / 4
        return M_N, save, display_tile, flip_rgb, stride


path = pick_img()
img_in = crop_img(path)
# model_path = pick_model()
out = img_in.split('.')[0] + '_inference.' + img_in.split('.')[1]
conf_out = out.split('.')[0] + '_conf_thresh.' + out.split('.')[1]
M_N, save, display_tile, flip_rgb, stride = allow_user_input()
