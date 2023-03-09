#Imports
from PIL import Image, ImageFilter                                                            # Importing image filtering options from PIL

class RotateImage(object):                                                                    # class for rotating the image
    '''
        Rotates the image about the centre of the image.
    '''

    def __init__(self, degrees):                                                              # initializing the degrees
        '''
            Arguments:
            degrees: rotation degree.
        '''
        
        # Write your code here
        self.degrees = degrees

    def __call__(self, sample):                                                               # defining the function for calling the class
        '''
            Arguments:
            image (numpy array or PIL image)
            Returns:
            image (numpy array or PIL image)
        '''

        # Write your code here
        sample = sample.rotate(self.degrees)                                                  # rotating the image
        return sample

