# N-Body
N-Body Simulator made as part of my degree

The simulation can use either the Euler, Euler-Cromer or Verlet algorithm to estimate the orbit of n-bodies.

To run the simulation download and decompress all files and run Main.py with python3. Select the algorithm, run time, timestep and bodies you wish to simulate and press the "Run Simulation" button.
To read the results file run Main.py and press the 'Read Previous Results' button, this will open a window with readable data and create a txt file with the readable data called 'SimulationDataOutput.txt. 

The following libraries are needed to run the simulation:

-os

-subprocess

-numpy 2.0.2

-poliastro 0.7.0

-matplotlib 3.10.0

-astropy 7.0.0

-tkinter




Main.py handles the GUI and allows the user to run and costumise the simulation

Body.py contains the class Body which is used to define bodies and calculate their orbits

Bodies.py creates instances of the class Body based on user input from Main.py

Simulation.py uses matplotlib to graph the movements of the bodies defined in Bodies.py

reader.py displays the data from simulationdata.npy in a readable format and creates a file SimulationDataOutput.txt containing the readable data
