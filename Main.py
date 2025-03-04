#imports required libraries
import tkinter as tk
from tkinter import ttk
import os
import subprocess
import numpy as np

def runSim():
    """Simulation start
    Takes the data inputed by the user in the GUI and saves it to selectedAlgoDT.npy and selectedBodies.npy and runs 'Simulation.py' 
    Checks inputs are valid before running
    """    
    try:
    #get the values in the algorithm, time step and time fields
        selectedAlgo = algo.get()
        selectedDT = float(dtEntry.get())
        selectedTime = float(totalTimeEntry.get())
        selectedAlgoDT=[selectedAlgo,selectedDT,selectedTime] #store algorithm, time step and time in a list
        
        #loops through all bodies and if the body is selected adds it to selectedBodies list
        selectedBodies = []
        for i, body in enumerate(bodies):
            if checkboxVars[i].get() == 1:  #check if the checkbox is selected
                selectedBodies.append(body)

        if selectedAlgo!='Euler' and selectedAlgo!='Euler-Cromer' and selectedAlgo!='Verlet': #ensures selected algorithm is one of the pre programmed algorithms
            label.config(text="Error: Algorithm must be selected from dropdown menu") #if not send error message
        elif len(selectedBodies)<2: #checks if at least 2 bodies are selected
            label.config(text="Error: At least 2 bodies must be selected") #if less than 2 bodies are selected sends error
        else: #if all inputs are okay procceeds to try to run the simulation
            #get the folder where this script is located
            scriptFolder = os.path.dirname(os.path.realpath(__file__))
            print(scriptFolder)
            #change the current working directory to the folder of this file
            os.chdir(scriptFolder)

            #save user inputs for Bodies.py and Simulation.py to use
            np.save('selectedBodies.npy', selectedBodies, allow_pickle=True)
            np.save('selectedAlgoDT.npy', selectedAlgoDT, allow_pickle=True)

            #run Simulation.py
            try:
                subprocess.run(['python', 'Simulation.py'], check=True)
            
            #if there is an error running Simulation.py send error message to GUI
            except subprocess.CalledProcessError as e:
                label.config(text=f"Error running the simulation: {e}")
                
    #if timestep or total time is not a number output an error
    except ValueError:
        label.config(text="Time step and Total Time must be numbers")

def runResults():
    """Display results
    runs 'reader.py'
    """    
    #get the folder where this script is located
    scriptFolder = os.path.dirname(os.path.realpath(__file__))

    #change the current working directory to the folder of this file as simulationData.npy shoukd be in that folder
    os.chdir(scriptFolder)
    
    try:
        subprocess.run(['python', 'reader.py'], check=True) #runs reader.py
    except subprocess.CalledProcessError as e:
        label.config(text=f"Error running Results reader (reader.py): {e}") #sends error message if there is an error running reader.py

def addBody():
    """Add user defined body
    Adds the body from the users inputted data checking the data and creating a new checkbox for the new body 
    """    
    #get the new body name, mass, and coordinates (position and velocity) from the entry fields
    bodyName = bodyNameEntry.get()
    bodyMass = bodyMassEntry.get()
    posX = posXEntry.get()
    posY = posYEntry.get()
    posZ = posZEntry.get()
    velX = velXEntry.get()
    velY = velYEntry.get()
    velZ = velZEntry.get()
    
    #ensures new body has a unique name
    uniqueName = True
    for i in range(len(bodies)):
        if bodies[i][0] == bodyName:
            uniqueName = False
    if bodyName == 'Moon' or bodyName == 'Luna': #due to the moon being referred to as either Luna or Moon, checks both names
        uniqueName = False
    
    if uniqueName == True: #if the new bodies name is unique adds the body as a checkbox
        
        #check if the inputs are not empty
        if bodyName and bodyMass and posX and posY and posZ and velX and velY and velZ:
            try:
                #try to convert mass and coordinates to appropriate data types
                bodyMass = float(bodyMass)
                posX = float(posX)
                posY = float(posY)
                posZ = float(posZ)
                velX = float(velX)
                velY = float(velY)
                velZ = float(velZ)
            
                #add the new body to the bodies list
                bodies.append([bodyName, bodyMass, posX, posY, posZ, velX, velY, velZ])
                newVar = tk.IntVar()

                #create a new checkbox for the new body and pack it immediately
                checkbox = tk.Checkbutton(checkboxFrame, text=bodyName, variable=newVar)
                checkbox.pack(anchor='w', padx=10)

                #add the new IntVar to the list of checkbox variables
                checkboxVars.append(newVar)

                #update the canvas and scroll region after adding the new body so the checkbox shows
                canvas.update_idletasks()
                canvas.config(scrollregion=canvas.bbox("all"))
            
                #clear the entry fields after adding the body
                bodyNameEntry.delete(0, tk.END)
                bodyMassEntry.delete(0, tk.END)
                posXEntry.delete(0, tk.END)
                posYEntry.delete(0, tk.END)
                posZEntry.delete(0, tk.END)
                velXEntry.delete(0, tk.END)
                velYEntry.delete(0, tk.END)
                velZEntry.delete(0, tk.END)

            except ValueError:
                #show an error message if any of the inputs are not valid numbers
                label.config(text="Please enter valid numbers for the body's mass, position, and velocity.")
        else:
            #if any input is empty, show an error message
            label.config(text="Please enter all fields: body name, mass, position, and velocity.")
    else:
        label.config(text="Please use a unique name for added bodies")


def onFocusIn(entry, placeholderText):
    """Focus on input box
    When an entry field is clicked on clears the placeholder text if it's still there
    """
    if entry.get() == placeholderText:#checks if placeholder text is in textbox
        entry.delete(0, tk.END) #deletes placeholder text
        entry.config(fg="black")  #change text colour to black 

def onFocusOut(entry, placeholderText):
    """Focus off input box
    When an entry field is clicked off of restores the placeholder text if the field is empty
    """
    if entry.get() == "": #checks if the textbox is empty
        entry.insert(0, placeholderText) #adds appropriate placeholder text
        entry.config(fg="grey")  #makes the placeholder text colour grey


#create the main window
root = tk.Tk()
root.title("Simulation")#window has the title Simulation

#create a label for displaying the source of the pre-programmed bodies and G and pack it
sourceLabel = tk.Label(root, text="Default bodies position and velocity data taken from JPL Ephemeris at time 2024-01-10 00:00:00.0 using the Astroquery library.\nThe mass of the bodies is obtained from Poliastro. The value of G used in calculation of acceleration obtained from the astropy library.")
sourceLabel.pack(pady=10)


#create a frame to hold the checkboxes on the right side of the GUI
rightFrame = tk.Frame(root)
rightFrame.pack(side="right", padx=10, pady=10)

#create a canvas to hold the checkboxs in the rightFrame and set its width to half the screen
canvas = tk.Canvas(rightFrame, width=200, height=300)
canvas.pack(side="left", fill="both", expand=True)

#add a scrollbar to the canvas
scrollbar = tk.Scrollbar(rightFrame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

#create a frame inside the canvas to hold the checkboxes
checkboxFrame = tk.Frame(canvas)
#create window to hold frame and allow scrollbar
canvas.create_window((0, 0), window=checkboxFrame, anchor="nw")

#create a frame for the algorithm, time step and total time
algodtFrame=tk.Frame(root)
algodtFrame.pack()

#create a label for the algorithm selection
label = tk.Label(algodtFrame, text="Algorithm:")
label.pack(pady=10)


#create a dropdown menu of preprogrammed algorithms
options = ["Euler", "Euler-Cromer", "Verlet"]
algo = ttk.Combobox(algodtFrame, values=options)
algo.pack(pady=10)
algo.set("Euler") #preset the dropdown menu to "Euler"

#create total time label and entry field
totalTimeLabel = tk.Label(algodtFrame, text="Total time simulated (in seconds):")
totalTimeLabel.pack(side='left',pady=5)
totalTimeEntry = tk.Entry(algodtFrame)
totalTimeEntry.pack(side='left',pady=5)
totalTimeEntry.insert(0, "e.g. 1.0e10")  #placeholder text for total time to show appropriate input
totalTimeEntry.config(fg="gray")  #set placeholder text colour
#bind focusIn and FocusOut functions to entry field
totalTimeEntry.bind("<FocusIn>", lambda event: onFocusIn(totalTimeEntry, "e.g. 1.0e10"))
totalTimeEntry.bind("<FocusOut>", lambda event: onFocusOut(totalTimeEntry, "e.g. 1.0e10"))


#create time step label and entry field
dtLabel = tk.Label(algodtFrame, text="Time step between calculations (in seconds):")
dtLabel.pack(side='left',pady=5)
dtEntry = tk.Entry(algodtFrame)
dtEntry.pack(side='left',pady=5)
dtEntry.insert(0, "e.g. 300")  #placeholder text for time step to show appropriate input
dtEntry.config(fg="gray")  #set placeholder text colour
#bind focusIn and FocusOut functions to entry field
dtEntry.bind("<FocusIn>", lambda event: onFocusIn(dtEntry, "e.g. 300"))
dtEntry.bind("<FocusOut>", lambda event: onFocusOut(dtEntry, "e.g. 300"))


#create list of bodies with checkboxes
bodies = [["Sun",0,0,0,0,0,0,0], ["Mercury",0,0,0,0,0,0,0], ["Venus",0,0,0,0,0,0,0], ["Earth",0,0,0,0,0,0,0], ["Luna(Moon)",0,0,0,0,0,0,0], ["Mars",0,0,0,0,0,0,0], ["Jupiter",0,0,0,0,0,0,0], ["Saturn",0,0,0,0,0,0,0], ["Uranus",0,0,0,0,0,0,0], ["Neptune",0,0,0,0,0,0,0], ["Pluto",0,0,0,0,0,0,0]]

#create list that holds the variables of what checkboxes are checked
checkboxVars = []
#create checkboxes for each body
for i in range(len(bodies)):
    var=tk.IntVar() #create variable for if box is checked
    checkbox = tk.Checkbutton(checkboxFrame, text=bodies[i][0],variable=var) #create checkbox button
    checkbox.pack(anchor='w', padx=10) #pack checkbox
    checkboxVars.append(var)#add var to checkboxVars

#update the scroll region to accommodate all checkboxes
canvas.config(scrollregion=canvas.bbox("all"))


#create input fields and button for adding new bodies
addBodyLabel = tk.Label(root, text="Add a new body:")
addBodyLabel.pack(pady=10)

bodyNameLabel = tk.Label(root, text="Body Name (Use a unique name for each body):")
bodyNameLabel.pack(pady=5)
bodyNameEntry = tk.Entry(root)
bodyNameEntry.pack(pady=5)
bodyNameEntry.insert(0, "e.g. Body 1") #placeholder text for body name to show appropriate input
bodyNameEntry.config(fg="gray")  #set placeholder text colour
#bind focusIn and FocusOut functions to entry field
bodyNameEntry.bind("<FocusIn>", lambda event: onFocusIn(bodyNameEntry, "e.g. Body 1"))
bodyNameEntry.bind("<FocusOut>", lambda event: onFocusOut(bodyNameEntry, "e.g. Body 1"))

bodyMassLabel = tk.Label(root, text="Body Mass (in kg):")
bodyMassLabel.pack(pady=5)
bodyMassEntry = tk.Entry(root)
bodyMassEntry.pack(pady=5)
bodyMassEntry.insert(0, "e.g. 1.0e10")  #placeholder text for body mass to show appropriate input
bodyMassEntry.config(fg="gray")  #set placeholder text colour
#bind focusIn and FocusOut functions to entry field
bodyMassEntry.bind("<FocusIn>", lambda event: onFocusIn(bodyMassEntry, "e.g. 1.0e10"))
bodyMassEntry.bind("<FocusOut>", lambda event: onFocusOut(bodyMassEntry, "e.g. 1.0e10"))

#label for position fields
posLabel = tk.Label(root, text="Position (x, y, z in m from SSB):")
posLabel.pack(pady=5)

#create a frame to hold the position inputs side by side
posFrame = tk.Frame(root)  
posFrame.pack(pady=5)

posXLabel = tk.Label(posFrame, text="X Coordinate:")
posXLabel.pack(side="left", padx=5)
posXEntry = tk.Entry(posFrame)
posXEntry.pack(side="left", padx=5)
posXEntry.insert(0, "e.g. 1.0e10") #placeholder text for x position to show appropriate input
posXEntry.config(fg="gray")  #set placeholder text colour
#bind focusIn and FocusOut functions to entry field
posXEntry.bind("<FocusIn>", lambda event: onFocusIn(posXEntry, "e.g. 1.0e10"))
posXEntry.bind("<FocusOut>", lambda event: onFocusOut(posXEntry, "e.g. 1.0e10"))

posYLabel = tk.Label(posFrame, text="Y Coordinate:")
posYLabel.pack(side="left", padx=5)
posYEntry = tk.Entry(posFrame)
posYEntry.pack(side="left", padx=5)
posYEntry.insert(0, "e.g. 1.0e10")  #placeholder text for y position to show appropriate input
posYEntry.config(fg="gray")  #set placeholder text colour
#bind focusIn and FocusOut functions to entry field
posYEntry.bind("<FocusIn>", lambda event: onFocusIn(posYEntry, "e.g. 1.0e10"))
posYEntry.bind("<FocusOut>", lambda event: onFocusOut(posYEntry, "e.g. 1.0e10"))

posZLabel = tk.Label(posFrame, text="Z Coordinate:")
posZLabel.pack(side="left", padx=5)
posZEntry = tk.Entry(posFrame)
posZEntry.pack(side="left", padx=5)
posZEntry.insert(0, "e.g. 1.0e10")  #placeholder text for z position to show appropriate input
posZEntry.config(fg="gray")  #set placeholder text colour
#bind focusIn and FocusOut functions to entry field
posZEntry.bind("<FocusIn>", lambda event: onFocusIn(posZEntry, "e.g. 1.0e10"))
posZEntry.bind("<FocusOut>", lambda event: onFocusOut(posZEntry, "e.g. 1.0e10"))

#label for velocity inputs
velLabel = tk.Label(root, text="Velocity (vx, vy, vz in m/s):")
velLabel.pack(pady=5)

#create a frame to hold the velocity inputs side by side
velFrame = tk.Frame(root)  
velFrame.pack(pady=5)

velXLabel = tk.Label(velFrame, text="VX:")
velXLabel.pack(side="left", padx=5)
velXEntry = tk.Entry(velFrame)
velXEntry.pack(side="left", padx=5)
velXEntry.insert(0, "e.g. 1.0e10")  #placeholder text for x velocity to show appropriate input
velXEntry.config(fg="gray")  #set placeholder text colour
#bind focusIn and FocusOut functions to entry field
velXEntry.bind("<FocusIn>", lambda event: onFocusIn(velXEntry, "e.g. 1.0e10"))
velXEntry.bind("<FocusOut>", lambda event: onFocusOut(velXEntry, "e.g. 1.0e10"))

velYLabel = tk.Label(velFrame, text="VY:")
velYLabel.pack(side="left", padx=5)
velYEntry = tk.Entry(velFrame)
velYEntry.pack(side="left", padx=5)
velYEntry.insert(0, "e.g. 1.0e10")  #placeholder text for y velocity to show appropriate input
velYEntry.config(fg="gray")  #set placeholder text colour
#bind focusIn and FocusOut functions to entry field
velYEntry.bind("<FocusIn>", lambda event: onFocusIn(velYEntry, "e.g. 1.0e10"))
velYEntry.bind("<FocusOut>", lambda event: onFocusOut(velYEntry, "e.g. 1.0e10"))

velZLabel = tk.Label(velFrame, text="VZ:")
velZLabel.pack(side="left", padx=5)
velZEntry = tk.Entry(velFrame)
velZEntry.pack(side="left", padx=5)
velZEntry.insert(0, "e.g. 1.0e10")  #placeholder text for z velocity to show appropriate input
velZEntry.config(fg="gray")  #set placeholder text colour
#bind focusIn and FocusOut functions to entry field
velZEntry.bind("<FocusIn>", lambda event: onFocusIn(velZEntry, "e.g. 1.0e10"))
velZEntry.bind("<FocusOut>", lambda event: onFocusOut(velZEntry, "e.g. 1.0e10"))

#create the add body button which runs addBody function
addButton = tk.Button(root, text="Add Body", command=addBody)
addButton.pack(pady=10)

#create the run simulation button which runs runSim function
addButton = tk.Button(root, text="Run Simulation", command=runSim)
addButton.pack(pady=10)

#create the read previous results button which runs runResults function
addButton = tk.Button(root, text="Read Previous Results", command=runResults)
addButton.pack(pady=10)

#start the main event loop to display GUI
root.mainloop()
