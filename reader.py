#import required modules
import tkinter as tk
import numpy as np


def printBody(body):
    """Create output of body
    Creates and packs labels outputting the name, mass, position, velocity and acceleration of the body taken as an argument

    Args:
        body (instance of Body class)
        
    Returns:
        output: a string containing readable data to be saved to SimulationDataOutput.txt
    """    
    #create a sting bodyData with the name and mass of the body
    bodyData="  Body: {0}\n     Mass: {1:.3e} kg,\n".format(body.name,body.mass)# 
    
    #create and pack label displaying bodyData
    results = tk.Label(resultsFrame, text=bodyData)
    results.pack(side="top", fill="x", pady=2)
    
    #create output string containing bodyData
    output=bodyData

    #define lists of attributes and the units of the attributes
    attribute=["position", "velocity", "acceleration"]
    units=['m','m/s','m.s^2']
    
    #loop for all attributes
    for i in range(3):
        #create string bodyData of attribute name, value and units
        bodyData="      {}: {}{}\n".format(attribute[i], body.__getattribute__(attribute[i]) + 0.0,units[i])
        
        #create and pack label displaying bodyData
        results = tk.Label(resultsFrame, text=bodyData)
        results.pack(side="top", fill="x", pady=2)
        
        #add bodyData to output
        output=output+bodyData
        
    return output #returns output string


#loads simulationdata.npy to variable data
data = np.load('simulationdata.npy', allow_pickle=True)

#creates tkinter window
root = tk.Tk()
root.title("Simulation Results")

#create a canvas widget
canvas = tk.Canvas(root, width=400, height=300)
canvas.pack(side="left", fill="both", expand=True)

#add a vertical scrollbar to the right of the canvas
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

#create a frame inside the canvas to hold the results
resultsFrame = tk.Frame(canvas)
#create window to hold frame and allow scrollbar
canvas.create_window((0, 0), window=resultsFrame, anchor="nw")

#create string to be saved in a text file for the user
text=""

#loop through all data
for i in range(len(data)):
    #create resultsData string taking time from data
    resultsData = "Time: {0} seconds\n".format(data[i][0])
    #add string to text
    text=text+resultsData
    #create and pack label to output resultsData
    results = tk.Label(resultsFrame, text=resultsData)
    results.pack(side="top", fill="x", pady=2)
    
    #loop through bodies at current data item
    for j in range(1,len(data[0])):
        #add returned string from print body for current body to text
        text=text+printBody(data[i][j])


#update the canvas and scroll region after adding the new body so the checkbox shows
canvas.update_idletasks() 
canvas.config(scrollregion=canvas.bbox("all"))

#start the main event loop to display GUI
root.mainloop()

#once GUI is closed create/edit 'SimulationDataOutput.txt'
f=open('SimulationDataOutput.txt','w')
#write text to 'SimulationDataOutput.txt'
f.write(text)
#save and close 'SimulationDataOutput.txt'
f.close()