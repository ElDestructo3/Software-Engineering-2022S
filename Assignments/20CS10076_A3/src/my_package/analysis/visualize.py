#Imports

from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import numpy as np


def plot_visualization(image, pred_boxes, pred_masks, pred_class, pred_scores, outputs,im_index,analysis_part): # Write the required arguments
  
    # The function should plot the predicted segmentation maps and the bounding boxes on the images and save them.
    # Tip: keep the dimensions of the output image less than 800 to avoid RAM crashes.
    image_copy=image.copy()                                                                          # creating copies for manipulation
    

    # PIL requries numpy array to be converted to image in format (height, width, channel) while the black box outputs it in format (channel, height, width), hence transpose is necessary
    # PIL also requries array values to be in range (0,255), while black box requires it in (0,1), hence multiplication is necessary
    # Finally, PIL also requires values in uint8 format, while black box outputs it in float32 format, hence type conversion is necessary
    # The following two lines convert the image to the required format

    image_copy_2 = Image.fromarray((image_copy.transpose(1,2,0) * 255).astype(np.uint8))             
    image_copy= Image.fromarray((image_copy.transpose(1,2,0) * 255).astype(np.uint8))
    width, height = image_copy.size
    if (width>800 or height>800):                                         # checking the image size and resizing it if a dimension is greater than 800
        image_copy.thumbnail((800,800))
        image_copy_2.thumbnail((800,800))
    f, axarr = plt.subplots(1,3)                                                                    # creating a subplot for the image and the segmentation map
    axarr[0].imshow(image_copy)                                                                   # plotting the image
    axarr[0].set_title('Original Image')
    # since we need to iterate over only 3 most confident predictions, we need to sort the predictions in descending order of confidence and also check for length of the predictions                                                                                             
    if len(pred_boxes)<=3:
    
        for i in range(len(pred_boxes)):                                                               
      
            segment_copy = pred_masks[i]

            # As before, the masks also need to be converted to PIL format.
            # In addition, it is also necessary to compress dimension of length 1 ( that is, ( height, width,1) to (height, width) ), hence the squeeze function is used.

            segment_copy = Image.fromarray(np.squeeze((segment_copy.transpose(1,2,0) * 255).astype(np.uint8),axis=2))
            draw = ImageDraw.Draw(image_copy)                                                                           # creating a draw object to draw the bounding boxes 
            draw.rectangle((pred_boxes[i]), outline='red')                                                              # drawing the bounding boxes
      
            image_copy_2.paste(segment_copy, (0,0), segment_copy)                                                       # overlaying the segmentation map on the image
            
      

    else:
      
        idx = (-np.array(pred_scores)).argsort()[:3]                                                                  # getting indices of 3 most confident predictions
      
        for i in range(3):                                                                                            # looping through the indices and applying similar method to previous conditional
            index= idx[i]
            segment_copy = pred_masks[index]
            segment_copy = Image.fromarray(np.squeeze((segment_copy.transpose(1,2,0) * 255).astype(np.uint8),axis=2))
            draw = ImageDraw.Draw(image_copy)
            draw.rectangle((pred_boxes[index]), outline='red')
            image_copy_2.paste(segment_copy, (0,0), segment_copy) 
    
    
    axarr[1].imshow(image_copy)                                                                                     # plotting the bounding boxes 
    axarr[1].set_title('Bounding Boxes')
    axarr[2].imshow(image_copy_2)                                                                                   # plotting the segmentation map
    axarr[2].set_title('Segmentation Map')
    if im_index==6:
        plt.savefig(outputs+'/analysis/' + str(im_index)+'_'+analysis_part+'.png')
                                                                               
    image_copy.save(outputs+'/bbox/'+str(im_index)+'.jpg')                                                         # saving the image with bounding boxes, uncomment to save
    image_copy_2.save(outputs+'/segmask/'+ str(im_index)+'.jpg')                                                   # saving the image with segmentation maps, uncomment to save    
    


      
  
  
  

