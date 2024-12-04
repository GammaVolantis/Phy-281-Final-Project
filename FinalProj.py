from vpython import *

running = True
def Run(b):
    global running
    running = not running
    if running: b.text = "Pause"
    else: b.text = "Play"

button(text="Pause", pos=scene.title_anchor, bind=Run)

# Initialize global variables
dt = 0.01
mew = 0.02  # Friction coefficient
gravity = 9.81  # Gravity
scene.camera.pos = vec(0, 2.5, 0)
ballPos = vec(0,0.6,9.144)

# slider ball start pos
def setsPos(s):
    wt.text = '{:1.2f}'.format(s.value)

slPos = slider(min=-0.5, max=0.5, value=ballPos.x, length=220, bind=setsPos, right=1)

wt = wtext(text='{:1.2f}'.format(slPos.value))
# slider angle

# A 14 lb (6.35 kg) Bowling Ball with initial velocity
ball = sphere(
    pos=vec(slPos.value,ballPos.y,ballPos.z),  # Initial position
    vel=vec(0,0,0),    # Initial velocity
    mass=6.35,               # Mass
    radius=0.04,             # Radius
    make_trail=False,
    trail_radius=0.02,
    retain=35,
    omega=vec(0, 0, 0)     # Initial angular velocity
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

# throwing ball button
start = False
def Start(b):
    global start
    start = True
    if start: 
        b.text = "Rolling"
        ball.vel = vec(0, 0, -5.36)
        ball.omega = vec(0,0,100)

button(text="Throw", pos=scene.title_anchor, bind=Start)

# Main loop
t = 0
scene.append_to_caption('Angular Velocity: ')

# Getting user input
def ChangeAngularVel(evt):
    AV = evt.text
    try:
        AV = int(AV)
        scene.append_to_caption('\nAngular Velocity is: ' + str(AV) + '\n')
        ball.omega = vec(0, 0, AV)
    except ValueError:  # Handle invalid input
        scene.append_to_caption('\nBAD INPUT: Please enter a valid number.\n')

# winput to create the input box on the screen
ww = winput(prompt='', bind=ChangeAngularVel, type='numeric')


while True:
    if running:

        # Sets position before the user throws the ball
        while not start:
            ball.make_trail = False
            ball.pos.x = slPos.value

        #brings trail in
        ball.make_trail= True
        rate(1 / dt)
        t += dt

        # Update ball position and velocity
        velocityRotationUpdate(ball)

        # Update position
        ball.pos = ball.pos + ball.vel * dt
        scene.camera.pos = scene.camera.pos + ball.vel * dt

        # Print velocity for debugging
        print(f"Velocity: {ball.vel}, Angular velocity: {ball.omega}")
