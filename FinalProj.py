from vpython import *

# Initialize global variables
dt = 0.01
mew = 0.02  # Friction coefficient
gravity = 9.81  # Gravity
scene.camera.pos = vec(0, 2.5, 0)

# A 14 lb (6.35 kg) Bowling Ball with initial velocity
ball = sphere(
    pos=vec(0, 0.6, 9.144),  # Initial position
    vel=vec(0, 0, -5.36),    # Initial velocity
    mass=6.35,               # Mass
    radius=0.04,             # Radius
    make_trail=True,
    trail_radius=0.02,
    retain=35,
    omega=vec(-.5, 0, 0)       # Initial angular velocity
)

# Lane (meters)
lane = box(pos=vec(0, 0, 0), width=1.0668, height=18.288, color=color.red)
lane.rotate(axis=vec(1, 0, 0), angle=pi/2, origin=lane.pos)
laneAr = []
def laneGenerator(laneArray,size,wid,len):
    tempBox = box(pos=vec(0,0,0, width=(1.0668/wid),length=(18.288/len), color=color.red))
    # for range(0,len):
    #     for range(0,wid):
            #generate an array of box objects in the correct pos and orientation
            #color based on their mew value and set the mew value
        


def velocityRotationUpdate(b):
    # Vector from the center of the ball to the floor
    r = vec(0, -b.radius, 0)

    # Relative velocity
    v_rel = b.vel + cross(b.omega, r)

    # Force
    Force = mew * b.mass * gravity * (-hat(v_rel))

    # Torque
    Torque = cross(r, Force)

    # Update velocity
    b.vel = b.vel + (Force / b.mass) * dt

    # Update angular velocity
    I = (2 / 5) * b.mass * b.radius ** 2  # Moment of inertia for a solid sphere
    b.omega = b.omega + (Torque / I) * dt

    # Update the ball's rotation
    b.rotate(axis=hat(b.omega), angle=mag(b.omega) * dt)

# Main loop
t = 0
while True:
    rate(1 / dt)
    t += dt

    # Update ball position and velocity
    velocityRotationUpdate(ball)

    # Update position
    ball.pos = ball.pos + ball.vel * dt
    scene.camera.pos = scene.camera.pos + ball.vel * dt

    # Print velocity for debugging
    print(f"Velocity: {ball.vel}, Angular velocity: {ball.omega}")
