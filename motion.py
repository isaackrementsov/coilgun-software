# Motion prediction module - Predict the projectile's motion as shown in figure B

class MotionPredictor:

    # Save initial y position and "dt" approximation parameters
    def __init__(self, initial_y, time_step):
        self.y0 = initial_y
        self.dt = time_step


    # Calculate the acceleration of the projectile for a given velocity, drag coefficient, and mass
    def a(self, D, m, vx, vy):
        g = 9.81 # Earth's acceleration due to gravity, 9.81 m/s^2

        common_coeff = -D/m*(vx**2 + vy**2)**(1/2) # The part of the drag force affecting both x and y acceleration to avoid repetition

        ax = common_coeff*vx # X-acceleration is from the x-component of the drag force (see equation 4)
        ay = common_coeff*vy - g # Y-acceleration is from the y-component of the drag force and gravity (see equation 5)

        return (ax, ay) # Return the two values as a tuple vector - [x acceleration, y acceleration]


    # Predict how far the projectile will travel in the x-direction before it is level with the distance sensor (y=0)
    def predict_max_distance(self, initial_v, drag_coefficient, mass):
        # Define variables for x and y position, starting at x=0 and y=y0, the coilgun's height above the distance sensor
        y = self.y0
        x = 0

        # Define variables for x and y velocity; since the projectile comes out of the coilgun moving horizontally, it only has an x-velocity to start
        vx = initial_v
        vy = 0

        # Get the object's drag coefficient and mass to calculate the affect of acceleration due to drag
        D = drag_coefficient
        m = mass

        # Use the approximation of "dt" as a time step for converting acceleration to velocity to position
        dt = self.dt

        # Continue predicting the object's motion until it lines up with the distance sensor (y=0)
        while y > 0:
            # Find the acceleration vector based on equations 4, 5, and the object's velocity
            (ax, ay) = self.a(D, m, vx, vy)

            # Increment velocities by accelerations times dt - dv/dt=a -> dv=a*dt
            vx += ax * dt
            vy += ay * dt

            # Increment position coordinates by velocities times dt - ds/dt=v ds=v*dt
            x += vx * dt
            y += vy * dt

        # Return the horizontal distance the object will travel before being level with the distance sensor
        return x
