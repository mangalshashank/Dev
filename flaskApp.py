from flask import Flask, render_template, redirect, url_for,request,session,jsonify
import geolocation
from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
import face_recognition

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

def face_encoding(image_path):
    image = face_recognition.load_image_file(image_path)
    face_encoding = face_recognition.face_encodings(image)
    if len(face_encoding) == 0:
        return None
    return face_encoding[0]

@app.route('/face_verification', methods=['POST','GET'])
def face_verification():
    phone = session['phone']
    image_file = request.files['image']
    image_bytes = image_file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite('temporary.jpg', image)
    x1 = face_encoding(agentDetails[phone]['facePath'])
    x2 = face_encoding('temporary.jpg')
    result = face_recognition.compare_faces([x1], x2, tolerance=0.6)
    print(result)
    if face_recognition.compare_faces([x1], x2, tolerance=0.6).__contains__(True):
        return jsonify({'success': True, 'redirect_url': '/agent_details'})  
    else:
        return jsonify({'success': True, 'redirect_url': '/agent_verification'}) 
    
@app.route('/process_image', methods=['POST','GET'])
def process_image():
    return render_template('face_verification.html')

@app.route('/user_details', methods=['POST','GET'])
def user_details():
    phone = registeredUsers[session['phone']]
    print(phone)
    #return render_template('index.html')
    return render_template('user_details.html', registeredUsers=phone)

@app.route('/find_user', methods=['POST','GET'])
def find_user():
    image_file = request.files['image']
    image_bytes = image_file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite('temporary.jpg', image)
    x2 = face_encoding('temporary.jpg')
    for user in registeredUsers:
        x1 = face_encoding(registeredUsers[user]['facePath'])
        if face_recognition.compare_faces([x1], x2, tolerance=0.6).__contains__(True):
            session['phone'] = user
            return jsonify({'success': True, 'redirect_url': '/user_details'})
    return jsonify({'success': False, 'redirect_url': '/userVerfication'})

@app.route('/agentApproval', methods=['POST','GET'])
def agentApproval():
    cond = True
    #will be replaced with api that will connect two pages and shop cam will be used
    #recording will be used
    return render_template('successful.html')

@app.route('/userVerfication', methods=['POST','GET'])
def userVerfication():
    return render_template('user_verification.html')

agentDetails = {
    '8982141036' : {
        'name' : 'Shashank Mangal',
        'location' : 'Bhopal',
        'phone' : '8982141036',
        'facePath' : 'registered_agent/shashankMangal.jpg'
    }
}

registeredUsers = {
    '8982141036' : {
        'name' : 'Shashank Mangal',
        'location' : 'Bhopal',
        'email' : 'user@example.com',
        'phone' : '8982141036',
        'gender' : 'male',
        'facePath' : 'registered_users/shashankMangal.jpg',
        'emi' : '10000',
        'instalments_left' : '5'
    }
}

if __name__ == '__main__':
    app.run(debug=True)
