from asyncio.windows_events import NULL
from tkinter import filedialog
from src.my_package.model import InstanceSegmentationModel
from src.my_package.data import Dataset
from src.my_package.analysis import plot_visualization
from src.my_package.data.transforms import FlipImage, RescaleImage, BlurImage, CropImage, RotateImage
from tkinter import *
from PIL import Image, ImageTk
import os
####### ADD THE ADDITIONAL IMPORTS FOR THIS ASSIGNMENT HERE #######

# Define the function you want to call when the filebrowser button is clicked.
def fileClick(clicked, dataset, segmentor):

    ####### CODE REQUIRED (START) #######
    # This function should pop-up a dialog for the user to select an input image file.
    # Once the image is selected by the user, it should automatically get the corresponding outputs from the segmentor.
    # Hint: Call the segmentor from here, then compute the output images from using the `plot_visualization` function and save it as an image.
    # Once the output is computed it should be shown automatically based on choice the dropdown button is at.
    # To have a better clarity, please check out the sample video.
    
    imagename = filedialog.askopenfilename(initialdir="/"+dataset.annotation_file, title="Select file", filetypes=(("jpeg files", "*.jpg"),))
    if not imagename:
        print("No file selected")
        return
    imagename = os.path.basename(imagename)
    image, bbox_image, mask_image = NULL, NULL, NULL
    for i in range(len(dataset)):
        data = dataset[i]
        temp = str(i) + ".jpg"
        if temp == imagename:
            image = data['image']
            pred_boxes, pred_masks, pred_class, pred_scores = segmentor(image)
            image, bbox_image, mask_image = plot_visualization(image, pred_boxes, pred_masks, pred_class, pred_scores, NULL,NULL,NULL)
            image.save("og.jpg")
            bbox_image.save("bbox.jpg")
            mask_image.save("mask.jpg")      
    ####### CODE REQUIRED (END) #######

# `process` function definition starts from here. will process the output when clicked.

def process(root,clicked,dataset, segmentor):

    ####### CODE REQUIRED (START) #######
    # Should show the corresponding segmentation or bounding boxes over the input image wrt the choice provided.
    # Note: this function will just show the output, which should have been already computed in the `fileClick` function above.
    # Note: also you should handle the case if the user clicks on the `Process` button without selecting any image file.
    try:
        Image.open("og.jpg")
    except FileNotFoundError:
        print("No image selected.")
        return
    og_image = ImageTk.PhotoImage(Image.open("og.jpg"))
    panel1 = Label(root, image = og_image)
    panel1.image = og_image
    panel1.grid(row=1, column=0)
    if clicked.get() == "Segmentation":
        seg_image = ImageTk.PhotoImage(Image.open("mask.jpg"))
        panel2 = Label(root, image=seg_image)
        panel2.image = seg_image
        panel2.grid(row=1, column=1)
    else:
        bbox_image = ImageTk.PhotoImage(Image.open("bbox.jpg"))
        panel2 = Label(root, image=bbox_image)
        panel2.image = bbox_image
        panel2.grid(row=1, column=1)

    ####### CODE REQUIRED (END) #######

# `main` function definition starts from here.
if __name__ == '__main__':

    # CODE REQUIRED (START) ####### (2 lines)
    # Instantiate the root window.
    # Provide a title to the root window.
    root = Tk()
    root.title("Segmentation and Bounding Boxes")
    ####### CODE REQUIRED (END) #######

    # Setting up the segmentor model.
    annotation_file = 'C:/Users/Vishal/Downloads/cp/Assignment_3_Python/data/annotations.jsonl'
    transforms = []

    # Instantiate the segmentor model.
    segmentor = InstanceSegmentationModel()
    # Instantiate the dataset.
    dataset = Dataset(annotation_file, transforms=transforms)
    
    
    # Declare the options.
    options = ["Segmentation", "Bounding-box"]
    clicked = StringVar(root)
    clicked.set(options[0])

    e = Entry(root, width=70)
    e.grid(row=0, column=0)

    ####### CODE REQUIRED (START) #######
    # Declare the file browsing button
    og_image, bbox_image, mask_image = NULL, NULL, NULL
    filebutton = Button(root, text="Browse", command= lambda: fileClick(clicked, dataset, segmentor))
    filebutton.grid(row=0, column=1)
    
    ####### CODE REQUIRED (END) #######

    ####### CODE REQUIRED (START) #######
    # Declare the drop-down button
    dropbutton = OptionMenu(root, clicked, *options)
    dropbutton.grid(row=0, column=2)
    ####### CODE REQUIRED (END) #######

    # This is a `Process` button, check out the sample video to know about its functionality
    myButton = Button(root, text="Process", command= lambda: process(root,clicked, dataset, segmentor))
    myButton.grid(row=0, column=3)

    # CODE REQUIRED (START) ####### (1 line)
    # Execute with mainloop()
    root.mainloop()
    ####### CODE REQUIRED (END) #######