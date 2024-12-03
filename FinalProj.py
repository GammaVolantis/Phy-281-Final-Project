import vpython as vp
#initialize the global variables
dt = 0.01
ball = vp.sphere()


#MAIN LOOP START
t = 0
while True:
    vp.rate(1/dt)
    t = t + dt
    print("hello world: " + str(t))


# MAIN LOOP END

