#!/usr/bin/env python
# coding: utf-8
import zipfile
from PIL import Image, ImageDraw
import pytesseract as py
import cv2 as cv
import numpy as np
from kraken import pageseg

# loading the face detection classifier
face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('readonly/haarcascade_eye.xml')

# Prototype steps:

# pull out one image

def loadImages(amount = 'all'): #Returns Image array
    with zipfile.ZipFile("readonly/images.zip", "r") as f:
        rep = f.namelist()
        img = []
        imgNames=[]
        if amount == 'all':
            for i in range(len(rep)):
                img.append(Image.open(f.open(rep[i],'r'),'r'))
                imgNames.append(rep[i])
        elif int(amount) >=0:
            amount = int(amount)
            for i in range(amount):
                img.append(Image.open(f.open(rep[i],'r'),'r'))
                imgNames.append(rep[i])
        else:
            print('Error')
        if len(img)>0:
            return (img,imgNames)
        else:
            print('Nothing to return')

# Display boxes around text

# Convert image to binary and use pageseg to draw boxes

def grabWords(img):
    d=img.copy()
    d=d.convert('1')
    draw= ImageDraw.Draw(d)
    bbox=pageseg.segment(d)['boxes']

# Output boxes to pytesseract
# Scan through coordinates, split sentences and add unique words to a running dictionary

    data=[]
    for box in bbox:
    #     draw.rectangle(box,outline='black')
        datum = py.image_to_string(d.crop(box))
        if " " in datum:
            datum = datum.split(" ")
        if len(datum) > 1 and type(datum) == type([]):
            for word in datum:
                if word not in data:
                    data.append(word)
        elif len(datum)==1 and type(datum) == type('string'):
            if word not in data:
                data.append(word)
 # Output text 
    return data


# Detect Faces

def grabFaces(img): #Returns array of faces
    grayScalePic = cv.cvtColor((np.asarray(img)),cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(grayScalePic)
    eyes = eye_cascade.detectMultiScale(grayScalePic)

    dCV=img.copy()
    drawCV = ImageDraw.Draw(dCV)
    correctFaces=[]
    for head in list(faces):
        matching = False
        for eye in list(eyes):
            hC = {'x':[head[0],head[2]+head[0]],'y':[head[1],head[1]+head[3]]}
            eC = {'x':[eye[0],eye[2]+eye[0]],'y':[eye[1],eye[1]+eye[3]]}
            if eC['x'][1]<=hC['x'][1] and eC['x'][0]>= eC['x'][0] and eC['y'][1] <= hC['y'][1] and eC['y'][0] >= hC['y'][0]:
                matching = True
                break
        if matching:
            correctFaces.append(head)
    if len(correctFaces) >0:
        return correctFaces
    else:
        return None

# Output contact sheet of faces
def outputContact(img,correctFaces):
    baseSheet = Image.new(img.mode,size=(5*200,200*2))
    templateSq = {'width':200,'height':200}
    x=0
    y=0
    for face in correctFaces:
        temp = img.crop((face[0],face[1],face[2]+face[0],face[3]+face[1]))
        temp = temp.resize((200,200))
        baseSheet.paste(temp, (x, y) )
        if x+templateSq['width'] == baseSheet.width:
            x=0
            y=y+templateSq['height']
        else:
            x=x+templateSq['width']
    display(baseSheet)
    
    
    
#Begin Main
correctAmt = False
while not correctAmt:
    amount = input("Type how many photos to scan (a positive integer, or 'all' to scan all of them): " )
    try:
        if str(amount.lower()) == 'all' or int(amount) >0:
            correctAmt = True
    except:
        print("Error, try again")
        
name = input("Type a keyword to decide on which photos to scan: \n")

# Load Images
images,imageNames=loadImages(amount)

#Compare words to keyword and filter images
count=0
filteredImages=[]
filteredNames=[]
for image in images:
    detectedWords=grabWords(image)
    if name in detectedWords:
        filteredImages.append(image)
        filteredNames.append(imageNames[count])
    count +=1

#Grab faces
detectedFaces=[]
for image in filteredImages:
    det = grabFaces(image)
    detectedFaces.append(det)

#Create contact sheets
count = 0
for faceSet in detectedFaces:
    print('\nResults found in in file {}'.format(filteredNames[count]))
    if faceSet == None:
        print('\nNo faces were detected')
        count+=1
        continue
    outputContact(filteredImages[count],faceSet)
    count+=1
    
