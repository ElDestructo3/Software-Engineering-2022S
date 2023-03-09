#Imports
from PIL import Image, ImageFilter                                                                      # Importing image filtering options from PIL

class RescaleImage(object):                                                                             # class for rescaling the image
    '''
        Rescales the image to a given size.
    '''

    def __init__(self, output_size):                                                                    # initializing the output size
        '''
            Arguments:
            output_size (tuple or int): Desired output size. If tuple, output is
            matched to output_size. If int, smaller of image edges is matched
            to output_size keeping aspect ratio the same.
        '''

        # Write your code 
        self.output_size = output_size

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)
            Returns:
            image (numpy array or PIL image)
            Note: You do not need to resize the bounding boxes. ONLY RESIZE THE IMAGE.
        '''

        # Write your code here
        if type(self.output_size) == tuple:                                                          # checking the type of output size
            output_size = self.output_size                                                           # assigning the output size directly if tuple
            image=image.resize(output_size)
            return image
        
        else :
            output_size = self.output_size                             
            width, height = image.size                                             
            if width > height :                                                                      # assigning the smaller of the two dimensions to the output size maintaining aspect ratio
                new_height = output_size 
                new_width = int(output_size * width / height)
            else :
                new_width = output_size
                new_height = int(output_size * height / width)
            image=image.resize((new_width, new_height))
            return image
    

