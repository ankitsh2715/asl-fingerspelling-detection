import cv2
import os
import time
import threading
from convert_to_csv import convert_to_csv
from frames_extractor import frameExtractor
from prediction import predict
from hand_shape_extraction_from_frame import extract_hand_frame
from Naked.toolshed.shell import execute_js, muterun_js


BASE_PATH=os.path.dirname(os.path.abspath(__file__))

# Path to the directory containing Video Files
path_to_video_files = os.path.join(BASE_PATH,'alphabet_videos')

hand_frames_folder =  os.path.join(BASE_PATH,'alphabet_hand_frames')
path_to_word_videos = os.path.join(BASE_PATH, 'word_videos')
path_to_word_frames = os.path.join(BASE_PATH, 'word_frames')
path_to_word_hand_frames = os.path.join(BASE_PATH, 'word_hand_frames')

path_to_frames = os.path.join(BASE_PATH,'alphabet_video_frames')
ALPHABET_ARRAY = [
    'A','B','C','D','E','F','G','H','I','J',
    'K', 'L', 'M', 'N','O','P','Q','R', 'V',
    'W','X','Y','Z'
]


if __name__=='__main__':
    print("Choose following options: \n1. Process Alphabet videos and predict \n2.Process word Videos and Predict \n3. Predict(if you have processed videos already)")
    choice = input("Choose an option: ")
    if choice == '1':
        thread = threading.Thread(target=frameExtractor(path_to_video_files, path_to_frames))
        thread.start()
        thread.join()
        for alphabet in ALPHABET_ARRAY:
            print("creating key points file for alphabet {}".format(alphabet))
            frame_path = os.path.join(path_to_frames, "{}/".format(alphabet))
            success = execute_js('posenet.js', frame_path)
            if success:
                convert_to_csv(frame_path)
                cropped_folder = os.path.join(hand_frames_folder, "{}_cropped".format(alphabet))
                extract_hand_frame(frame_path, cropped_folder)
        predict(
           alphabet_video_path= path_to_video_files,
           alphabet_frame_path= hand_frames_folder
        )

    if choice == '2':
        thread = threading.Thread(target=frameExtractor(path_to_word_videos, path_to_word_frames))
        thread.start()
        thread.join()
        videoFileNames =  [file for file in os.listdir(path_to_word_videos) if file.endswith('.mp4')]

        for fileName in videoFileNames:
            word_name = fileName.split('.')[0]
            print("creating key points file for word {}".format(fileName.split('.')[0]))
            frame_path = os.path.join(path_to_word_frames, "{}/".format(word_name))
            success = execute_js('posenet.js', frame_path)
            if success:
                convert_to_csv(frame_path)
                cropped_folder = os.path.join(path_to_word_hand_frames, "{}_cropped".format(word_name))
                extract_hand_frame(frame_path, cropped_folder)


        predict(
            word_video_path= path_to_word_videos,
            word_frame_path=path_to_word_hand_frames,
            pos_key_path=path_to_word_frames
        )

    if choice == '3':
        predict(
            alphabet_video_path=path_to_video_files,
            alphabet_frame_path=hand_frames_folder,
            word_video_path= path_to_word_videos,
            word_frame_path=path_to_word_hand_frames,
            pos_key_path=path_to_word_frames
        )


