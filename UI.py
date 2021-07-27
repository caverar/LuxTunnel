import sys, os
import tkinter as tk

from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog
from tkinter import ttk
import math
from PIL import Image, ImageTk
from illuminancePictureFrame import illuminancePictureFrame
from LuminanceCalculator import LuminanceCalculator
from L20Calculator import L20Calculator
from PDFGenerator import PDFGenerator
class Ventana: #Se crea clase ventana la cual va realizar la interfaz gráfica.

    def __init__(self,master):
        self.widgets=[[],[],[],[],[],[]]
        self.active=[False for i in range(7)]
        self.active[-1]=True
        self.menushow(master)
        self.last=-1
        self.recreado=[False for i in range(len(self.widgets))]
        self.recrear(4)
        self.gridFileName="L20DefaultImage.jpg"
        self.stopDistanceCalculator = L20Calculator()
        self.stopDistanceCalculator.SD = 100


    def recrear(self,id):
        if self.last!=-1:
            for j in self.widgets[self.last]:
                j.place_forget()
        self.last=id
        self.active[id]=True

        
        self.dayLight = Button(self.master, text="1.Evaluar\nRequerimientos",width=12,height=3,command=lambda:self.recrear(4))
        self.dayLight.place(x=40,y=85)
        if self.active[2]:
            self.foto = Button(self.master, text="3.Areas del \n Portal",width=12,height=3,command=lambda:self.recrear(1))
            self.foto.place(x=40,y=160+75)    
        self.l20 = Button(self.master, text="2.Parametros\n de calculo",width=12,height=3,command=lambda: self.recrear(2))
        self.l20.place(x=40,y=160)

        if(self.active[1]):
            self.LuminanciaTunel = Button(self.master, text="Luminancia Tunel",width=16,height=3,highlightbackground='#336B87',command=self.reboot)
            self.LuminanciaTunel.place(x=10,y=310)
            self.configuraciónSecciones = Button(self.master, text="1.Configuración\nde secciones",width=12,height=3,command=lambda: self.recrear(3))
            self.configuraciónSecciones.place(x=40,y=385)

        if(self.active[3]):        
            self.distribucionLuminarias = Button(self.master, text="2.Distribución\n luminarias",width=12,height=3,command=lambda: self.recrear(5))
            self.distribucionLuminarias.place(x=40,y=385+75)



        if id==1:
            self.foto = Button(self.master, text="3.Areas del \n Portal",width=12,height=3,bg='#336B87',command=lambda:self.recrear(1))
            self.foto.place(x=40,y=160+75)
        elif id==2:
            self.l20 = Button(self.master, text="2.Parametros\n de calculo",width=12,bg='#336B87',height=3,command=lambda: self.recrear(2))
            self.l20.place(x=40,y=160)

        elif id==5:
            self.distribucionLuminarias = Button(self.master, text="2.Distribución\n luminarias",width=12,height=3,command=lambda: self.recrear(5),bg='#336B87')
            self.distribucionLuminarias.place(x=40,y=385+75)
        
        elif id==4:
            self.dayLight = Button(self.master, text="1.Evaluar\nRequerimientos",width=12,height=3,command=lambda:self.recrear(4),bg='#336B87')
            self.dayLight.place(x=40,y=85)
        elif id==3:
            self.configuraciónSecciones = Button(self.master, text="1.Configuración\nde secciones",width=12,height=3,command=lambda: self.recrear(3),bg='#336B87')
            self.configuraciónSecciones.place(x=40,y=385)

        if self.recreado[id]==False:
            self.recreado[id]=True
            if id==0:
                self.distanciaParada()
            elif id==1:
                self.vistafoto()
            elif id==2:
                self.l20_peque()
            elif id==5:
                self.distribucionDeLuminarias()
            elif id ==4:
                self.viewDayLight()
            elif id==3:
                self.configuracionDeLuminarias()
            return 
        for i in self.widgets[id]:
            i.place(width=i.winfo_width(),height=i.winfo_height(),x=i.winfo_rootx()-self.master.winfo_rootx(),y=i.winfo_rooty()-self.master.winfo_rooty())
            
        return 
    def generar(self):
        return True
    def guardarDatos(self):
        return True
    def reboot(self):
        return True

    def generarCircunferencia(self):
        self.grilla.reset(escalate = True)

        print("Pendiente bug de distancia de parada")
        self.grilla.firsStep(newGridCenterOffsetX = float(self.coordenada_x_entry.get()),newGridCenterOffsetY = float(self.coordenada_y_entry.get()),SD = self.stopDistanceCalculator.SD, newInteriorCircleRadius = float(self.radio_circulo_entry.get()),entranceRadiusMeters = float(self.radio_portal_entry.get()))        
        self.grilla.secondStep(int(self.divisiones_angulo_entry.get()),int(self.divisiones_radio_entry.get()))
        self.grilla.fillGrid()

    def actualizarBinder(self):
        if self.grilla.binder != None:
            self.grilla.myCanvas.unbind("<Button-1>",self.grilla.binder)
        self.grilla.binder= self.grilla.myCanvas.bind("<Button-1>",self.grilla.markArea)

    def cambiarColorCielo(self):
        self.actualizarBinder()
        self.grilla.currentMaterial=0
    def cambiarColorCalzada(self):
        self.actualizarBinder()
        self.grilla.currentMaterial=1

    def cambiarColorRocas(self):
        self.actualizarBinder()
        self.grilla.currentMaterial=2

    def cambiarColorEdificios(self):
        self.actualizarBinder()
        self.grilla.currentMaterial=3

    def cambiarColorNieve(self):
        self.actualizarBinder()
        self.grilla.currentMaterial=4

    def cambiarColorPrados(self):
        self.actualizarBinder()
        self.grilla.currentMaterial=5

    def cambiarColorTunel(self):
        self.actualizarBinder()
        self.grilla.currentMaterial=6

    def cargarImagen(self):
        filename = filedialog.askopenfilename(initialdir = "L20DefaultImage.jpg",title = "Select a File")                                                        
        # Change label contents
        self.grilla.loadImage(filename, escalate = True)
        self.grilla.drawImage()
        self.rutaFoto1.delete(0, 'end')
        self.rutaFoto1.insert(END,filename)
        self.gridFileName=filename
    def cargarFotometria(self,name):
        print("Cargar Fotometria ", name)
        filename = filedialog.askopenfilename(initialdir = "Fotometrias",title = "Select a File")
        setattr(self,name,filename)

    def getDayLight(self):
        mat=[[False for i in range(5)] for i in range(5)]

        mat[0][0]=(self.tamañoTunelOpcion1Value.get())
        mat[0][1]=(self.tamañoTunelOpcion2Value.get())
        mat[0][2]=(self.tamañoTunelOpcion3Value.get())
        mat[0][3]=(self.tamañoTunelOpcion4Value.get())



        mat[1][0]=(self.salidaVisibleOpcion1Value.get())
        mat[1][1]=(self.salidaVisibleOpcion2Value.get())

        mat[2][0]=(self.luzDelDiaOpcion1Value.get())
        mat[2][1]=(self.luzDelDiaOpcion2Value.get())

        mat[3][0]=(self.reflectanciaParedOpcion1Value.get())
        mat[3][1]=(self.reflectanciaParedOpcion2Value.get())

        mat[4][0]=(self.traficoOpcion1Value.get())
        mat[4][1]=(self.traficoOpcion2Value.get())


        message = "Configuración invalida no definida en la norma CIE 88"

        for i in range(5):
            if mat[i].count(True)>1:
                message="Atencion! Seleccione solo una casilla por opción"
        
        if(message!="Atencion! Seleccione solo una casilla por opción"):

            if mat[0][0] or (mat[0][1] and mat[1][0] and mat[4][0]) or (mat[0][1] and mat[1][1] and mat[2][0] and mat[3][0] and mat[4][0]):
                message="No se requiere diseñar la iluminación diurna."
            elif (mat[0][1] and mat[0][0] and mat[4][1]) or (mat[0][1] and mat[1][1] and mat[2][0] and mat[3][1]) or (mat[0][1] and mat[1][1] and mat[2][1]) or (mat[0][2] and mat[1][0] and mat[4][0]) or (mat[0][2] and mat[1][1] and mat[2][0] and mat[3][0] and mat[4][0]):
                message="Se requiere iluminación diurna cumpliendo el requerimiento del 50% de la luminancia de la zona limite."
            elif mat[0][3] or (mat[0][2] and ( (mat[1][0] and mat[4][1]) or (mat[1][1] and (mat[2][1] or (mat[2][0] and mat[3][1]))))):
                message="Se requiere iluminación diurna cumpliendo el requerimiento del 100% de la luminancia de la zona limite."


        mb.showinfo(title="Requerimientos para el de iluminación de dia",message=message)
        return message

    def getDataPhoto(self):
        areasPercentageArray=self.grilla.getTotalAreas()
        hemisferio=dict()
        hemisferio["Norte"]=0
        hemisferio["Sur"]=1
        direction=dict()
        direction["Norte"]=0
        direction["Occidente"]=1
        direction["Sur"]=2
        direction["Oriente"]=3
        montañoso=dict()
        montañoso["Si"]=True
        montañoso["No"]=False

        self.l20Resultados = L20Calculator(maxSpeed = float(self.vMax.get()), slope = float(self.inclinacionCarretera.get()), fiftyPercentThreshold= False,
                    MountainousTerrain=montañoso[self.esMontañoso.get()],
                    cardinalDirection = direction[self.orientacionTunel.get()], Hemisphere = hemisferio[self.hemisferio.get()],
                    Lc = float(self.lc.get()), Lr = float(self.lr.get()), LeRocks = float(self.ler.get()), LeBuildings = float(self.leb.get()),
                    LeSnow =float(self.les.get()), LeMeadows = float(self.lem.get()),
                    percentArray = self.grilla.getTotalAreas())

        names=["Cielo","Calzada","Rocas", "Edificios", "Nieve", "Vegetacion","Túnel"]
        message=""
        for i in range(7):
            message+= str(round(areasPercentageArray[i]*100,1))+"% de "+names[i]
            if i<6:
                message+=", "
        mb.showinfo(title="Porcentaje Materiales",message=message)
        unidades = "cd/m2"

        out=("Luminancias: Lc: " + str(self.l20Resultados.Lc)+unidades  +", LeRocks: "
             + str(self.l20Resultados.LeRocks)+unidades  + ", LeBuildings: " + str(self.l20Resultados.LeBuildings) +unidades +
             ", LeSnow: " + str(self.l20Resultados.LeSnow) +unidades + ", LeMeadows: " + str(self.l20Resultados.LeMeadows) +unidades + ", Lr: " +
             str(self.l20Resultados.Lr)+unidades 
             +", Lth: "+ str(round(self.l20Resultados.Lth,3))+unidades )
        mb.showinfo(title="Calculo L20",message=out)




    def createEntry(self,name,x1,y1,id,width1=150,height1=89,default=0.0):

        globals()[name]=Entry(font=('Verdana',30),justify='center')
        globals()[name]= Entry(font=('Verdana',30),justify='center')
        globals()[name].insert(END,default)
        globals()[name].place(width=width1,height=height1,x=x1,y=y1)
        setattr(self,name,globals()[name])
        self.widgets[id].append(getattr(self,name))

    def createCheck(self,name,x1,y1,id,condition,width1=10,height1=2,text="check", checkType = 0):
        
        def checkCallBackBinary():            
            checkBoxNumber = name[len(name)-1]
            rootName = name[0:len(name)-1]            
            globals()[rootName+"1"].deselect()
            globals()[rootName+"2"].deselect()
            globals()[rootName+str(checkBoxNumber)].select()

        def checkCallBackMultiple():
            checkBoxNumber = name[len(name)-1]
            rootName = name[0:len(name)-1]            
            globals()[rootName+"1"].deselect()
            globals()[rootName+"2"].deselect()
            globals()[rootName+"3"].deselect()
            globals()[rootName+"4"].deselect()
            globals()[rootName+str(checkBoxNumber)].select()

        setattr(self,name+"Value",BooleanVar())

        if(checkType == 0):
            globals()[name]=Checkbutton(self.master, text =condition, variable = getattr(self,name+"Value"),onvalue = True, offvalue = False, height=height1, width = width1,bg='#90AFC5', command=checkCallBackBinary)
        else:
            globals()[name]=Checkbutton(self.master, text =condition, variable = getattr(self,name+"Value"),onvalue = True, offvalue = False, height=height1, width = width1,bg='#90AFC5', command=checkCallBackMultiple)
      
        globals()[name].place(x=x1,y=y1)
        setattr(self,name,globals()[name])
        self.widgets[id].append(getattr(self,name))

    def createLabel(self,name,x1,y1,id,width1=150,height1=89,label="jk"):
        color= '#336B87'
        globals()[name]=Label(self.master, text=label,width=width1,height=height1,bg=color,fg='white')
        globals()[name].place(x=x1,y=y1)
        setattr(self,name,globals()[name])
        self.widgets[id].append(getattr(self,name))
    def createButton(self,name,x1,y1,id,width1=7,height1=2,command="cambiarColorCalzada"):
        color= '#336B87'
        globals()[name]= Button(self.master, text=name,width=width1,height=height1,background=color,command=getattr(self,command), fg='white')
        globals()[name].place(x=x1,y=y1)
        setattr(self,name,globals()[name])
        self.widgets[id].append(getattr(self,name))
    def createPhoto(self,name,ruta,id,width,height,x,y):
        
        globals()["img"+name]=Image.open(ruta)
        globals()["img"+name]=globals()["img"+name].resize((width, height))
        setattr(self,"img"+name,globals()["img"+name])
        globals()["imagen"+name]=ImageTk.PhotoImage(getattr(self,"img"+name))
        setattr(self,"imagen"+name,globals()["imagen"+name])
        globals()[name] =Label(self.master,image=getattr(self,"imagen"+name))
        globals()[name].place(x=x,y=y)
        setattr(self,name,globals()[name])
        self.widgets[id].append(getattr(self,name))
    def createSelector(self,name,values,id,x,y,width,height):
        globals()[name] =ttk.Combobox(self.master,width=width,height=height)
        globals()[name].place(x=x, y=y)
        globals()[name]["values"] = values
        globals()[name].set(values[0])
        setattr(self,name,globals()[name])
        self.widgets[id].append(getattr(self,name))
    def createPathSelector(self,name,text1,id,x1,y1,width1,height1,command):
        globals()[name]= Button(self.master, text=text1,width=width1,height=height1,background='#336B87',command=command, fg='white')
        globals()[name].place(x=x1,y=y1)
        setattr(self,name,globals()[name])
        self.widgets[id].append(getattr(self,name))
    def viewDayLight(self):
        id=4
        """
        self.createEntry("entryPrueba",500,500,3)
        self.createButton("buton1dfd",600,400,3,14,3)
        self.createCheck("check1",30,30,2,"Yes",text="jk")
        """
        self.createLabel("DayTime",760,50,id,17,3,label="Requerimientos de \n iluminación dia")
        epsx=200
        epsy=80
        
        self.createLabel("tamañoTunel",240,130,id,20,3,label="1. Tamaño del túnel:")
        self
        self.createCheck("tamañoTunelOpcion1",480,135,id,"<25m", checkType = 1)
        self.createCheck("tamañoTunelOpcion2",480+epsx,135,id,"25m-75m", checkType = 1)
        self.createCheck("tamañoTunelOpcion3",480+epsx*2,135,id,"75m-125m", checkType = 1)
        self.createCheck("tamañoTunelOpcion4",480+epsx*3,135,id,">125m", checkType = 1)

 
        self.createLabel("salidaVisible",240,130+epsy,id,20,3,label="2. Salida visible desde\ndistancia de parada:")
        self.createCheck("salidaVisibleOpcion1",480+epsx,135+epsy,id,"Si")
        self.createCheck("salidaVisibleOpcion2",480+epsx*2,135+epsy,id,"No")

        self.createLabel("luzDelDia",240,130+epsy*2,id,20,3,label="3. Penetración de la\n luz del día:")
        self.createCheck("luzDelDiaOpcion1",480+epsx,135+epsy*2,id,"Buena")
        self.createCheck("luzDelDiaOpcion2",480+epsx*2,135+epsy*2,id,"Mala")
        
        self.createLabel("reflectanciaPared",240,130+epsy*3,id,20,3,label="4. Reflectancia\n de pared:")
        self.createCheck("reflectanciaParedOpcion1",480+epsx,135+epsy*3,id,">0,4")
        self.createCheck("reflectanciaParedOpcion2",480+epsx*2,135+epsy*3,id,"<0,2")

        self.createLabel("trafico",240,130+epsy*4,id,20,3,label="5. Trafico:")
        self.createCheck("traficoOpcion1",480+epsx,135+epsy*4,id,"Ligero")
        self.createCheck("traficoOpcion2",480+epsx*2,135+epsy*4,id,"Pesado")

        

        self.createButton("Evaluar configuración",725,570,id,24,3,command="getDayLight")
    
    def vistafoto(self):
        id=1
        color= '#336B87'.upper() #Color azúl de botón
        color1= '#336B87'.upper() #Color azúl de botón
        over="#763626"
        master=self.master
        # crear label
        self.grilla = illuminancePictureFrame(widowsSizeX = 600, widowsSizeY = 450)
        self.grilla.grid( row = 0, column = 0,rowspan = 3, columnspan = 6, sticky = tk.W+tk.E+tk.N+tk.S)
        self.grilla.place(x=240,y=160-55)
        self.widgets[1].append(self.grilla)
        areasPercentageArray = [0 for i in range(7)]
        self.ruta_foto =Label(master, text="Ruta foto:",width=20,height=2,bg=color,fg='white') 
        self.ruta_foto.place(x=240,y=60)
        self.widgets[1].append(self.ruta_foto )
        # crear entry
        self.rutaFoto1 = Entry(font=('Verdana',15),justify='center')
        self.rutaFoto1.insert(END,os.getcwd())
        self.rutaFoto1.place(width=400,height=38,x=425,y=60)
        self.widgets[1].append(self.rutaFoto1)

        self.cargarImagen= Button(master, text="cargar imagen",width=15,height=2,background=color,command=self.cargarImagen, fg='white')
        self.cargarImagen.place(x=850,y=60)
        self.widgets[1].append(self.cargarImagen)

        corrimiento=55

        """
        self.img2=Image.open("circunferencia.png")
        self.img2=self.img2.resize((600, 400))
        self.imagenCarros =ImageTk.PhotoImage(self.img2)
        self.imagen3 =Label(master,image=self.imagenCarros)
        self.imagen3.place(x=270,y=160)
        self.widgets[1].append(self.imagen3)
        """
        corrimiento2=45

        
        self.radio_portal =Label(master, text="Altura real\n del portal en metros:",width=20,height=2,bg=color,fg='white')
        self.radio_portal.place(x=850,y=60+corrimiento)
        self.widgets[1].append(self.radio_portal )
        
        self.radio_circulo =Label(master, text="Radio de circulo interno:",width=20,height=2,bg=color,fg='white')
        self.radio_circulo.place(x=850,y=60+corrimiento+corrimiento2)
        self.widgets[1].append(self.radio_circulo )
        
        self.coordenada_x =Label(master, text="Coordenada de la\ngrilla en x:",width=20,height=2,bg=color,fg='white')
        self.coordenada_x.place(x=850,y=60+corrimiento+corrimiento2*2)
        self.widgets[1].append(self.coordenada_x )
        
        self.coordenada_y=Label(master, text="Coordenada de la\ngrilla en y:",width=20,height=2,bg=color,fg='white')
        self.coordenada_y.place(x=850,y=60+corrimiento+corrimiento2*3)
        self.widgets[1].append(self.coordenada_y )
        
        self.divisiones_angulo =Label(master, text="Divisiones angulo:",width=20,height=2,bg=color,fg='white')
        self.divisiones_angulo.place(x=850,y=60+corrimiento+corrimiento2*4+20)
        self.widgets[1].append(self.divisiones_angulo )

        self.divisiones_radio =Label(master, text="Divisiones radio:",width=20,height=2,bg=color,fg='white')
        self.divisiones_radio.place(x=850,y=60+corrimiento+corrimiento2*5+20)
        self.widgets[1].append(self.divisiones_radio )

        self.radio_portal_entry = Entry(font=('Verdana',15),justify='center')
        self.radio_portal_entry.insert(END,5)
        self.radio_portal_entry.place(width=70,height=38,x=1020,y=60+corrimiento+corrimiento2*0)
        self.widgets[1].append(self.radio_portal_entry)

        self.radio_circulo_entry = Entry(font=('Verdana',15),justify='center')
        self.radio_circulo_entry.insert(END,45)
        self.radio_circulo_entry.place(width=70,height=38,x=1020,y=60+corrimiento+corrimiento2*1)
        self.widgets[1].append(self.radio_circulo_entry)

        self.coordenada_x_entry = Entry(font=('Verdana',15),justify='center')
        self.coordenada_x_entry.insert(END,0)
        self.coordenada_x_entry.place(width=70,height=38,x=1020,y=60+corrimiento+corrimiento2*2)
        self.widgets[1].append(self.coordenada_x_entry)

        self.coordenada_y_entry = Entry(font=('Verdana',15),justify='center')
        self.coordenada_y_entry.insert(END,0)
        self.coordenada_y_entry.place(width=70,height=38,x=1020,y=60+corrimiento+corrimiento2*3)
        self.widgets[1].append(self.coordenada_y_entry)
        
        self.divisiones_angulo_entry = Entry(font=('Verdana',15),justify='center')
        self.divisiones_angulo_entry.insert(END,4)
        self.divisiones_angulo_entry.place(width=70,height=38,x=1020,y=60+corrimiento+corrimiento2*4+20)
        self.widgets[1].append(self.divisiones_angulo_entry)

        
        self.divisiones_radio_entry = Entry(font=('Verdana',15),justify='center')
        self.divisiones_radio_entry .insert(END,4)
        self.divisiones_radio_entry .place(width=70,height=38,x=1020,y=60+corrimiento+corrimiento2*5+20)
        self.widgets[1].append(self.divisiones_radio_entry )

        corrimiento3=80
        y1=60+corrimiento+corrimiento2*5+20+corrimiento3
        
        self.cielo= Button(master, text="Cielo",width=10,height=1,background=color,command=self.cambiarColorCielo, fg='white')
        self.cielo.place(x=850,y=y1)
        self.widgets[1].append(self.cielo)
        
        self.calzada= Button(master, text="Pavimento",width=10,height=1,background=color,command=self.cambiarColorCalzada, fg='white')
        self.calzada.place(x=850+100,y=y1)
        self.widgets[1].append(self.calzada)

        self.rocas= Button(master, text="Rocas",width=10,height=1,background=color,command=self.cambiarColorRocas, fg='white')
        self.rocas.place(x=850+100+100,y=y1)
        self.widgets[1].append(self.rocas)



        self.nieve= Button(master, text="Nieve",width=10,height=1,background=color,command=self.cambiarColorNieve, fg='white')
        self.nieve.place(x=850,y=y1+40)
        self.widgets[1].append(self.nieve)

        self.prados= Button(master, text="Vegetación",width=10,height=1,background=color,command=self.cambiarColorPrados, fg='white')
        self.prados.place(x=850+100,y=y1+40)
        self.widgets[1].append(self.prados)
        
        self.tunel = Button(master, text="Túnel",width=10,height=1,background=color,command=self.cambiarColorTunel, fg='white')
        self.tunel.place(x=850+100+100,y=y1+40)
        self.widgets[1].append(self.tunel)


        self.edificios= Button(master, text="Edificaciones",width=10,height=1,background=color,command=self.cambiarColorEdificios, fg='white')
        self.edificios.place(x=850+100+100+100,y=y1)
        self.widgets[1].append(self.edificios)



        self.generarCircunFerencia = Button(master, text="Generar grilla",width=20,height=2,background=color,command=self.generarCircunferencia, fg='white')
        self.generarCircunFerencia.place(x=480,y=565)
        self.widgets[1].append(self.generarCircunFerencia)


        self.createButton("Calcular areas",725,565,id,20,2,command="getDataPhoto")

    def menushow(self,master):
        color= '#336B87'.upper() #Colore botón
        color1= '#336B87'.upper() #Color  botón
        over="#763626"
        self.master = master #Creando objeto (gráfica)
        self.master.title("Lux Tunnel") #Nombre de ventana 
        self.master.geometry("1400x650") #  Tamaño de ventana
        self.master['bg'] = '#2A3132'.upper() #Color de background
        self.L20 = Button(master, text="L20",width=16,height=3,highlightbackground=color1,command=self.reboot)
        self.L20.place(x=10,y=10)
        w = Canvas(master, width=1150, height=650)
        w.create_rectangle(0, 0, 1150, 650, fill="#90AFC5", outline = 'black')
        w.place(x=200,y=25)
    
    def l20_peque(self):
        id=2
        corrimientoy=55
        self.createLabel("LuminanciaCielo",230,55,id,27,2,label="Luminancia cielo (Lc)")
        self.createLabel("LuminanciaCarretera",230,55+corrimientoy,id,27,2,label="Luminancia carretera (Lr)")
        self.createLabel("LuminanciaZonasRocosas",230,55+corrimientoy*2,id,27,2,label="Luminancia zonas rocosas (LeR)")
        self.createLabel("LuminanciaConstrucciones",230,55+corrimientoy*3,id,27,2,label="Luminancia construcciones (LeB)")
        self.createLabel("LuminanciaNieve",230,55+corrimientoy*4,id,27,2,label="Luminancia nieve (LeS)")
        self.createLabel("LuminanciaVegetacion",230,55+corrimientoy*5,id,27,2,label="Luminancia vegetacion (LeM)")

        self.createEntry("lc",460,55,id,width1=100,height1=38,default=0.0)
        self.createEntry("lr",460,55+corrimientoy*1,id,width1=100,height1=38,default=0.0)
        self.createEntry("ler",460,55+corrimientoy*2,id,width1=100,height1=38,default=0.0)
        self.createEntry("leb",460,55+corrimientoy*3,id,width1=100,height1=38,default=0.0)
        self.createEntry("les",460,55+corrimientoy*4,id,width1=100,height1=38,default=0.0)
        self.createEntry("lem",460,55+corrimientoy*5,id,width1=100,height1=38,default=0.0)
        for i in range(6):
            self.createLabel("unidadesluminacias"+str(i),570,55+corrimientoy*i,id,7,2,label="cd/m^2")
            
        self.createLabel("velocidadMaximaLabel",730,55,id,27,2,label="Velocidad Maxima:")
        self.createLabel("inclinacionDeLaCarreteraLabel",730,55+corrimientoy*1,id,27,2,label="Inclinación de la carretera")
        self.createLabel("terrenoMontañosoLabel",730,55+corrimientoy*2,id,27,2,label="Terreno Montañoso")

        self.createLabel("orientacionHaciaElTunelLabel",730,55+corrimientoy*3,id,27,2,label="Orientacion hacia el tunel")
        self.createLabel("hemisferioLabel",730,55+corrimientoy*4,id,27,2,label="Hemisferio")

        self.createLabel("kiloh",730+340,55,id,7,2,label="Km/h")
        self.createLabel("gradossimbolo",730+340,55+corrimientoy*1,id,7,2,label="°")

        self.createEntry("vMax",730+230,55,id,width1=100,height1=38,default=90)
        self.createEntry("inclinacionCarretera",730+230,55+corrimientoy*1,id,width1=100,height1=38,default=0.1)
        self.createSelector("esMontañoso",["Si","No"],id,730+230,55+corrimientoy*2+7,11,9)
        self.createSelector("orientacionTunel",["Norte","Occidente","Sur","Oriente"],id,730+230,55+corrimientoy*3+7,11,9)
        self.createSelector("hemisferio",["Norte","Sur"],id,730+230,55+corrimientoy*4+7,11,9)
        self.createButton("Cálcular distancia de parada",675,605,id,25,2,command="parametrosCalculo")


    def configuracionDeLuminarias(self):
        color= '#336B87'.upper() #Color azúl de botón
        color1= '#336B87'.upper() #Color azúl de botón
        over="#763626"
        id=3
        master = self.master
        self.seccionDelTunel =Label(master, text="Sección del\n Tunel",width=14,height=3,bg=color,fg='white')
        self.seccionDelTunel.place(x=250,y=50)
        self.widgets[3].append(self.seccionDelTunel)
        corrimiento=60
        
        self.alturaLuminarias =Label(master, text="Altura de\n luminarias(m)",width=14,height=3,bg=color,fg='white')
        self.alturaLuminarias.place(x=250,y=50+corrimiento)
        self.widgets[3].append(self.alturaLuminarias)
        
        self.interDistancia =Label(master, text="Inter\n distancia(m)",width=14,height=3,bg=color,fg='white')
        self.interDistancia.place(x=250,y=50+corrimiento*2)
        self.widgets[3].append(self.interDistancia)

        self.anchoDelCamino =Label(master, text="Ancho del\n camino(m)",width=14,height=3,bg=color,fg='white')
        self.anchoDelCamino.place(x=250,y=50+corrimiento*3)
        self.widgets[3].append(self.anchoDelCamino)

        self.numeroCarriles =Label(master, text="# de carriles",width=14,height=3,bg=color,fg='white')
        self.numeroCarriles.place(x=250,y=50+corrimiento*4)
        self.widgets[3].append(self.numeroCarriles)

        self.fotometria =Label(master, text="fotometria",width=14,height=3,bg=color,fg='white')
        self.fotometria.place(x=250,y=50+corrimiento*5)
        self.widgets[3].append(self.fotometria)


        corrimiento2=130
        numeroSecciones=5
        for i in range(numeroSecciones):
            self.seccion1 =Label(master, text="Sección "+str(i+1),width=14,height=3,bg=color,fg='white')
            self.seccion1.place(x=270+corrimiento2*(i+1),y=50)
            self.widgets[3].append(self.seccion1)
        defaultRuta="Fotometrias/Sit2.ies"
        for i in range(5):
            for j in range(numeroSecciones):
                if i!=4:
                    defaultValue=0
                    if i==0:
                        defaultValue=4
                    if i==1:
                        defaultValue=40
                    if i==2:
                        defaultValue=10
                    if i==3:
                        defaultValue=2
                    self.createEntry("seccion1"+str(j)+str(i),270+corrimiento2*(j+1)+7,60+corrimiento*(i+1),id,width1=70,height1=38,default=defaultValue)
        name1="ruta04"
        setattr(self,name1,defaultRuta)
        self.fun1=lambda : self.cargarFotometria(name1)
        self.createPathSelector("obtenerRuta"+str(0)+str(4),"Ruta",id,270+corrimiento2*(0+1)+7,60+corrimiento*(4+1),5,1,self.fun1)
        name2="ruta14"
        setattr(self,name2,defaultRuta)

        self.fun2=lambda : self.cargarFotometria(name2)
        self.createPathSelector("obtenerRuta"+str(1)+str(4),"Ruta",id,270+corrimiento2*(1+1)+7,60+corrimiento*(4+1),5,1,self.fun2)
        name3="ruta24"
        setattr(self,name3,defaultRuta)

        self.fun3=lambda : self.cargarFotometria(name3)
        self.createPathSelector("obtenerRuta"+str(2)+str(4),"Ruta",id,270+corrimiento2*(2+1)+7,60+corrimiento*(4+1),5,1,self.fun3)
        name4="ruta34"
        setattr(self,name4,defaultRuta)

        self.fun4=lambda : self.cargarFotometria(name4)
        self.createPathSelector("obtenerRuta"+str(3)+str(4),"Ruta",id,270+corrimiento2*(3+1)+7,60+corrimiento*(4+1),5,1,self.fun4)
        name5="ruta44"
        setattr(self,name5,defaultRuta)
        self.fun5=lambda : self.cargarFotometria(name5)
        self.createPathSelector("obtenerRuta"+str(4)+str(4),"Ruta",id,270+corrimiento2*(4+1)+7,60+corrimiento*(4+1),5,1,self.fun5)
       
        self.createLabel("factorDeMantenimiento",250,440,3,17,3,label="Factor de \n mantenimiento")
        self.createEntry("factorDeMantenimientoEntry",250,495,3,width1=140,height1=60,default=0.8)
        self.createPhoto("photoSeccionTunel","secciones.jpeg",3,500,200,500,440)
    def luminanciaTunel(self):
 
        print("distribucionLuminarias")
        for i in range(5):
            print(i)
        numeroSecciones=5
        secciones=[[] for i in range(numeroSecciones)]
        for i in range(numeroSecciones):
            secciones[i].append(getattr(self,"ruta"+str(i)+"4"))
            for j in range(5):
                if j==4:
                    continue
                secciones[i].append(float(getattr(self,"seccion1"+str(i)+str(j)).get()))
        for i in range(numeroSecciones):
            for j in range(3):
                if j!=1:
                    secciones[i].append(float(getattr(self,"seccion2"+str(i)+str(j)).get()))
                else:
                    secciones[i].append(int(getattr(self,"seccion2"+str(i)+str(j)).get()[-1]))
        fm=float(self.factorDeMantenimientoEntry.get())

        luminancias=[]
        for i in range(numeroSecciones):
            print("Distribución: " + str(secciones[i][7]))
            luminancias.append(LuminanceCalculator(IESroute=secciones[i][0], luminairesHeight = secciones[i][1], luminairesBetweenDistance = secciones[i][2],
                                                   roadWidth = secciones[i][3],
                                   roadLanes=int(secciones[i][4]), luminairesRotation = secciones[i][5], luminariesOverhang = secciones[i][7],
                                                   luminariesDistribution = int(secciones[i][6]),
                                                   Fm= fm))

        test = PDFGenerator()
        files = [('PDF', '*.pdf'),('Todos los archivos', '*.*')]
        self.routePdf=filedialog.asksaveasfile(title = "Guardar pdf de resultados como :", defaultextension="pdf", initialfile="Informe",filetypes=files).name

        test.exportData(route=self.routePdf, luminanceTunnelEntranceImageRoute=self.gridFileName,l20=self.l20Resultados,sections= luminancias)
        mb.showinfo(title="Resultados Generados",message="Atención, cálculo satisfactorio, se ha generado un informe de resultados en la ruta: "+self.routePdf)

    def distribucionDeLuminarias(self):

        id=5

        self.createLabel("SeccionDeTuneles",250,50,id,14,3,label="Sección del\n Tunel")

        self.createLabel("imagen angulo rotacion",1100,50,id,24,3,label="Angulo de rotación\nluminaria")

        self.createPhoto("imagen angulo Rot","angulo.png",id,193,220,1100,120)

        corrimiento=73

        self.createLabel("Angulo de rotaciónluminaria(grados)",250,50+corrimiento,id,14,4,label="Angulo de \nrotación\nluminaria")

        self.createLabel("distribucion de las luminarias",250,50+corrimiento*2,id,14,4,label="Distribución de\nluminarias\n(0,1,2,3)")

        self.createLabel("saliente calzada",250,50+corrimiento*3,id,14,4,label="Saliente sobre\nla calzada en\nmetros(h)")

        corrimiento2=130
        numeroSecciones=5
        for i in range(numeroSecciones):
            self.createLabel("Seccion2"+str(i),270+corrimiento2*(i+1),50,id,14,3,label="Sección "+str(i+1))

        for i in range(3):
            for j in range(numeroSecciones):
                if i!=1:
                    defaultValue=0
                    if i==2:
                        defaultValue=2
                    self.createEntry("seccion2"+str(j)+str(i),270+corrimiento2*(j+1)+7,60+corrimiento*(i+1)-5,id,width1=100,height1=60,default=0.0)
                else:
                    self.createSelector("seccion2"+str(j)+str(i),["Distribución 0","Distribución 1","Distribución 2","Distribución 3"],id,270+corrimiento2*(j+1),60+corrimiento*(i+1)+13,12,8)
        corrimiento=280
        for i in range(4):
            self.createLabel("distribucionLuminaria"+str(i),250+corrimiento*i,370,id,24,3,label="Distribución de luminarias "+str(i))
            self.createPhoto("distribucionLuminariaFoto"+str(i),"distributionImages/"+str(i)+".jpg",id,193,150,250+corrimiento*i,370+60)

        self.createButton("Ejecutar cálculos",675,605,id,20,2,command="luminanciaTunel")

    def parametrosCalculo(self):
        
        print("lc",self.lc.get())
        print("lr",self.lr.get())
        print("ler",self.ler.get())
        print("leb",self.leb.get())

        print("les",self.les.get())
        print("lem",self.lem.get())

        print("vMax",self.vMax.get())
        print("inclinacionCarretera",self.inclinacionCarretera.get())
        print("hemisferio",self.hemisferio.get())
        hemisferio=dict()
        hemisferio["Norte"]=0
        hemisferio["Sur"]=1
        direction=dict()
        direction["Norte"]=0
        direction["Occidente"]=1
        direction["Sur"]=2
        direction["Oriente"]=3
        montañoso=dict()
        montañoso["Si"]=True
        montañoso["No"]=False

        self.stopDistanceCalculator = L20Calculator(maxSpeed = float(self.vMax.get()), slope = float(self.inclinacionCarretera.get()), fiftyPercentThreshold= False)

        mb.showinfo(title="Distancia de Parada",message="La distancia de parada es de: " + "{:.2f}".format(self.stopDistanceCalculator.SD) + "m")



def main():  
    root = Tk()
    v=Ventana(root)
    root.mainloop()


if __name__ == '__main__':
    main()
        
