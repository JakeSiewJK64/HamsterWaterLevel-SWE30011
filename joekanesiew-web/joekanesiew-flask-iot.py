from flask import Flask, render_template
import serial, time

app = Flask(__name__)

ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)

@app.route('/')
def index():

    status = {
            "valveStatus": 0
    }

    return render_template('HamsterReading.html', **status)

@app.route('/<action>')
def processAction(action):

    status = {
            "valveStatus": 0
    }

    if action == 'turnoffvalve':
        ser.write(b'2')
        status['valveStatus'] = 0
    elif action == 'turnonvalve':
        ser.write(b'1')
        status['valveStatus'] = 1
    else:
        ser.write(b'2')
        status['valveStatus'] = 1
    return render_template('HamsterReading.html', **status)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)