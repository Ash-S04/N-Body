#import required libraries
import numpy as np
from astropy.constants import G 

#although radius is not used currently in this simulation the Body class has a radius attribute for use in other simulations or programs
#kinetic energy is also not currently used but this class has a function to calculate it

class Body:
    """Class Body
    
    Class for bodies in the simulation
    
    Methods:
        __init__: initiates instance of the class
        __self__: returns information about instance
        update: updates velocity and position of instance
        updateGravitationalAcceleration: updates the acceleration of instance
        kineticEnergy: returns the kinetic energy of instance
        momentum: returns momentum of instance
    """    
    bodies=[] #list of all instances of the class Body
    def __init__(
        self,
        position=np.array([0, 0, 0], dtype=float), #default position to 0,0,0
        velocity=np.array([0, 0, 0], dtype=float), #default velocity to 0,0,0
        acceleration=np.array([0, 0, 0], dtype=float), #default acceleration to 0,0,0
        name='Ball', #default name to 'ball'
        mass=1.0, #default mass to 1
        radius=100, #default radius to 100
        G = G.value, #default G to the value of the gravitaional constant from astropy
        colour="red" #defaults colour to red
    ):
        """Instance initiation

        Creates an instance of the class

        Args:
            position (numpy array float): The position in m of the body as a vector about [0,0,0] Defaults to np.array([0, 0, 0], dtype=float).
            velocity (numpy array float): The velocity in m/s of the body as a vector about Defaults to np.array([0, 0, 0], dtype=float).
            acceleration (numpy array float): The acceleration in m/s^2 of the body as a vector about Defaults to np.array([0, -10, 0], dtype=float).
            name (str): Name of the body. Defaults to 'Ball'.
            mass (float): Mass of the body in kg. Defaults to 1.0.
            radius (int): Radius of body in m. Defaults to 100.
            G (float): Gravitation Constant. Defaults to 6.67408e-11.
            colour (str): colour of body on graph. Defaults to "red".
        """     
        #sets attributes to defaults or if argument exists to argument value   
        self.position = np.copy(position).astype(float) #copies the array taken in as a numpy array of floats
        self.velocity = np.copy(velocity).astype(float)#copies the array taken in as a numpy array of floats
        self.acceleration = np.copy(acceleration).astype(float)#copies the array taken in as a numpy array of floats
        self.name=name
        self.mass=mass
        self.radius=radius
        self.G = G
        self.colour=colour
        
        #adds this new instance to list of instances bodies
        Body.bodies.append(self)
    
    def __str__(self):
        """string of self
        
        Returns:
            str: Description of the body stating its name, mass, position, velocity and acceleration
        """        
        #returns a string that includes the attributes of an instance of body
        return "Body: {0}, Mass: {1:.3e}, Position: {2}, Velocity: {3}, Acceleration: {4}".format(self.name, self.mass,self.position, self.velocity, self.acceleration)

    def update(self, deltaT,algorithm):
        """Velocity and position updater
        
        Updates the velocity and position using one of 3 algorithms:
        Euler
        Euler-Cromer
        Verlet
        
        Usually only updates self but if using verlet updates all instances as verlet requires the acceleration to be updated
        
        Args:
            deltaT (float): the time step by which the velocity and positon are updated
            algorithm (str): the choice of which algorithm to use
        """     
        #set p,v and a to the position, velocity and acceleration of this instance of Body   
        p=self.position
        v=self.velocity
        a=self.acceleration
        
        #checks what algorithm to use
        if algorithm=="Euler":
            #Euler is the most basic and just adds the velocity*time to postion and acceleration*time to velocity
            self.position=p+v*deltaT #sets the attribute position of the calculated position
            self.velocity=v+a*deltaT #sets the attribute velocity of the calculated velocity
            
        elif algorithm=="Euler-Cromer":
            #Euler cromer is similar to Euler but instead uses the new velocity to calculate the position
            self.velocity=v+a*deltaT #sets the attribute velocity of the calculated velocity
            self.position=p+self.velocity*deltaT #sets the attribute position of the calculated position
            
        else:#as the GUI limits the inputs the only other algorithm would be Verlet so else is used
            #verlet requires the position and velocity of all bodies to be updated
            
            a=[]#create a list of the acceleration of all bodies
            l=len(Body.bodies) #gets the number of instances of Body
            
            for i in range(l):#for all instances of body
                a.append(Body.bodies[i].acceleration) #add instances acceleration attribute to list a
                #calculate position of instance using verlet method equation and set attribute position of instance to calculated array
                Body.bodies[i].position=Body.bodies[i].position+Body.bodies[i].velocity*deltaT+(Body.bodies[i].acceleration*deltaT**2)/2
                
            for i in range(l):#for all instances of body
                Body.bodies[i].updateGravitationalAcceleration() #run updateGravitationalAcceleration() method on instance
                
            for i in range(l):#for all instances of body
                #calculate velocity of instance using verlet method equation and set attribute velocity of instance to calculated array
                Body.bodies[i].velocity=Body.bodies[i].velocity+((Body.bodies[i].acceleration+a[i])*deltaT)/2
    
    def updateGravitationalAcceleration(self):
        """Update Acceleration
        Updates the acceleration of a body based on the force of gravity it experiences from the other bodies
        """  
        #set p and G to the position and G attributes of current instance      
        p=self.position
        G=self.G
        
        #set A to a numpy array of floats 
        A=np.array([0, 0, 0], dtype=float)
        
        #calculate total acceleration due to gravity from all other bodies
        for i in range(len(Body.bodies)):#loop through all instances of Body class
            
            #gui requires different names for instances of Body so checks that the other body name is not the same as current instance name
            if Body.bodies[i].name != self.name: 
                
                #sets M and P to the mass and position of the other body
                M=Body.bodies[i].mass
                P=Body.bodies[i].position
                
                r=p-P #r calculated as the displacement between current body and other body
                
                R=np.sqrt(r[0]**2+r[1]**2+r[2]**2) #R is the magnitude of the displacement r 
                
                if R!=0: #to avoid divide by 0 error ensures bodies are not in same position
                    A=A+(-(G*M)/R**3)*(r) # uses newtons equation to calculate acceleration due to the other body and adds it to the total acceleration
        
        self.acceleration=A #sets acceleration attribute to calculated total acceleration A

    def kineticEnergy(self):
        """Kinetic Energy
        Calculates the kinetic energy
        
        Returns:
            float: Kinetic Energy in Joules
        """        
        
        v=self.velocity #sets v to instances velocity
        vsqu=(v[0]**2+v[1]**2+v[2]**2)#square of the magnitude of the velocity
        m=self.mass #sets m to instances mass
        
        Ek=0.5*m*vsqu #calculate kinteric energy Ek using Ek=1/2*m*v^2
        return Ek #returns calculated kinetic energy
    
    def momentum(self):
        """Momentum
        Calculates the momentum

        Returns:
            Numpy Array Float: The momentum in kg*m/s
        """        
        momentum=self.mass*self.velocity #calculates momentum as an array of the mass of the instance multiplied by the velocity
        return momentum #returns calculaed momentum
