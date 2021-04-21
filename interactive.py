import tkinter as tk
import math
# pip install pillow
from PIL import Image, ImageTk

class illuminancePictureFrame(tk.Frame):

    def __init__(self):
        self.initVariables()             
        self.initUI()
        self.initEvents()
        
    
    def initEvents(self):
        # Presionar en
        self.myCanvas.bind("<Button-1>",self.markArea)

    def initVariables(self):
        self.widowsSizeX=800
        self.widowsSizeY=800

        #Offset del centro de la grilla de la imagen
        self.gridCenterOffsetX = -2
        self.gridCenterOffsetY = 0
        #Datos de los circulos
        super().__init__(width=800, height=800)
        self.circleQuantity = 5
        self.circleSize = 250
        self.interiorCircleRadius = 50
        self.circlesRadiusArray = [0 for i in range(50)]

        # Estructura de datos con los circulos a dibujar
        self.circles = [[None for i in range(12)] for j in range(50)]
        # Estructura de datos con las rectas a dibujar
        self.lines = []
        # Estructura de datos con los indicadores de areas
        self.areaIndicators = []

        # Matriz con la informacion de cada area
        # [anillo][arco], [radio][radianes]
        self.areaMatrix = [[None for i in range(12)] for j in range(50)]

        # Distribución lineal de los radios:
        for i in range(self.circleQuantity):
            self.circlesRadiusArray[i]=self.interiorCircleRadius + (i*((self.circleSize-self.interiorCircleRadius)/self.circleQuantity))


    def initUI(self):
        # Canvas para dibujo de circulos

        self.myCanvas = tk.Canvas(self, width=self.widowsSizeX, height=self.widowsSizeY, borderwidth=0, highlightthickness=0, )

        # Cargar imagen:

        tunnelImage = Image.open("image.jpg")
        size = self.widowsSizeX, (int)((self.widowsSizeX/16)*9)
        tunnelImage = tunnelImage.resize(size, Image.ANTIALIAS)    
        self.renderedTunnelImage = ImageTk.PhotoImage(tunnelImage)
        
        # Dibujar Imagen        

        imagePositionX = self.widowsSizeX/2
        imagePositionY = self.widowsSizeY/2
        self.canvasImage =self.myCanvas.create_image( imagePositionX, imagePositionY, image=self.renderedTunnelImage)


        # Dibujar circulos:
        
        for i in range(self.circleQuantity):
            self.circles.append(self.create_circle(self.widowsSizeX/2 + self.gridCenterOffsetX, self.widowsSizeY/2 + self.gridCenterOffsetY,self.circlesRadiusArray[self.circleQuantity-i-1],self.myCanvas))
        # Dibujar rectas
        for i in range(6):
            R =self.circlesRadiusArray[self.circleQuantity-1]
            x = R*math.cos(i*(math.pi/6))
            y = R*math.sin(i*(math.pi/6))
            x1= self.widowsSizeX/2 + self.gridCenterOffsetX + x
            y1= self.widowsSizeY/2 + self.gridCenterOffsetX + y
            x2= self.widowsSizeX/2 + self.gridCenterOffsetX - x
            y2= self.widowsSizeY/2 + self.gridCenterOffsetX - y
            self.lines.append(self.myCanvas.create_line(x1, y1, x2, y2 ,width=2, fill = "white"))       
        

        self.myCanvas.place(x = self.winfo_rootx(), y=self.winfo_rooty())
        self.myCanvas.pack()
       
    # CallBacks:
    def doSomething(self,event):
        print("test mouse")
        print(event.x)
        print(event.y)


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
            for i in range(12):
                if(Theta<((12-i)*(math.pi/6))):
                    ThetaRegion=11-i

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
                ThetaPos=(math.pi/6)/2
            else:
                ThetaPos=(((ThetaRegion+1)*(math.pi/6)-((ThetaRegion)*(math.pi/6)))/2) + ((ThetaRegion)*(math.pi/6))

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
            print("tamaño: " + str(len(self.circles)))
            
            if self.circles[rRegion][ThetaRegion] is None:  
                self.circles[rRegion][ThetaRegion]=(self.create_circle(xPos, yPos, 5, self.myCanvas))
            else:
                self.myCanvas.delete(self.circles[rRegion][ThetaRegion])
                self.circles[rRegion][ThetaRegion]=None
                #self.circles[rRegion][ThetaRegion]=(self.create_circle(xPos, yPos, 5, self.myCanvas))
            #self.myCanvas.pack()






    # Funciones auxiliares
    def create_circle(self,x, y, r, canvasName): #center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvasName.create_oval(x0, y0, x1, y1, width=2, outline = "green")


class Application(tk.Frame):
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.master.title("Lux Tunnel")

        for r in range(6):
            self.master.rowconfigure(r, weight=1)    
        for c in range(5):
            self.master.columnconfigure(c, weight=1)
            tk.Button(master, text="Button {0}".format(c)).grid(row=6,column=c,sticky=tk.E+tk.W)

        #Frame importante
        Frame1 = illuminancePictureFrame()
        Frame1.grid( row = 0, column = 0,rowspan = 3, columnspan = 2, sticky = tk.W+tk.E+tk.N+tk.S)

        
        Frame2 = tk.Frame(master, bg="blue")
        Frame2.grid(row = 3, column = 0, rowspan = 3, columnspan = 2, sticky = tk.W+tk.E+tk.N+tk.S)
        Frame3 = tk.Frame(master, bg="green")
        Frame3.grid(row = 0, column = 2, rowspan = 6, columnspan = 3, sticky = tk.W+tk.E+tk.N+tk.S)
  



def main():

    root = tk.Tk()
    root.geometry("1280x720")

    app = Application(master=root)
    app.mainloop()
  

if __name__ == '__main__':
    main()