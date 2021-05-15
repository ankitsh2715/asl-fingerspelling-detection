import cv2
import os
import random

def frameExtractor(path_to_video_files, path_to_frames):
    video_files = os.listdir(path_to_video_files)

    for file in video_files:
        try:
            if os.path.splitext(file)[1] !='.mp4':
                continue
            print('extracting frames for video {}'.format(file));
            video = cv2.VideoCapture(os.path.join(path_to_video_files, file))
            count = 0
            success = 1
            arr_img = []
            # If such a directory doesn't exist, creates one and stores its Images
            if not os.path.isdir(os.path.join(path_to_frames, os.path.splitext(file)[0])):
                os.mkdir(os.path.join(path_to_frames, os.path.splitext(file)[0]))
                new_path = os.path.join(path_to_frames, os.path.splitext(file)[0])
                while success:
                    success, image = video.read()
                    arr_img.append(image)
                    count += 1
                count = 0
                for i in range(len(arr_img)-1):
                    image_path = os.path.join(new_path,"%d.png" % count)
                    cv2.imwrite(image_path, arr_img[i])
                    count += 1
        except:
            continue
