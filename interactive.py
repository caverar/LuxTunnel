import tkinter as tk

class illuminancePictureFrame(tk.Frame):

    def __init__(self):
        super().__init__()
        



        self.widowsSizeX=600
        self.widowsSizeY=600
        self.circleQuantity = 5
        self.circleSize = 250
        self.interiorCircleRadius = 50
        self.circlesRadiusArray = [0,0,0,0,0,0,0,0,0,0,0]
        
        # Distribución lineal de los radios:

        for i in range(self.circleQuantity):
            self.circlesRadiusArray[i]=self.interiorCircleRadius + (i*((self.circleSize-self.interiorCircleRadius)/self.circleQuantity))
            print(self.circlesRadiusArray[i])


        self.initUI()



    def initUI(self):
        #self.master.title("Test de figuras")
        
        #self.pack(fill=tk.BOTH, expand=1)
        #self.bg="red"

        canvas = tk.Canvas(self)
        

        canvas=tk.Canvas( width=self.widowsSizeX, height=self.widowsSizeY, borderwidth=0, highlightthickness=0, bg="white")
        
        #self.create_circle(300, 300, 200, "yellow",canvas)
        #self.create_circle(300, 300, 20, "red",canvas)
        #self.create_circle(50, 25, 10, canvas)

        
        for i in range(self.circleQuantity):
            self.create_circle(self.widowsSizeX/2, self.widowsSizeY/2 ,self.circlesRadiusArray[self.circleQuantity-i],canvas )
        
        
        #canvas.pack(fill=tk.BOTH, expand=1)
        
        canvas.grid(row = 0, column = 0)
        

 
       


    def create_circle(self,x, y, r, canvasName): #center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvasName.create_oval(x0, y0, x1, y1)


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

        Frame1 = illuminancePictureFrame()
        Frame1.grid(row = 0, column = 0,rowspan = 3,columnspan = 2, sticky = tk.W+tk.E+tk.N+tk.S)

        #Frame1 = tk.Frame(master, bg="red")
        #Frame1.grid(row = 0, column = 0, rowspan = 3, columnspan = 2, sticky = tk.W+tk.E+tk.N+tk.S) 
        
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