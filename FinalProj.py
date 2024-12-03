from vpython import *
#initialize the global variables
dt = 0.01
mew = 0.5
scene.camera.pos = vec(0,1.5,-4.5)

# A 14 lb (6.35 kg) Bowling Ball with 10 initial velocity
ball = sphere(pos=vec(0,.6,9.144), vel=vec(0,0,-0.005), mass=6.35, radius=.04, make_trail=True, trail_radius=0.04, omega =vec(0,0,0))

# Lane (meters)
lane = box(pos=vec(0,0,0), width=1.0668, height=18.288, color=color.red) 
lane.rotate(axis=vec(1,0,0), angle=pi/2, origin=lane.pos)

def velocityRotationUpdate(b):
    #relative velocity  
    vrel = b.vel + cross(b.omega,b.pos)
    #force calculation
    Force = mew*b.mass*9.81*(-vrel)
    #torque calculation
    Torque = cross(b.pos,Force)
    #change in velocity
    b.vel = b.vel + (Force/b.mass)*dt
    #change in rotationalvelocity
    I = (2/3)*b.mass*b.radius**2
    deltButt = (Torque/I)*dt
    #change in r
    b.pos = b.pos + b.vel*dt
    b.rotate(axis=hat(deltButt),angle=mag(deltButt)*dt)

#MAIN LOOP START
t = 0
while True:
    rate(1/dt)
    t = t + dt
    
    # Position Update
    velocityRotationUpdate(ball)
    scene.camera.pos = scene.camera.pos + ball.vel * dt

    print("hello world: " + str(t))


# MAIN LOOP END



