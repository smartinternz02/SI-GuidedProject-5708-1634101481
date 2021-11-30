# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 14:00:55 2021

@author: Tulasi
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 00:48:19 2020

@author: Tulasi
"""


# USAGE

# import the necessary packages
from flask import Flask,render_template,request
# Flask-It is our framework which we are going to use to run/serve our application.
#request-for accessing file which was uploaded by the user on our application.
#import operator
import cv2 # opencv library
from tensorflow.keras.models import load_model#to load our trained model
import numpy as np
#import os
from werkzeug.utils import secure_filename
#from playsound import playsound
#from gtts import gTTS
'''
def playaudio(text):
    speech=gTTS(text)
    print(type(speech))
    speech.save("output1.mp3")
    playsound("output1.mp3")
    return
'''
app = Flask(__name__,template_folder="templates") # initializing a flask app
# Loading the model
model=load_model('missing_person.h5')
print("Loaded model from disk")


#app=Flask(__name__,template_folder="templates") 
#@app.route('/', methods=['GET'])
#def index():
 #   return render_template('home.html')
#@app.route('/home', methods=['GET'])
#def home():
#    return render_template('home.html')q
@app.route('/', methods=['GET'])
def about():
    return render_template('intro.html')
@app.route('/upload', methods=['GET', 'POST'])
def predict():
            
        # Get a reference to webcam #0 (the default one)
        
        print("[INFO] starting video stream...")
        vs = cv2.VideoCapture(0)
        #writer = None
        (W, H) = (None, None)
 
# loop over frames from the video file stream
        while True:
        	# read the next frame from the file
            (grabbed, frame) = vs.read()
         
        	# if the frame was not grabbed, then we have reached the end
        	# of the stream
            if not grabbed:
                break
         
        	# if the frame dimensions are empty, grab them
            if W is None or H is None:
                (H, W) = frame.shape[:2]
        
        	# clone the output frame, then convert it from BGR to RGB
        	# ordering and resize the frame to a fixed 64x64
            output = frame.copy()
            #print("apple")
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (64, 64))
            #frame = frame.astype("float32")
            x=np.expand_dims(frame, axis=0)
            result = int (model.predict(x))
            #result=np.argmax(result,axis=1)
            
            index=['Found Missing', 'Normal']
            result=str(index[result])
            #print(result)
            #result=result.tolist()
            
            cv2.putText(output, "activity: {}".format(result), (10, 120), cv2.FONT_HERSHEY_PLAIN,
                        1, (0,255,255), 1)
            #playaudio("Emergency it is a disaster")
            cv2.imshow("Output", output)
            key = cv2.waitKey(1) & 0xFF
        	 
        		# if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
         
        # release the file pointers
        print("[INFO] cleaning up...")
        vs.release()
        cv2.destroyAllWindows()
        return render_template("home.html")

    
if __name__ == '__main__':
      app.run(host='0.0.0.0', port="8000", debug=False)
 