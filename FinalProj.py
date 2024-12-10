from vpython import *
import random

# Initialize global variables
running = True
start = False
ballAngle=0
oldAngle =0
dt = 0.01
mew = 0.02  # Friction coefficient
gravity = 9.81  # Gravity
laneAr = []
laneX=1.0668
offX=-laneX/2
laneZ=18.288
offZ=-laneZ/2
ballPos = vec(0,0.10,-offZ)
ballAngleArrow = arrow(radius=0.3, pos=vector(ballPos.x,ballPos.y,ballPos.z), color=color.red, emissive=True, axis=vec(0,0,-1), shaftwidth=.02)

# pin1 = cylinder(pos=vec(0, 0, 0), axis=vec(0, 1, 0), color=color.red, radius=0.12065, length=.381)

def Run(b):
    global running
    running = not running
    if running: b.text = "Pause"
    else: b.text = "Play"\

button(text="Pause", pos=scene.title_anchor, bind=Run)

def MakePins():
    xdf = .14
    global laneZ
    global offZ

    ivec = vec(0,0,offZ-offZ/8)
    kvec = vec(0,0,0)
    ivOff = vec(-xdf,0,-2*xdf)
    jvOff = vec(2*xdf,0,0)
    for i in range(4):
        jvec = ivec
        for k in range(i+1):
            pin1 = cylinder(pos = jvec, axis=vec(0, 1, 0), color=color.red, radius=0.12065, length=.381)
            jvec+= jvOff
            print(jvec)
        ivec+=ivOff

# slider ball start pos
def setsPos(s):
    wt.text = '{:1.2f}'.format(s.value)
slPos = slider(min=-0.5, max=0.5, value=ballPos.x, length=220, bind=setsPos, right=1)
wt = wtext(text='{:1.2f}'.format(slPos.value))

def sgn(x):
    return x/abs(x) if x!=0 else 0

def collisionSphereCylinder(s,c):
    a = c.axis.hat
    r = s.pos - c.pos
    R = r-(r*a)*a
    d = max(0,mag(dot(r,a))-0.5*c.length)*a*sgn(dot(r,a))+max(0,r*R-(c.pos-c.axis/2))*hat(R)
    

#input box for angle
def ChangeAngleOfBall(ev):
    global ballAngle
    global oldAngle
    A = ev.text
    try:
        A = int(A)
        if oldAngle!=A:
            ballAngleArrow.rotate(angle= radians(oldAngle), axis=vec(0,1,0), origin=ball.pos)
            oldAngle = A
        elif A == oldAngle:
            A=0
            ballAngle=oldAngle
        ballAngleArrow.rotate(angle=radians(-A), axis=vec(0,1,0), origin=ball.pos)
        scene.append_to_caption(str(oldAngle)+' Degrees')

    except ValueError:  # Handle invalid input
        scene.append_to_caption('\nBAD INPUT: Please enter a valid number.\n')

# winput to create the input box on the screen
wa = winput(prompt='', bind=ChangeAngleOfBall, type='numeric')
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

# A 14 lb (6.35 kg) Bowling Ball with initial velocity
ball = sphere(
    pos=vec(slPos.value,ballPos.y,ballPos.z),  # Initial position
    vel=vec(0,0,-4),         # Initial velocity
    mass=6.35,               # Mass
    radius=0.04,             # Radius
    make_trail=False,
    trail_radius=0.02,
    retain=35,
    omega=vec(0, 0, 0)     # Initial angular velocity
)
scene.camera.pos = vec(0, 1.8+ballPos.y, 14-ballPos.z)
# Lane (meters)
#lane = box(pos=vec(0, 0, 0), width=1.0668, height=18.288, color=color.red)
#lane.rotate(axis=vec(1, 0, 0), angle=pi/2, origin=lane.pos)


def laneGenerator(laneArray,wid,len):
    global laneAr
    global laneX
    global offX
    global laneZ
    global offZ
    x=(1.0668/wid)
    z=(18.288/len)
    tempBox = [x,z, vector(random.random(),random.random(),random.random())]
    for i in range(len):
       for j in range(wid):
            tempBox[2] = vector(random.random(),random.random(),random.random())
            posX = x*j+x/2
            posZ = z*i+z/2
            print(f"{(x*j+x/2)+offX} and {(z*i+z/2)+offZ}")
            laneAr.append(box(
                pos = vector(posX+offX,0,posZ+offZ),
                size = vector(tempBox[0],tempBox[0],tempBox[1]),
                height = tempBox[1],
                color = tempBox[2]
            ))        
    oilingLane(laneAr)
def oilingLane(lane):
    for l in lane:
        x = l.pos.x #+0.3534
        y = -l.pos.z+10
    #-37.5\left(x-\frac{.8}{2}\right)\left(x+\frac{.8}{2}\right)
        if -37.5*(x-0.4)*(x+0.4)>=y :
            l.mew = 0.01
            l.color = color.blue
        elif -28.2*(x-0.5534)*(x+0.5534)>=y :
            l.mew = 0.05
            l.color = color.cyan
        elif abs(x**3)+0.5>=y*abs(x**3) :
             l.mew = 0.02
             l.color = color.blue
        else :
            l.mew = 0.04
            l.color = color.cyan
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
def Start(b):
    global start
    start = True
    if start: 
        b.text = "Rolling"
        ballAngleArrow.opacity=0
        ball.vel = rotate(vec(0, 0, ball.vel.z),angle = -ballAngle,axis= vec(0,1,0))

#-5.36
button(text="Throw", pos=scene.title_anchor, bind=Start)

#laneGenerator(laneAr,1,1)
laneGenerator(laneAr,70,150)
MakePins()
# Main loop
t = 0
scene.append_to_caption('\nDegrees (-90 - 90)')
scene.append_to_caption('\nAngular Velocity: ')

while True:
    if running:

        # Sets position before the user throws the ball
        while not start:
            ball.make_trail = False
            ball.pos.x = slPos.value
            ballAngleArrow.pos = ball.pos


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
        # Print velocity for debugging
        #print(f"Velocity: {ball.vel}, Angular velocity: {ball.omega}")
