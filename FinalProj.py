from vpython import *
#initialize the global variables
dt = 0.01

scene.camera.pos = vec(0,1.5,-4.5)

# A 14 lb (6.35 kg) Bowling Ball with 10 initial velocity
ball = sphere(pos=vec(0,.6,9.144), vel=vec(0,0,-0.005), mass=6.35, radius=.04, make_trail=True, trail_radius=0.04)

# Lane (meters)
lane = box(pos=vec(0,0,0), width=1.0668, height=18.288, color=color.red) 
lane.rotate(axis=vec(1,0,0), angle=pi/2, origin=lane.pos)

#MAIN LOOP START
t = 0
while True:
    rate(1/dt)
    t = t + dt
    
    # Position Update
    ball.pos = ball.pos + ball.vel * t
    scene.camera.pos = scene.camera.pos + ball.vel * t

    print("hello world: " + str(t))


# MAIN LOOP END

