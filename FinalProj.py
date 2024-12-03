import vpython as vp
#initialize the global variables
dt = 0.01
vp.scene.camera.pos = vp.vec(0,1.5,-4.5)

# A 14 lb (6.35 kg) Bowling Ball with 10 initial velocity
ball = vp.sphere(pos=vp.vec(0,.6,9.144), vel=vp.vec(10,0,0), mass=6.35, radius=.04, make_trail=True)
ball.pos = vp.vec(0,.6,9.144)
ball.vel= vp.vec(0,0,-.005)

# Lane (meters)
lane = vp.box(pos=vp.vec(0,0,0), width=1.0668, height=18.288, color=vp.color.red) 
lane.rotate(axis=vp.vec(1,0,0), angle=vp.pi/2, origin=lane.pos)


#MAIN LOOP START
t = 0
while True:
    vp.rate(1/dt)
    t = t + dt
    
    # Position Update
    ball.pos = ball.pos + ball.vel * t
    vp.scene.camera.pos = vp.scene.camera.pos + ball.vel * t

    print("hello world: " + str(t))


# MAIN LOOP END

