#Imports
from PIL import Image, ImageFilter                                              # Importing image filtering options from PIL

class BlurImage(object):                                                        # class for blurring the image
    '''
        Applies Gaussian Blur on the image.
    '''

    def __init__(self, radius):
        '''
            Arguments:
            radius (int): radius to blur
        ''' 
        self.radius = radius                                                    # initializing radius
        # Write your code here
        

    def __call__(self, image):                                                  # defining the function for calling the class
        '''
            Arguments:
            image (numpy array or PIL Image)
            Returns:
            image (numpy array or PIL Image)
        '''
        image=image.filter(ImageFilter.GaussianBlur(self.radius))               # applying the filter
        return image
        # Write your code here


