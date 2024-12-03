import vpython as vp
#initialize the global variables
dt = 0.01

# A 14 lb (6.35 kg) Bowling Ball with 10 initial velocity
ball = vp.sphere(pos=vp.vec(0,0,0), vel=vp.vec(10,0,0), mass=6.35, radius=1)

# Lane (meters)
lane = vp.box(pos=vp.vec(0,0,0), width=1.0668, height=18.288, color=vp.color.red) 
lane.rotate(axis=vp.vec(1,0,0), angle=vp.pi/2, origin=lane.pos)


#MAIN LOOP START
t = 0
while True:
    vp.rate(1/dt)
    t = t + dt
    print("hello world: " + str(t))


# MAIN LOOP END

