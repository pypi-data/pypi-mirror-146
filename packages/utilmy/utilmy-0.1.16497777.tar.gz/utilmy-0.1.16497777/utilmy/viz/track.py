import skimage.io
import os
import cv2
import numpy as np
def frames_to_video(pathIn,
            pathOut,
             fps,
             
            ):
    

    frame_array = []
    files = [f for f in os.listdir(pathIn) if os.path.isfile(os.path.join(pathIn, f))]

    #for sorting the file names properly
    files.sort(key = lambda x: int(x[:-4]))

    for i in range(len(files)):
        filename= os.path.join(pathIn,files[i])
        #reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
#         print(filename)
        #inserting the frames into an image array
        frame_array.append(img)

    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()
