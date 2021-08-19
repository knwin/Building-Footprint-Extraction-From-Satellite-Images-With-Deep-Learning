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


def crop(src_img, model_input_w, model_input_h, numpy_output = False):
    """
    Crops an image into tiles of provided width and height
    
    arguments:
        src_img(PIL image): image to be cropped into tiles
        model_input_w(int): input image width for model   
        model_input_h(int): input image height for model
        numpy_output(bool): output a list of numpy arrays or PIL images(default)
        
    returns:
        list: a list of cropped tiles in numpy array or PIL image format
    """
    
    img_width, img_height = src_img.size
    
    images = []
    for i in range(img_height//model_input_h):
        hori = []
        for j in range(img_width//model_input_w):
            box = (j*model_input_w, i*model_input_h, (j+1)*model_input_w, (i+1)*model_input_h)
            images.append(src_img.crop(box))
    
    if numpy_output:
        images = np.array([np.array(img) for img in images])

    return images


def resize_image(image, percent = 0.7, interpolation = None):
    """
    Resizes an image
    - best interpolation methods for image resizing
        Enlarge: INTER_LINEAR or INTER_CUBIC
        Shrink: INTER_AREA
    
    arguments:
        image (numpy array): original image to be resized 
        percent (float): percentage of the original image size(e.g. 0.5 means 50% of the original size)
        interpolation (cv2 interpolation): interpolation method for resizing

    returns:
        numpy array: new resized image
    """
    
    ori_height = image.shape[0]
    ori_width = image.shape[1]
    
    # calculate target image height and width
    new_height = int(ori_height * percent)
    new_width = int(ori_width * percent)
    
    print(f'original height= {ori_height}, original width = {ori_width}')
    print(f'new height = {new_height}, new width = {new_width}') 
    
    # resize image
    if interpolation:
        new_img = cv2.resize(image, (new_width , new_height), interpolation = interpolation)[:,:,:]
    else:
        new_img = cv2.resize(image, (new_width , new_height))[:,:,:]
 
    return new_img


def reconstruct(tiles_list, img_width, img_height, model_input_w, model_input_h, numpy_output = False):
    """
    Reconstruct one single image from a list of tiles
    
    arguments:
        tiles_list (list): a list of tiles(numpy array or PIL Image)
        img_width (int):  width of image before padding/cropping
        img_height (int): height of image before padding/cropping
        model_input_w (int): input tile width for model 
        model_input_h (int): input tile height for model
    
    returns:
        PIL image or numpy array: reconstructed image
    """
    
    # if input is in numpy array format, convert to PIL first
    if type(tiles_list[0]) == np.ndarray:
        
        # check if image is black & white
        if tiles_list[0].ndim == 2:
            tiles_list = [Image.fromarray(i, 'L') for i in tiles_list]

        # if RGB image
        else:
            tiles_list = [Image.fromarray(i.astype('uint8'), 'RGB') for i in tiles_list]

    first_image = tiles_list[0]
    
    num_row = int(np.ceil(img_height / model_input_h))
    num_col = int(np.ceil(img_width / model_input_w))
    
    # create a blank sheet
    contact_sheet=PIL.Image.new(first_image.mode, (first_image.width * num_col,first_image.height * num_row))
    x, y = 0, 0

    # paste tiles in blank sheet
    for img in tiles_list:
        
        # paste a single tile in sheet
        contact_sheet.paste(img, (x, y) )

        # calculate next position
        if x+first_image.width == contact_sheet.width:
            x=0
            y=y+first_image.height
        else:
            x=x+first_image.width

    # remove extra padded area
    crop_box = (0, 0, img_width, img_height)
    new_img = contact_sheet.crop(crop_box)
    
    if numpy_output:
        new_img = np.array(new_img)
        
    return new_img