import cv2 as cv
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import time
import pandas as pd
import datetime
import Settings as s #Global settings variables
import threading



class Detection (threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        print("init detection")

    def run(self):
        # For webcam input:
        cap = cv.VideoCapture(0)
        frameNumber=0
        # cap = cv2.VideoCapture("NewTry.MP4")  # video input
        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose

        # For Video input:
        prevTime = 0
        with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.5) as pose:
            landmarkes_data = pd.DataFrame()
            landmarkes_data_all = pd.DataFrame() #for test
            while cap.isOpened(): # testing only this class
            #while (not s.finish_workout): #for the all components
                success, image = cap.read()
                image_width = cap.get(cv.CAP_PROP_FRAME_WIDTH)  # float `width`
                image_height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)  # float `height`
                # total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # float `total_frame_in_the_video` (should not be applicable for camera)
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                # Convert the BGR image to RGB - change the colors.
                image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                results = pose.process(image)

                if not results.pose_landmarks:
                    continue #back to the beginning of the loop

                # Draw the pose annotation on the image.
                image.flags.writeable = True
                image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
                #for the getSkelatonData function in cameraNew Class
                #s.prev_frame=frameNumber
                frameNumber = frameNumber + 1
                s.current_frame = frameNumber

                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                # currTime = time.time()
                # fps = 1 / (currTime - prevTime)
                # prevTime = currTime
                cv.putText(image, f'FrameNumber: {int(frameNumber)}', (20, 70), cv.FONT_HERSHEY_PLAIN, 3, (0, 196, 255), 2)
                path=R'C:\git\poppyCode\Naama\MediaPipe\images'+"\\"+str(frameNumber)+".jpg"
                cv.imwrite(path,image)
                cv.imshow('Final_Project', image) #show the picture

                joint_humam_dict={'R_Shoulder': "12",'R_Elbow': "14",'R_Wrist': "16",'R_Hip': "24",
                                  'L_Shoulder': "11",'L_Elbow': "13",'L_Wrist': "15",'L_Hip': "23"}
                joint_humam_dict_exist={'frameNumber':frameNumber}
                joint_humam_dict_all = {'frameNumber':frameNumber}
                for key,value in joint_humam_dict.items(): #go over each joints that we need
                    if (results.pose_landmarks.landmark[int(value)].visibility >=0.7):
                        joint_humam_dict_exist[key]=[value,
                                                     results.pose_landmarks.landmark[int(value)].x * image_width,
                                                     results.pose_landmarks.landmark[int(value)].y * -image_height,
                                                     results.pose_landmarks.landmark[int(value)].z * image_width]

                    joint_humam_dict_all[key] = [value,
                                                 results.pose_landmarks.landmark[int(value)].visibility,
                                                 results.pose_landmarks.landmark[int(value)].x * image_width,
                                                 results.pose_landmarks.landmark[int(value)].y * -image_height,
                                                 results.pose_landmarks.landmark[int(value)].z * image_width]

                new_row_landmarkes=pd.DataFrame(joint_humam_dict_exist)
                landmarkes_data=pd.concat([landmarkes_data,new_row_landmarkes])
                del new_row_landmarkes['frameNumber']
                s.current_joint_list = new_row_landmarkes



                #for testing
                new_all_row_landmarkes = pd.DataFrame(joint_humam_dict_all)
                landmarkes_data_all = pd.concat([landmarkes_data_all, new_all_row_landmarkes])
                #print(s.current_frame)
                #print(s.prev_frame)

                key = cv.waitKey(1)
                if key == ord('q'):
                    current_time = datetime.datetime.now()
                    worksheet_name_exist = str(current_time.day) + "." + str(current_time.month) + " " + str(
                        current_time.hour) + "." + str(current_time.minute) + "." +str(current_time.second) + ".xlsx"
                    landmarkes_data.to_excel(excel_writer=R'C:\git\poppyCode\Naama\MediaPipe\Excel/' + worksheet_name_exist,
                                             sheet_name="Try")
                    worksheet_name_all = str(current_time.day) + "." + str(current_time.month) + " " + str(
                        current_time.hour) + "." + str(current_time.minute) + "." + str(current_time.second) +" all"+".xlsx"
                    landmarkes_data_all.to_excel(
                        excel_writer=R'C:\git\poppyCode\Naama\MediaPipe\Excel/' + worksheet_name_all,
                        sheet_name="Try")
                    cap.release()
                    break
            cap.release()
            self.closeCamera(landmarkes_data, landmarkes_data_all)

    def closeCamera(self,landmarkes_data, landmarkes_data_all):
        current_time = datetime.datetime.now()
        worksheet_name_exist = str(current_time.day) + "." + str(current_time.month) + " " + str(
            current_time.hour) + "." + str(current_time.minute) + "." + str(current_time.second) + ".xlsx"
        landmarkes_data.to_excel(excel_writer=R'C:\git\poppyCode\Naama\MediaPipe\Excel/' + worksheet_name_exist,
                                 sheet_name="Try")
        worksheet_name_all = str(current_time.day) + "." + str(current_time.month) + " " + str(
            current_time.hour) + "." + str(current_time.minute) + "." + str(current_time.second) + " all" + ".xlsx"
        landmarkes_data_all.to_excel(
            excel_writer=R'C:\git\poppyCode\Naama\MediaPipe\Excel/' + worksheet_name_all,
            sheet_name="Try")


if __name__ == '__main__':
    r = Detection()
    r.run()

