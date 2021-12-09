import matplotlib.pyplot as plt               #map plotting
import numpy as np                            # Array


def GenerateDrifterFileName (location):                 #file name given tag
    fname = "VirginiaKey8723214_meantrend.txt"
    print (fname)                                 # show name before positions
    return fname


def ReadTidalData (fname, linetoSkip = 0):
    fObj = open(fname,'r')
    lineList = []
    lineList = fObj.readlines()
    fObj.close
    
    nitems = len (lineList)
    data = np.zeros((nitems,3))
    datyear = np.zeros(nitems)
    tidalmean = np.zeros(nitems)
    
    for i, line in enumerate(lineList[linetoSkip:]):
        if i == 0:
            header = line
        else:
            dataList = line.split ()
            #print(dataList)
            year = dataList[0]
            month = dataList[1]
            mean = dataList[2]
            datyear[i] = YeartoMonth(year,month)
            tidalmean[i] = mean
            data [i,0] = year
            data [i,1] = month
            data [i,2] = mean   
    #print (year,month,mean)                     # ensure code is functioning
    #print(datyear)
    #print(tidalmean)
    return datyear, tidalmean                   # adaptation of array

    
def YeartoMonth (year,month):                   # change date format
     # mon = int(month)/12
     # montstr = str(mon)
     # this = montstr[-1]                       # allows change to float
     yf = int(year)+int(month)/12
     #print ("year to month", yf)
     return yf

    
def RegressionAlg (xa,fa):
    """ Compute the linear regression for the data in arrays xa, fa. Usage is
     a = LinearRegression(xa,fa)
     where a[0] is the intercept and a[1] is the slope of the regression line.
    """
    a = [0,0]
    S = len(xa)
    tmean = xa.mean()
    fmean = fa.mean()
    t2mean = (xa**2).mean()
    tfmean = (xa*fa).mean()
    a[0] = (t2mean*fmean-tmean*tfmean)/(t2mean-tmean**2)
    a[1] = (tfmean-tmean*fmean)/(t2mean-tmean**2)
    return a

def RegressionLine (xa,a):
    """ compute the linear regression fit for array xa.
        Usage is ffit = RegressiontoLine (xa,a), where ffit = a[0]+a[1]*xa
    """
    ffit = a[0] + a[1]*xa
    return ffit
    
def slope(x1,y1,x2,y2):
    return (y2-y1)/(x2-x1)


def PlotMap (x,y):
    """ tidal data shown as black ’+’ 
        while the regression line should be shown in red
    
        plot for each city and report the name of the city 
        and the rate of sea-level rise in the title in mm/year
    """
    plt.scatter(x,y,c='black',marker='+')

def main(filename,sealevelrise):
    """ print to the screen the city name and the slope of its sea-level rise.
    """
    city = ""
    for p in filename:
        if p.isdigit():
            break
        city += p
        
    x,y = ReadTidalData(filename)
    PlotMap(x[1:],y[1:])                                        # skip header
    a = RegressionAlg(x[1:],y[1:])                              # skip header
    line = RegressionLine(x[1:],a)
    plt.plot(x[1:],line,'r')                                    # plot data
    plt.title(city + " " + sealevelrise)                        # title
    plt.xlabel("year")
    plt.ylabel("mm")
    plt.show()
    plt.close()
    
    print("City: ",city,"Slope: ",slope(x[1],line[0],x[-1],line[-1]))
    
    
    # j = np.array([1.0,2,3])
    # k = np.array([3.0,4,5])
    # q = RegressionAlg(j,k)
    # line = RegressionLine(j,q)
    # print(k)
    # print(line)
    

main("VirginiaKey8723214_meantrend.txt","2.97 mm/year")
main("Honolulu1612340_meantrend.txt","n/a")
#main("KeyBiscayne.txt")
main("LaJolla9410230_meantrend.txt","1.55  mm/year")
main("Philadelphia8545240_meantrend.txt","3.04 mm/year")
main("SanFrancisco9414290_meantrend.txt","1.97 mm/year")
main("Seattle9447130_meantrend.txt","2.06 mm/year")
