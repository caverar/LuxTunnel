from tkinter import messagebox as mb
import math
import numpy as np

class LuminanceCalculator():

    def __init__(self, IESroute="Sit4.ies", luminairesHeight = 10, luminairesBetweenDistance = 40, roadWidth = 25, roadLanes=2, luminairesRotation = 0, luminariesOverhang = 0, luminariesDistribution = 0, Fm= 0.5):
        


        self.luminariesOverhang = luminariesOverhang        
        self.luminariesDistribution = luminariesDistribution                                    # 0:Single-side-Left, 1:Single-side-Right, 2:Double-side, 3:Double-side-staggered 
        self.Fm = Fm                                                                            # default value 10
        self.luminairesHeight = luminairesHeight                            
        self.luminairesBetweenDistance = luminairesBetweenDistance                              
        self.roadWidth = roadWidth                                                              # 30 max
        self.roadLanes = roadLanes                                                              # 3 max                    
        self.luminairesRotation = -luminairesRotation                                           # Degrees
        
        
        self.getMeshPoints()
        self.getGammaCCoordinates()
        self.loadIES(loadFile = True, route = IESroute, rotationAngle = -luminairesRotation)
        

        try:
            
            self.getstepGammaCeL()
            self.luminanceFirstStep()
            self.luminanceSecondStep()
            self.luminanceThirdStep()
            self.luminanceFourthStep()
        except:
            mb.showerror("ERROR","No se pudo completar apropiadamente el proceso de calculo.")
               
        


    

    
    
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

        if not (0 <=self.luminariesDistribution <=3):
            mb.showerror("ERROR","Ditribución de luminarias indefinida.")
            raise Exception   


        Nlumback=int((5*self.luminairesHeight)/self.luminairesBetweenDistance)
        Nlumfor=int((12*self.luminairesHeight)/self.luminairesBetweenDistance)+1
        Nlum=Nlumback+Nlumfor+1

        #print("Nlum:" + str(Nlum))
        #print("Nlumfor:" + str(Nlumfor))
    
        Ly = [0 for i in range(Nlum)]
        Lx = [0 for i in range(Nlum)]         
           

        if(self.luminariesDistribution == 0):                                                   # 0:Single-side-Left 
            for i in range(Nlum):    
                Lx[i] = -(Nlumback-i)*self.luminairesBetweenDistance
                Ly[i] = self.luminariesOverhang
        elif(self.luminariesDistribution == 1):                                                 # 1:Single-side-Right
            for i in range(Nlum):    
                Lx[i] = -(Nlumback-i)*self.luminairesBetweenDistance
                Ly[i] = self.roadWidth - self.luminariesOverhang

        elif(self.luminariesDistribution == 2):                                                 # 2:Double-side
            Ly = [0 for i in range(2*Nlum)]
            Lx = [0 for i in range(2*Nlum)]
            for i in range(Nlum): 
                Lx[i] = -(Nlumback-i)*self.luminairesBetweenDistance
                Ly[i] = self.luminariesOverhang
                Lx[i+Nlumback] = -(Nlumback-i)*self.luminairesBetweenDistance                
                Ly[i+Nlumback] = self.roadWidth - self.luminariesOverhang  
            Nlum=2*Nlum
        elif(self.luminariesDistribution == 3):                                                 # 3:Double-side-staggered
            Ly = [0 for i in range(2*Nlum)]
            Lx = [0 for i in range(2*Nlum)]
            for i in range(Nlum):  
                Lx[i] = -(Nlumback-i)*self.luminairesBetweenDistance
                Ly[i] = self.luminariesOverhang
                Lx[i+Nlumback] = (self.luminairesBetweenDistance/2)-(Nlumback-i)*self.luminairesBetweenDistance                
                Ly[i+Nlumback] = self.roadWidth - self.luminariesOverhang   
            Nlum=2*Nlum

        for i in range(Nlum):    
            Lx[i] = -(Nlumback-i)*self.luminairesBetweenDistance
            Ly[i] = 0
        
        #print("self.Lx: + str(self.Lx))
        #print("self.Ly: + str(self.Ly))



        CeL = np.zeros((Nlum, self.N, 3*self.roadLanes))
        GammaL = np.zeros((Nlum, self.N, 3*self.roadLanes))

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
        self.Nlumback = Nlumback
        #print("CeL")
        #print(CeL)
        #print("GammaL")
        #print(GammaL)


    def loadIES(self, loadFile = True, route = "Sit4.ies", StepGamma = 5, StepC=10, rotationAngle=0):
        if(loadFile):

            
            self.StepGamma=StepGamma
            self.StepC=StepC
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
                        #print("j: " + str(j) + ", k: " + str(k))
                        #print("index: " + str(i+(rawGammaSize*j)+k) +", value: " + str(float(iesText[i+(rawGammaSize*j)+k])*luxMultiplier))
                        rawIES[j][k] = float(iesText[i+(rawGammaSize*j)+k])*luxMultiplier

                # Interpolation:

                preRotationIESGammaSize = int((180/self.StepGamma)+1)
                preRotationIESCSize = int((360/self.StepC)+1)
                
                preRotationIES = np.zeros((preRotationIESCSize, preRotationIESGammaSize ))
                rawGammaFSO = rawGammaIndex[len(rawGammaIndex)-1]-rawGammaIndex[0]  
                rawCFSO = rawCIndex[len(rawCIndex)-1]-rawCIndex[0]

                #print("rawIES")
                #print(rawIES)

                # Type 3 photometry symmetry

                ## Indexes and sizes
                auxIESCSize = int((360/(self.StepC))+1)
                if(rawCFSO == 0):
                    auxIESCSize = int((360/(self.StepC))+1)
                    auxCIndex =  np.zeros((auxIESCSize))
                    for j in range(auxIESCSize):
                        auxCIndex[j] = j*self.StepC

                elif(rawCFSO <=90):
                    auxIESCSize = 4*(len(rawCIndex)-1)+1
                    #print("auxIESCSize: " + str(auxIESCSize))
                    auxCIndex = np.zeros((auxIESCSize))

                    for j in range(auxIESCSize):
                        #print("j: " + str(j))
                        if(j < (rawCSize-1)):
                            auxCIndex[j] = rawCIndex[j]
                        elif(j < 2*(rawCSize-1)):
                            auxCIndex[j] = rawCIndex[j-rawCSize+1]+90
                        elif(j < 3*(rawCSize-1)):
                            auxCIndex[j] = rawCIndex[j-(2*(rawCSize-1))]+180
                        else:
                            auxCIndex[j] = rawCIndex[j-(3*(rawCSize-1))]+270
  

                elif(rawCFSO <=180):                    
                    auxIESCSize = 2*(len(rawCIndex)-1)+1
                    auxCIndex = np.zeros((auxIESCSize))

                    for j in range(auxIESCSize):
                        if(j < (rawCSize-1)):
                            auxCIndex[j] = rawCIndex[j]
                        else:
                            auxCIndex[j] = rawCIndex[j-rawCSize+1]+180
                
                elif(rawCFSO <=360):
                    auxIESCSize = len(rawCIndex)
                    auxCIndex = rawCIndex

                if(rawGammaFSO == 90):
                    auxIESGammaSize = 2*(len(rawGammaIndex)-1)+1
                    auxGammaIndex = np.zeros((auxIESGammaSize))

                    for j in range(auxIESGammaSize):
                        if(auxGammaIndex[j] <= 90):
                            auxGammaIndex[j] = rawGammaIndex[j]
                        else:
                            auxGammaIndex[j] = rawGammaIndex[j-rawGammaSize]+90
                else:
                    auxIESGammaSize = len(rawGammaIndex)
                    auxGammaIndex = rawGammaIndex

                       
                #print("auxCIndex")
                #print(auxCIndex)                



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
                    #print("auxIES") 
                    #print(auxIES)
                    if(rawCFSO == 0):                                                           # CSize = 0, replication
                        for j in range(auxIESCSize):
                            for k in range(auxIESGammaSize):
                                auxIES[j][k] = auxIES[0][k]

                    elif(rawCFSO == 90):                                                        # Csize = 90
                        #print("auxIES_RLD:")
                        # look for j index
                        j90 = 0
                        j180 = 0
                        j360 = 0
                        for j in range(auxIESCSize):
                            if(auxCIndex[j] == 90):
                                j90 = j
                            elif(auxCIndex[j] == 180):
                                j180 = j
                            elif(auxCIndex[j] == 360):
                                j360 = j
                        # apply symmetry

                        for j in range(auxIESCSize):
                            for k in range(auxIESGammaSize):

                                if(auxCIndex[j]<=90):
                                    auxIES[j][k] = auxIES[j][k]
                                elif(auxCIndex[j]<=180):
                                    auxIES[j][k] = auxIES[j180-j][k]
                                elif(auxCIndex[j]<=270):
                                    auxIES[j][k] = auxIES[j-j180][k]
                                elif(auxCIndex[j]<=360):
                                    auxIES[j][k] = auxIES[j360-j][k]                      
                        
                            #print("indexC: " + str(auxCIndex[j]))
                            #print("jindex" + str())
                            #print(str(j) + ": auxIES:")
                            #print(auxIES[j]) 

                    elif(rawCFSO == 180):                                                        # Csize = 90
                    
                         # look for j index
                        j360 = 0
                        for j in range(auxIESCSize):
                            if(auxCIndex[j] == 360):
                                j360 = j

                        # apply symmetry
                        for j in range(auxIESCSize):
                            for k in range(auxIESGammaSize):

                                if(auxCIndex[j]<=180):
                                    auxIES[j][k] = auxIES[j][k]
                                else:
                                    auxIES[j][k] = auxIES[j360-j][k]                           
                        
                            #print("indexC: " + str(auxCIndex[j]))
                            #print("jindex: " + str(jindex))
                            #print(str(j) + ": auxIES:")
                            #print(auxIES[j]) 
                    else:                                                                       # Cmax = 360
                        pass


                    #print(auxIES)

                # interpolation equation apply

                #print("preRotationIESCSize: " + str(preRotationIESCSize))
                #print("preRotationIESGammaSize: " + str(preRotationIESGammaSize))
                for j in range(preRotationIESCSize):
                    wantedC = j * self.StepC
                    for k in range(preRotationIESGammaSize):
                        wantedGamma = k * self.StepGamma                        
                        if(rawCFSO == 0):                                                       # C = 0 case

                            if(wantedGamma not in auxGammaIndex):
                                # look for near index
                                nearOverGammaIndex = 0
                                for l in range(auxIESGammaSize):
                                    if(auxGammaIndex[l]>wantedGamma):
                                        nearOverGammaIndex = l
                                        break
                                m = (auxIES[0][nearOverGammaIndex] - auxIES[0][nearOverGammaIndex-1])/(auxGammaIndex[nearOverGammaIndex]-auxGammaIndex[nearOverGammaIndex-1])
                                preRotationIES[j][k] =  (m * (wantedGamma-auxGammaIndex[nearOverGammaIndex-1])) + auxIES[0][nearOverGammaIndex-1]
                            else:

                                # look for k index
                                for l in range(auxIESGammaSize):
                                    if(auxGammaIndex[l]==wantedGamma):
                                        nearOverGammaIndex = l
                                        break
                                preRotationIES[j][k] = auxIES[0][nearOverGammaIndex]

                        elif wantedGamma in auxGammaIndex and wantedC in auxCIndex:               # Default case, Interpolation don't needed             
                            #print("wantedGamma: " + str(wantedGamma))
                            #print("wantedC: " + str(wantedC))

                            # look for j index
                            for l in range(auxIESCSize):
                                if(auxCIndex[l]==wantedC):
                                    nearOverCIndex = l
                                    break
                            # look for k index
                            for l in range(auxIESGammaSize):
                                if(auxGammaIndex[l]==wantedGamma):
                                    nearOverGammaIndex = l
                                    break

                            preRotationIES[j][k] = auxIES[nearOverCIndex][nearOverGammaIndex]
                        elif(wantedGamma not in auxGammaIndex and wantedC in auxCIndex):
                            # look for j index
                            for l in range(auxIESCSize):
                                if(auxCIndex[l]==wantedC):
                                    nearOverCIndex = l
                                    break

                            # look for near index
                            nearOverGammaIndex = 0
                            for l in range(auxIESGammaSize):
                                if(auxGammaIndex[l]>wantedGamma):
                                    nearOverGammaIndex = l
                                    break
                            m = (auxIES[nearOverCIndex][nearOverGammaIndex] - auxIES[nearOverCIndex][nearOverGammaIndex-1])/(auxGammaIndex[nearOverGammaIndex]-auxGammaIndex[nearOverGammaIndex-1])
                            preRotationIES[j][k] =  (m * (wantedGamma-auxGammaIndex[nearOverGammaIndex-1])) + auxIES[nearOverCIndex][nearOverGammaIndex-1]
                        
                        elif(wantedGamma in auxGammaIndex and wantedC not in auxCIndex):
                            # look for k index
                            for l in range(auxIESGammaSize):
                                if(auxGammaIndex[l]==wantedGamma):
                                    nearOverGammaIndex = l
                                    break

                            # look for near index
                            nearOverCIndex = 0
                            for l in range(auxIESCSize):
                                if(auxCIndex[l]>wantedC):
                                    nearOverCIndex = l
                                    break
                            m = (auxIES[nearOverCIndex][nearOverGammaIndex] - auxIES[nearOverCIndex-1][nearOverGammaIndex])/(auxCIndex[nearOverCIndex]-auxCIndex[nearOverCIndex-1])
                            preRotationIES[j][k] =  (m * (wantedC-auxCIndex[nearOverCIndex-1])) + auxIES[nearOverCIndex-1][nearOverGammaIndex]

                        else:                                                                      # 2D Interpolation
                            # look for near index
                            nearOverGammaIndex = 0
                            for l in range(auxIESGammaSize):
                                if(auxGammaIndex[l]>wantedGamma):
                                    nearOverGammaIndex = l
                                    break
                            nearOverCIndex = 0
                            for l in range(auxIESCSize):
                                if(auxCIndex[l]>wantedC):
                                    nearOverCIndex = l
                                    break 
                            GammaO = auxGammaIndex[nearOverGammaIndex-1]   
                            GammaF = auxGammaIndex[nearOverGammaIndex]
                            CO = auxCIndex[nearOverCIndex-1]
                            CF = auxCIndex[nearOverCIndex]
                            GammaOx = nearOverGammaIndex-1   
                            GammaFx = nearOverGammaIndex
                            COx = nearOverCIndex-1
                            CFx = nearOverCIndex    

                            # Calculation 
                            

                            m1 = (auxIES[COx][GammaFx] - auxIES[COx][GammaOx])/(GammaF-GammaO)
                            IGiCO =  (m1 * (wantedGamma-GammaO)) + auxIES[COx][GammaOx]

                            m2 = (auxIES[CFx][GammaFx] - auxIES[CFx][GammaOx])/(GammaF-GammaO)
                            IGiCF =  (m1 * (wantedGamma-GammaO)) + auxIES[CFx][GammaOx]

                            m = (IGiCF - IGiCO)/(CF-CO)
                            preRotationIES[j][k] =  (m * (wantedC-CO)) + IGiCO

                # User Rotation:
                 
                #print("rotationAngle: " + str(rotationAngle))
                                                                  
                if(rotationAngle == 0):
                    IES=preRotationIES
                else:
                    
                    preRotationIESCIndex = np.zeros((preRotationIESCSize))
                    for i in range(preRotationIESCSize):
                        preRotationIESCIndex[i] = i*self.StepC
                    IES =  np.zeros((preRotationIESCSize, preRotationIESGammaSize))
                    
                    for i in range(preRotationIESCSize-1):
                        wantedC = (i * self.StepC) + rotationAngle
                        if wantedC < 0: wantedC += 360
                        if wantedC >= 360: wantedC -= wantedC
                        #print("wantedC: " + str(wantedC))
                        if ((wantedC/self.StepC) in preRotationIESCIndex):
                            for j in range(preRotationIESGammaSize):
                                IES[i][j] = preRotationIES[(int(wantedC/self.StepC))][j]
                        else:
                            #print("OUT OF RANGE")
                            for j in range(preRotationIESCSize):
                                if(preRotationIESCIndex[j]>wantedC):
                                    nearOverCIndex = j
                                    break
                            
                            for j in range(preRotationIESGammaSize):
                                IES[i][j] = preRotationIES[nearOverCIndex-1][j] + ( ( (preRotationIES[nearOverCIndex][j]-preRotationIES[nearOverCIndex-1][j]) / (self.StepC) ) * (wantedC-((nearOverCIndex-1)*self.StepC)) )  


                    IES[preRotationIESCSize-1] = preRotationIES[0]
                                                
                self.IES = IES

                #print("preRotationIES: ")
                #for i in range(preRotationIESCSize):
                #    print(str(preRotationIES[i]))
                #print("IES: ")
                #for i in range(preRotationIESCSize):
                #    print(str(IES[i]))
                
                


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


    def getstepGammaCeL(self):
        # floor and ceil
        CL=self.CeL/self.StepC
        self.CL=CL
        self.CfL=np.floor(self.CL)
        self.CcL=np.ceil(self.CL)
        yL=self.GammaL/self.StepGamma
        self.yL=yL
        self.yfL=np.floor(self.yL)
        self.ycL=np.ceil(self.yL)
        
        #print("yL")
        #print(self.yL)        
        #print("yfl")
        #print(self.yfL)
        #print("ycL")
        #print(self.ycL)
    
    # luminance
    
    def luminanceFirstStep(self):
        IL = np.zeros((self.Nlum, self.N, 3*self.roadLanes))
        eq3 = np.zeros((self.N, 3*self.roadLanes))
        eq4 = np.zeros((self.N, 3*self.roadLanes))
        #print(IL)
        #print("luminanceFirstStep")
        #print("Ln: " + str(3*self.roadLanes))
        #print("N: " + str(self.N))
        #print("Nlum: " + str(self.Nlum))
        #print("IL shape: ")
        #print(IL.shape)

        #print("eq3 shape: ")
        #print(eq3.shape)
        #print(len(eq3[0]))

        #print("IES shape: ")
        #print(self.IES.shape)

        #print("yfL shape: ")
        #print(self.yfL.shape)
        #print(self.yfL)

        
        for i in range(self.Nlum):
            for j in range(self.N):
                for k in range(3*self.roadLanes):
                    
                    eq3[j][k]=self.IES[int(self.CfL[i][j][k])][int(self.yfL[i][j][k])]+((self.CL[i][j][k]-self.CfL[i][j][k])/(self.CcL[i][j][k]-self.CfL[i][j][k]))*(self.IES[int(self.CcL[i][j][k])][int(self.yfL[i][j][k])]-self.IES[int(self.CfL[i][j][k])][int(self.yfL[i][j][k])])
                    eq4[j][k]=self.IES[int(self.CfL[i][j][k])][int(self.ycL[i][j][k])]+((self.CL[i][j][k]-self.CfL[i][j][k])/(self.CcL[i][j][k]-self.CfL[i][j][k]))*(self.IES[int(self.CcL[i][j][k])][int(self.ycL[i][j][k])]-self.IES[int(self.CfL[i][j][k])][int(self.ycL[i][j][k])])
                    IL[i][j][k]=eq3[j][k]+((self.yL[i][j][k]-self.yfL[i][j][k])/(self.ycL[i][j][k]-self.yfL[i][j][k]))*(eq4[j][k]-eq3[j][k])
                    c = self.IES[int(self.CfL[i][j][k])][int(self.yfL[i][j][k])]
                    
                    #print("i: " + str(i) + ", j: " + str(j)+ ", k: " + str(k) + ", C: " + str(int(self.CfL[i][j][k])) + ", Y: " + str(int(self.yfL[i][j][k])) + ",IL: " +  str(IL[i][j][k]) + ", eq3: " + str(eq3[j][k]) + ", eq4: " + str(eq4[j][k]) + ", c: " + str(c))      
        
        #print("Il")
        #print(IL.shape)
        #print(IL) 
        
        Illuminance = np.zeros((self.N, 3*self.roadLanes))
        
        
        for i in range(self.N):
            for j in range(3*self.roadLanes):
                for k in range(self.Nlum):
                    Illuminance[i][j] += IL[k][i][j]*pow(np.cos(self.GammaL[k][i][j]*np.pi/180),3)

        #ThIncrementIlluminance = Illuminance * self.Fm / pow(self.luminairesHeight-1.5,2)     
        Illuminance = Illuminance * self.Fm / pow(self.luminairesHeight,2)

        
        
        Emax=np.max(Illuminance);
        Emax=np.max(Emax)
        
        self.IL = IL
        Emin=np.min(Illuminance);
        Emin=np.min(Emin)
        Eav=np.mean(Illuminance);
        Eav=np.mean(Eav)
        g1=Emin/Eav
        g2=Emin/Emax
        g3=Eav/Emax

        self.Illuminance = Illuminance
        #self.ThIncrementIlluminance = ThIncrementIlluminance
        self.Emax = Emax
        self.Emin = Emin
        self.Eav = Eav
        self.g1 = g1
        self.g2 = g2
        self.g3 = g3
        #print("Illuminance")
        #print(Illuminance)
        #print("Emax: "+str(Emax))
        #print("Emin, : "+str(Emin))
        #print("Eav, : "+str(Eav))
        #print("g1, : "+str(g1))
        #print("g2, : "+str(g2))
        #print("g3, : "+str(g3))
        
    def luminanceSecondStep(self):
        # Observer
        Ox = np.zeros((self.roadLanes))
        Oy = np.zeros((self.roadLanes))
        Oz = np.zeros((self.roadLanes))
        for i in range(self.roadLanes):
            Ox[i] = -60
            Oz[i] = 1.5
            Oy[i] = self.Py[0][1+(3*i)]
        #print(Oy)

        #C en grados

        Beta = np.zeros((self.roadLanes,self.Nlum,self.N, 3*self.roadLanes))
        for i in range(self.roadLanes):
            for j in range(self.Nlum):
                for k in range(self.N):
                    for l in range(3*self.roadLanes):
                        if(j < self.Nlumback+1):
                            if(self.Py[k][l] == Oy[i]):
                                Beta[i][j][k][l] = 180 - self.CeL[j][k][l]
                            elif(self.Py[k][l] < Oy[i]):
                                Beta[i][j][k][l]=180-(np.arctan((Oy[i]-self.Py[k][l])/(self.Px[k][l]-Ox[i]))*180/np.pi)- self.CeL[j][k][l]
                            else:
                                Beta[i][j][k][l]=180-(45-(np.arctan((self.Py[k][l]-Oy[i])/(self.Px[k][l]-Ox[i]))*180/np.pi))-(self.CeL[j][k][l]-45)
                        else:
                            if(self.Py[k][l] == Oy[i]):
                                Beta[i][j][k][l] = 180 - self.CeL[j][k][l]
                            elif(self.Py[k][l] < Oy[i]):

                                if (180-(np.arctan((Oy[i]-self.Py[k][l])/(self.Px[k][l]-Ox[i]))*180/np.pi)-self.CeL[j][k][l]>=0):
                                    Beta[i][j][k][l]=180-(np.arctan((Oy[i]-self.Py[k][l])/(self.Px[k][l]-Ox[i]))*180/np.pi)-self.CeL[j][k][l]
                                else:
                                    Beta[i][j][k][l]=np.abs(180-(np.arctan((Oy[i]-self.Py[k][l])/(self.Px[k][l]-Ox[i]))*180/np.pi)-self.CeL[j][k][l])

                                #print("TODO")
                                #Beta[i][j][k][l]=180-(np.arctan((Oy[i]-self.Py[k][l])/(self.Px[k][l]-Ox[i]))*180/np.pi)- self.CeL[j][k][l]

                                
                            else:
                                Beta[i][j][k][l]=180-(180-90-(np.arctan((self.Py[k][l]-Oy[i])/(self.Px[k][l]-Ox[i]))*180/np.pi))-(self.CeL[j][k][l]-90);
        #print("BETA")
        #print(Beta)
        
        tanG=np.tan(self.GammaL*np.pi/180)

        B = np.zeros((self.roadLanes,self.Nlum,self.N, 3*self.roadLanes))

        for i in range(self.roadLanes):
            for j in range(self.Nlum):
                for k in range(self.N):
                    for l in range(3*self.roadLanes):
                        if(Beta[i][j][k][l]<=2):
                            B[i][j][k][l]=Beta[i][j][k][l]/2

                        elif (Beta[i][j][k][l]<=45):
                            B[i][j][k][l]=Beta[i][j][k][l]/5+1

                        elif (Beta[i][j][k][l]<180):
                            B[i][j][k][l]=Beta[i][j][k][l]/15+7

                        else: 
                            B[i][j][k][l]=19



        tG = np.zeros((self.Nlum,self.N, 3*self.roadLanes))

        for i in range(self.Nlum):
            for j in range(self.N):
                for k in range(3*self.roadLanes):
                    if(tanG[i][j][k] <= 2):
                        tG[i][j][k]=tanG[i][j][k]/0.25
                    elif(tanG[i][j][k] <= 12):
                        tG[i][j][k]=tanG[i][j][k]/0.5+4
                    else:
                        tG[i][j][k]=28
        
        self.B = B 
        self.Bf=np.floor(self.B)
        self.Bc=np.ceil(self.B)
        self.tG=tG
        self.tGf=np.floor(self.tG)
        self.tGc=np.ceil(self.tG)
        self.Ox = Ox
        self.Oy = Oy
        self.Oz = Oz

        #print("B:")
        #print(self.B)
        #print("Bf:")
        #print(self.Bf)
        #print("Bc:")
        #print(self.Bc)
        #print("tG:")
        #print(self.tG)
        #print("tGf:")
        #print(self.tGf)
        #print("tGc:")
        #print(self.tGc)

    def luminanceThirdStep(self):
        
        # load R matrix

        R = np.loadtxt("t.txt")
        # Beta Interpolation
        R1 = np.zeros((self.roadLanes,self.Nlum,self.N, 3*self.roadLanes))
        eq3 = np.zeros((self.N, 3*self.roadLanes))
        eq4 = np.zeros((self.N, 3*self.roadLanes))
        #print("R: ")
        #print(R)
        #print("Rtype: " +  str(R.shape))
        for i in range(self.roadLanes):
            for j in range(self.Nlum):
                for k in range(self.N):
                    for l in range(3*self.roadLanes):


                        if(self.Bc[i][j][k][l] == self.Bf[i][j][k][l]):

                            R1[i][j][k][l] = R[int(self.tG[j][k][l])][int(self.B[i][j][k][l])]

                        else:
                            eq3[k][l]=R[int(self.tGf[j][k][l])][int(self.Bf[i][j][k][l])]+((self.B[i][j][k][l]-self.Bf[i][j][k][l])/(self.Bc[i][j][k][l]-self.Bf[i][j][k][l]))*(R[int(self.tGf[j][k][l])][int(self.Bc[i][j][k][l])]-R[int(self.tGf[j][k][l])][int(self.Bf[i][j][k][l])])
                            eq4[k][l]=R[int(self.tGc[j][k][l])][int(self.Bf[i][j][k][l])]+((self.B[i][j][k][l]-self.Bf[i][j][k][l])/(self.Bc[i][j][k][l]-self.Bf[i][j][k][l]))*(R[int(self.tGc[j][k][l])][int(self.Bc[i][j][k][l])]-R[int(self.tGc[j][k][l])][int(self.Bf[i][j][k][l])])
                        
                            if(not (self.tGc[j][k][l] == self.tGf[j][k][l])):
                            
                                R1[i][j][k][l]= eq3[k][l]+((self.tG[j][k][l]-self.tGf[j][k][l])/(self.tGc[j][k][l]-self.tGf[j][k][l]))*(eq4[k][l]-eq3[k][l])                       
                            else:
                                R1[i][j][k][l] = 0

                        #print("i: " + str(i) + ", j: " + str(j) + ", k: " + str(k) + ", l: " + str(l) + ", eq3: " +  str(eq3[k][l]) + ", eq4: " +  str(eq4[k][l]) + ", R1: " + str(R1[i][j][k][l]))

                        

        luminance = np.zeros((self.roadLanes,self.N, 3*self.roadLanes))
        #print(R1)
        for i in range(self.roadLanes):
            for j in range(self.Nlum):        
                for k in range(self.N):
                    for l in range(3*self.roadLanes):
                        luminance[i][k][l] += self.IL[j][k][l]*R1[i][j][k][l]

        luminance=luminance*0.0001*self.Fm/pow(self.luminairesHeight,2)

        Lmax = np.zeros((self.roadLanes))
        Lmin = np.zeros((self.roadLanes))
        Lav = np.zeros((self.roadLanes))

        for i in range(self.roadLanes):

            Lmax[i]=np.max(luminance[i])
            Lmin[i]=np.min(luminance[i])
            Lav[i]=np.mean(luminance[i])

        self.Lmax = Lmax
        self.Lmin = Lmin
        self.Lav = Lav
        self.luminance = luminance
        
        #print("luminance:" + str(luminance))
        #print("Lmax: " + str(Lmax))
        #print("Lmin: " + str(Lmin))
        #print("Lav: " + str(Lav))

    def luminanceFourthStep(self):
        #GammaCL
        Nlumback = 0
        Nlumfor=int((12*(self.luminairesHeight-1.5))/self.luminairesBetweenDistance)+1
        Nlum=Nlumback+Nlumfor+1
        print("Nlum:"+str(Nlum))
        print("Nlumfor:"+str(Nlumfor))
        Ly = [0 for i in range(Nlum)]
        Lx = [0 for i in range(Nlum)]

        for i in range(Nlum):    
            Lx[i] = -(Nlumback-i)*self.luminairesBetweenDistance
            Ly[i] = 0
        

        print("Lx" + str(Lx))
        #print("self.Py")
        #print(self.Py)


        CeL = np.zeros((Nlum, self.N, 3*self.roadLanes))
        GammaL = np.zeros((Nlum, self.N, 3*self.roadLanes))

        for i in range(Nlum):
            for j in range(self.N):
                for k in range(3*self.roadLanes):      

                    CeL[i][j][k] = math.atan((self.Py[j][k]-Ly[i])/(self.Px[j][k]-Lx[i]))*(180/math.pi)
                    GammaL[i][j][k]=math.atan((math.sqrt(math.pow(self.Px[j][k]-Lx[i],2)+math.pow(self.Py[j][k]-Ly[i],2))/(self.luminairesHeight-1.5)))*(180/math.pi)
                    if(i>Nlumback):
                        CeL[i][j][k] += 180


        CL=CeL/self.StepC
        CfL=np.floor(CL)
        CcL=np.ceil(CL)
        yL=GammaL/self.StepGamma
        yfL=np.floor(yL)
        ycL=np.ceil(yL)


        # luminance firstStep

        IL = np.zeros((Nlum, self.N, 3*self.roadLanes))
        eq3 = np.zeros((self.N, 3*self.roadLanes))
        eq4 = np.zeros((self.N, 3*self.roadLanes))
        #print(IL)
        #print("luminanceFirstStep")
        #print("Ln: " + str(3*self.roadLanes))
        #print("N: " + str(self.N))
        #print("Nlum: " + str(Nlum))
        #print("IL shape: ")
        #print(IL.shape)

        #print("eq3 shape: ")
        #print(eq3.shape)
        #print(len(eq3[0]))

        #print("IES shape: ")
        #print(self.IES.shape)

        #print("yfL shape: ")
        #print(self.yfL.shape)
        #print(self.yfL)

        print("Nlum: " + str(Nlum))
        print("N: " + str(self.N))
        print("3XroadLanes: " + str(3*self.roadLanes))
        
        for i in range(Nlum):
            for j in range(self.N):
                for k in range(3*self.roadLanes):
                    
                    eq3[j][k]=self.IES[int(CfL[i][j][k])][int(yfL[i][j][k])]+((CL[i][j][k]-CfL[i][j][k])/(CcL[i][j][k]-CfL[i][j][k]))*(self.IES[int(CcL[i][j][k])][int(yfL[i][j][k])]-self.IES[int(CfL[i][j][k])][int(yfL[i][j][k])])
                    eq4[j][k]=self.IES[int(CfL[i][j][k])][int(ycL[i][j][k])]+((CL[i][j][k]-CfL[i][j][k])/(CcL[i][j][k]-CfL[i][j][k]))*(self.IES[int(CcL[i][j][k])][int(ycL[i][j][k])]-self.IES[int(CfL[i][j][k])][int(ycL[i][j][k])])
                    IL[i][j][k]=eq3[j][k]+((yL[i][j][k]-yfL[i][j][k])/(ycL[i][j][k]-yfL[i][j][k]))*(eq4[j][k]-eq3[j][k])
                    # c = self.IES[int(CfL[i][j][k])][int(yfL[i][j][k])]
                    
                    #print("i: " + str(i) + ", j: " + str(j)+ ", k: " + str(k) + ", C: " + str(int(self.CfL[i][j][k])) + ", Y: " + str(int(self.yfL[i][j][k])) + ",IL: " +  str(IL[i][j][k]) + ", eq3: " + str(eq3[j][k]) + ", eq4: " + str(eq4[j][k]) + ", c: " + str(c))      
        
        #print("Il")
        #print(IL.shape)
        #print(IL) 
        
        Illuminance = np.zeros((self.N, 3*self.roadLanes))
        Ek = np.zeros((Nlum))
        for k in range(Nlum):
            for i in range(self.N):
                for j in range(3*self.roadLanes):
                
                    Illuminance[i][j] += IL[k][i][j]*pow(np.cos(GammaL[k][i][j]*np.pi/180),3)
            
            ThIncrementIlluminance = Illuminance * self.Fm / pow(self.luminairesHeight-1.5,2)     
            Ek[k] = np.average(ThIncrementIlluminance[i][j])



        # thetaK:
        driverAge = 23
        thetaK = np.zeros((self.roadLanes, self.Nlum))
        for i in range(self.roadLanes):
            for j in range(Nlum):
                thetaK[i][j] = (180/np.pi)*np.arccos(((Lx[j]-self.Ox[i])*np.cos(-1*np.pi/180)+ ((self.luminairesHeight-1.5)-self.Oz[i])*np.sin(-1*np.pi/180))/( math.sqrt(pow(Lx[j]-self.Ox[i],2)+pow(Ly[j]-self.Oy[i],2)+pow((self.luminairesHeight-1.5)-self.Oz[i],2)) ))
       

        LV = np.zeros((self.roadLanes))

        for i in range(self.roadLanes):
            for j in range(Nlum):

                if thetaK[i][j]<60 and 1.5<=thetaK[i][j]:
                    LV[i] += 9.86 * pow(1+(driverAge/66.4),4) * Ek[j]/pow(thetaK[i][j],2)

                elif thetaK[i][j]<1.5 and 0.1<=thetaK[i][j]:
                    LV[i] += 5 * pow(1+(driverAge/62.5),4) * Ek[j]/pow(thetaK[i][j],2)+10*Ek[j]/pow(thetaK[i][j],3)

        
        fTI = np.zeros((self.roadLanes))
        self.Lav
        for i in range(self.roadLanes):
            if self.Lav[i]<=5:
                fTI[i] = 65*LV[i]/(0.8*self.Lav[i])

            elif self.Lav[i] >5:
                fTI[i] = 95*LV[i]/(1.05*self.Lav[i])
            
        
        
        print("Ek: ")
        print(Ek)
        
        print("thetaK: ")
        print(thetaK)

        print("LV: ")
        print(LV)

        print("fTI: ")
        print(fTI)

    # Extras
    def printData(self):
        print("Px: ")
        print(self.Px)
        print("Py: ")
        print(self.Py)

        print("------------------------------------")
        print("luminance:" + str(self.luminance))
        print("Lmax: " + str(self.Lmax))
        print("Lmin: " + str(self.Lmin))
        print("Lav: " + str(self.Lav))
    
        print("------------------------------------")
        print("Illuminance:" + str(self.Illuminance))
        print("Emax: " + str(self.Emax))
        print("Emin: " + str(self.Emin))
        print("Eav: " + str(self.Eav))


def main():

    test = LuminanceCalculator(IESroute="Sit1.ies", luminairesHeight = 4, luminairesBetweenDistance = 20, roadWidth = 10, roadLanes=2, luminairesRotation = 0, luminariesOverhang = 0, luminariesDistribution = 0, Fm= 0.5)

    test.printData()





if __name__ == '__main__':
    main()
        
