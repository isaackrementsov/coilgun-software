# Isaac Krementsov
# 4/5/2020
# Introduction to Systems Engineering
# Coilgun Software - Controls the user interface for working with coilgun projectile launcher

# Import local classes
import motion
import uds

import threading
import json

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

# Initialize new flask app and WebSockets (for real-time server communication)
app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')


# Initialize the projectile motion modelling code
y0 = 2 # The initial vertical launch position of the coilgun, relative to the distance sensor's line of "sight"
dt = 0.000001 # An approximation for the dt (an infinitesimally small time step) used in figure B - converts rates of change to actual quantities
predictor = motion.MotionPredictor(y0, dt) # Initialize the motion predictor with these parameters

# Initialize the distance sensor
PIN_ECHO = 0 # GPIO pin connected to the sensor's echo sensor
PIN_TRIG = 0 # GPIO pin connected to the sensor's pulse trigger
distance_sensor = uds.DistanceSensor(PIN_ECHO, PIN_TRIG) # Initialize the distance sensor with these pins


# Render base template for user interface
@app.route('/', methods=['GET'])
def index():
    return render_template('coilgun.html')


# Get the predicted maximum travel distance for a given projectile and initial velocity
@app.route('/distance', methods=['GET'])
def get_distance():
    # Get the user-entered form data
    A = float(request.values['projectile_area']) # Cross-sectional projectile area
    m = float(request.values['projectile_mass']) # Mass of the projectile
    rho = float(request.values['fluid_density']) # Density of the fluid the projectile is moving through (probably air)
    Cd = float(request.values['drag_constant']) # Drag constant of the projectile; depends on its aerodynamic qualities
    v0 = float(request.values['initial_velocity']) # Initial launch velocity of the projectile, experimentally determined

    if A and rho and Cd and v0 and m:
        # Determine drag coefficient using equation 6
        D = 1/2*Cd*A*rho

        # Use the motion predictor to find the maximum distance the projectile can travel
        max_distance = predictor.predict_max_distance(v0, D, m)

        # Send this to the frontend to handle
        return json.dumps(max_distance)
    else:
        # If no form data is input, return a maximum distance of 0
        return json.dumps(0)


# Send continuous stream of readings to the user interface via WebSockets
def send_readings():
    # This loop will run until the thread is forcibly stopped
    while True:
        # Get a reading from the UDS
        reading = distance_sensor.get_reading()
        # Emit the data via WebSockets
        socketio.emit('data', {'reading': reading})


# Start streaming sensor data once the client connects to WebSockets
@socketio.on('connect')
def start_sensor():
    # Start loop to send continuous distance readings via WebSockets on a parallel thread, passing the SocketIO "send" function as an argument
    parallel_thread = socketio.start_background_task(send_readings)


if __name__ == '__main__':
    # Start the WebSocket server
    socketio.run(app)
