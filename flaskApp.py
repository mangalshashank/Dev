from flask import Flask, render_template, redirect, url_for,request,session,jsonify
import geolocation
from flask import Flask, render_template, request, redirect, url_for
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import base64
import json
from time import sleep
from deepface import DeepFace

app = Flask(__name__)

#set session key
app.secret_key = 'JG^&R&&YU@)_)kjasd087qnhn*&^(#h32087YNIHIT82YH)'

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/invalid_location')
def invalid_location():
    return render_template('invalid_location.html')
@app.route('/camera_check')
def camera_check():
    return render_template('camera_check.html')
@app.route('/agent_verification')
def agent_verification():
    return render_template('agent_verification.html')
@app.route('/verify_agent', methods=['POST'])
def verify_agent():
    phone = request.form['phone']
    if agentDetails.get(phone):
        session['phone'] = phone
        return redirect(url_for('process_image'))
    else:
        return redirect(url_for('agent_verification'))
@app.route('/location_verification', methods=['POST'])
def location_verification():
    validLocation = geolocation.verifyLocation()  
    cameraCheck = True
    #will be replaced by another script that returns 
    # true if shop camera is working else false
    if validLocation:
        if cameraCheck:
            return redirect(url_for('agent_verification'))
        else:
            return redirect(url_for('camera_check'))
    else:
        return redirect(url_for('invalid_location'))

@app.route('/agent_details', methods=['GET','POST'])
def agent_details():
    phone = session['phone']
    return render_template('agent_details.html', agentDetails=agentDetails[phone])
   

@app.route('/face_verification', methods=['POST','GET'])
def face_verification():
    phone = session['phone']

    image_file = request.files['image']
    image_bytes = image_file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    result = DeepFace.verify(agentDetails[phone]['facePath'], image,enforce_detection=False)

    if result['verified']:
        return jsonify({'success': True, 'redirect_url': '/agent_details'})  
    else:
        return jsonify({'success': True, 'redirect_url': '/agent_verification'}) 
   

@app.route('/process_image', methods=['POST','GET'])
def process_image():
    return render_template('face_verification.html')

agentDetails = {
    '8982141036' : {
        'name' : 'Shashank Mangal',
        'location' : 'Bhopal',
        'facePath' : 'registered_agent/shashankMangal.jpg'
    }
}

if __name__ == '__main__':
    app.run(debug=True)
