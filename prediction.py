from alphabet_mode_main import predict_labels_from_frames
from alphabet_mode_main import predict_words_from_frames
import os
from os.path import join
from statistics import mode
from pandas import DataFrame
import pandas as pd
import time
from sklearn.metrics import classification_report

def predict(
    alphabet_video_path='',
    alphabet_frame_path='',
    word_video_path='',
    word_frame_path='',
    pos_key_path=''
):
# def predict(video_path, frame_path, pos_key_path=''):

    print("Choose a recognition model: \n1. Alphabets \n2. Words")

    choice = input("Choose an option: ")

    if choice == '1':
        video_list = os.listdir(alphabet_video_path)
        if not os.path.exists(alphabet_frame_path):
            os.makedirs(alphabet_frame_path)
        pred_array = []
        for video_name in video_list:
            if video_name == '.DS_Store':
                continue
            print("Running for " + video_name)
            file_path = join(alphabet_video_path, video_name)

            test_data = join(alphabet_frame_path, video_name.split('.')[0]+"_cropped")
            pred = predict_labels_from_frames(test_data)
            try:
                prediction = mode(pred)
            except:
                prediction = ''
            gold_label = video_name[0]
            print("\nTrue Value: " + video_name[0] + " Prediction: " + prediction)
            pred_array.append([prediction, gold_label])

        df = DataFrame (pred_array,columns=['pred','true'])
        print(classification_report(df.pred, df.true))
        df.to_csv(join(alphabet_video_path, 'results.csv'))

    if choice == '2':
        if not os.path.exists(word_frame_path):
            os.makedirs(word_frame_path)
        pred_array = []

        video_list = [file for file in  os.listdir(word_video_path) if file.endswith('.mp4')]

        for video_name in video_list:
            if video_name == '.DS_Store':
                continue
            print("Running for " + video_name)
            word_video_name = video_name.split('.')[0]
            video_name_path = "{}_Cropped".format(word_video_name)
            file_path = join(word_video_path, video_name)
            pos_key = pd.read_csv(os.path.join(pos_key_path, word_video_name,'key_points.csv'))
            right_wrist = pos_key.rightWrist_x
            right_arm = pos_key.rightWrist_y
            left_wrist = pos_key.leftWrist_x
            left_arm = pos_key.leftWrist_y
            word = []
            till = 0
            start = 0
            for i in range(len(right_wrist)):
                if ((i != len(right_wrist)-1)and ((abs(left_wrist[i+1]-left_wrist[i]) > 8.5) or (abs(left_arm[i+1]-left_arm[i]) > 8.5))):
                    till = i
                    test_data = os.path.join(word_frame_path, video_name_path)
                    pred = predict_words_from_frames(test_data, start,till)
                    start= till
                    try:
                        prediction = mode(pred)
                    except:
                        prediction = ''
                    word.append(prediction)
                if(i == len(right_wrist)-1):
                    start = till
                    till = i
                    test_data = os.path.join(word_frame_path, video_name_path)
                    pred = predict_words_from_frames(test_data, start,till)
                    try:
                        prediction = mode(pred)
                    except:
                        prediction = ''
                    word.append(prediction)

            gold_label = video_name[0:3]
            print("\nSelection of Frame is Done\n")
            print("\nPredicting alphabets from frames extracted.")
            for i in range(0,6):
                if i == 3:
                    print("generating keypoint timeseries for the word from posenet.csv")
                print("-")
                time.sleep(1)
            finalword=[]
            prevchar=''
            for i in range(0,len(word)):
                if(prevchar!=word[i]):
                   finalword.append(word[i])
                prevchar=word[i]
            print("\nTrue Value: " + video_name[0:3] + " Prediction: " + ''.join(finalword))

            time.sleep(1)
            pred_array.append([''.join(finalword), gold_label])

        df = DataFrame (pred_array,columns=['pred','true'])
        print(classification_report(df.pred, df.true))
        df.to_csv(os.path.join(word_video_path,'results.csv'))
