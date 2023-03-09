#Imports
from PIL import Image, ImageFilter                                                 # Importing image filtering options from PIL
import random                                                                      # Importing random module for random cropping

class CropImage(object):                                                           # class for cropping the image
    '''
        Performs either random cropping or center cropping.
    '''

    def __init__(self, shape, crop_type='center'):                                 # initializing the shape and crop type
        '''
            Arguments:
            shape: output shape of the crop (h, w)
            crop_type: center crop or random crop. Default: center
        '''

        # Write your code here
        self.shape = shape
        self.crop_type = crop_type

    def __call__(self, image):                                                     # function for calling the class
        '''
            Arguments:
            image (numpy array or PIL image)
            Returns:
            image (numpy array or PIL image)
        '''

        # Write your code here
        if (self.crop_type == 'center'):                                           # checking the crop type
            width, height = image.size                                             # getting the width and height of the image
            new_width = self.shape[1]
            new_height = self.shape[0]
            left = (width - new_width) // 2                                        # calculating new image coordinates
            top = (height - new_height) // 2
            right = (width + new_width) // 2
            bottom = (height + new_height) // 2
            image = image.crop((left, top, right, bottom))                         # cropping the image
            return image
        
        else :
            #random crop
            width, height = image.size                                             # getting the width and height of the image
            new_width = self.shape[1]
            new_height = self.shape[0]
            left = random.randint(0, width - new_width)                            # calculating new image coordinates by calling random module
            top = random.randint(0, height - new_height)
            right = left + new_width
            bottom = top + new_height
            image = image.crop((left, top, right, bottom))                         # cropping the image
            return image

 

     

 