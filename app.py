# Isaac Krementsov
# 4/5/2020
# Introduction to Systems Engineering
# Coilgun Software - Controls the user interface for working with coilgun projectile launcher

# Import local motion detection class (./motion.py)
import motion

import json
from flask import Flask, render_template, request


# Initialize new flask app
app = Flask(__name__)

# Initialize the projectile motion modelling code
y0 = 2 # The initial vertical launch position of the coilgun, relative to the distance sensor's line of "sight"
dt = 0.000001 # An approximation for the dt (an infinitesimally small time step) used in figure B - converts rates of change to actual quantities
predictor = motion.MotionPredictor(y0, dt) # Initialize the motion predictor with these parameters


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
