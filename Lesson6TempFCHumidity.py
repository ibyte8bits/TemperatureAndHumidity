from vpython import *
import serial
import numpy as np
import time
import re

tempC = 0.0
tempF = 0.0
humidity = 0.0
faceRadius = 1.0
faceThickness = .1
faceColor = vector(1,1,1)
distanceMultiplier = 2.25

mySceneF = canvas(title='Temperature Fahrenheit',
    width=200,
    height=200,
    background=vector(78/255,52/255,46/255),
    center=vector(-distanceMultiplier*faceRadius,0,0))
mySceneC = canvas(title='Temperature Celsius',
    width=200,
    height=200,
    background=vector(78/255,52/255,46/255),
    center=vector(0,0,0))
mySceneH = canvas(title=' Relative Humidity',
    width=200,
    height=200,
    background=vector(78/255,52/255,46/255),
    center=vector(distanceMultiplier*faceRadius,0,0))

# Gage faces

mySceneF.select()
faceF = cylinder(radius=faceRadius,
    color=faceColor,
    axis=vector(0,0,faceThickness),
    pos=vector(-distanceMultiplier*faceRadius,0,-3.0*faceThickness/2.0))
mySceneC.select()
faceC = cylinder(radius=faceRadius,
    color=faceColor,
    axis=vector(0,0,faceThickness),
    pos=vector(0,0,-3.0*faceThickness/2.0))
mySceneH.select()
faceH = cylinder(radius=faceRadius,
    color=faceColor,
    length=faceThickness,
    axis=vector(0,0,faceThickness),
    pos=vector(distanceMultiplier*faceRadius,0,-3.0*faceThickness/2.0))

# Meter Needles
arrowLength = faceRadius * .9
arrowWidth = .02
mySceneF.select()
myArrorF = arrow(length=arrowLength,
    shaftwidth=arrowWidth,
    color=color.red,
    axis=vector(0,.9*faceRadius,0),
    pos=vector(-distanceMultiplier*faceRadius,0,.1))
mySceneC.select()
myArrorC = arrow(length=arrowLength,
    shaftwidth=arrowWidth,
    color=color.red,
    axis=vector(0,.9*faceRadius,0),
    pos=vector(0,0,.1))
mySceneH.select()
myArrorH = arrow(length=arrowLength,
    shaftwidth=arrowWidth,
    color=color.red,
    axis=vector(0,.9*faceRadius,0),
    pos=vector(distanceMultiplier*faceRadius,0,0.1))

# Fahrenheit Ticks start at 30 end at 130
tickStart = 5.0*np.pi/4.0
tickEnd = -np.pi/4.0
tickLength = .07
tickWidth = .01
tickHeight = .02
tempFRangeStart = 30
tempFRangeEnd = 130
tempFSteps = tempFRangeEnd - tempFRangeStart
majorTick = 0
mySceneF.select()
for theta in np.linspace(tickStart,tickEnd,tempFSteps+1):
    if majorTick % 10 == 0:
        tickMajor=box(color=color.black,
            pos=vector(arrowLength*np.cos(theta)-distanceMultiplier*faceRadius,arrowLength*np.sin(theta),0),
            size=vector(2*tickLength,2*tickWidth,2*tickHeight),
            axis=vector(np.cos(theta),np.sin(theta)*faceRadius,-faceThickness/2))
        textF = text(text=str(majorTick+30),
            color=color.black,
            align='center',
            pos=vector(.8*arrowLength*np.cos(theta)-distanceMultiplier*faceRadius,
                .8*arrowLength*np.sin(theta),
                0),
            height=.07)
    else:
        tickMajor=box(color=color.black,
            pos=vector(arrowLength*np.cos(theta)-distanceMultiplier*faceRadius,arrowLength*np.sin(theta),0),
            size=vector(tickLength,tickHeight,tickWidth),
            axis=vector(np.cos(theta),np.sin(theta),-faceThickness/2))
    majorTick = majorTick + 1
tempCRangeStart = 0
tempCRangeEnd = 50
tempCSteps = tempCRangeEnd - tempCRangeStart
majorTick = 0
mySceneC.select()
for theta in np.linspace(tickStart,tickEnd,tempCSteps+1):
    if majorTick % 10 == 0:
        tickMajorC=box(color=color.black,
            pos=vector(arrowLength*np.cos(theta),arrowLength*np.sin(theta),0),
            size=vector(2*tickLength,2*tickWidth,2*tickHeight),
            axis=vector(np.cos(theta),np.sin(theta)*faceRadius,-faceThickness/2))
        textC = text(text=str(majorTick),
            color=color.black,
            align='center',
            pos=vector(.8*arrowLength*np.cos(theta),
                .8*arrowLength*np.sin(theta),
                0),
            height=.07)
    else:
        tickMajorC=box(color=color.black,
            pos=vector(arrowLength*np.cos(theta),arrowLength*np.sin(theta),0),
            size=vector(tickLength,tickHeight,tickWidth),
            axis=vector(np.cos(theta),np.sin(theta),-faceThickness/2))
    majorTick = majorTick + 1
tempHRangeStart = 20
tempHRangeEnd = 90
tempHSteps = tempHRangeEnd - tempHRangeStart
majorTick = 0
mySceneH.select()
for theta in np.linspace(tickStart,tickEnd,tempHSteps+1):
    if majorTick % 10 == 0:
        tickMajor=box(color=color.black,
            pos=vector(arrowLength*np.cos(theta)+distanceMultiplier*faceRadius,arrowLength*np.sin(theta),0),
            size=vector(2*tickLength,2*tickWidth,2*tickHeight),
            axis=vector(np.cos(theta),np.sin(theta)*faceRadius,-faceThickness/2))
        textH = text(text=str(majorTick+20),
            color=color.black,
            align='center',
            pos=vector(.8*arrowLength*np.cos(theta)+distanceMultiplier*faceRadius,
                .8*arrowLength*np.sin(theta),
                0),
            height=.07)
    else:
        tickMajor=box(color=color.black,
            pos=vector(arrowLength*np.cos(theta)+distanceMultiplier*faceRadius,arrowLength*np.sin(theta),0),
            size=vector(tickLength,tickHeight,tickWidth),
            axis=vector(np.cos(theta),np.sin(theta),-faceThickness/2))
    majorTick = majorTick + 1    

# Rotating Arrows to start Angle
mySceneF.select()
myArrorF.rotate(angle=tickStart-np.pi/2, 
    origin=vector(-distanceMultiplier*faceRadius,0,0),
    axis=vector(0,0,1))
mySceneC.select()
myArrorC.rotate(angle=tickStart-np.pi/2, 
    origin=vector(0,0,0),
    axis=vector(0,0,1))
mySceneH.select()
myArrorH.rotate(angle=tickStart-np.pi/2, 
    origin=vector(distanceMultiplier*faceRadius,0,0),
    axis=vector(0,0,1))

# Hubs
mySceneF.select()
hubF = cylinder(radius=.06,
    color=color.red,
    axis=vector(0,0,faceThickness),
    pos=vector(-distanceMultiplier*faceRadius,0,0))
mySceneC.select()
hubC = cylinder(radius=.06,
    color=color.red,
    axis=vector(0,0,faceThickness),
    pos=vector(0,0,0))
mySceneH
hubH = cylinder(radius=.06,
    color=color.red,
    axis=vector(0,0,faceThickness),
    pos=vector(distanceMultiplier*faceRadius,0,0))

# Labels
mySceneF.select()
textFLabel=text(text='Temperature F',
    color=color.black,
    align='center',
    pos=vector(-distanceMultiplier*faceRadius,-.2,0),
    height=.1)
mySceneC.select()
textCLabel=text(text='Temperature C',
    color=color.black,
    align='center',
    pos=vector(0,-.2,0),
    height=.1)
mySceneH.select()
textHLabel=text(text='Relative Humidity',
    color=color.black,
    align='center',
    pos=vector(distanceMultiplier*faceRadius,-.2,0),
    height=.1)

arduino = serial.Serial('/dev/ttyUSB1', 115200)
readings = []

oldFTemp = 32.0
oldCTemp = 0.0
oldRH = 20.0
FDegreesToRadians = (tickEnd - tickStart) / (tempFRangeEnd - tempFRangeStart)
CDegreesToRadians = (tickEnd - tickStart) / (tempCRangeEnd - tempCRangeStart)
RHToRadians = (tickEnd - tickStart) / (tempHRangeEnd - tempHRangeStart)
while True:
    while arduino.in_waiting == 0:
        pass
    dataPacket = arduino.readline()
    dataPacket = str(dataPacket, 'utf-8')
    dataPacket = dataPacket.strip('\r\n')
    readings = re.split(' ', dataPacket)
    temperatureF = float(readings[0])
    temperatureC = float(readings[3])
    RHumidity = float(readings[6].strip('%'))
    print('Degrees F = ' + str(temperatureF))
    print('Degrees C = ' + str(temperatureC))
    print('Humidity = ' + str(RHumidity))
    deltaF = temperatureF - oldFTemp
    deltaC = temperatureC - oldCTemp
    deltaH = RHumidity - oldRH
    oldFTemp = temperatureF
    oldCTemp = temperatureC
    oldRH = RHumidity 
    thetaF = deltaF * FDegreesToRadians
    thetaC = deltaC * CDegreesToRadians
    thetaH = deltaH * RHToRadians
    myArrorF.rotate(angle=thetaF, 
        origin=vector(-distanceMultiplier*faceRadius,0,0),
        axis=vector(0,0,1))
    myArrorC.rotate(angle=thetaC, 
        origin=vector(0,0,0),
        axis=vector(0,0,1))
    myArrorH.rotate(angle=thetaH, 
        origin=vector(distanceMultiplier*faceRadius,0,0),
        axis=vector(0,0,1)) 
  


