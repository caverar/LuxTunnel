from tkinter import messagebox as mb
import math
import numpy as np
class calculator():

#---FIRST-PHASE-L20---------------------------------------------------------------------------------------------------------------------------------------------
    
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

#---SECOND-PHASE-LUMINANCE---------------------------------------------------------------------------------------------------------------------------------------
    def secondPhaseReset(self,luminairesHeight = 10, luminairesBetweenDistance = 40, roadWidth = 25, roadLanes=2, luminairesRotation = 90):
        
        
        self.luminairesHeight = luminairesHeight                            
        self.luminairesBetweenDistance = luminairesBetweenDistance          
        self.roadWidth = roadWidth
        self.roadLanes = roadLanes                                          
        self.luminairesRotation = luminairesRotation                    # Degrees
        self.getMeshPoints()
        self.getGammaCCoordinates()

        self.loadIES(loadFile = True, route = "sit.ies")
        try:
            #self.loadIES(loadFile = True)
            self.getstepGammaCeL()
            self.illuminanceFirstStep()
        except:
            mb.showerror("ERROR","No se pudo completar apropiadamente el proceso de calculo.")
            pass    


    def printSencondPhaseData(self):
        print("Px: ")
        print(self.Px)
        print("Py: ")
        print(self.Py)
    def getMeshPoints(self):
        
        if self.luminairesBetweenDistance <= 30:
            N = 10
            D = self.luminairesBetweenDistance/10   
        else:
            N = 11
            D = self.luminairesBetweenDistance/11 
            while(D > 3):
                N=N+1
                D=self.luminairesBetweenDistance/N

        Px = [[0 for j in range(3*self.roadLanes)] for i in range(N)]
        Py = [[0 for j in range(3*self.roadLanes)] for i in range(N)]     
        
        
        
        for i in range(N):
            for j in range(3*self.roadLanes):
                Px[i][j] = (D/2) + (D*i)
                Py[i][j] = (self.roadWidth/(3*self.roadLanes))*(0.5+j)            

        self.Px = Px
        self.Py = Py
        self.N = N

    def getGammaCCoordinates(self):
        Nlumback=int((5*self.luminairesHeight)/self.luminairesBetweenDistance);
        Nlumfor=int((12*self.luminairesHeight)/self.luminairesBetweenDistance)+1;
        Nlum=Nlumback+Nlumfor+1;

        Ly = [0 for i in range(Nlum)]
        Lx = [0 for i in range(Nlum)]

        for i in range(Nlum):    
            Lx[i] = -(Nlumback-i)*self.luminairesBetweenDistance;
            Ly[i] = 0;
        

        #print("self.Px")
        #print(self.Px)
        #print("self.Py")
        #print(self.Py)


        CeL = np.zeros((3*self.roadLanes, self.N, Nlum))
        GammaL = np.zeros((3*self.roadLanes, self.N, Nlum))

        for i in range(Nlum):
            for j in range(self.N):
                for k in range(3*self.roadLanes):      

                    CeL[i][j][k] = math.atan((self.Py[j][k]-Ly[i])/(self.Px[j][k]-Lx[i]))*(180/math.pi)
                    GammaL[i][j][k]=math.atan((math.sqrt(math.pow(self.Px[j][k]-Lx[i],2)+math.pow(self.Py[j][k]-Ly[i],2))/self.luminairesHeight))*(180/math.pi)
                    if(i>Nlumback):
                        CeL[i][j][k] += 180


        self.CeL = CeL
        self.GammaL = GammaL 
        self.Nlum = Nlum
        
        #print("CeL")
        #print(CeL)
        #print("GammaL")
        #print(GammaL)



    def loadIES(self, loadFile = True, route = "Sit4.ies"):
        if(loadFile):
            class tiltUnsupportedError(Exception):
                pass
            class corruptFile(Exception):
                pass
            class metricSystem(Exception):
                pass
            class unsupportedGeometry(Exception):
                pass 
            class unsupportedPhotometry(Exception):
                pass 
            try:
                with open(route,'r') as file:
                    iesText = file.read()
                iesText= iesText.split()
                #print(iesText)
                tiltAlreadyRead = True
                i = 0
                while(tiltAlreadyRead):
                    if(iesText[i]=="TILT=INCLUDE"):
                        raise tiltUnsupportedError
                    elif(iesText[i]=="TILT=NONE"):
                        tiltAlreadyRead = False
                        break
                    elif i >100:
                        raise corruptFile
                    i+=1
                i+=3
                luxMultiplier = float(iesText[i])
                rawGammaSize = int(iesText[i+1])
                rawCSize = int(iesText[i+2])
                photometricType = int(iesText[i+3])
                if(photometricType != 1):
                    raise unsupportedPhotometry

                unitsType = int(iesText[i+4])

                if(unitsType != 2 ):
                    raise metricSystem
                i+=5
                width = float(iesText[i])
                length = float(iesText[i+1])
                height = float(iesText[i+2])
                #if not (width != 0 and length != 0 and height != 0):
                #    raise unsupportedGeometry
                i+=6
                rawGammaIndex = np.zeros((rawGammaSize))
                rawCIndex = np.zeros((rawCSize))
                rawIES = np.zeros((rawCSize,rawGammaSize))

                for j in range(rawGammaSize):
                    rawGammaIndex[j] = iesText[i+j]
                i+= rawGammaSize
                for j in range(rawCSize):
                    rawCIndex[j] = iesText[i+j]
                i+= rawCSize   
                #print("rawGammaSize: "+str(rawGammaSize))
                #print("rawCSize: "+str(rawCSize))
 

                for j in range(rawCSize):
                    for k in range(rawGammaSize):
                        #print("j: " + str(j))
                        #print("k: " + str(k))
                        #print("index: " + str(i+(rawCSize*j)+k))
                        #print("value: " + str(float(iesText[i+(rawCSize*j)+k])*luxMultiplier))
                        rawIES[j][k] = float(iesText[i+(rawCSize*j)+k])*luxMultiplier

                # Interpolation:

                self.StepGamma=5
                self.StepC=10
                preRotationIESGammaSize = int((180/self.StepGamma)+1)
                preRotationIESCSize = int((360/self.StepC)+1)
                
                preRotationIES = np.zeros((preRotationIESCSize, preRotationIESGammaSize ))
                rawGammaFSO = rawGammaIndex[len(rawGammaIndex)-1]-rawGammaIndex[0]  
                rawCFSO = rawCIndex[len(rawCIndex)-1]-rawCIndex[0]

                # Type 3 photometry symmetry
                if(rawCFSO == 0 ):
                    auxIESCSize = int((360/(self.StepC))+1)
                else:
                    auxIESCSize = int((360/(rawCIndex[1]-rawCIndex[0]))+1)

                auxIESGammaSize = int((180/(rawGammaIndex[1]-rawGammaIndex[0]))+1)
                auxIES = np.zeros((auxIESCSize, auxIESGammaSize))

                if(photometricType == 1):
                    # Gamma
                    if(int(rawGammaIndex[0]) == 0 and  int(rawGammaIndex[len(rawGammaIndex)-1]) == 90):
                        for j in range(rawCSize):
                            for k in range(rawGammaSize):
                                if(rawGammaIndex[k]<=90):
                                    auxIES[j][k] = rawIES[j][k]
                    elif(int(rawGammaIndex[0]) == 90 and int(rawGammaIndex[len(rawGammaIndex)-1]) == 180):
                        for j in range(rawCSize):
                            for k in range(rawGammaSize):
                                if(rawGammaIndex[k]>=90):
                                    auxIES[j][k] = rawIES[j][k]
                    else:
                        for j in range(rawCSize):
                            for k in range(rawGammaSize):
                                    auxIES[j][k] = rawIES[j][k]

                    #print(auxIES)
                    #print("auxIESCSize: " + str(auxIESCSize))
                    #print("auxIESGammaSize: " + str(auxIESGammaSize))
                    # C 

                    if(rawCFSO == 0):                                                           # CSize = 0, replication
                        rawCIndex =  np.zeros((auxIESCSize))
                        for j in range(auxIESCSize):
                            for k in range(auxIESGammaSize):
                                auxIES[j][k] = auxIES[0][k]
                                rawCIndex[j] = j*self.StepC
                        print("rawCIndex")
                        print(rawCIndex)

                    elif(rawCFSO == 90):                                                        # Csize = 90
                        for j in range(auxIESCSize):
                            for k in range(auxIESGammaSize):
                                if(j<=  90):
                                    auxIES[j][k] = auxIES[j][k]
                                elif(j<=180):
                                   auxIES[j][k] = auxIES[j][k] 
                                

                    #print(auxIES)


                for j in range(preRotationIESCSize):
                    wantedC = j * self.StepGamma
                    for k in range(preRotationIESGammaSize):
                        wantedGamma = k * self.StepC
                        if wantedGamma in rawGammaIndex and wantedC in rawCIndex:               # Default case, Interpolation don't needed             
                            #print("wantedGamma: " + str(wantedGamma))
                            #print("wantedC: " + str(wantedC))
                            preRotationIES[j][k] = auxIES[j][k]
                        elif(True):
                            pass
                            #print("TODO")                                                                 

                            

                print("width: " + str(width))
                print("length: " + str(length))
                print("height: " + str(height))    
                print("multiplier: " + str(luxMultiplier))
                print(rawGammaIndex)
                print(rawCIndex)
                print(preRotationIES[0])


            except FileNotFoundError:
                mb.showerror("ERROR","Ruta no encontrada.")
            except corruptFile:
                mb.showerror("ERROR","Archivo .ies corrupto.")  
            except tiltUnsupportedError:
                mb.showerror("ERROR","No se soportan fotometrias con TILT.")
            except metricSystem:
                mb.showerror("ERROR","Solo se soportan fotometrías en sistema métrico.")
            except unsupportedGeometry:
                mb.showerror("ERROR","Geometría de fotometría no soportada.")
            except unsupportedPhotometry:
                mb.showerror("ERROR","Solo se soportan fotometrías de tipo 3")

        else:

            self.IES = np.loadtxt("proof.txt")
            self.StepGamma=5
            self.StepC=10
            self.Indexgamma=180/5+1

            # print((self.IES))
            # Rotation:
            print("TODO Rotation")



    def getstepGammaCeL(self):
        # floor and ceil
        CL=self.CeL/self.StepC
        self.CL=CL+1
        self.CfL=np.floor(CL)
        self.CcL=np.ceil(CL)
        yL=self.GammaL/self.StepGamma
        self.yL=yL+1
        self.yfL=np.floor(yL)
        self.ycL=np.ceil(yL)
        
        print()
        #print("Cfl")
        #print(CfL)
        #print("CcL")
        #print(CcL)
    
    # illuminance
    
    def illuminanceFirstStep(self):
        IL = np.zeros((3*self.roadLanes, self.N, self.Nlum))
        eq3 = np.zeros((3*self.roadLanes, self.N))
        eq4 = np.zeros((3*self.roadLanes, self.N))
        #print(IL)
        print("Ln: " + str(3*self.roadLanes))
        print("N: " + str(self.N))
        print("Nlum: " + str(self.Nlum))
        print("IL shape: ")
        print(IL.shape)

        print("eq3 shape: ")
        print(eq3.shape)
        print(len(eq3[0]))

        
        for i in range(self.Nlum):
            for j in range(self.N):
                for k in range(3*self.roadLanes):
                    #print("i: " + str(i) + ", j: " + str(j) + ", k: " + str(k))
                    eq3[k][j]=self.yfL[i][j][k]
                    #print(c)
                    #eq3[j][k]=self.IES[int(self.yfL[i][j][k])][int(self.CfL[i][j][k])]+((self.CL[i][j][k]-self.CfL[i][j][k])/(self.CcL[i][j][k]-self.CfL[i][j][k]))*(self.IES[int(self.yfL[i][j][k])][int(self.CcL[i][j][k])]-self.IES[int(self.yfL[i][j][k])][int(self.CfL[i][j][k])])
                    #eq4[j][k]=self.IES[int(self.ycL[i][j][k])][int(self.CfL[i][j][k])]+((self.CL[i][j][k]-self.CfL[i][j][k])/(self.CcL[i][j][k]-self.CfL[i][j][k]))*(self.IES[int(self.ycL[i][j][k])][int(self.CcL[i][j][k])]-self.IES[int(self.ycL[i][j][k])][int(self.CfL[i][j][k])])
                    #IL[i][j][k]=eq3[j][k]+((self.yL[i][j][k]-self.yfL[i][j][k])/(self.ycL[i][j][k]-self.yfL[i][j][k]))*(eq4[j][k]-eq3[j][k])      
                    
        self.IL = IL
        
        #print(self.IL)            


def main():

    test = calculator()
    test.updatefirstData(maxSpeed = 60, slope = 0.5, fiftyPercentThreshold= False,  cardinalDirection = 0, Hemisphere = 0 )
    #test.printFirstData()
    #test.percentArray = [0.10,0.10,0.10,0.10,0.10,0.20,0.30]
    #test.doL20()
    #test.printSecondData()

    test.secondPhaseReset()
    #test.printSencondPhaseData()



if __name__ == '__main__':
    main()
        
