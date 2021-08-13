import numpy as np
import tensorflow as tf
import cv2 as cv2
import PIL
from PIL import Image, ImageOps


def pad(src_img, model_input_w, model_input_h):
    """
    Add extra black area to image to make it ready for cropping
    
    arguments:
        src_img (PIL (or) np array): image to be padded
        model_input_w (int): input image width for model   
        model_input_h (int): input image height for model
    
    returns:
        PIL image: padded image
    """
    
    img_type = type(src_img)

    # change to numpy array
    if img_type  == np.ndarray : 
        img = src_img.copy()
    else: 
        img = np.array(src_img)
    
    img_width = img.shape[1]
    img_height = img.shape[0]
    
    pad_width = int((np.ceil(img_width / model_input_w) * model_input_w) - img_width)
    pad_height = int((np.ceil(img_height / model_input_h) * model_input_h) - img_height)
    
    print('image width = ', img_width, ', image height = ', img_height)
    print('pad width = ', pad_width, ', pad height = ', pad_height)
    
    result_image = cv2.copyMakeBorder( img, 0, pad_height, 0, pad_width, cv2.BORDER_CONSTANT)
    
    # convert numpy array to PIL image format
    # check if result_image is binary mask
    if len(result_image.shape) == 2:
        result_image = Image.fromarray(result_image, 'L') 
    else:
        result_image = Image.fromarray(result_image.astype('uint8'), 'RGB') 
    
    return result_image


def crop(src_img, model_input_w, model_input_h):
    """
    Crops an image into tiles of provided width and height
    
    arguments:
        src_img(PIL image): image to be cropped into tiles
        model_input_w(int): input image width for model   
        model_input_h(int): input image height for model   
        
    returns:
        list: a list of cropped tiles in PIL image format
    """
    
    img_width, img_height = src_img.size
    
    images = []
    for i in range(img_height//model_input_h):
        hori = []
        for j in range(img_width//model_input_w):
            box = (j*model_input_w, i*model_input_h, (j+1)*model_input_w, (i+1)*model_input_h)
            images.append(src_img.crop(box))
        
    return images