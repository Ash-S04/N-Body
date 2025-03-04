#import required libraries
from astroquery.jplhorizons import Horizons
from astropy.constants import G 
from poliastro import constants
import astropy.units as u
import numpy as np

#import class Body from Body.py
from Body import Body

#although radius is not used currently in this simulation the Body class has a radius attribute for use in other simulations or programs

selectedBodies=np.load('selectedBodies.npy',allow_pickle=True) #load bodies selected by user from Main.py GUI

t = "2024-01-10 00:00:00.0000" #time at which the the data is pulled from JPL Ephemeris Horizons

#runs through all selected bodies and if any are defaults sets data from JPL ephemeris and poliastro
for i in range(len(selectedBodies)): 
    
    if selectedBodies[i][0]=='Sun': #for sun
        #gets mass and radius of sun from radius and GM of sun from astropy and G from astropy and the radius and remove units
        m=(constants.GM_sun/G).value 
        r=(constants.R_sun).value 
        
        jplData=Horizons(id=10, location='500@0', epochs={t}) #uses astroquery Horizons to get information for the Sun in vector form around SSB at time t
        
        #get the position and velocity from jplData as numpy arrays
        #jplData.vector().columns[string] gets the data in the column eith that label and stores it in a list. 
        #.to(u.m) and .to(u.m/u.s) converts the data to the appropriate units (from AU to m and days to seconds)
        #[0].value gets the number from the list and  removes the units so it can be stored as a float
        position=np.array([float(jplData.vectors().columns['x'].to(u.m)[0].value),float(jplData.vectors().columns['y'].to(u.m)[0].value),float(jplData.vectors().columns['z'].to(u.m)[0].value)],dtype='float')
        velocity=np.array([float(jplData.vectors().columns['vx'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vy'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vz'].to(u.m/u.s)[0].value)],dtype='float')
        
        #create instance of Body class for sun
        Sun=Body(
            position=position, #set position
            velocity=velocity, #set velocity
            name='Sun', #set name
            mass=m, #set mass
            radius=r, #set radius
            colour="orange" #set colour
        )
        
    elif selectedBodies[i][0]=='Mercury':#for mercury
        #gets mass and radius of mercury from radius and GM of mercury from astropy and G from astropy and the radius and remove units
        m=(constants.GM_mercury/G).value
        r=(constants.R_mercury).value
        
        jplData=Horizons(id=1, location='500@0', epochs={t})#uses astroquery Horizons to get information for Mercury in vector form around SSB at time t
        
        #get position and velocity (see first if for expaination of the method used below to get position and velocity)
        position=np.array([float(jplData.vectors().columns['x'].to(u.m)[0].value),float(jplData.vectors().columns['y'].to(u.m)[0].value),float(jplData.vectors().columns['z'].to(u.m)[0].value)],dtype='float')
        velocity=np.array([float(jplData.vectors().columns['vx'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vy'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vz'].to(u.m/u.s)[0].value)],dtype='float')
        
        #create instance of Body class for mercury
        Mercury=Body(
            position=position, #set position
            velocity=velocity, #set velocity
            name='Mercury',#set name
            mass=m, #set mass
            radius=r, #set radius
            colour="grey"#set colour
        )
        
    elif selectedBodies[i][0]=='Venus':#for venus
        #gets mass and radius of venus from radius and GM of venus from astropy and G from astropy and the radius and remove units
        m=(constants.GM_venus/G).value
        r=(constants.R_venus).value
        
        jplData=Horizons(id=299, location='500@0', epochs={t})#uses astroquery Horizons to get information for Venus in vector form around SSB at time t
        
        #get position and velocity (see first if for expaination of the method used below to get position and velocity)
        position=np.array([float(jplData.vectors().columns['x'].to(u.m)[0].value),float(jplData.vectors().columns['y'].to(u.m)[0].value),float(jplData.vectors().columns['z'].to(u.m)[0].value)],dtype='float')
        velocity=np.array([float(jplData.vectors().columns['vx'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vy'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vz'].to(u.m/u.s)[0].value)],dtype='float')
        
        #create instance of Body class for venus
        Venus=Body(
            position=position, #set position
            velocity=velocity, #set velocity
            name='Venus',#set name
            mass=m, #set mass
            radius=r, #set radius
            colour="orangered"#set colour
        )
        
    elif selectedBodies[i][0]=='Earth': #for earth
        #gets mass and radius of earth from radius and GM of earth from astropy and G from astropy and the radius and remove units
        m=(constants.GM_earth/G).value 
        r=(constants.R_earth).value
        
        jplData=Horizons(id=399, location='500@0', epochs={t})#uses astroquery Horizons to get information for the Earth in vector form around SSB at time t
        
        #get position and velocity (see first if for expaination of the method used below to get position and velocity)
        position=np.array([float(jplData.vectors().columns['x'].to(u.m)[0].value),float(jplData.vectors().columns['y'].to(u.m)[0].value),float(jplData.vectors().columns['z'].to(u.m)[0].value)],dtype='float')
        velocity=np.array([float(jplData.vectors().columns['vx'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vy'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vz'].to(u.m/u.s)[0].value)],dtype='float')
        
        #create instance of Body class for the earth
        Earth=Body(
            position=position, #set position
            velocity=velocity, #set velocity
            name='Earth',#set name
            mass=m, #set mass
            radius=r, #set radius
            colour='blue'#set colour
        )
    elif selectedBodies[i][0]=='Mars':#for mars
        #gets mass and radius of mars from radius and GM of mars from astropy and G from astropy and the radius and remove units
        m=(constants.GM_mars/G).value
        r=(constants.R_mars).value
        
        jplData=Horizons(id=499, location='500@0', epochs={t})#uses astroquery Horizons to get information for Mars in vector form around SSB at time t
        
        #get position and velocity (see first if for expaination of the method used below to get position and velocity)
        position=np.array([float(jplData.vectors().columns['x'].to(u.m)[0].value),float(jplData.vectors().columns['y'].to(u.m)[0].value),float(jplData.vectors().columns['z'].to(u.m)[0].value)],dtype='float')
        velocity=np.array([float(jplData.vectors().columns['vx'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vy'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vz'].to(u.m/u.s)[0].value)],dtype='float')
        
        #create instance of Body class for mars
        Mars=Body(
            position=position, #set position
            velocity=velocity, #set velocity
            name='Mars',#set name
            mass=m, #set mass
            radius=r, #set radius
            colour='red'#set colour
        )
        
    elif selectedBodies[i][0]=='Jupiter':#for jupiter
        #gets mass and radius of jupiter from radius and GM of jupiter from astropy and G from astropy and the radius and remove units
        m=(constants.GM_jupiter/G).value
        r=(constants.R_jupiter).value
        
        jplData=Horizons(id=599, location='500@0', epochs={t})#uses astroquery Horizons to get information for Jupiter in vector form around SSB at time t
        
        #get position and velocity (see first if for expaination of the method used below to get position and velocity)
        position=np.array([float(jplData.vectors().columns['x'].to(u.m)[0].value),float(jplData.vectors().columns['y'].to(u.m)[0].value),float(jplData.vectors().columns['z'].to(u.m)[0].value)],dtype='float')
        velocity=np.array([float(jplData.vectors().columns['vx'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vy'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vz'].to(u.m/u.s)[0].value)],dtype='float')
        
        #create instance of Body class for jupiter
        Jupiter=Body(
            position=position, #set position
            velocity=velocity, #set velocity
            name='Jupiter',#set name
            mass=m, #set mass
            radius=r, #set radius
            colour='tan'#set colour
        )
        
    elif selectedBodies[i][0]=='Saturn':#for saturn
        #gets mass and radius of saturn from radius and GM of saturn from astropy and G from astropy and the radius and remove units
        m=(constants.GM_saturn/G).value
        r=(constants.R_saturn).value
        
        jplData=Horizons(id=699, location='500@0', epochs={t})#uses astroquery Horizons to get information for Saturn in vector form around SSB at time t
        
        #get position and velocity (see first if for expaination of the method used below to get position and velocity)
        position=np.array([float(jplData.vectors().columns['x'].to(u.m)[0].value),float(jplData.vectors().columns['y'].to(u.m)[0].value),float(jplData.vectors().columns['z'].to(u.m)[0].value)],dtype='float')
        velocity=np.array([float(jplData.vectors().columns['vx'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vy'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vz'].to(u.m/u.s)[0].value)],dtype='float')
        
        #create instance of Body class for saturn
        Saturn=Body(
            position=position, #set position
            velocity=velocity, #set velocity
            name='Saturn',#set name
            mass=m, #set mass
            radius=r, #set radius
            colour='gold'#set colour
        )
        
    elif selectedBodies[i][0]=='Uranus':#for uranus
        #gets mass and radius of uranus from radius and GM of uranus from astropy and G from astropy and the radius and remove units
        m=(constants.GM_uranus/G).value
        r=(constants.R_uranus).value
        
        jplData=Horizons(id='799', location='500@0', epochs={t})#uses astroquery Horizons to get information for Uranus in vector form around SSB at time t
        
        #get position and velocity (see first if for expaination of the method used below to get position and velocity)
        position=np.array([float(jplData.vectors().columns['x'].to(u.m)[0].value),float(jplData.vectors().columns['y'].to(u.m)[0].value),float(jplData.vectors().columns['z'].to(u.m)[0].value)],dtype='float')
        velocity=np.array([float(jplData.vectors().columns['vx'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vy'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vz'].to(u.m/u.s)[0].value)],dtype='float')
        
        #create instance of Body class for uranus
        Uranus=Body(
            position=position, #set position
            velocity=velocity, #set velocity
            name='Uranus',#set name
            mass=m, #set mass
            radius=r, #set radius
            colour="aqua"#set colour
        )
        
    elif selectedBodies[i][0]=='Neptune':#for neptune
        #gets mass and radius of neptune from radius and GM of neptune from astropy and G from astropy and the radius and remove units
        m=(constants.GM_neptune/G).value
        r=(constants.R_neptune).value
        
        jplData=Horizons(id='899', location='500@0', epochs={t})#uses astroquery Horizons to get information for Neptune in vector form around SSB at time t
        
        #get position and velocity (see first if for expaination of the method used below to get position and velocity)
        position=np.array([float(jplData.vectors().columns['x'].to(u.m)[0].value),float(jplData.vectors().columns['y'].to(u.m)[0].value),float(jplData.vectors().columns['z'].to(u.m)[0].value)],dtype='float')
        velocity=np.array([float(jplData.vectors().columns['vx'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vy'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vz'].to(u.m/u.s)[0].value)],dtype='float')
        
        #create instance of Body class for neptune
        Neptune=Body(
            position=position, #set position
            velocity=velocity, #set velocity
            name='Neptune',#set name
            mass=m, #set mass
            radius=r, #set radius
            colour='navy'#set colour
        )
        
    elif selectedBodies[i][0]=='Pluto':#for pluto
        #gets mass and radius of pluto from radius and GM of pluto from astropy and G from astropy and the radius and remove units
        m=(constants.GM_pluto/G).value
        r=(constants.R_pluto).value
        
        jplData=Horizons(id=999, location='500@0', epochs={t})#uses astroquery Horizons to get information for Pluto in vector form around SSB at time t
        
        #get position and velocity (see first if for expaination of the method used below to get position and velocity)
        position=np.array([float(jplData.vectors().columns['x'].to(u.m)[0].value),float(jplData.vectors().columns['y'].to(u.m)[0].value),float(jplData.vectors().columns['z'].to(u.m)[0].value)],dtype='float')
        velocity=np.array([float(jplData.vectors().columns['vx'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vy'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vz'].to(u.m/u.s)[0].value)],dtype='float')
        
        #create instance of Body class for pluto
        Pluto=Body(
            position=position, #set position
            velocity=velocity, #set velocity
            name='Pluto',#set name
            mass=m, #set mass
            radius=r, #set radius
            colour='lightblue'#set colour
        )
        
    elif selectedBodies[i][0]=='Luna(Moon)':#for the moon
        #gets mass and radius of the moon from radius and GM of the moon from astropy and G from astropy and the radius and remove units
        m=(constants.GM_moon/G).value
        r=(constants.R_moon).value
        
        jplData=Horizons(id=301, location='500@0', epochs={t})#uses astroquery Horizons to get information for the Moon in vector form around SSB at time t
        
        #get position and velocity (see first if for expaination of the method used below to get position and velocity)
        position=np.array([float(jplData.vectors().columns['x'].to(u.m)[0].value),float(jplData.vectors().columns['y'].to(u.m)[0].value),float(jplData.vectors().columns['z'].to(u.m)[0].value)],dtype='float')
        velocity=np.array([float(jplData.vectors().columns['vx'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vy'].to(u.m/u.s)[0].value),float(jplData.vectors().columns['vz'].to(u.m/u.s)[0].value)],dtype='float')
        
        #create instance of Body class for the moon
        Luna=Body(
            position=position, #set position
            velocity=velocity, #set velocity
            name='Moon',#set name
            mass=m, #set mass
            radius=r, #set radius
            colour='pink'#set colour
        )
    
    else: #if not a pre defined body use intputted data to create instance of body
        #get user defined position and velocity from selectedBodies and add to numpy float arrays
        position=np.array([selectedBodies[i][2],selectedBodies[i][3],selectedBodies[i][4]], dtype=float)
        velocity=np.array([selectedBodies[i][5],selectedBodies[i][6],selectedBodies[i][7]], dtype=float)
        
        #define a new instance of body with users inputs
        BodyArbitrary=Body(
            position=position,#set position
            velocity=velocity,#set velocity
            name=selectedBodies[i][0],#set name to user defined name from selectedBodies
            mass=float(selectedBodies[i][1])#set mass to user defined mass from selectedBodies
        )

