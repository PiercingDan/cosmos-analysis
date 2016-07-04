from visual import *
from visual.graph import *
import random

scene.height=800
scene.width=600
scene.range=(400,400,400)
scene.autoscale=False
scene.background=color.white

#Creating Celestial bodies

class body:
    def __init__ (self, position, mass, velocity):
        body.position=position
        body.mass=mass
        body.velocity=velocity
        body.radius=mass**1/3
    def display (self):
        print self.position
        print self.mass
        print self.velocity

CB = []

def ran_bodies (n):
     for i in range (0, n):
         px=random.uniform(-10.0,10.0)
         py=random.uniform(-10.0,10.0)
         pz=random.uniform(-10.0,10.0)
         vx=random.uniform(-10.0,10.0)
         vy=random.uniform(-10.0,10.0)
         vz=random.uniform(-10.0,10.0)
         m=random.uniform(0.0,10.0)
         p=vector(px,py,pz)
         v=vector(vx,vy,vz)
         print p
         tempbod=body(p,m,v)
         CB.append(tempbod)
         CB[i].display
         
#numbodies = input ("Number of Bodies: ")
#ran_bodies (numbodies)

x=(0,0,0)
y = vector(0.0,0.0,0.0)

