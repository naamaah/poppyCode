import xlsxwriter
import datetime
import Settings as s
from Joint import joint
import os
import pandas as pd

# from openpyxl import Workbook

"""
    create new excel file named the current time.

"""


def create_workbook():
    # current_time = datetime.datetime.now()
    # worksheet_name = str(s.subjectNum)+"_"+str(current_time.day) + "." + str(current_time.month) + "_" + str(current_time.hour) + "." + \
    #                  str(current_time.minute) + "." + str(current_time.second) + ".xlsx"
    # create a folder for the subjectNumber - in the folder will be all the excel data
    folder_path = s.excel_path + str(s.subjectNum)+"_robot"+s.robotNumber
    print(folder_path)
    if (s.sessionNumber == 1):
        os.mkdir(folder_path)
    worksheet_name = str(s.subjectNum) + "_" + str(s.sessionNumber)+"_" + str(s.TBALevel) + ".xlsx"
    s.excel_workbook = xlsxwriter.Workbook(folder_path + "/" + worksheet_name)
    s.ex_list = []
    s.Q_answer = []


def wf_joints(ex_name, list_joints):
    '''
    Writing joints data for an exercise in Excel file in two versions
    :param ex_name:
    :param list_joints:
    :return:
    '''
    # current_time = datetime.datetime.now()
    # name = ex_name +"_"+ str(current_time.day)+str(current_time.month)+str(current_time.hour)+str(current_time.minute) + str(current_time.second)
    name = str(s.subjectNum) + ex_name
    print(name)
    print(len(name))
    if len(name) > 30:
        name=name[0:31]  # from the start until 31
    s.worksheet = s.excel_workbook.add_worksheet(name)
    frame_number = 1

    # first version
    for l in range(1, len(list_joints)):
        row = 1
        s.worksheet.write(0, frame_number, frame_number)
        for j in list_joints[l]:
            if type(j) == joint:
                j_ar = j.joint_to_array()
                for i in range(len(j_ar)):
                    s.worksheet.write(row, frame_number, str(j_ar[i]))
                    row += 1
            else:
                s.worksheet.write(row, frame_number, j)
                row += 1
        frame_number += 1

    # # second version
    # name2 = ex_name + "v2" + str(current_time.minute) + str(current_time.second)
    # s.worksheet = s.excel_workbook.add_worksheet(name2)
    # row = 0
    # frame_number = 0
    # for l in range(1, len(list_joints)):
    #     for j in list_joints[l]:
    #         if type(j) == joint:
    #             j_ar = j.joint_to_array()
    #             s.worksheet.write(row, 0, frame_number)
    #             for i in range(len(j_ar)):
    #                 s.worksheet.write(row, i + 1, str(j_ar[i]))
    #             row += 1
    #         else:
    #             s.worksheet.write(row-1, i + 2,j)
    #     frame_number += 1


# write to execl file exercises names and the successful repetition number
def wf_exercise():
    name = "exercises_session" + str(s.sessionNumber)
    row = 1
    col = 0
    s.worksheet = s.excel_workbook.add_worksheet(name)
    print("________")
    print(s.ex_list)
    for ex in s.ex_list:
        s.worksheet.write(row, col, ex[0])  # name
        s.worksheet.write(row, col + 1, ex[1])  # the number of repetition of the subject
        s.worksheet.write(row, col + 2, ex[2])  # the number the subject try todo
        row += 1


# write to execl file exercises names and the successful repetition number
def wf_QA():
    name = "Data_session" + str(s.sessionNumber)
    s.worksheet = s.excel_workbook.add_worksheet(name)
    s.worksheet.write(0, 1, "Q1")
    s.worksheet.write(0, 2, "Q2")
    #s.worksheet.write(0, 3, "Q3")
    row = 1
    col = 1
    for i in s.Q_answer:
        s.worksheet.write(row, col, i[0])  # q1 answer
        s.worksheet.write(row, col + 1, i[1])  # q2 answer
        #s.worksheet.write(row, col + 2, i[2])  # q3 answer
        row += 1


def readFromExcelQA():
    print("insideQA")
    worksheet_name = str(s.subjectNum) + "_1" + ".xlsx"
    path = s.excel_path + str(s.subjectNum) + "/" + worksheet_name  # path include the number of the excel file
    data = pd.read_excel(io=path, sheet_name="Data_session1", index_col=None, header=None)
    # print(data)
    s.Q1_answer = data.iloc[1, 1]
    s.Q2_answer = data.iloc[1, 2]
    s.Q3_answer = data.iloc[1, 3]
    s.rep = int(data.iloc[2, 1])
    s.whichExercise_Q2 = data.iloc[2, 2]
    s.whichExercise_Q3 = data.iloc[2, 3]
    print(s.Q1_answer, s.Q2_answer, s.Q3_answer, s.rep, s.whichExercise_Q2, s.whichExercise_Q3)
    print("finishesQA")


def readFromExcelExercise():
    # only one session of exercise was:
    print("inside EX")
    worksheet_name1 = str(s.subjectNum) + "_1" + ".xlsx"
    path1 = s.excel_path + str(s.subjectNum) + "/" + worksheet_name1  # path include the number of the excel file
    data1 = pd.read_excel(io=path1, sheet_name="exercises_session1", index_col=None, header=None)
    s.exercises_session1 = exerciseFromSession(data1)
    print("_________")
    print(s.exercises_session1)
    if (s.sessionNumber == 3):  # s.sessionNumber==3 #session 1 doesnt have perivous exercise
        worksheet_name2 = str(s.subjectNum) + "_2" + ".xlsx"
        path2 = s.excel_path + str(s.subjectNum) + "/" + worksheet_name2  # path include the number of the excel file
        data2 = pd.read_excel(io=path2, sheet_name="exercises_session2", index_col=None, header=None)
        s.exercises_session2 = exerciseFromSession(data2)
        print("_________")
        print(s.exercises_session2)


def exerciseFromSession(data):
    exerciseList=[]
    for i in range(1,data.shape[0]):
        exerciseList.append(data.iloc[i,0])
    #exerciseList = [data.iloc[1, 0], data.iloc[2, 0], data.iloc[3, 0]]
    print(exerciseList)
    return exerciseList


def close_workbook():
    s.excel_workbook.close()


if __name__ == "__main__":
    s.excel_path = R'C:/Git/poppyCode/greatoded/excel_folder/'
    s.subjectNum = 20
    s.sessionNumber = 2
    # s.TBALevel=1
    #readFromExcelQA()
    #readFromExcelExercise()
    #print("done")
    create_workbook()
    # s.ex_list = [
    #     ['raise up', 8, 9],
    #     ['bend', 8, 10],
    #     ['raise up', 3, 6],
    #     ['raise up', 8, 12],
    # ]
    # s.Q_answer = [
    #     ['a', 'b', 'c'],
    #     [8, 'Left', 'Weight'],
    # ]
    join = [[12, 496.793, 98.652, 927.991],
    [6, 457.266, 80.806, 757.736],
    [13, 496.610, 91.162, 930.897]]
    wf_joints("123456789123456789123456789123456789",join)
    # wf_QA()
    # wf_exercise()
    # close_workbook()
