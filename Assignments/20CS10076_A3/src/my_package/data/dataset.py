#Imports
import json
import os.path
import numpy as np
from PIL import Image
import sys

class Dataset(object):                                                                             # Create the dataset class.
    '''
        A class for the dataset that will return data items as per the given index
    '''

    def __init__(self, annotation_file, transforms = None):                                        # Initialize the dataset.
        '''
            Arguments:
            annotation_file: path to the annotation file
            transforms: list of transforms (class instances)
                        For instance, [<class 'RandomCrop'>, <class 'Rotate'>]
        '''

        self.annotation_file = annotation_file
        self.transforms= transforms
        
        

    def __len__(self):                                                                             # Return the length of the dataset.
        '''
            return the number of data points in the dataset
        '''
        data = [json.loads(line) for line in open(self.annotation_file, 'r')]                      # extracting data from the annotation file
        return len(data)
        

    def __getitem__(self, idx):                                                                    # Return the data item at the given index.
        '''
            return the dataset element for the index: "idx"
            Arguments:
                idx: index of the data element.
            Returns: A dictionary with:
                image: image (in the form of a numpy array) (shape: (3, H, W))
                gt_png_ann: the segmentation annotation image (in the form of a numpy array) (shape: (1, H, W))
                gt_bboxes: N X 5 array where N is the number of bounding boxes, each 
                            consisting of [class, x1, y1, x2, y2]
                            x1 and x2 lie between 0 and width of the image,
                            y1 and y2 lie between 0 and height of the image.
            You need to do the following, 
            1. Extract the correct annotation using the idx provided.
            2. Read the image, png segmentation and convert it into a numpy array (wont be necessary
                with some libraries). The shape of the arrays would be (3, H, W) and (1, H, W), respectively.
            3. Scale the values in the arrays to be with [0, 1].
            4. Perform the desired transformations on the image.
            5. Return the dictionary of the transformed image and annotations as specified.
        '''

        data = [json.loads(line) for line in open(self.annotation_file, 'r')]                                         # extracting data from the annotation file
        image_path = os.path.dirname(self.annotation_file) + '/' +data[idx]['img_fn']                                 # image path
        gt_png_ann_path = os.path.dirname(self.annotation_file) + '/' +data[idx]['png_ann_fn']                        # png segmentation path
        gt_bboxes = data[idx]['bboxes']                                                                               # bounding boxes
        image = Image.open(image_path)                                                                                # reading images
        gt_png_ann = Image.open(gt_png_ann_path)

        if self.transforms:                                                                                           # applying all necessary transformations
            for transform in self.transforms:
                image = transform(image)
                gt_png_ann = transform(gt_png_ann)
        
        image = np.array(image).transpose(2, 0, 1)                                                                    # Transposing PIL image for required shape and converting to numpy array
        gt_png_ann = np.array(gt_png_ann)
        gt_png_ann = gt_png_ann[np.newaxis, :, :]                                                                     # adding a dimension for obtaining required shape

        image= (image - np.min(image))/(np.max(image) - np.min(image))                                                # normalizing images to get values in [0,1]
        gt_png_ann = (gt_png_ann - np.min(gt_png_ann))/(np.max(gt_png_ann) - np.min(gt_png_ann))
        
        gt_bboxes = np.array(gt_bboxes)                                                                               # modifying the bboxes to extract category id and coordinates
        new_gt_bboxes = np.zeros((gt_bboxes.shape[0], 5))
        for i in range(gt_bboxes.shape[0]):
            new_gt_bboxes[i, :] = np.append(gt_bboxes[i]['category_id'],np.array(gt_bboxes[i]['bbox']))

        
        gt_bboxes = new_gt_bboxes
        return {'image': image, 'gt_png_ann': gt_png_ann, 'gt_bboxes': gt_bboxes}                                     # returning the dictionary of the transformed image and mask and annotations

