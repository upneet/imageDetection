#!/usr/bin/env python
# coding: utf-8

# In[12]:


#library installations
from flask import Flask,redirect,url_for,render_template,request
import cv2
from datetime import datetime,timedelta

import time
import os


#print(current_time)
import numpy as np
import matplotlib.pyplot as plt
import imutils
import pytesseract
from IPython.display import Image
import pymongo
from pymongo import MongoClient
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#database connection to mongoDB
myclient = pymongo.MongoClient("mongodb+srv://douglas:douglas@cluster0.1gfc0.mongodb.net")
myDb = myclient.CarParkingDatabase


# In[17]:


app = Flask(__name__)
path    = r"C:\Users\user\OneDrive - Douglas College\Applied_Research_Proj\image\uploads";
app.config["IMAGE_UPLOADS"]= r"C:\Users\user\OneDrive - Douglas College\Applied_Research_Proj\image\uploads"
@app.route('/',methods=["GET","POST"])
def upload_image():
    
    if request.method =="POST":
        print("Inside post")

        if request.files:
            print("inside request files")
            image = request.files["image"]
            image.save(os.path.join(app.config["IMAGE_UPLOADS"],image.filename))
            print("image saved")
            full_path = os.path.join(path,image.filename)
            

            print(full_path)
            
            

            print(image)
            print("iupneet")

            return redirect(request.url)





    return render_template('form.html')


if __name__ == "__main__":
    app.run(port=5000,debug=True)


# In[2]:






# In[6]:


image = r'https://www.chargepoint.com/sites/default/files/inline-images/CP_Blog_Image_2018_License_DISRUPT.jpg'
id=1

def imgageToText(image):

    img = cv2.imread(image,cv2.IMREAD_COLOR)
    img = cv2.resize(img, (600,400) )
    imgTogray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    imgTOgray = cv2.bilateralFilter(imgTogray, 13, 15, 15)

    #img_arr = np.asarray(imgTogray)

    imgCanny = cv2.Canny(imgTOgray, 30, 200) 
    # Find Canny edges 

    contours = cv2.findContours(imgCanny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)#1st argument passes the image
    #CHAIN_APPROX_SIMPLE it will just save the end points for the shape not all the points connecting the path

    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    print("Number of Contours found = " + str(len(contours))) 

    cv2.imshow('Canny Edges After Contouring', imgCanny) 
    plt.imshow(imgCanny)
    #print(contours)
    plt.show()
    for c in contours:

        perimeter = cv2.arcLength(c, True)
        #It is also called arc length. It can be found out using cv2.arcLength() function. 
        #Second argument specify whether shape is a closed contour (if passed True), or just a curve.
        approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        detected = 0
        print ("No contour detected")
    else:
         detected = 1


    if detected == 1:
        print("in detected")
        print(screenCnt)
        cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

    mask = np.zeros(imgTogray.shape,np.uint8)
    plt.imshow(mask)
    plt.show()
    new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
    new_image = cv2.bitwise_and(img,img,mask=mask)
    plt.imshow(new_image)
    plt.show()
    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = imgTOgray[topx:bottomx+1, topy:bottomy+1]
    plt.imshow(Cropped)
    plt.show()
    liscencePlateText = pytesseract.image_to_string(Cropped, config='--psm 11')
    return liscencePlateText

textLiscence = imgageToText(image)
print(textLiscence + "functionOutput")


    
current_time = datetime.now()
hours_user=2
#current_time = time.strftime("%H:%M:%S", t)
out_time = datetime.now() + timedelta(hours=hours_user)
print(out_time)
#out_time=time.strftime("%H:%M:%S", out_time)
print( out_time)
print(current_time)


curr_time_str = str(current_time)
#print(current_time +"currentitme")
#time_in= datetime.now().time() 
#time_out = datetime.now().time() 
#date = datetime.date()

price_calc = 2 + 0.5*hours_user;

print("Detected license plate Number is:",textLiscence)
mycol = myDb.Customers
myList = [{"id":id,
    "Car Registration Number" : textLiscence,
    "Date" : datetime.now(),
    "Entry Time In" : curr_time_str,
    "Entry Time Out" : curr_time_str,
    "Time Billable" : price_calc,
    "Price Per Hour0" : 0.5}]


print(myList)
result = mycol.insert(myList)






