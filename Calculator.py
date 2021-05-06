from tkinter import messagebox as mb
class calculator():
    def __init__(self,maxSpeed = 60, slope = 0.1, fiftyPercentThreshold= False, MountainousTerrain = False, cardinalDirection = 0, Hemisphere = 0):
        self.maxSpeed = maxSpeed                                        # Max speed at tunnel entrance, Km/h
        self.fiftyPercentThreshold = fiftyPercentThreshold              # If the illuminance must be over 50% Lth 
        self.slope = slope                                              # slope percent, ratio between Verticaldistance/Horizontaldistance, (-1,1) = (-45º, 45º)
        self.MountainousTerrain = MountainousTerrain                                        
        self.cardinalDirection = cardinalDirection                      # 0: North, 1: West, 2: South, 3: East
        self.Hemisphere = Hemisphere                                    # 0: North, 1: South
        self.Lc = 0                                                     # Sky Luminance
        self.Le = 0                                                     # EnvironmentLuminance
        self.LeRocks = 0
        self.LeBuildings = 0
        self.LeSnow = 0
        self.LeMeadows = 0
        self.Lr = 0                                                     # Road Luminance
        self.setIlluminances()
        self.k = 0                                                      # k factor Lth/L20
        self.setKFactor()
        self.f = 0                                                      # wet friction
        self.setFriction()
        self.SD = 0.0                                                   # Stop Distance
        self.setstopDistance()
        if(self.SD <=0):
            mb.showerror("ERROR","La pendiente de la carretera es muy pronunciada y no es posible frenar en las condiciones seleccionadas de velocidad máxima y fricción de pavimento. ")
            self.SD = 0
        self.percentArray = [0 for i in range(6)]                       # Area materials percent array
        
        self.Lth = 0
        self.L20 = 0
        # self.slope < -(self.f)
        # f must be set before slope, to do the comparison

    def setKFactor(self):

        if self.maxSpeed <= 60:
            self.k = 0.05
        else:
            self.k =((1/120000)*pow(self.maxSpeed,2))-((1/1500)*(self.maxSpeed))+(3/50)

    def setFriction(self):
        self.f= -((1/7980000)*pow(self.maxSpeed,3))+((137/2660000)*pow(self.maxSpeed,2))-((5837/798000)*self.maxSpeed)+(62/95)

    def setstopDistance(self):
        self.SD = ((self.maxSpeed*10)/36)+ (pow((self.maxSpeed*10)/36,2)/(2*(9.80665)*(self.f+self.slope)))

    def setIlluminances(self):

        if (self.cardinalDirection == 0 and self.Hemisphere == 0 ) or (self.cardinalDirection == 2 and self.Hemisphere == 1):
            self.Lc = 8
            self.Lr = 3
            self.LeRocks = 3
            self.LeBuildings = 8
            self.LeSnow = 15
            self.LeMeadows = 2
        elif (self.cardinalDirection == 2 and self.Hemisphere == 0) or (self.cardinalDirection == 0 and self.Hemisphere == 1) :
            self.Lc = 12
            self.Lr = 4
            self.LeRocks = 2
            self.LeBuildings = 6
            if self.MountainousTerrain:
                self.LeSnow = 10
            else:
                self.LeSnow = 15
            self.LeMeadows = 2
        else:
            self.Lc = 16
            self.Lr = 5
            self.LeRocks = 1
            self.LeBuildings = 4
            if self.MountainousTerrain:
                self.LeSnow = 5
            else:
                self.LeSnow = 15
            self.LeMeadows = 2
    

    def doL20(self):
        self.Lth = ((self.percentArray[0]*self.Lc)+(self.percentArray[1]*self.Lr)+(self.percentArray[2]*self.LeRocks)
                   +(self.percentArray[3]*self.LeBuildings)+(self.percentArray[4]*self.LeSnow)+(self.percentArray[5]*self.LeMeadows))/((1/self.k)+self.percentArray[6])

        self.L20 = self.Lth/self.k
    
    def setManualIlluminances(self, Lc = 0, LeRocks = 0, LeBuildings = 0, LeSnow =0, LeMeadows = 0, Lr = 0 ):
        self.LeRocks = LeRocks
        self.LeBuildings = LeBuildings
        self.LeSnow = LeSnow
        self.LeMeadows = LeMeadows
        self.Lc = Lc
        self.Lr = Lr


    def updatefirstData(self,maxSpeed = 60, slope = 0.1, fiftyPercentThreshold= False, MountainousTerrain = False, cardinalDirection = 0, Hemisphere = 0):
        self.maxSpeed = maxSpeed
        self.fiftyPercentThreshold = fiftyPercentThreshold
        self.slope = slope
        self.MountainousTerrain = MountainousTerrain 
        self.cardinalDirection = cardinalDirection
        self.Hemisphere = Hemisphere

        self.setKFactor()
        self.setFriction()
        self.setstopDistance()
        

        if(self.SD <=0):
            mb.showerror("ERROR","La pendiente de la carretera es muy pronunciada y no es posible frenar en las condiciones seleccionadas de velocidad máxima y fricción de pavimento. ")
            self.SD = 0
        self.setIlluminances()

    def updateSecondData(self, Lc = 0, LeRocks = 0, LeBuildings = 0, LeSnow =0, LeMeadows = 0, Lr = 0):
        self.setManualIlluminances(Lc = Lc, LeRocks = LeRocks, LeBuildings = LeBuildings, LeSnow =LeSnow, LeMeadows = LeMeadows, Lr = Lr)

    def printFirstData(self):
        print("Velocidad maxima: " + str(self.maxSpeed)+ "km/h")
        print("Coeficiente de friccion: " + str(self.f))
        print("Distancia de parada: "+str(self.SD)+"m")
        print("Medio Lth?: "+str(self.fiftyPercentThreshold))
        ori = ["North", "West", "South", "East"]
        print("Orientacion: " + str(ori[self.cardinalDirection]))
        print("Hemisferio: " + str(ori[self.Hemisphere+1]))
    
    def printSecondData(self):
        print("Iluminancias: Lc: " + str(self.Lc) + ", LeRocks: " + str(self.LeRocks) + ", LeBuildings: " + str(self.LeBuildings) + ", LeSnow: " + str(self.LeSnow) + ", LeMeadows: " + str(self.LeMeadows) + ", Lr: " + str(self.Lr))
        print("L20: " + str(self.L20))
        print("Lth: " + str(self.Lth))


def main():

    test = calculator()
    test.updatefirstData(maxSpeed = 60, slope = -0.1, fiftyPercentThreshold= False,  cardinalDirection = 0, Hemisphere = 0 )
    test.printFirstData()
    test.percentArray = [0.10,0.10,0.10,0.10,0.10,0.20,0.30]
    test.doL20()
    test.printSecondData()

    




  

if __name__ == '__main__':
    main()
        
