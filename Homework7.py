import matplotlib.pyplot as plt               #map plotting
import numpy as np

import cartopy.crs as ccrs 
import cartopy.feature as cfeature


def GenerateDrifterFileName (driftertag):                 #file name given tag
    fname = "CARTHE_{:03}".format(driftertag) + ".dat"    #three numbers at end
    #print (fname)                                 # show name before positions
    return fname

def ReadDrifterData (fname, linetoSkip = 0):            # read data in fname
    fObj = open (fname, 'r')                           # open file
    lineList = []
    #print(lineList)
    lineList = fObj.readlines()                         # read
    fObj.close()                                        # close
    
    nitems = len (lineList)                             # length of data                                                 
    positions = np.zeros([nitems,2])                    # create array
    
    for i,line in enumerate (lineList[linetoSkip: ]):
        itemList = line.split ()
        lat = float (itemList [2])
        lon = float (itemList [3])
        positions [i, 0] = lon 
        positions [i, 1] = lat
    #print (positions, positions) 
    return positions

def ReadDrifters (driftertagList):
    drifterList = []                                     # empty list
    for tag in driftertagList:                      # read and change filename
        filename = GenerateDrifterFileName(tag)
        drifterData = ReadDrifterData (filename)
        drifterList.append(drifterData)                  # add to list
    return drifterList

def FDAapproximation (positions, dt):
    df = np.zeros (positions.shape)
    for i  in range(len(positions)):
        if (i==0):
            df[i,:] = (-3*positions[0]+4*positions[1]-positions[i-1])/(2*dt)
        elif (i <= len(positions)-2):
            df[i,:]= (positions[i+1]-positions[i-1])/(2*dt)
        else:
            df[i,:]= (positions[len(positions)-3]+4*positions[1])/ (2*dt)
    return df 

def GetDrifterVelocity (positions,dt):
    vel = np.zeros(positions.shape)
    posRad = positions * np.pi/180.0
    dp = FDAapproximation (posRad, dt)
    rdp = dp * 6371e3
    vel[:,0] = rdp [:,0]* np.cos(posRad[:,1])
    vel[:,1] = rdp[:,1]
    return vel

def GetDrifterSpeed (positions,dt):
    speed = np.zeros(positions.shape)
    posRad = positions * np.pi/180.0
    dp = FDAapproximation (posRad, dt)
    rdp = dp * 6371e3
    speed[:,0] = abs(rdp [:,0]* np.cos(posRad[:,1]))
    speed[:,1] = abs(rdp[:,1])
    return speed

def main ():
    driftertagList = [1,2,3,4,5,6,7,8,10,11]
    drifterPosList = ReadDrifters(driftertagList)
    #print(drifterPosList)
    
    latlim = [17,33]            #  define south/north limit
    lonlim = [-100,-75]         # define east/west limit
    
    latGridLineSpacing = np.linspace(latlim[0],latlim[1],11)
    lonGridLineSpacing = 0.5*(lonlim[0]+lonlim[1])+np.zeros_like(latGridLineSpacing)
    

    #ax.set_xticks(np.arange(lonlim[0],lonlim[1],lonGridLineSpacing))
    #ax.set_yticks(np.arange(latlim[0],latlim[1],latGridLineSpacing))
    #fig.canvas.draw ()
    #plt.pause (0.1)
    
        
    lons = 0
    drifterList = ReadDrifters(driftertagList)
    #print(drifterPosList)
    counter = 0
    for tag in drifterList:
        fig = plt.figure ()
        projObj = ccrs.PlateCarree()
        ax = plt.axes(projection = projObj)         # generate axis
        ax.set_extent(lonlim+latlim)                # define the map
        ax.stock_img()
        ax.coastlines(resolution = '50m')           # coastline
        ax.add_feature(cfeature.LAND)               # add land
        ax.add_feature(cfeature.OCEAN)              # add ocean
        ax.gridlines(draw_labels = True)            # add grind lines

        ccounter = driftertagList[counter]
        #print(drifterList)
        print ('Drifter: ', tag)
        print("launch: ", tag[0]) #printing launch point
        ax.plot(tag[0][0],tag[0][1], marker="*")
        for bouy in tag:
            ax.plot(bouy[0],bouy[1],'r')
        print("last: ",tag[-1]) #printing last point
        ax.plot(tag[-1][0],tag[-1][1], marker=".")
        
        lons = lons + 0.05
        dt = 15*60
        positions = ReadDrifterData(GenerateDrifterFileName(ccounter))
        counter += 1
        #print(positions)
        Velocity = GetDrifterVelocity(positions, dt)
        print("Velocity = ", Velocity)
        ax.quiver(positions[::len(positions)],positions[::len(positions)], Velocity[::len(Velocity)], Velocity[::len(Velocity)], color="b")
        Speed = GetDrifterSpeed(positions, dt)
        print("Speed = ", Speed)
        
        #fig,ax = plt.subplot()
        ax.plot(positions[:, 0], positions [:,1], 'r',transform=projObj)
        #fig.canvas.draw ()
        #plt.pause (0.1)
        plt.show()
        speedMean = np.mean(Speed)
        speedMax = np.max(Speed)
        speedStddev = np.std(Speed)
        speedVar = np.var(Speed)
        print ("speed: mean = ", speedMean)
        print ("speed: Max = ", speedMax)
        print ("speed: Stddev = ", speedStddev)
        print ("speed: variance = ", speedVar)
main()

