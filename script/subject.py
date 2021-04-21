from __init__ import PYTHON_PATH
import os
import pandas as pd
import requests
import json

HOST = "http://172.16.1.212:8080/api/init/register_full"

REGISTER = "./script/register"

SEMESTER = 'semester'
GROUPCODE = 'groupCode'
SUBJECTID = 'subjectID'
NAME = 'name'
STUDENTLIST = 'studentList'



for file in os.listdir(REGISTER):
    semester = int(file.split("_")[0])
    subjectID = file.split("_")[1]
    groupCode = file.split("_")[2]
    name = file.split("_")[3].split(".")[0]

    df = pd.read_csv(os.path.join(REGISTER, file))
    studentList = df["students"].tolist()
    msg = {SEMESTER: semester, SUBJECTID: subjectID, GROUPCODE: groupCode,
           NAME: name, STUDENTLIST: studentList}
    rep = requests.post(HOST, json=msg)
    print(rep.text)
    