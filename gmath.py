import math
from display import *

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    normalize(normal)
    normalize(view)
    normalize(light[LOCATION])
    a=calculate_ambient(ambient, areflect)
    d=calculate_diffuse(light, dreflect, normal)
    s=calculate_specular(light, sreflect, view, normal)
    color=[a+b+c for a,b,c in zip(a,d,s)]
    return limit_color(color)
    
def calculate_ambient(alight, areflect):
    return [a*b for a,b in zip(alight, areflect)]

def calculate_diffuse(light, dreflect, normal):
    c=dot_product(normal, light[LOCATION])
    d= [a*b*c for a,b in zip(light[COLOR], dreflect)]
    return limit_color(d)
    
def calculate_specular(light, sreflect, view, normal):
    scale=dot_product(normal,light[LOCATION])
    first=[2*a*scale for a in normal]
    new=[a-b for a,b in zip(first, light[LOCATION])]
    c=dot_product(new, view)
    if c<0:
        c=-1*c**SPECULAR_EXP
    else:
        c=c**SPECULAR_EXP
    s= [a*b*c for a,b in zip(light[COLOR], sreflect)]
    return limit_color(s)

def limit_color(color):
    for i in range(3):
        if color[i]>255:
            color[i]=255
        if color[i]<0:
            color[i]=0
        color[i]=round(color[i])
    return color

#vector functions
#normalize vetor, should modify the parameter
def normalize(vector):
    mag=math.sqrt(vector[0]**2+vector[1]**2+vector[2]**2)
    vector[0]/=mag
    vector[1]/=mag
    vector[2]/=mag

#Return the dot porduct of a . b
def dot_product(a, b=[0,0,1]):
    return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]

#Calculate the surface normal for the triangle whose first
#point is located at index i in polygons
def calculate_normal(polygons, i):
    a=[polygons[i+1][0]-polygons[i][0],polygons[i+1][1]-polygons[i][1],polygons[i+1][2]-polygons[i][2]]
    b=[polygons[i+2][0]-polygons[i][0],polygons[i+2][1]-polygons[i][1],polygons[i+2][2]-polygons[i][2]]    
    return [a[1]*b[2]-b[1]*a[2],a[2]*b[0]-b[2]*a[0],a[0]*b[1]-b[0]*a[1]]
