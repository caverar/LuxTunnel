import tkinter as tk
from tkinter import messagebox as mb
import math
from tkinter.constants import CURRENT
# pip install pillow
from PIL import Image, ImageTk

class illuminancePictureFrame(tk.Frame):

    def __init__(self, widowsSizeX = 800, widowsSizeY = 600):
        self.initVariables(widowsSizeX = widowsSizeX, widowsSizeY = widowsSizeY)             
        self.initUI()
        
    def initSelectionEvents(self):

        if self.binder != None:
            self.myCanvas.unbind("<Button-1>",self.binder)
        self.binder= self.myCanvas.bind("<Button-1>",self.markArea)        
        
    def initVariables(self, widowsSizeX = 800, widowsSizeY = 600):

        self.binder = None              # Gestor de eventos

        self.currentMaterial = 0        # Materiales: 0,1,2,3,4,5,6
        self.materialColor = ["blue","red","orange","yellow","white","green", "purple"]
        
        # Cielo: Azul
        # Calzada: rojo
        # Rocas: naranja
        # Edificios: Amarillo
        # Nieve: Blanco
        # Vegetacion: Verde
        # Túnel: Violeta

        self.widowsSizeX=widowsSizeX
        self.widowsSizeY=widowsSizeY

        #Offset del centro de la grilla de la imagen
        self.gridCenterOffsetX = 0
        self.gridCenterOffsetY = 0
        #Datos de los circulos
        super().__init__(width=800, height=800)
        self.circleQuantity = 5
        self.halfAngleQuantity = 6 
        self.circleSize = 225
        self.interiorCircleRadius = 50
        self.circlesRadiusArray = [0 for i in range(50)]

        # Estructura de datos con los circulos a dibujar
        self.circles = [None for i in range(50)]
        # Estructura de datos con las rectas a dibujar
        self.lines = [None for i in range(30)]
        # Estructura de datos con los indicadores de areas
        self.areaIndicators =  [[None for i in range(50)] for j in range(50)]

        # Matriz con la informacion de cada area
        # [anillo][arco], [radio][radianes]
        self.areaMatrix = [[None for i in range(50)] for j in range(50)]

        self.renderedTunnelImage = None

    def initUI(self):
        # Canvas para dibujo de círculos

        self.myCanvas = tk.Canvas(self, width=self.widowsSizeX, height=self.widowsSizeY, borderwidth=0, highlightthickness=0,background="black" )

        self.loadImage("L20DefaultImage.jpg",escalate=True)

        self.drawImage()
        #self.drawInnerCircle()
        #self.drawCircles()        
        #self.drawLines()
        #self.initSelectionEvents()

        # Ubicar Canvas
        self.myCanvas.place(x = self.winfo_rootx(), y=self.winfo_rooty())
        self.myCanvas.pack()
        
    def loadImage(self,route="L20DefaultImage.jpg",escalate=False):

        self.route = route
        # Catch_try TODO
        # Cargar imagen:
        tunnelImage = Image.open(route)

        
        # Bloque peligroso, escalado implica errores de distoricion en la imagen

        if(escalate):
            print("ancho: " + str(tunnelImage.width))
            print("altura: " + str(tunnelImage.height))
            
            if(tunnelImage.width<self.widowsSizeX):
                size = self.widowsSizeX,(int)((self.widowsSizeX*tunnelImage.height)/tunnelImage.width)
                tunnelImage = tunnelImage.resize(size, Image.ANTIALIAS)
                print("Imagen pequeña")

            else:
                size = self.widowsSizeX, self.widowsSizeY
                tunnelImage.thumbnail(size,Image.ANTIALIAS)
                print("Imagen grande")
        

        print("ancho: " + str(tunnelImage.width))
        print("altura: " + str(tunnelImage.height))    
        self.renderedTunnelImage = ImageTk.PhotoImage(tunnelImage)

    def drawImage(self):
        # Dibujar Imagen        

        imagePositionX = self.widowsSizeX/2
        imagePositionY = self.widowsSizeY/2
        self.canvasImage =self.myCanvas.create_image( imagePositionX, imagePositionY, image=self.renderedTunnelImage)
    
    def drawInnerCircle(self):
        if(self.circles[0] != None):
            self.myCanvas.delete(self.circles[0])
        self.circles[0] = self.create_circle(self.widowsSizeX/2 + self.gridCenterOffsetX, self.widowsSizeY/2 + self.gridCenterOffsetY,self.interiorCircleRadius, "white" ,self.myCanvas)

    def drawCircles(self):
        # Dibujar circulos:

        # Distribución lineal de los radios:
        for i in range(self.circleQuantity):
            self.circlesRadiusArray[i]=self.interiorCircleRadius + (i*((self.circleSize-self.interiorCircleRadius)/(self.circleQuantity-1)))

        for i in range(self.circleQuantity-1):
            if(self.circles[i+1] != None):
                print(i)
                self.myCanvas.delete(self.circles[i+1])
            self.circles[i+1]=self.create_circle(self.widowsSizeX/2 + self.gridCenterOffsetX, self.widowsSizeY/2 + self.gridCenterOffsetY,self.circlesRadiusArray[i+1], "white",self.myCanvas)
               
    def drawLines(self): 


        # Dibujar rectas

        for i in range(self.halfAngleQuantity):
            R = self.circleSize 
            x = R*math.cos(i*(math.pi/self.halfAngleQuantity))
            y = R*math.sin(i*(math.pi/self.halfAngleQuantity))
            x1= self.widowsSizeX/2 + self.gridCenterOffsetX + x
            y1= self.widowsSizeY/2 + self.gridCenterOffsetY + y
            x2= self.widowsSizeX/2 + self.gridCenterOffsetX - x
            y2= self.widowsSizeY/2 + self.gridCenterOffsetY - y
            if(self.lines[i] != None):
                self.myCanvas.delete(self.lines[i])
            self.lines[i]= (self.myCanvas.create_line(x1, y1, x2, y2 ,width=1, fill = "white")) 

    def clearALL(self):
        self.myCanvas.delete("all")
        # Estructura de datos con los circulos a dibujar
        self.circles = [None for i in range(50)]
        # Estructura de datos con las rectas a dibujar
        self.lines = [None for i in range(30)]
        # Estructura de datos con los indicadores de areas
        self.areaIndicators =  [[None for i in range(50)] for j in range(50)]

        # Matriz con la informacion de cada area
        # [anillo][arco], [radio][radianes]
        self.areaMatrix = [[None for i in range(50)] for j in range(50)]

    # CallBacks:
    def doSomething(self,event):
        print("test mouse")
        print(event.x)
        print(event.y)

    def reset(self, escalate = False):
        self.clearALL()
        if self.binder != None:
            self.myCanvas.unbind("<Button-1>",self.binder)
            self.binder = None
        self.loadImage(self.route,escalate = escalate)
        self.drawImage()

    def firsStep(self , newGridCenterOffsetX=0, newGridCenterOffsetY=0, newInteriorCircleRadius=50, SD=100, entranceRadiusMeters = 5):
        #self.clearALL()
        #self.loadImage(self.route,escalate = False)
        #self.drawImage()

        # Desactivar seleccion de colores
        if self.binder != None:
            self.myCanvas.unbind("<Button-1>",self.binder)
            self.binder = None
            # Desdibujar indicadores de area y sus valores
            for i in range(50):
                for j in range(50):
                    self.areaMatrix[i][j] = None
                    if self.areaIndicators[i][j] != None:
                        self.myCanvas.delete(self.areaIndicators[i][j])
                    self.areaIndicators[i][j] = None


        self.gridCenterOffsetX = newGridCenterOffsetX
        self.gridCenterOffsetY = newGridCenterOffsetY
        self.interiorCircleRadius = newInteriorCircleRadius
        self.circleSize = int( SD * (newInteriorCircleRadius/entranceRadiusMeters) * math.tan(math.pi/18))
        # Primer paso, redibujar el circulo interior para ajustar radio y offset
        self.drawInnerCircle()

    def secondStep(self, newCircleQuantity = 8, newhalfAngleQuantity=12):

        # Desactivar selección de colores
        if self.binder != None:
            self.myCanvas.unbind("<Button-1>",self.binder)
            self.binder = None
            # Desdibujar indicadores de area y sus valores
            for i in range(50):
                for j in range(50):
                    self.areaMatrix[i][j] = None
                    if self.areaIndicators[i][j] != None:
                        self.myCanvas.delete(self.areaIndicators[i][j])
                    self.areaIndicators[i][j] = None
                

        self.circleQuantity = newCircleQuantity
        self.halfAngleQuantity = newhalfAngleQuantity
        self.drawCircles()
        self.drawLines() 

    def thirdStep(self):
        self.initSelectionEvents()

    def markArea(self,event):

        x=(event.x -self.widowsSizeX/2 - self.gridCenterOffsetX)
        y=-(event.y -self.widowsSizeY/2 - self.gridCenterOffsetY)

        # Angulo convencional desde el eje x, de 0 a 2pi

        R=int(math.sqrt(pow(x,2)+pow(y,2)))
        if(R<self.circleSize and R>0):
            if(y==0):
                if(x>0):
                    Theta = 0
                else:
                    Theta = math.pi
            elif(x==0):
                if(y>0):
                    Theta = math.pi/2                    
                else:
                    Theta = 3*(math.pi/2)
            elif(y>0 and x>0):
                Theta=math.atan(abs(y)/abs(x))
            elif(y>0 and x<0):
                Theta=math.atan(abs(x)/abs(y))+(math.pi/2)
            elif(y<0 and x<0):
                Theta=math.atan(abs(y)/abs(x))+(math.pi)
            else:
                Theta=math.atan(abs(x)/abs(y))+(3*(math.pi/2))

            #Region del angulo
            ThetaRegion=0
            for i in range(2*self.halfAngleQuantity):
                if(Theta<(((self.halfAngleQuantity*2)-i)*(math.pi/self.halfAngleQuantity))):
                    ThetaRegion=(2*self.halfAngleQuantity)-1-i

            #Region del radio
            rRegion=0
            for i in range(self.circleQuantity):
                print(self.circlesRadiusArray[self.circleQuantity-i-1])
                if(R<self.circlesRadiusArray[self.circleQuantity-i-1]):
                    rRegion=self.circleQuantity-i-1                

            # Calculo de coordenada de la figura
            print("---------------")
            print("ThetaRegion: " +str(ThetaRegion))
            print("rRegion: " +str(rRegion))

            ThetaPos=0
            RPos=0
            if(ThetaRegion==0):
                ThetaPos=(math.pi/self.halfAngleQuantity)/2
            else:
                ThetaPos=(((ThetaRegion+1)*(math.pi/self.halfAngleQuantity)-((ThetaRegion)*(math.pi/self.halfAngleQuantity)))/2) + ((ThetaRegion)*(math.pi/self.halfAngleQuantity))

            if(rRegion==0):
                RPos=3*((self.circlesRadiusArray[rRegion])/4) 
            else:
                RPos=((self.circlesRadiusArray[rRegion]-self.circlesRadiusArray[rRegion-1])/2) +self.circlesRadiusArray[rRegion-1]

            print("ThetaPos: " +str(ThetaPos))
            print("RPos: " + str(RPos))

            # conversion coordenadas polares a cartesianas
            xPos = (RPos * math.cos(ThetaPos)) + self.widowsSizeX/2 + self.gridCenterOffsetX
            yPos = -(RPos * math.sin(ThetaPos)) + self.widowsSizeY/2 + self.gridCenterOffsetY
            
            # Dibujar figura
            print("tamaño: " + str(len(self.areaIndicators)))  
            
            

            if self.areaIndicators[rRegion][ThetaRegion] is None:  
                
                self.areaIndicators[rRegion][ThetaRegion]=(self.create_circle(xPos, yPos, 5,self.materialColor[self.currentMaterial] ,self.myCanvas))
                self.areaMatrix[rRegion][ThetaRegion] = (self.getArea(rRegion),self.currentMaterial)


            elif self.areaMatrix[rRegion][ThetaRegion][1] != self.currentMaterial:
                self.myCanvas.delete(self.areaIndicators[rRegion][ThetaRegion])
                self.areaIndicators[rRegion][ThetaRegion]=None
                self.areaIndicators[rRegion][ThetaRegion]=(self.create_circle(xPos, yPos, 5,self.materialColor[self.currentMaterial] ,self.myCanvas))
               
                self.areaMatrix[rRegion][ThetaRegion] = (self.getArea(rRegion),self.currentMaterial)                


            else:
                self.myCanvas.delete(self.areaIndicators[rRegion][ThetaRegion])
                self.areaIndicators[rRegion][ThetaRegion]=None
                self.areaMatrix[rRegion][ThetaRegion]= None
                


            #self.myCanvas.pack()

    def selectMaterial(self, newMaterial):
        if self.binder != None:
            self.myCanvas.unbind("<Button-1>",self.binder)
        self.binder= self.myCanvas.bind("<Button-1>",self.markArea) 
        
        self.currentMaterial = newMaterial

    def selectMaterial1(self):
        if self.binder != None:
            self.myCanvas.unbind("<Button-1>",self.binder)
        self.binder= self.myCanvas.bind("<Button-1>",self.markArea) 
        
        if(self.currentMaterial<6):
            self.currentMaterial += 1
        else:
            self.currentMaterial = 0
    
    def fillGrid(self):
        # Desactivar selección de colores
        if self.binder != None:
            self.myCanvas.unbind("<Button-1>",self.binder)
            self.binder = None
        # Desdibujar indicadores de area y sus valores
        for i in range(50):
            for j in range(50):
                self.areaMatrix[i][j] = None
                if self.areaIndicators[i][j] != None:
                    self.myCanvas.delete(self.areaIndicators[i][j])
                self.areaIndicators[i][j] = None


        for i in range(self.circleQuantity):
            for j in range(2*self.halfAngleQuantity):
                ThetaPos=0
                RPos=0
                if(j==0):
                    ThetaPos=(math.pi/self.halfAngleQuantity)/2
                else:
                    ThetaPos=(((j+1)*(math.pi/self.halfAngleQuantity)-((j)*(math.pi/self.halfAngleQuantity)))/2) + ((j)*(math.pi/self.halfAngleQuantity))

                if(i==0):
                    RPos=3*((self.circlesRadiusArray[i])/4) 
                else:
                    RPos=((self.circlesRadiusArray[i]-self.circlesRadiusArray[i-1])/2) +self.circlesRadiusArray[i-1]

                print("ThetaPos: " +str(ThetaPos))
                print("RPos: " + str(RPos))

                # conversion coordenadas polares a cartesianas
                xPos = (RPos * math.cos(ThetaPos)) + self.widowsSizeX/2 + self.gridCenterOffsetX
                yPos = -(RPos * math.sin(ThetaPos)) + self.widowsSizeY/2 + self.gridCenterOffsetY
                
                
                
                self.areaIndicators[i][j]=(self.create_circle(xPos, yPos, 5,self.materialColor[self.currentMaterial] ,self.myCanvas))
               
                self.areaMatrix[i][j] = (self.getArea(i), self.currentMaterial)   

    def getTotalAreas(self, percentageArray = [0 for i in range(7)]):

        partialAreasArray =[0 for i in range(7)]
        
        totalArea = math.pi*pow(self.circleSize,2)

        for i in range(self.circleQuantity):
            for j in range(2*self.halfAngleQuantity):
                if(self.areaMatrix[i][j] != None):
                    partialAreasArray[self.areaMatrix[i][j][1]] += self.areaMatrix[i][j][0]
        
            
        print(totalArea)
        print(partialAreasArray)
        print(int(partialAreasArray[0]+partialAreasArray[1]+partialAreasArray[2]+partialAreasArray[3]+partialAreasArray[4]+partialAreasArray[5]+partialAreasArray[6]))
        print(int(totalArea))

        if(int(totalArea) != int(partialAreasArray[0]+partialAreasArray[1]+partialAreasArray[2]+partialAreasArray[3]+partialAreasArray[4]+partialAreasArray[5]+partialAreasArray[6])):
            print("!ERROR: no ha seleccionado todas las areas")

            mb.showerror("ERROR","Asegúrese de que selecciono todas las áreas de la imagen")
        else:
            percentageArray[0] = partialAreasArray[0]/totalArea
            percentageArray[1] = partialAreasArray[1]/totalArea
            percentageArray[2] = partialAreasArray[2]/totalArea
            percentageArray[3] = partialAreasArray[3]/totalArea
            percentageArray[4] = partialAreasArray[4]/totalArea
            percentageArray[5] = partialAreasArray[5]/totalArea
            percentageArray[6] = partialAreasArray[6]/totalArea

            print("CORRECTO:")
            print(percentageArray)
            print(percentageArray[0]+percentageArray[1]+percentageArray[2]+percentageArray[3]+percentageArray[4]+percentageArray[5]+percentageArray[6])

            return percentageArray

    # Funciones auxiliares
    def getArea(self,rRegion):
        area = 0    
        if(rRegion == 0):
            area = pow(self.circlesRadiusArray[0],2)*((math.pi/self.halfAngleQuantity)/2)
        else:
            area = (pow(self.circlesRadiusArray[rRegion],2)-pow(self.circlesRadiusArray[rRegion-1],2))*((math.pi/self.halfAngleQuantity)/2)
        print("Area: " + str(area))
        return area

    def create_circle(self,x, y, r, color, canvasName): #center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvasName.create_oval(x0, y0, x1, y1, width=1, outline = color)


class Application(tk.Frame):
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.master.title("Lux Tunnel")

        for r in range(6):
            self.master.rowconfigure(r, weight=1)        

        #Frame importante
        Frame1 = illuminancePictureFrame()
        Frame1.grid( row = 0, column = 0,rowspan = 3, columnspan = 6, sticky = tk.W+tk.E+tk.N+tk.S)
        array = [0,0,0,0,0,0,0]
        #Botones
        functions = [None for i in range(6)]
        functions[0] = lambda: Frame1.reset(escalate=True)
        functions[1] = lambda: Frame1.firsStep()
        functions[2] = lambda: Frame1.secondStep()
        functions[3] = lambda: Frame1.fillGrid()
        functions[4] = lambda: Frame1.selectMaterial1()
        functions[5] = lambda: Frame1.getTotalAreas(array)
        names = [None for i in range(6)]
        
        names[0] = "Reiniciar"
        names[1] = "Circulo Interno"
        names[2] = "Grilla"
        names[3] = "llenar grilla" 
        names[4] = "Seleccionar material" 
        names[5] = "Calcular porcentajes" 

        for c in range(6):
            self.master.columnconfigure(c, weight=1)
            tk.Button(master, text=names[c], command=functions[c]).grid(row=6,column=c,sticky=tk.E+tk.W)
        

        # Frames relleno

def main():

    root = tk.Tk()
    root.geometry("1280x720")

    app = Application(master=root)
    app.mainloop()
  

if __name__ == '__main__':
    main()

