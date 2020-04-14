# Isaac Krementsov
# 4/5/2020
# Introduction to Systems Engineering
# Coilgun Software - Controls the user interface for working with coilgun projectile launcher

# Import local classes
import motion
import uds
import coil_circuit
import ir_pair

import mysql.connector
import threading
import json
import RPi.GPIO as GPIO

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

# Initialize new flask app and WebSockets (for real-time server communication)
app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')


# Connect to MySQL database
# Get JSON credentials to connect
credentials = json.load(open('credentials.json', 'r'))

# Use credentials to connect to database
database = mysql.connector.connect(
    host=credentials['host'],
    user=credentials['user'],
    passwd=credentials['password'],
    database=credentials['database']
)

# Initialize the projectile motion modelling code
y0 = 2 # The initial vertical launch position of the coilgun, relative to the distance sensor's line of "sight"
dt = 0.000001 # An approximation for the dt (an infinitesimally small time step) used in figure B - converts rates of change to actual quantities
predictor = motion.MotionPredictor(y0, dt) # Initialize the motion predictor with these parameters

# Initialize the distance sensor
PIN_ECHO = 0 # GPIO pin connected to the sensor's echo sensor
PIN_TRIG = 0 # GPIO pin connected to the sensor's pulse trigger
distance_sensor = uds.DistanceSensor(PIN_ECHO, PIN_TRIG) # Initialize the distance sensor with these pins

# Initialize the coil circuit
PIN_COIL_1 = 0
PIN_COIL_2 = 0
PULSE_TIME_1 = 0.1
PULSE_TIME_2 = 0.01
coils = coil_circuit.Coils(PIN_COIL_1, PIN_COIL_2, PULSE_TIME_1, PULSE_TIME_2)

# Set up the IR emitter/reciever pairs
PIN_EMITTER_1 = 0
PIN_RECIEVER_1 = 0
ir_pair_1 = ir_pair.IRPair(PIN_EMITTER_1, PIN_RECIEVER_1)

PIN_EMITTER_2 = 0
PIN_RECIEVER_2 = 0
ir_pair_2 = ir_pair.IRPair(PIN_EMITTER_2, PIN_RECIEVER_2)

# Set up GPIO header board to connect circuits
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Set up GPIO input ports
GPIO.setup(PIN_ECHO, GPIO.IN)
GPIO.setup(PIN_RECIEVER_1, GPIO.IN)
GPIO.setup(PIN_RECIEVER_2, GPIO.IN)

# Set up GPIO output ports
GPIO.setup(PIN_TRIG, GPIO.OUT)
GPIO.setup(PIN_COIL_1, GPIO.OUT)
GPIO.setup(PIN_COIL_2, GPIO.OUT)
GPIO.setup(PIN_EMITTER_1, GPIO.OUT)
GPIO.setup(PIN_EMITTER_2, GPIO.OUT)

# Make sure UDS trigger is set to low by default
GPIO.output(PIN_TRIG, GPIO.LOW)

# Render base template for user interface
@app.route('/', methods=['GET'])
def index():
    # Select all records from the coilgun data database
    select_statement = 'SELECT * FROM coilgun_data'

    # Create a DB cursor to execute statements
    cursor = database.cursor()

    # Get saved projectile data profiles
    cursor.execute(select_statement)
    data_profiles = cursor.fetchall()
    print(data_profiles)
    # Close this database session
    cursor.close()

    # Send the data to the client with the user interface
    return render_template('coilgun.html', data_profiles=data_profiles)


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


# Save a user-entered data profile for future use
@app.route('/save-data', methods=['POST'])
def save_projectile_data():
    # Get the user-entered form data to save
    A = float(request.values['projectile_area'])
    m = float(request.values['projectile_mass'])
    rho = float(request.values['fluid_density'])
    Cd = float(request.values['drag_constant'])
    v0 = float(request.values['initial_velocity'])
    name = request.values['name']

    if A and m and rho and Cd and v0 and name:
        # Try to insert new data or update an existing data profile if it already exists
        insert_statement = 'INSERT INTO `coilgun_data` (`area`, `mass`, `density`, `constant`, `velocity`, `name`) VALUES (%s, %s, %s, %s, %s, %s)'
        insert_statement += 'ON DUPLICATE KEY UPDATE `area`=VALUES(area), `mass`=VALUES(mass), `density`=VALUES(density), `constant`=VALUES(constant), `velocity`=VALUES(velocity);'

        # Create a DB cursor to execute statements
        cursor = database.cursor()

        # Group the data to insert and inject it into the query
        insert_data = (A, m, rho, Cd, v0, name)
        cursor.execute(insert_statement, insert_data)

        # Get the newly created record's id
        id = cursor.lastrowid

        # Wrap up the insert by committing and closing DB
        database.commit()
        cursor.close()

        # Send new id to client
        return json.dumps({'id': id})

    return json.dumps({'id': None})


# Trigger the coilgun from the user interface
@app.route('/trigger', methods=['POST'])
def trigger_coils():
    # Turn on the IR LEDs
    ir_pair_1.on()
    ir_pair_2.on()

    # Wait for the first coil to be pulsed
    pulsed = False
    while not pulsed:

        # Once the IR pair has been obstructed by the projectile, trigger the coil
        if ir_pair_1.reciever_covered():
            # Pulse current through the coil briefly
            coils.pulse_coil(0)
            pulsed = True

    # Wait for the second coil to be pulsed
    pulsed = False
    while not pulsed:

        if ir_pair_2.reciever_covered():
            # Pulse current through the second coil briefly
            coils.pulse_coil(1)
            pulsed = True

    # Send "ok" message to frontend
    return json.dumps({'ok': True})


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
