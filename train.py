import tkinter as tk
from tkinter import Message ,Text
import cv2,os
import shutil
import csv
import numpy as np

import pandas as pd

import time
import tkinter.ttk as ttk
import tkinter.font as font
import inspect
import datetime

import time
import threading
import tkinter
from tkinter import ttk
from tkinter import *
import serial

from PIL import Image, ImageTk
from os import path
import random
from time import sleep
from ftplib import FTP
import json

def CreateFolder(path):
    '''
    Creates new folder at the given path
    '''
    if not os.path.exists(path):
        os.makedirs(path)
    return
def Wait(seconds=None):
    '''
    Stall the execution of the preceding functions for a specified number of seconds.
    '''
    sleep(seconds)
def RemoveFile(path):
    '''
    Entering "C:\\Users\\Downloads\\Automagica.xlsx" will delete the file named "Automagica.xlsx" at the location specified by
    the given path.
    '''
    if os.path.isfile(path):
        os.remove(path)
    return

CurDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

df_ip =  pd.read_excel(open(CurDir +'\\setting.xlsx','rb'), sheet_name = 0, dtype = object, header = 0)
current_time = datetime.datetime.now().strftime("%d%m%y")



try:
    ftp = FTP(str(df_ip['IP_FTP'][0]).strip())
    ftp.login(str(df_ip['USER_FTP'][0]).strip(),str(df_ip['PASSWORD_FTP'][0]).strip())
except:
    DisplayMessageBox('Connection to FTP failed, check file setting.xlsx')
    exit()




def ftp_upload(localfile, remotefile):
    fp = open(localfile, 'rb')
    ftp.storbinary('STOR %s' % os.path.basename(localfile), fp, 1024)
    fp.close()
    print("after upload " + localfile + " to " + remotefile)


def chdir(dir): 
    if directory_exists(dir) is False: # (or negate, whatever you prefer for readability)
        ftp.mkd(dir)
    ftp.cwd(dir)
def chdir_file(dir,fileromote): 
    if checkfile_train(fileromote) is False:
        ftp_upload(dir,fileromote)
def checkfile_train(fileromote):
    filelist = []
    ftp.retrlines('LIST',filelist.append)
    for f in filelist:
        if f.split()[-1] == fileromote:
            return True
    return False
def directory_exists(dir):
    filelist = []
    ftp.retrlines('LIST',filelist.append)

    for f in filelist:
        print(f)
        if f.split()[-1] == dir and f.upper().startswith('D'):
            return True
    return False

ftp.cwd('/')  
chdir('FaceRecognition')




ftp.cwd('/FaceRecognition')
#check folder  DATA exists
chdir('DATA')
#check file trainner.yml DATA exists and upload file
chdir_file(CurDir+'\\tmpl\\trainner.yml','trainner.yml')



#check file employee.csv exists and upload file
ftp.cwd('/FaceRecognition')
chdir('employee')
chdir_file(CurDir+'\\tmpl\\employee.csv','employee.csv')


ftp.cwd('/FaceRecognition')
#check folder TrainingImage exists
chdir('TrainingImage')
chdir(str(current_time))

#remove file trainner local
RemoveFile(CurDir + '\\Data\\trainner.yml')
Wait(1)

ftp.cwd('/FaceRecognition')
#check folder TrainingImage exists


#dowload file trainner FTP to folder local
ftp.cwd('/FaceRecognition/DATA')
ftp.retrbinary("RETR " + 'trainner.yml' ,open('data\\trainner.yml', 'wb').write)



#remove file trainner local
RemoveFile(CurDir + '\\employee\\employee.csv')
Wait(1)

#dowload file employ FTP to folder local
ftp.cwd('/FaceRecognition/employee')
ftp.retrbinary("RETR " + 'employee.csv' ,open('employee\\employee.csv', 'wb').write)

CreateFolder(CurDir +'\\'+str('ImagesUnknown')+'\\'+str(current_time))
# CreateFolder(str(df_ip['IP_img'][0]).strip().lower().replace('nan','') +'\\TrainingImage')
# CreateFolder(str(df_ip['IP_data'][0]).strip().lower().replace('nan','') +'\\Data')
CreateFolder(CurDir+'\\TrainingImage\\'+str(current_time))
Wait(1)
# print(str(path.exists(str(df_ip['IP_data'][0]).strip().lower().replace('nan','') +'\\Data\\trainner.yml')))
dfFile_input = pd.read_csv(CurDir +'\\employee\\employee.csv')



# if str(path.exists(str(df_ip['IP_data'][0]).strip().lower().replace('nan','') +'\\Data\\trainner.yml')) == 'False':
#     CopyFile(CurDir+'\\tmpl\\trainner.yml',str(df_ip['IP_data'][0]).strip().lower().replace('nan','') +'\\Data\\trainner.yml')
    
window = tk.Tk()
#helv36 = tk.Font(family='Helvetica', size=36, weight='bold')
window.title("Hệ Thống chấm công bằng nhận diện khuôn mặt")
window.iconbitmap(r'img\\test_4Cv_icon.ico')
dialog_title = 'QUIT'
dialog_text = 'Are you sure?'

#answer = messagebox.askquestion(dialog_title, dialog_text)
 
window.geometry('1550x850')
window.configure(background='gainsboro')



window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)


photo = PhotoImage(file = r'img\\take.png') 
photoimage = photo.subsample(3, 3)

photo_train1 = PhotoImage(file = r'img\\train.png')
photo_train = photo_train1.subsample(3, 3)
  
photo_track1 = PhotoImage(file = r'img\\faceid.png')
photo_track = photo_track1.subsample(3, 3)


photo_exit1 = PhotoImage(file = r'img\\exit.png')
photo_exit = photo_exit1.subsample(3, 3)
# Resizing image to fit on button 

 # ,bg="lightgoldenrodyellow"

message = tk.Label(window, text="Hệ Thống Chấm Công Bằng Nhận Diện Khuôn Mặt" ,bg="beige"  ,fg="darkslategray"  ,width=50  ,height=3,font=('times', 20)) 

message.place(x=450, y=10)
# button1 = Button(text = "Send", width = 6).place(x = 15, y = 250)
# disconnect = Button(text = "Disconnect").place(x =300, y = 360)

lbl = tk.Label(window, text="ID",width=20  ,height=2  ,fg="darkslategray"  ,font=('times', 15, ' bold ') ) 
lbl.place(x=400, y=150)

while True:
    strID = str(random.randint(1000,9999)) 
    print(strID)
    if str(strID) not in  str(list(dfFile_input['Id'])):
        break
var = StringVar()
var.set(strID)


txt = tk.Entry(window,width=20,bg="white" ,fg="darkslategray",font=('times', 15, ' bold '),state="disabled",textvariable = var)
txt.place(x=700, y=155)

print(txt.get())

lbl2 = tk.Label(window, text="NHẬP TÊN",width=20  ,fg="darkslategray"     ,height=2 ,font=('times', 15, ' bold ')) 
lbl2.place(x=400, y=260)

txt2 = tk.Entry(window,width=25  ,bg="white"  ,fg="darkslategray",font=('times', 15, ' bold ')  )
txt2.place(x=700, y=265)

lbl3 = tk.Label(window, text="THÔNG BÁO : ",width=20  ,fg="red"  ,height=2 ,font=('times', 15, ' bold underline ')) 
lbl3.place(x=400, y=450)

message = tk.Label(window, text="" ,bg="white"  ,fg="darkslategray"  ,width=30  ,height=2, activebackground = "lightgoldenrodyellow" ,font=('times', 15, ' bold ')) 
message.place(x=700, y=450)

lbl3 = tk.Label(window, text="THÔNG TIN DỮ LIỆU : ",width=20  ,fg="darkslategray"  ,height=2 ,font=('times', 15, ' bold  underline')) 
lbl3.place(x=400, y=550)


message2 = tk.Label(window, text="" ,fg="darkslategray"   ,bg="white",activeforeground = "green",width=30  ,height=4  ,font=('times', 15, ' bold ')) 
message2.place(x=700, y=550)
 
def clear():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text= res)

def clear2():
    txt2.delete(0, 'end')    
    res = ""
    message.configure(text= res)    
    
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False


#chụp ảnh để train
def TakeImages(): 
    


    print(txt.get()+'---------------------------')
    Id=(txt.get())
    name=(txt2.get())
    if ' vooooo' == str(Id) + ' vooooo':
        DisplayMessageBox('Vui lòng nhập tên người dùng')
    # CreateFolder(CurDir+"\\DoneTrain\\"+name)
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "tmpl\\haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        font = cv2.FONT_HERSHEY_SIMPLEX 
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                #incrementing sample number 
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                current_time = datetime.datetime.now().strftime("%d%m%y")

                cv2.imwrite(CurDir+"\\TrainingImage\\"+str(current_time)+'\\'+"\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                cv2.putText(img,str(sampleNum),(x,y+h), font, 1,(255,255,255),2) 
                ftp.cwd('/FaceRecognition/TrainingImage/'+str(current_time))
                ftp_upload(CurDir+"\\TrainingImage\\"+str(current_time)+'\\'+"\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg",name +"."+Id +'.'+ str(sampleNum) + ".jpg")
                #display the frame
                cv2.imshow('frame',img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum>100:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Ảnh đã được lưu với ID : " + Id +" Name : "+ name
        row = [Id , name]
        with open('employee\employee.csv','a+',encoding="utf-8") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)
    else:
        if(is_number(Id)):
            res = "Vui lòng nhập tên với ký tự alpha"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Vui lòng nhập ID"
            message.configure(text= res)
#train các ảnh đã chụp
def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()#recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath = "tmpl\\haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    a = 0
    try:
        faces,Id = getImagesAndLabels(CurDir+"\\TrainingImage\\"+str(current_time))
        recognizer.train(faces, np.array(Id))
        recognizer.save(CurDir+"\\Data\\trainner.yml")
        res = "Image Trained"#+",".join(str(f) for f in Id)
        message.configure(text= res)
        ftp.cwd('/FaceRecognition/DATA')
        ftp_upload(CurDir+'\\Data\\trainner.yml','trainner.yml')

        ftp.cwd('/FaceRecognition/employee')
        ftp_upload(CurDir+'\\employee\\employee.csv','employee.csv')
        a = 1
    except:
        pass
    if a == 1:
        while True:
            strID = str(random.randint(1000,9999)) 
            print(strID)
            if str(strID) not in  str(list(dfFile_input['Id'])):
                break
        var.set(strID)
def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    
    #create empth face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)  

    # for imageDone in os.listdir('TrainingImage\\'):
    #     MoveFile(CurDir+"\\TrainingImage\\"+imageDone,CurDir+"\\DoneTrain\\"+str(txt2.get())+"\\")
    return faces,Ids

#nhận diện khuôn mặt trên CAMERA
def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read(CurDir+"\\Data\\trainner.yml")
    harcascadePath = "tmpl\\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);    
    df=pd.read_csv("employee\employee.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['Id','Name','Date','Time']
    attendance = pd.DataFrame(columns = col_names) 
    while True:
        ret, im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray, 1.2,5)    
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w]) 
            if(conf < 50):
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa=df.loc[df['Id'] == Id]['Name'].values

                tt=str(Id)+"-"+aa
                
                attendance.loc[len(attendance)] = [Id,aa,date,timeStamp]
                
            else:
                Id='Unknown'                
                tt=str(Id)  
            if(conf > 75):
                noOfFile=len(os.listdir("ImagesUnknown"+"\\"+str(current_time)))+1
                cv2.imwrite("ImagesUnknown"+"\\"+str(current_time)+"\\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
        attendance=attendance.drop_duplicates(subset=['Id'],keep='first')    
        cv2.imshow('im',im) 
        if (cv2.waitKey(1)==ord('q')):
            break
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    fileName="Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName,index=False)
    cam.release()
    cv2.destroyAllWindows()
    #print(attendance)
    res=attendance
    message2.configure(text= res)



# clearButton1 = tk.Button(window, text=" Clear", command=clear  ,fg="darkslategray",width=200  ,height=40, font=('times', 20, ' bold ')  , image = photoimage, 
#                     compound = LEFT)
# clearButton1.place(x=950, y=200)

# clearButton2 = tk.Button(window, text=" Clear", command=clear2  ,fg="darkslategray",width=200  ,height=40, font=('times', 20, ' bold ')  , image = photoimage, 
#                     compound = LEFT)
# clearButton2.place(x=950, y=300)


# clearButton = tk.Button(window, text="Clear", command=clear  ,fg="darkslategray"   ,width=20  ,height=2 ,activebackground = "darkslategray" ,font=('times', 15, ' bold '))
# clearButton.place(x=950, y=200)
# clearButton2 = tk.Button(window, text="Clear", command=clear2  ,fg="darkslategray"    ,width=20  ,height=2, activebackground = "darkslategray" ,font=('times', 15, ' bold '))
# clearButton2.place(x=950, y=300)    
# takeImg = tk.Button(window, text="TAKE A PHOTO", command=TakeImages  ,fg="darkslategray"   ,width=20  ,height=3, activebackground = "darkslategray" ,font=('times', 15, ' bold '))
# takeImg.place(x=200, y=500)
takeImg = tk.Button(window, text=" Chụp ảnh", command=TakeImages  ,fg="darkslategray",width=250  ,height=40, font=('times', 15, ' bold ')  , image = photoimage, 
                    compound = LEFT)
takeImg.place(x=400, y=350)






trainImg = tk.Button(window, text=" Train ảnh", command=TrainImages  ,fg="darkslategray"   ,width=250  ,height=40, activebackground = "darkslategray" ,font=('times', 15, ' bold '), image = photo_train, 
                    compound = LEFT)
trainImg.place(x=700, y=350)




trainImg1 = tk.Button(window, text=" Nhận diện", command=TrackImages  ,fg="darkslategray"   ,width=250  ,height=40, activebackground = "darkslategray" ,font=('times', 15, ' bold '), image = photo_track, 
                    compound = LEFT)
trainImg1.place(x=1000, y=350)

# trackImg = tk.Button(window, text="IDENTIFIED", command=TrackImages  ,fg="darkslategray"    ,width=20  ,height=3, activebackground = "darkslategray" ,font=('times', 15, ' bold '))
# trackImg.place(x=700, y=550)


# quitWindow = tk.Button(window, text="EXIT", command=window.destroy  ,fg="red"   ,width=250  ,height=40, activebackground = "darkslategray" ,font=('times', 15, ' bold '), image = photo_exit, 
#                     compound = LEFT)
# quitWindow.place(x=700, y=700)

quitWindow = tk.Button(window, text="EXIT", command=window.destroy  ,fg="red"   ,width=20  ,height=1, activebackground = "darkslategray" ,font=('times', 15, ' bold '))
quitWindow.place(x=700, y=700)




copyWrite = tk.Text(window, background=window.cget("background"), borderwidth=0,font=('times', 30, 'italic bold underline'))
copyWrite.tag_configure("superscript", offset=10)
# copyWrite.insert("insert", "JiBanNet","", "", "superscript")
copyWrite.configure(state="disabled",fg="darkslategray"  )
copyWrite.pack(side="left")
copyWrite.place(x=800, y=750)
window.mainloop()