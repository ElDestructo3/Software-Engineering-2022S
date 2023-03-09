#Imports
from __future__ import annotations
from src.my_package import InstanceSegmentationModel
from src.my_package.data import Dataset
from src.my_package.analysis import plot_visualization
from src.my_package.data.transforms import FlipImage, BlurImage, RescaleImage, RotateImage, CropImage
import numpy as np
from PIL import Image

def experiment(annotation_file, segmentor, transforms, outputs,analysis_part):
    '''
        Function to perform the desired experiments
        Arguments:
        annotation_file: Path to annotation file
        segmentor: The image segmentor
        transforms: List of transformation classes
        outputs: path of the output folder to store the images
    '''

    #Create the instance of the dataset.
    dataset = Dataset(annotation_file, transforms)

    #Iterate over all data items.
    for i in range(len(dataset)):
        #Obtaining the data item.
        data = dataset[i]
        image = data['image']

        #Get the predictions from the segmentor.
        pred_boxes, pred_masks, pred_class, pred_scores = segmentor(image)
    
        #Draw the segmentation maps on the image and save them.1
        plot_visualization(image, pred_boxes, pred_masks, pred_class, pred_scores, outputs,i,analysis_part)
   
def main():
    segmentor = InstanceSegmentationModel()                                                                                                   # Create the segmentor.
    output_path= 'C:/Users/vishal/Downloads/cp/Assignment_3_Python/outputs'                                                                   # Path to the output folder.
    annotations_path= "C:/Users/vishal/Downloads/cp/Assignment_3_Python/data/annotations.jsonl"
  
    # The following function calls can be used for obtaining trasnformed images with bounding boxes, segmentation masks.
    # Also, since my roll number is 20CS10076, I have used the transformations on image 6 and have saved them
    # The 'outputs' folder consists of the following:-
        # analysis folder: contains the subplots of side-by-side images of 6.jpg along with the necessary transformations
        # bbox folder: contains bounding boxes for all original images provided in the dataset
        # segmask folder: contains segmentation masks for all original images provided in the dataset  

    experiment(annotations_path, segmentor,None,output_path,'a') # Sample arguments to call experiment()
    #experiment(annotations_path, segmentor,[FlipImage()],  output_path,'b')
    #experiment(annotations_path, segmentor,[BlurImage(2)],  output_path,'c')
    #experiment(annotations_path, segmentor,[RescaleImage((1000,750))],  output_path,'d')
    #experiment(annotations_path, segmentor,[RescaleImage((250,187))],  output_path,'e')
    #experiment(annotations_path, segmentor,[RotateImage(270)],  output_path,'f')
    #experiment(annotations_path, segmentor,[RotateImage(45)],  output_path,'g')

if __name__ == '__main__':
    main()