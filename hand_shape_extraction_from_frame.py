import glob
import cv2
import math
import pandas as pd
import os
from os.path import join

def extract_hand_frame(frames_folder,hand_frames_folder):
    print("Extracting handshape from Frames .....")
    pos_key = pd.read_csv(os.path.join(frames_folder,'key_points.csv'))
    rightWrist_x = pos_key.rightWrist_x
    rightWrist_y = pos_key.rightWrist_y
    leftWrist_x = pos_key.leftWrist_x
    leftWrist_y = pos_key.leftWrist_y

    frames =  [file for file in os.listdir(frames_folder) if file.endswith('.png')]
    files = sorted(frames,key=lambda x: int(os.path.splitext(x)[0]))
    i = 0

    if not os.path.isdir(hand_frames_folder):
        os.mkdir(hand_frames_folder)

    for video_frame in files:
        try:
            if i< len(leftWrist_x):
                image_path = os.path.join(frames_folder, video_frame)
                img = cv2.imread(image_path)
                cropped_image = img[round(leftWrist_y[i])-400:round(leftWrist_y[i])+100 , round(leftWrist_x[i])-200:round(leftWrist_x[i])+300]
                flipped_cropped_image = cv2.flip(cropped_image,1)
                image_path = os.path.join(hand_frames_folder, str(i)+".png")
                cv2.imwrite(image_path,flipped_cropped_image)
                i = i + 1
        except:
            i = i + 1
