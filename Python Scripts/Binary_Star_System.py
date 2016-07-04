from visual import *
from visual.graph import *

scene.height=800
scene.width=600
scene.range=(400,400,400)
scene.autoscale=False
scene.background=color.white

Mscale=10
Gscale=4.0

#initial star one position
x1i=vector(-40.0,0.0,0.0)
#star one mass E30 (equal to sun)
m1 = 1.989*Mscale
#initial star one velocity
v1i=vector(0.0,30.0,0.0)
#star one radius
radius1 = 2.0

#initial star two position
x2i = -x1i
#star two mass E30, half of that of star one
m2 = 0.5*m1
#initial star two velocity
v2i = (-m1/m2)*v1i
#star two radius
radius2=1.0


#initial planet position
x3i = vector (43.0, 0.0, 0.0)
#planet mass
m3 = m1/333000.0
#initial planet velocity
v3i = vector(0.0,5.3,0.0)
#planet radius
radius3=1.0

z= vector (0,0,-1)

#Newton's Gravitational Constant E-11
G=6.673*(10**Gscale)

#initial magnitude of gravitational force between the stars
Fgstar=G*m1*m2/(mag(x2i-x1i))**2
#initial magnitude of gravitational force by the stars on the Earth
Fg13=G*m1*m3/(mag(x3i-x1i))**2
Fg23=G*m2*m3/(mag(x2i-x3i))**2

#time
time=0.0


#making stars,planet objects
star1 = sphere(pos=x1i, radius=radius1, color=color.red, make_trail=True)
star2 = sphere(pos=x2i, radius=radius2, color=color.blue,make_trail=True)
planet = sphere(pos=x3i, radius=radius3, color=color.green, make_trail=True)

dt=0.0001

#centre of mass, ignoring small mass of planet
CM=sphere(pos=(star1.pos*m1+star2.pos*m2)/(m1+m2), radius=0.5, color=color.black, make_trail=True)

#norm(cross(CM.pos,(0,1,0)))

#star 1 and 2, planet velocity
star1.velocity=v1i
star2.velocity=v2i

orbitalvelocity = (2*G*(m1)/(mag(star1.pos-planet.pos)))**0.5
planet.velocity=mag(v3i)*cross(planet.pos-star1.pos, z)

#star 1 and 2, planet gravity
star1.gravity=Fgstar*(star2.pos-star1.pos)/mag(star2.pos-star1.pos)
star2.gravity=Fgstar*(star1.pos-star2.pos)/mag(star1.pos-star2.pos)
planet.gravity=Fg13*(star1.pos-planet.pos)/mag(star1.pos-planet.pos)+Fg23*(star2.pos-planet.pos)/mag(star2.pos-planet.pos)

#planet acceleration
planet.accelstar1=G*m1/(mag(x3i-x1i))**2*norm(star1.pos-planet.pos)
planet.accelstar2=G*m2/(mag(x3i-x2i))**2*norm(star2.pos-planet.pos)
planet.accel=planet.gravity/m3

#defining velocity arrow
star1.velocityarrow=arrow(pos=star1.pos, axis=star1.velocity, color=color.yellow)
star2.velocityarrow=arrow(pos=star2.pos, axis=star2.velocity, color=color.yellow)
planet.velocityarrow=arrow(pos=planet.pos, axis=planet.velocity, color=color.yellow)

#defining Fg arrow for stars
#star1.gravityarrow=arrow(pos=star1.pos, axis=star1.gravity, color=color.green)
#star2.gravityarrow=arrow(pos=star2.pos, axis=star2.gravity, color=color.green)

#acceleration arrow for planet since Fg is too small in comparison
##planet.accelarrow=arrow(pos=planet.pos, axis=planet.accel, color=color.magenta)
##planet.accelstar1arrow=arrow(pos=planet.pos, axis=planet.accelstar1, color=color.cyan)
##planet.accelstar2arrow=arrow(pos=planet.pos, axis=planet.accelstar2, color=color.orange)

#arrow that points from planet to CM
#planet.CMarrow=arrow(pos=planet.pos,axis=CM.pos-planet.pos, color=color.red)

#Danny's value
DV=2.0*(star1.pos-CM.pos)/(mag(star1.pos-planet.pos))**3+(star2.pos-CM.pos)/(mag(star2.pos-planet.pos))**3

#Graphing stuff
#Position Graphs 
display2=gdisplay(background=color.white,foreground=color.black)
distanceplanettoCM = gcurve(color=color.green)
velocityplanet = gcurve(color=color.orange)
distanceplanettostar1 = gcurve(color=color.red)
distanceplanettostar2 = gcurve (color=color.blue)
##
###Accel graphs
display2=gdisplay(background=color.white,foreground=color.black)
accelstar1onplanet = gcurve (color=color.cyan)
accelstar2onplanet = gcurve (color=color.orange)
accelplanet = gcurve (color=color.magenta)
#for comparison
star1gravity= gcurve(color=color.black)



while 1==1:
    #planet.Emech=.5*m1*mag(planet.velocity)**2-G*m1*m3/(mag(x3i-x1i))-G*m2*m3/(mag(x2i-x3i))
    #print planet.Emech
    rate(1.0/dt)
    time += dt
    #print time
    #updating Danny's Value

    #defining gravity magnitudes and vectors
    Fgmag=G*m1*m2/(mag(star1.pos-star2.pos))**2
    Fg13=G*m1*m3/(mag(planet.pos-star1.pos))**2
    Fg23=G*m2*m3/(mag(planet.pos-star2.pos))**2
    star1.gravity=Fgmag*(star2.pos-star1.pos)/mag(star2.pos-star1.pos)
    star2.gravity=Fgmag*(star1.pos-star2.pos)/mag(star1.pos-star2.pos)
    planet.gravity=Fg13*norm(star1.pos-planet.pos)+Fg23*norm(star2.pos-planet.pos)

    #print Fg13
    #print Fg23

    #acceleration
    a1=star1.gravity/m1
    a2=star2.gravity/m2
    planet.accel=planet.gravity/m3

    #acceleration components to better understand dynamic system
    planet.accelstar1=Fg13/m3*norm(star1.pos-planet.pos)
    planet.accelstar2=Fg23/m3*norm(star2.pos-planet.pos)

    #velocity
    star1.velocity+=a1*dt
    star2.velocity+=a2*dt
    planet.velocity+=planet.accel*dt

    #storing old position
    planet.oldpos=planet.pos
    #position
    star1.pos=star1.pos+star1.velocity*dt
    star2.pos=star2.pos+star2.velocity*dt
    planet.pos=planet.pos+planet.velocity*dt
    CM.pos=(star1.pos*m1+star2.pos*m2+planet.pos*m3)/(m1+m2+m3)

    planetCM=shapes.line(start=planet.pos, end = CM.pos, thickness = 10)

    #velocity arrow
    star1.velocityarrow.pos=star1.pos
    star1.velocityarrow.axis=star1.velocity/5
    star2.velocityarrow.pos=star2.pos
    star2.velocityarrow.axis=star2.velocity/5
    planet.velocityarrow.pos=planet.pos
    planet.velocityarrow.axis=planet.velocity/50

    #gravity arrow

##    star1.gravityarrow.pos=star1.pos
##    star1.gravityarrow.axis=star1.gravity/(Gscale*90)
##    star2.gravityarrow.pos=star2.pos
##    star2.gravityarrow.axis=star2.gravity/(Gscale*90)

    #planet accel arrow
##    planet.accelarrow.pos=planet.pos
##    planet.accelarrow.axis=planet.accel/20
##
##   #planet accel components arrow
##    planet.accelstar1arrow.pos=planet.pos
##    planet.accelstar1arrow.axis=planet.accelstar1/20
##    planet.accelstar2arrow.pos=planet.pos
##    planet.accelstar2arrow.axis=planet.accelstar2/20
    
    #planet CM arrow
    #planet.CMarrow.pos=planet.pos
    #planet.CMarrow.axis=CM.pos-planet.pos

##    #plotting accel graphs
    accelstar1onplanet.plot(pos=(time,mag(planet.accelstar1)))
    accelstar2onplanet.plot(pos=(time,mag(planet.accelstar2)))
    accelplanet.plot(pos=(time,mag(planet.accel)))
    star1gravity.plot(pos=(time,mag(star1.gravity)/1.0E2))
##    
##    #plotting position graphs
    distanceplanettoCM.plot(pos=(time,mag(CM.pos-planet.pos)))
    distanceplanettostar1.plot(pos=(time,mag(star1.pos-planet.pos)))
    distanceplanettostar2.plot(pos=(time,mag(star2.pos-planet.pos)))
    velocityplanet.plot(pos=(time,mag(planet.velocity)))
    
    #print 360/(2*pi)*diff_angle(planet.gravity, CM.pos-planet.pos)
    #Danny's Value Update
    DV=2.0*(star1.pos-CM.pos)/(mag(star1.pos-planet.pos))**3+(star2.pos-CM.pos)/(mag(star2.pos-planet.pos))**3
    #print DV

