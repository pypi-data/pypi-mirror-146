from email import header
import glob
import Authorize
import os
import json
import pandas as pd

def test_Create_Case_With_Subjects():
    #region header data
    directory = os.getcwd()
    directory = directory + "\TestData\Createcase.json"
    file = open(directory,'r')
    json_input = file.read()
    request_json_case = json.loads(json_input)
    print(request_json_case)
    processed_token, oauth = Authorize.Get_AccessToken()  
    headers = {"Authorization":processed_token,"accept":"application/json"}
    #endregion

    #region Create case and capture case id
    CaseID = oauth.post('https://crs-api-qa.kroll.com/v1/cases', verify=False, headers=headers, json=request_json_case)
    print(str(CaseID))
    # print(CaseID.status_code)
    #endregion

    #region Create subjects
    exceldata = {"SubjectId":[],"SubjectName":[]}
    directory = os.getcwd()
    directory = directory + "\TestData\RobertData"
    for files in glob.glob(directory+'\*'):
        print(files)
        file = open(files,'r')
        json_input = file.read()
        request_json_subject = json.loads(json_input)
        request_json_subject["caseId"] = str(CaseID.text).replace("\"","")
        print(request_json_subject)
        if request_json_subject["subjectType"] == 1:
            exceldata["SubjectName"].append(str(request_json_subject["entityName"]).replace("%20"," ").replace("%2C",","))
        else:
            exceldata["SubjectName"].append(str(request_json_subject["individualName"]["fullName"]))
        subject_id = oauth.post("https://crs-api-qa.kroll.com/v1/subjects", verify=False,headers=headers,json=request_json_subject)
        print(subject_id.status_code)
        print(subject_id.text)
        exceldata["SubjectId"].append(str(subject_id.text).replace("\"",""))
    #endregion

    #region Create Excel
    df = pd.DataFrame(exceldata)
    print(df)
    df.to_excel('SubjectsOutput.xlsx')
    #endregion

# def test_EnrichProfile():
#     subjects_data = os.getcwd()
#     subjects_data = subjects_data + "\SubjectsData.xlsx"
#     sub