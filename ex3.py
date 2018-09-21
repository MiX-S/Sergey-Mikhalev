import turtle
import math
turtle.shape('turtle')
a = 50
for i in range(360):
    t = i * math.pi/180
    x = 2*a*math.cos(t) - a*math.cos(2*t)
    y = 2*a*math.sin(t) - a*math.sin(2*t)
    turtle.goto(x, y)
