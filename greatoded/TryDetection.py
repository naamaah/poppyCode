import cv2 as cv
import mediapipe as mp
import time
import pandas as pd
import datetime
import Settings as s #Global settings variables
from PIL import Image, ImageTk

"""
    This function capture the date on the web camera until key press q
    after the web camera is done, it create a excel file with all the relevant joint. every line represent a diffrent frame.
"""
def pose_live():
    # For webcam input:
    #cap = cv.VideoCapture(0)
    cap = cv2.VideoCapture("NewTry.MP4")  # video input
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # For Video input:
    prevTime = 0
    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.5) as pose:
        nolist = True
        landmarkes_data = pd.DataFrame()
        #landmarkes_data = pd.Series()
        while cap.isOpened():
            success, image = cap.read()
            image_width = cap.get(cv.CAP_PROP_FRAME_WIDTH)  # float `width`
            image_height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)  # float `height`
            #total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # float `total_frame_in_the_video` (should not be applicable for camera)
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # Convert the BGR image to RGB.
            image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = pose.process(image)

            try:
                landmarks = results.pose_landmarks.landmark
                if nolist:
                    lndmark_list = []
                    for lndmark in mp_pose.PoseLandmark:
                        lndmark_list = lndmark_list.append(lndmark.value)
                    print(lndmark_list)
                    nolist = False
            except:
                pass

            if not results.pose_landmarks:
                continue
            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            currTime = time.time()
            fps = 1 / (currTime - prevTime)
            prevTime = currTime
            cv.putText(image, f'FPS: {int(fps)}', (20, 70), cv.FONT_HERSHEY_PLAIN, 3, (0, 196, 255), 2)
            cv.imshow('Final_Project', image)
            landmarkes_data = landmarkes_data.append(
            #landmarkes_data = pd.concat(
                {
                    'L_Shoulder_X': results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width,
                    'L_Shoulder_Y': results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height,
                    'R_Shoulder_X': results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image_width,
                    'R_Shoulder_Y': results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height,
                    'L_Elbow_X': results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x * image_width,
                    'L_Elbow_Y': results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y * image_height,
                    'R_Elbow_X': results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x * image_width,
                    'R_Elbow_Y': results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y * image_height,
                    'L_Wrist_X': results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x * image_width,
                    'L_Wrist_Y': results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y * image_height,
                    'R_Wrist_X': results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x * image_width,
                    'R_Wrist_Y': results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y * image_height,
                    'L_Hip_X': results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x * image_width,
                    'L_Hip_Y': results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y * image_height,
                    'R_Hip_X': results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x * image_width,
                    'R_Hip_Y': results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y * image_height,
                    'L_Knee_X': results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].x * image_width,
                    'L_Knee_Y': results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].y * image_height,
                    'R_Knee_X': results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].x * image_width,
                    'R_Knee_Y': results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].y * image_height,
                    'L_Ankle_X': results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].x * image_width,
                    'L_Ankle_Y': results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].y * image_height,
                    'R_Ankle_X': results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].x * image_width,
                    'R_Ankle_Y': results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].y * image_height,
                    'L_Heal_X': results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HEEL].x * image_width,
                    'L_Heal_Y': results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HEEL].y * image_height,
                    'R_Heal_X': results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HEEL].x * image_width,
                    'R_Heal_Y': results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HEEL].y * image_height,
                    'L_Index_X': results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].x * image_width,
                    'L_Index_Y': results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].y * image_height,
                    'R_Index_X': results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].x * image_width,
                    'R_Index_Y': results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].y * image_height
                }, ignore_index=True)
            s.current_joint_list=landmarkes_data.iloc[-1:]
            print(s.current_joint_list)
            key = cv.waitKey(1)
            if key == ord('q'):
                current_time = datetime.datetime.now()
                worksheet_name = str(current_time.day) + "." + str(current_time.month) + " " + str(current_time.hour) + "." + str(current_time.minute) + "." + str(current_time.second) + ".xlsx"
                landmarkes_data.to_excel(excel_writer=R'C:/Git/poppyCode/greatoded/excel_folder/'+worksheet_name, sheet_name="Try")
                break

    cap.release()


def post_static():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose

    # For static images:
    #pic_path=R'C:\Users\TEMP.NAAMA\Documents\נעמה\מיתר\תכנות\TrainingNaama'
    #image2 = Image.open(pic_path + '\\2.jpeg')
    image2=cv.VideoCapture(R'C:\Users\TEMP.NAAMA\Documents\נעמה\מיתר\תכנות\TrainingNaama\2.jpeg')
    IMAGE_FILES = [image2] # cap = cv2.VideoCapture("NewTry.MP4")  # video input
    BG_COLOR = (192, 192, 192)  # gray
    with mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.5) as pose:
        for idx, file in enumerate(IMAGE_FILES):
            #image = cv.imread(str(file))
            image = cv.VideoCapture(R'C:\Users\TEMP.NAAMA\Documents\נעמה\מיתר\תכנות\TrainingNaama\2.jpeg')
            image_height, image_width, _ = image.shape
            # Convert the BGR image to RGB before processing.
            results = pose.process(cv.cvtColor(image, cv.COLOR_BGR2RGB))

            if not results.pose_landmarks:
                continue
            new_row_landmarkes = pd.DataFrame(
                {
                    'R_Shoulder': ["11",
                                   results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * image_width,
                                   results.pose_landmarks.landmark[
                                       mp_pose.PoseLandmark.RIGHT_SHOULDER].y * image_height,
                                   results.pose_landmarks.landmark[
                                       mp_pose.PoseLandmark.RIGHT_SHOULDER].z * image_width],
                    'R_Elbow': ["13",
                                results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x * image_width,
                                results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y * image_height,
                                results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].z * image_width],
                    'R_Wrist': ["15",
                                results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x * image_width,
                                results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y * image_height,
                                results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].z * image_width],
                    'R_Wrist': ["23",
                                results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x * image_width,
                                results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y * image_height,
                                results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].z * image_width],
                    'L_Shoulder': ["12",
                                   results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * image_width,
                                   results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y * image_height,
                                   results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].z * image_width],

                    'L_Elbow': ["14",
                                results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x * image_width,
                                results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y * image_height,
                                results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].z * image_width],

                    'L_Wrist': ["16",
                                results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x * image_width,
                                results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y * image_height,
                                results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].z * image_width],
                    'R_Wrist': ["24",
                                results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x * image_width,
                                results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y * image_height,
                                results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].z * image_width]
                })  # ignore_index=True) if we use append
            landmarkes_data = pd.concat([landmarkes_data, new_row_landmarkes])
            worksheet_name = idx + ".xlsx"
            landmarkes_data.to_excel(excel_writer=R'C:\Users\TEMP.NAAMA\Documents\נעמה\מיתר\תכנות\TrainingNaama' + worksheet_name,
                                     sheet_name="Try")

            annotated_image = image.copy()
            # Draw segmentation on the image.
            # To improve segmentation around boundaries, consider applying a joint
            # bilateral filter to "results.segmentation_mask" with "image".
            condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
            bg_image = np.zeros(image.shape, dtype=np.uint8)
            bg_image[:] = BG_COLOR
            annotated_image = np.where(condition, annotated_image, bg_image)
            # Draw pose landmarks on the image.
            mp_drawing.draw_landmarks(
                annotated_image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            cv.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
            # Plot pose world landmarks.
            mp_drawing.plot_landmarks(
                results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)


if __name__ == '__main__':
    post_static()