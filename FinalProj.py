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
pinAr = []
laneX=1.0668
offX=-laneX/2
laneZ=18.288
offZ=-laneZ/2
ballPos = vec(0,0.10,-offZ)
gutter = 0.63
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
            pinAr.append(cylinder(pos = jvec, axis=vec(0, 1, 0), color=color.red, radius=0.12065, length=.381, vel = vec(0,0,0),mass = 1))
            jvec+= jvOff
            #print(jvec)
        ivec+=ivOff

# slider ball start pos
def setsPos(s):
    wt.text = '{:1.2f}'.format(s.value)

scene.append_to_caption('\nBall Position:')
slPos = slider(min=-0.5, max=0.5, value=ballPos.x, length=220, bind=setsPos, right=1)
wt = wtext(text='{:1.2f}'.format(slPos.value))

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
        # scene.append_to_caption(str(oldAngle)+' Degrees')

    except ValueError:  # Handle invalid input
        scene.append_to_caption('\nBAD INPUT: Please enter a valid number.\n')

def sgn(x):
    return x/abs(x) if x!=0 else 0

def collisionSphereCylinder(s,c):
    a = c.axis.hat
    r = s.pos - c.pos
    R = r-(dot(r,a))*a
    g =max(0,abs(dot(r,a)-0.5*c.length))
    f = sgn(dot(r,a))
    k = max(0,dot(r,hat(R))-c.radius)*hat(R)
    d = g*a*f+k
    n=hat(d) #COLLISION dont know where go
    if(s.radius-mag(d)>0):  #CONDITIONAL dont know where go
        rp =s.pos-s.radius*n #POINT OF CONTACT dont know where go
        print(rp)

def collide_spheres(a, b):
    dist = a.pos - b.pos
    if(mag(dist)<= a.radius+b.radius):
        #math goes here for circle collisions
        n=hat(dist)
        relVel = a.vel-b.vel
        r = 1
        ic= dot(relVel,n)
        if(dot(relVel,n)<0):
            #impulse
            print("AHHHH")
            aj = -((1+r)*(ic)/(1/b.mass+1/a.mass))
            a.vel += (aj*n)/a.mass
            print(a.vel)
            b.vel -= (aj*n)/b.mass

#input box for angle


# winput to create the input box on the screen
scene.append_to_caption('\nEnter Degrees (-90 to 90):')
wa = winput(prompt='', bind=ChangeAngleOfBall, type='numeric')
# Getting user input
def ChangeAngularVel(evt):
    AV = evt.text
    try:
        AV = int(AV)
        ball.omega = vec(0, 0, AV)
    except ValueError:  # Handle invalid input
        scene.append_to_caption('\nBAD INPUT: Please enter a valid number.\n')

# winput to create the input box on the screen
scene.append_to_caption('\nAngular Velocity (-): RIGHT, (+): LEFT: ')
ww = winput(prompt='', bind=ChangeAngularVel, type='numeric')

# A 14 lb (6.35 kg) Bowling Ball with initial velocity
ball = sphere(
    pos=vec(slPos.value,ballPos.y,ballPos.z),  # Initial position
    vel=vec(0,0,-6),         # Initial velocity
    mass=6.35,               # Mass
    radius=0.1,            # Radius
    make_trail=False,
    trail_radius=0.02,
    retain=35,
    omega=vec(0, 0, 0)     # Initial angular velocity
)
scene.camera.pos = vec(0, 1.8+ballPos.y, 14-ballPos.z)
# gutters
gutterLeft = box(
    pos=vec(-0.6,0,0),
    size = vec(0.1,0.1,18.288),
    color = color.red
)
gutterRigth = box(
    pos=vec(0.6,0,0),
    size = vec(0.1,0.1,18.288),
    color = color.red
)

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
            #print(f"{(x*j+x/2)+offX} and {(z*i+z/2)+offZ}")
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
        if (l.pos.z<offZ-offZ/3.5):
            l.color = color.yellow
        else:   
            if -37.5*(x-0.4)*(x+0.4)>=y :
                l.color = color.blue
            elif -28.2*(x-0.5534)*(x+0.5534)>=y :
                l.color = color.cyan
            elif abs(x**3)+0.5>=y*abs(x**3) :
                l.color = color.blue
            else :
                l.color = color.cyan
def mewCalculator(l):
    x = l.pos.x #+0.3534
    y = -l.pos.z+10
#-37.5\left(x-\frac{.8}{2}\right)\left(x+\frac{.8}{2}\right)
    if (l.pos.z<offZ-offZ/3.5):
        return 0.3
    else:   
        if -37.5*(x-0.4)*(x+0.4)>=y :
            return 0.01
        elif -28.2*(x-0.5534)*(x+0.5534)>=y :
            return 0.02
        elif abs(x**3)+0.5>=y*abs(x**3) :
            return 0.01
        else :
            return 0.02
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
def guttersBackStop():
    global ball
    global running
    if ball.pos.z<-10.5:
        running = False
    else:
        if ball.pos.x < -gutter:
            ball.omega = vec(0,0,0)
            ball.vel = vec(0,0,-4)
        if ball.pos.x > gutter:
            ball.omega = vec(0,0,0)
            ball.vel = vec(0,0,-4)
# throwing ball button
def Start(b):
    global start
    start = True
    if start: 
        b.text = "Rolling"
        ballAngleArrow.opacity=0
        ball.vel = rotate(vec(0, 0, ball.vel.z),angle = -radians(ballAngle),axis= vec(0,1,0))

button(text="Throw", pos=scene.title_anchor, bind=Start)

#laneGenerator(laneAr,1,1)
laneGenerator(laneAr,70,150)
MakePins()
# Main loop
t = 0

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
        mew = mewCalculator(ball)
        velocityRotationUpdate(ball)
        for p in pinAr:
            collide_spheres(ball,p)
            p.pos=p.pos+p.vel*dt
        for p in pinAr:
            for g in pinAr:
                collide_spheres(p,g)

        # Update position
        ball.pos = ball.pos + ball.vel * dt
        scene.camera.pos = scene.camera.pos + ball.vel * dt

        # Gutter ball
        guttersBackStop()


    # Print velocity for debugging
        #print(f"Velocity: {ball.vel}, Angular velocity: {ball.omega}")
        # Print velocity for debugging
        #print(f"Velocity: {ball.vel}, Angular velocity: {ball.omega}")