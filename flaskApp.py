from flask import Flask, render_template, redirect, url_for,request
import geolocation

app = Flask(__name__)

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
    print(agentDetails[phone])
    return redirect(url_for('index'))

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

#this data can be fetched from a database
#we assume that agent is registered with company
#and there is a api to fetch agent details along with his image
agentDetails = {
    '8982141036' : {
        'name' : 'Shashank Mangal',
        'location' : 'Bhopal',
        'facePath' : 'registered_agent/shashankMangal.jpg'
    }
}


if __name__ == '__main__':
    app.run(debug=True)
