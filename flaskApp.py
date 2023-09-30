from flask import Flask, render_template, redirect, url_for
import geolocation

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/invalid_location')
def invalid_location():
    return render_template('invalid_location.html')

@app.route('/agent_verification')
def agent_verification():
    return render_template('agent_verification.html')

@app.route('/location_verification', methods=['POST'])
def location_verification():
    validLocation = geolocation.verifyLocation()  
    if validLocation:
        return redirect(url_for('agent_verification'))
    else:
        return redirect(url_for('invalid_location'))



if __name__ == '__main__':
    app.run(debug=True)
