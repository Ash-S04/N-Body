#import required libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import gridspec
import copy

#import the Body class and instances defined in the Bodies.py file
from Bodies import Body


def init():
    """Initiate
    Initiates the animation of the plots and sets the limit of the 3d plot
    Returns:
        pl: returns the 3d plot
    """
    
    #sets limits for the 3d plot based on the radius of the orbiting bodies  
    radius=0
    for i in range(numBodies):
        pos=Body.bodies[i].position
        #checks if the magnitude of the position in each direction is greater than the radius and if so sets it as the new radius
        if abs(pos[0])>radius:
            radius=abs(pos[0])
        if abs(pos[1])>radius:
            radius=abs(pos[1])
        if abs(pos[2])>radius:
            radius=abs(pos[2])
    negradius=0-radius #makes a negative radius as a lower limit
    #sets the limits of all axis to +/- radius
    ax.set_xlim(negradius, radius)
    ax.set_ylim(negradius, radius)
    ax.set_zlim(negradius, radius)
    return pl, #returns pl

# Update function for the animation
def update(frame, dt, timeData, momentumX, momentumY, momentumZ, frames, data):
    """Frame Update
    Performs all the updates for each frame and saves data when animation finishes to 'simulationdata.npy'

    Args:
        frame (int): Current frame
        dt (int): time step for updates
        timeData (list): list of all times at which momentum, position, velocity and acceleration are calculated in s
        momentumX (list): total momentum in x direction
        momentumY (list): total momentum in y direction
        momentumZ (list): total momentum in z direction
        frames (int): total number of frames
        data (list): list of data the will be saved 

    Returns:
        pl, momentumPlotX, momentumPlotY, momentumPlotZ: all plots are returned to be updated on the GUI
        data : the list of data is returned
    """
    if selectedAlgo != 'Verlet': #as verlet algorithm uses different form check that algorithm isnt verlet
        for i in range(numBodies): # loops through bodies to update the gravitational acceleration
            Body.bodies[i].updateGravitationalAcceleration()
        for i in range(numBodies): #if alorithm isnt verlet loop through all bodies
            Body.bodies[i].update(dt,selectedAlgo)#run update on each body
    else:
        Body.bodies[0].update(dt,selectedAlgo)#if algorithm is verlet run update on one body (Verlet on one body acts as update on all bodies and update also updates gravitational acceleration)

        
    #update the position data for each body and total momentum
    xPos, yPos, zPos = [], [], [] #create list of postion in each direction
    momentum = np.array([0, 0, 0], dtype=float) #create numpy array of floats of the total momentum
    for i in range(numBodies): #for each body
        #append position of body to lists
        xPos.append(Body.bodies[i].position[0])
        yPos.append(Body.bodies[i].position[1])
        zPos.append(Body.bodies[i].position[2])
        momentum += Body.bodies[i].momentum()  #add momentum of the body to total
        
    #append new momentum values to graph data
    momentumX.append(momentum[0])
    momentumY.append(momentum[1])
    momentumZ.append(momentum[2])
    
    #append new time to graph data
    timeData.append(timeData[-1] + dt)
    
    #update the scatter plot with new positions
    pl._offsets3d = (xPos, yPos, zPos)
    
    #update the momentum plots with new data
    momentumPlotX.set_xdata(timeData)
    momentumPlotX.set_ydata(momentumX)
    
    momentumPlotY.set_xdata(timeData)
    momentumPlotY.set_ydata(momentumY)
    
    momentumPlotZ.set_xdata(timeData)
    momentumPlotZ.set_ydata(momentumZ)
    
    #update the x-limits for the momentum plot dynamically based on time
    mo.set_xlim(0, max(timeData)) 
    
    #update the y-limits for the momentum plots dynamically based on new data
    maxMomentum = max(max(momentumX), max(momentumY), max(momentumZ))
    minMomentum = min(min(momentumX), min(momentumY), min(momentumZ))
    margin = (maxMomentum - minMomentum) * 0.1  #add a margin of 10% of the range of the min and max momentum to limits so all values are in frame
    mo.set_ylim(minMomentum - margin, maxMomentum + margin) #sets new limits for momentum figure
    
    dataAdd=[timeData[-1]]#gets most recent time
    for i in range(numBodies):
        dataAdd.append(copy.deepcopy(Body.bodies[i])) #uses deepcopy to copy all the data for each instance of Body
    data.append(dataAdd)#appends new data to the data list
    
    if frame==frames-1: #when all frames have run
        np.save('simulationdata.npy', data, allow_pickle=True) #save data in simulationdata.npy
        anim.event_source.stop() #stops animation so no more frames run

        
    return pl, momentumPlotX, momentumPlotY, momentumPlotZ, data, #returns all plots and data list

#loads file with user inputs from Main.py
selectedAlgoDT=np.load('selectedAlgoDT.npy',allow_pickle=True)

#sets selectedAlgo to algorithm selected by user
selectedAlgo=selectedAlgoDT[0]

#sets time and dt to user inputs from Main.py
time = float(selectedAlgoDT[2])
dt = float(selectedAlgoDT[1])

frames = int(time/dt)#sets number of frames to the number of timesteps in the total time


#set numBodies to the number of instances of the class body imported from Bodies.py
numBodies = len(Body.bodies)

#create a variable to store the data of the simulation to be saved and accessed later
dataAdd=[0]#adds data at time=0s
for i in range(numBodies):#loops through all bodies
    Body.bodies[i].updateGravitationalAcceleration()#updates gravitaional acceleration so it is based on the bodies on the simulation and not the default
    dataAdd.append(copy.deepcopy(Body.bodies[i]))#uses deepcopy to copy all the data for each instance of Body
data=[dataAdd]#creates a 2d list of time and Body instances

#have plot use style _mpl-gallery
plt.style.use('_mpl-gallery')

#create figure with increased figsize
fig = plt.figure(figsize=(10, 10))

#creates spec which sets the size of the subplots to fit better on fig
spec = gridspec.GridSpec(ncols=1, nrows=2,
                        width_ratios=[1], wspace=0.1,
                        hspace=0.1, height_ratios=[3, 2],
                        bottom=0.05,left=0.05)

ax = fig.add_subplot(spec[0],projection="3d")  #3D axes for body positions on the top
mo = fig.add_subplot(spec[1])  #2D plot for momentum below

#get scatter plot data
colours = [] #default bodies have distinct colours to help differentiate them so colours need to be a list
xPos, yPos, zPos = [], [], [] #create list for position on each axis
for i in range(numBodies): #iterate through bodies
    colours.append(Body.bodies[i].colour) #adds colour to colours list
    #adds position of the body to the correlating list
    xPos.append(Body.bodies[i].position[0])
    yPos.append(Body.bodies[i].position[1])
    zPos.append(Body.bodies[i].position[2]) 

#create scatter plot of the bodies' positions and colours on the 3D axes and label the axis
pl = ax.scatter(xPos, yPos, zPos, color=colours)

#label 3D plot axes
ax.set_xlabel('Distance from SSB (m)')
ax.set_ylabel('Distance from SSB (m)')
ax.set_zlabel('Distance from SSB (m)')
ax.grid(False) #remove grid from 3D plot

#get data for momentum subplot
timeData = [0] #add time 0 seconds
momentum = np.array([0, 0, 0], dtype=float) #creates a numpy array of floats for the total momentum
for i in range(numBodies):#for each body
    momentum += Body.bodies[i].momentum() #add the momentum of the body to the total momentum

#puts momentum in each direction into correlating list
momentumX = [momentum[0]]
momentumY = [momentum[1]]
momentumZ = [momentum[2]]

#initialize momentum plots in each directions with markers and labels for legend
momentumPlotX, = mo.plot(timeData, momentumX, label="Momentum X", marker='o', markersize=2.5)
momentumPlotY, = mo.plot(timeData, momentumY, label="Momentum Y", marker='o', markersize=2.5)
momentumPlotZ, = mo.plot(timeData, momentumZ, label="Momentum Z", marker='o', markersize=2.5)

mo.legend(loc=1) #adds legend labeling momentum data on subplot and sets position so it does not move when subplot is updated

#labels axes of subplot mo with appropriate labels and units
mo.set_xlabel('Time (s)')
mo.set_ylabel('Momentum (kg*m/s)')

#set limits of mo subplot based on momentum values
maxMomentum = max(max(momentumX), max(momentumY), max(momentumZ))
minMomentum = min(min(momentumX), min(momentumY), min(momentumZ))
margin = (maxMomentum - minMomentum) * 0.1  #add a margin of 10% of the range of the min and max momentum to limits so all values are in frame
mo.set_ylim(minMomentum - margin, maxMomentum + margin) #sets new limits for momentum figure

#create the animation of fig that uses the update function, that updates every 0.5s (value of interval)
anim = FuncAnimation(fig, update, frames=frames, fargs=(dt, timeData, momentumX, momentumY, momentumZ, frames, data), init_func=init, interval=0.5, blit=False)

#display the plot and runs animation anim
plt.show()
