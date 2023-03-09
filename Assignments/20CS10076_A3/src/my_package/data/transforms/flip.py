#Imports
from PIL import Image, ImageFilter                                                             # Importing image filtering options from PIL

class FlipImage(object):                                                                       # class for flipping the image
    '''
        Flips the image.
    '''

    def __init__(self, flip_type='horizontal'):
        '''
            Arguments:
            flip_type: 'horizontal' or 'vertical' Default: 'horizontal'
        '''

        # Write your code here
        self.flip_type = flip_type                                                             # initializing the flip type
 
        
    def __call__(self, image):                                                                 # function for calling the class
        '''
            Arguments:
            image (numpy array or PIL image)
            Returns:
            image (numpy array or PIL image)
        '''

        # Write your code here
        if self.flip_type== 'horizontal' :                                                     # applying the appropriate flip
            image=image.transpose(Image.FLIP_LEFT_RIGHT)
            return image
        else :
            image= image.transpose(Image.FLIP_TOP_BOTTOM)
            return image


