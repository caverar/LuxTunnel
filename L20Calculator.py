from tkinter import messagebox as mb
import math
import numpy as np
class L20Calculator():

#---FIRST-PHASE-L20---------------------------------------------------------------------------------------------------------------------------------------------
    
    def __init__(self,maxSpeed = 60, slope = 0.1, fiftyPercentThreshold= False, MountainousTerrain = False, cardinalDirection = 0, Hemisphere = 0, 
                Lc = 0, Lr = 0, LeRocks = 0, LeBuildings = 0, LeSnow =0, LeMeadows = 0,  
                percentArray = [0.10,0.10,0.10,0.10,0.10,0.20,0.30]):
        
        self.percentArray = percentArray                                # Area materials percent array [Lc, Lr, LeRocks, LeBuildings, LeSnow, LeMeadows]
        
        self.maxSpeed = maxSpeed                                        # Max speed at tunnel entrance, Km/h
        self.fiftyPercentThreshold = fiftyPercentThreshold              # If the illuminance must be over 50% Lth 
        self.slope = slope                                              # slope percent, ratio between Verticaldistance/Horizontaldistance, (-1,1) = (-45º, 45º)
        self.MountainousTerrain = MountainousTerrain                                        
        self.cardinalDirection = cardinalDirection                      # 0: North, 1: West, 2: South, 3: East
        self.Hemisphere = Hemisphere                                    # 0: North, 1: South


        self.setLuminances(Lc = Lc, Lr = Lr, LeRocks = LeRocks, LeBuildings = LeBuildings, LeSnow =LeSnow, LeMeadows = LeMeadows )
                                                            
        self.setKFactor()                                               # k factor Lth/L20
        self.setFriction()                                              # wet friction 
        self.setstopDistance()                                          # Stop Distance

        if(self.SD <=0):
            mb.showerror("ERROR","La pendiente de la carretera es muy pronunciada y no es posible frenar en las condiciones seleccionadas de velocidad máxima y fricción de pavimento. ")
            self.SD = 0
       
        
        # self.slope < -(self.f)
        # f must be set before slope, to do the comparison
        self.doL20()




    def setKFactor(self):
        self.k = 0 
        if self.maxSpeed <= 60:
            self.k = 0.05
        else:
            self.k =((1/120000)*pow(self.maxSpeed,2))-((1/1500)*(self.maxSpeed))+(3/50)

    def setFriction(self):

        self.f= -((1/7980000)*pow(self.maxSpeed,3))+((137/2660000)*pow(self.maxSpeed,2))-((5837/798000)*self.maxSpeed)+(62/95)

    def setstopDistance(self):
        self.SD = ((self.maxSpeed*10)/36)+ (pow((self.maxSpeed*10)/36,2)/(2*(9.80665)*(self.f+self.slope)))

    def setLuminances(self,Lc = 0,  Lr = 0, LeRocks = 0, LeBuildings = 0, LeSnow =0, LeMeadows = 0):
        
        if (self.cardinalDirection == 0 and self.Hemisphere == 0 ) or (self.cardinalDirection == 2 and self.Hemisphere == 1):
            self.Lc = 8000
            self.Lr = 3000
            self.LeRocks = 3000
            self.LeBuildings = 8000
            self.LeSnow = 15000
            self.LeMeadows = 2000
        elif (self.cardinalDirection == 2 and self.Hemisphere == 0) or (self.cardinalDirection == 0 and self.Hemisphere == 1) :
            self.Lc = 12000
            self.Lr = 4000
            self.LeRocks = 2000
            self.LeBuildings = 6000
            if self.MountainousTerrain:
                self.LeSnow = 10000
            else:
                self.LeSnow = 15000
            self.LeMeadows = 2000
        else:
            self.Lc = 16000
            self.Lr = 5000
            self.LeRocks = 1000
            self.LeBuildings = 4000
            if self.MountainousTerrain:
                self.LeSnow = 5000
            else:
                self.LeSnow = 15000
            self.LeMeadows = 2000
        
        if(Lc>0) : self.Lc = Lc
        if(LeRocks>0) : self.LeRocks = LeRocks
        if(LeBuildings>0) : self.LeBuildings = LeBuildings
        if(LeSnow>0) : self.LeSnow = LeSnow
        if(LeMeadows>0) : self.LeMeadows = LeMeadows
        if(Lr>0) : self.Lr = Lr
    
    def doL20(self):
        self.Lth = ((self.percentArray[0]*self.Lc)+(self.percentArray[1]*self.Lr)+(self.percentArray[2]*self.LeRocks)
                   +(self.percentArray[3]*self.LeBuildings)+(self.percentArray[4]*self.LeSnow)+(self.percentArray[5]*self.LeMeadows))/((1/self.k)+self.percentArray[6])
        self.L20 = self.Lth/self.k
    

    # Print
    def printData(self):
        print("Velocidad maxima: " + str(self.maxSpeed)+ "km/h")
        print("Coeficiente de fricción: " + str(self.f))
        print("Distancia de parada: "+str(self.SD)+"m")
        print("Medio Lth?: "+str(self.fiftyPercentThreshold))
        ori = ["North", "West", "South", "East"]
        print("Orientación: " + str(ori[self.cardinalDirection]))
        print("Hemisferio: " + str(ori[self.Hemisphere+1]))
        print("Luminancias: Lc: " + str(self.Lc) + ", LeRocks: " + str(self.LeRocks) + ", LeBuildings: " + str(self.LeBuildings) + ", LeSnow: " + str(self.LeSnow) + ", LeMeadows: " + str(self.LeMeadows) + ", Lr: " + str(self.Lr))
        print("L20: " + str(self.L20))
        print("Lth: " + str(self.Lth))



def main():

    test = L20Calculator(maxSpeed = 60, slope = 0.5, fiftyPercentThreshold= False,  cardinalDirection = 0, Hemisphere = 0, 
                        percentArray = [0.10,0.10,0.10,0.10,0.10,0.20,0.30])
    test.printData()
 



if __name__ == '__main__':
    main()
        
