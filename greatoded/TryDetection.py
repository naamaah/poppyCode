import cv2
import mediapipe as mp
import time
import pandas as pd
import datetime


def pose_video_input():
    # For webcam input:
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture("NewTry.MP4")  # video input

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose


    # For Video input:
    prevTime = 0
    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.5) as pose:
        nolist = True
        landmarkes_data = pd.DataFrame()
        while cap.isOpened():
            success, image = cap.read()
            image_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float `width`
            image_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
            #total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # float `total_frame_in_the_video` (should not be applicable for camera)
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # Convert the BGR image to RGB.
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
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
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            currTime = time.time()
            fps = 1 / (currTime - prevTime)
            prevTime = currTime
            cv2.putText(image, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 196, 255), 2)
            cv2.imshow('Final_Project', image)
            landmarkes_data = landmarkes_data.append(
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

            key = cv2.waitKey(1)
            if key == ord('q'):
                current_time = datetime.datetime.now()
                worksheet_name = str(current_time.day) + "." + str(current_time.month) + " " + str(current_time.hour) + "." + str(current_time.minute) + "." + str(current_time.second) + ".xlsx"
                landmarkes_data.to_excel(excel_writer=R'C:/Git/poppyCode/greatoded/excel_folder/'+worksheet_name, sheet_name="Try")
                break

    cap.release()

if __name__ == '__main__':
    pose_video_input()