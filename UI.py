import sys, os
import tkinter as tk

from tkinter import *
from tkinter import messagebox as mb
from tkinter import filedialog
import math
from PIL import Image, ImageTk
from illuminancePictureFrame import illuminancePictureFrame
class Ventana: #Se crea clase ventana la cual va realizar la interfaz gráfica.

    def __init__(self,master):
        self.widgets=[[],[],[],[],[]]
        self.menushow(master)
        self.last=-1
        self.recreado=[False for i in range(len(self.widgets))]
        self.recrear(4)

    def recrear(self,id):
        if self.last!=-1:
            for j in self.widgets[self.last]:
                j.place_forget()
        self.last=id

        
        self.distanciaDeParada = Button(self.master, text="Distancia De\nParada",width=12,height=3,command=lambda:self.recrear(0))
        self.distanciaDeParada.place(x=40,y=85+75)
        self.foto = Button(self.master, text="Areas Portal",width=12,height=3,command=lambda:self.recrear(1))
        self.foto.place(x=40,y=160+75)    
        self.l20 = Button(self.master, text="L20",width=12,height=3,command=lambda: self.recrear(2))
        self.l20.place(x=40,y=160+75*2)
        self.l20 = Button(self.master, text="L20",width=12,height=3,command=lambda: self.recrear(2))
        self.distribucionLuminarias = Button(self.master, text="Distribución\n luminarias",width=12,height=3,command=lambda: self.recrear(3))
        self.distribucionLuminarias.place(x=40,y=385+75)
        
        self.dayLight = Button(self.master, text="Evaluar\nRequerimientos",width=12,height=3,command=lambda:self.recrear(4))
        self.dayLight.place(x=40,y=85)

        if id==0:
            self.distanciaDeParada = Button(self.master, text="Distancia De\nParada",width=12,height=3,bg='#336B87',command=lambda:self.recrear(0))
            self.distanciaDeParada.place(x=40,y=85+75)
        elif id==1:
            self.foto = Button(self.master, text="Areas Portal",width=12,height=3,bg='#336B87',command=lambda:self.recrear(1))
            self.foto.place(x=40,y=160+75)
        elif id==2:
            self.l20 = Button(self.master, text="L20",width=12,bg='#336B87',height=3,command=lambda: self.recrear(2))
            self.l20.place(x=40,y=160+75*2)

        elif id==3:
            self.distribucionLuminarias = Button(self.master, text="Distribución\n luminarias",width=12,height=3,command=lambda: self.recrear(3),bg='#336B87')
            self.distribucionLuminarias.place(x=40,y=385+75)
        
        elif id==4:
            self.dayLight = Button(self.master, text="Evaluar\nRequerimientos",width=12,height=3,command=lambda:self.recrear(4),bg='#336B87')
            self.dayLight.place(x=40,y=85)
        if self.recreado[id]==False:
            self.recreado[id]=True
            if id==0:
                self.distanciaParada()
            elif id==1:
                self.vistafoto()
            elif id==2:
                self.l20_peque()
            elif id==3:
                self.distribucionDeLuminarias()
            else:
                self.viewDayLight()
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
        self.grilla.firsStep(float(self.coordenada_x_entry.get()),float(self.coordenada_y_entry.get()),float(self.radio_circulo_entry.get()),float(self.radio_portal_entry.get()))
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
    def cambiarColorPrados(self):
        self.actualizarBinder()
        self.grilla.currentMaterial=2
    def cambiarColorEdificios(self):
        self.actualizarBinder()
        self.grilla.currentMaterial=3
    def cambiarColorNieve(self):
        self.actualizarBinder()
        self.grilla.currentMaterial=4
    def cambiarColorRocas(self):
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

    def getDayLight(self):
        mat=[[False for i in range(5)] for i in range(5)]
        mat[0][0]=(self.tamañoTuneOpcion1Value.get())
        mat[0][1]=(self.tamañoTuneOpcion2Value.get())
        mat[0][2]=(self.tamañoTuneOpcion3Value.get())
        mat[0][3]=(self.tamañoTuneOpcion4Value.get())

        mat[1][0]=(self.salidaVisibleOpcion1Value.get())
        mat[1][1]=(self.salidaVisibleOpcion2Value.get())

        mat[2][0]=(self.luzDelDiaOpcion1Value.get())
        mat[2][1]=(self.luzDelDiaOpcion2Value.get())

        mat[3][0]=(self.reflectanciaParedOpcion1Value.get())
        mat[3][1]=(self.reflectanciaParedOpcion2Value.get())

        mat[4][0]=(self.traficoOpcion1Value.get())
        mat[4][1]=(self.traficoOpcion1Value.get())
        message="Configuración Invalida"
        if mat[0][0] or  (mat[0][1] and mat[1][0] and mat[4][0]) or (mat[0][1] and mat[1][1] and mat[2][0] and mat[3][0] and mat[4][0]):
            message="No se requiere diseñar la iluminación diurna."
        elif (mat[0][1] and mat[0][0] and mat[4][1]) or (mat[0][1] and mat[1][1] and mat[2][0] and mat[3][1]) or (mat[0][1] and mat[1][1] and mat[2][1]) or (mat[0][2] and mat[1][0] and mat[4][0]):
            message="Se requiere iluminación diurna cumpliendo el requerimiento del 50% de la luminancia de la zona limite."
        elif mat[0][3] or (mat[0][2] and ( (mat[1][0] and mat[4][1]) or (mat[1][1] and (mat[2][1] or (mat[2][0] and mat[3][1]))))):
            message="Se requiere iluminación diurna cumpliendo el requerimiento del 100% de la luminancia de la zona limite."
        for i in range(5):
            if mat[i].count(True)>1:
                message="Configuración Invalida"
        mb.showinfo(title="DayLight",message=message)
        return message

    def getDataPhoto(self):
        arr=self.grilla.getTotalAreas()
        newArr=[0 for i in range(7)]
        newArr[0]=arr[0]
        newArr[1]=arr[1]
        newArr[2]=arr[5]
        newArr[3]=arr[4]
        newArr[4]=arr[2]
        newArr[5]=arr[6]
        names=["Cielo","Calzada","Rocas","Nieve","Prados","Túnel"]
        message=""
        for i in range(6):
            message+= str(round(newArr[i],1))+"% de "+names[i]
            if i<5:
                message+=", "
        mb.showinfo(title="Porcentaje Materiales",message=message)
    def createEntry(self,name,x1,y1,id,width1=150,height1=89,default=0.0):

        globals()[name]=Entry(font=('Verdana',30),justify='center')
        globals()[name]= Entry(font=('Verdana',30),justify='center')
        globals()[name].insert(END,default)
        globals()[name].place(width=width1,height=height1,x=x1,y=y1)
        setattr(self,name,globals()[name])
        self.widgets[id].append(getattr(self,name))
    def createCheck(self,name,x1,y1,id,condition,width1=10,height1=2,text="check"):
        setattr(self,name+"Value",BooleanVar())
        globals()[name]=Checkbutton(self.master, text =condition, variable = getattr(self,name+"Value"),onvalue = True, offvalue = False, height=height1, width = width1,bg='#90AFC5')
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
        self.createCheck("tamañoTuneOpcion1",480,135,id,"<25m")
        self.createCheck("tamañoTuneOpcion2",480+epsx,135,id,"25m-75m")
        self.createCheck("tamañoTuneOpcion3",480+epsx*2,135,id,"75m-125m")
        self.createCheck("tamañoTuneOpcion4",480+epsx*3,135,id,">125m")

 
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

        

        self.createButton("Generar informe de luz del dia",725,570,id,24,3,command="getDayLight")
    
    def distanciaParada(self):
        color= '#336B87'.upper() #Color azúl de botón
        color1= '#336B87'.upper() #Color azúl de botón
        over="#763626"
        master=self.master
        self.velocidadMaxima =Label(master, text="Velocidad máxima:",width=20,height=5,bg=color,fg='white')
        self.velocidadMaxima.place(x=240,y=60)
        self.widgets[0].append(self.velocidadMaxima)
        self.vMax = Entry(font=('Verdana',30),justify='center')
        self.vMax.insert(END,0.0)
        self.vMax.place(width=150,height=89,x=425,y=60)
        self.widgets[0].append(self.vMax)
        self.label_frameVelocidad = Frame(width=80,height=89,bg=color)
        self.label_frameVelocidad.pack_propagate(0)
        self.kms=Label(self.label_frameVelocidad, font=('Verdana',17),text="Km/s",bg=color,fg='white',anchor="center")
        self.kms.place(x=3,y=27)
        self.label_frameVelocidad.place(x=580,y=60)
        self.widgets[0].append(self.label_frameVelocidad)


        corrimiento=120
        self.inclinacionL =Label(master, text="Inclinación de la\n carretera",width=20,height=5,bg=color,fg='white')
        self.inclinacionL.place(x=240,y=60+corrimiento)
        self.widgets[0].append(self.inclinacionL)
        self.inclinacion = Entry(font=('Verdana',30),justify='center')
        self.inclinacion.insert(END,0.0)
        self.inclinacion.place(width=150,height=89,x=425,y=60+corrimiento) 
        self.widgets[0].append(self.inclinacion)
        self.label_frameInclinacion = Frame(width=80,height=89,bg=color)
        self.label_frameInclinacion.pack_propagate(0)
        self.grado=Label(self.label_frameInclinacion, font=('Verdana',17),text="º",bg=color,fg='white',anchor="center")
        self.grado.place(x=33,y=27)
        self.label_frameInclinacion.place(x=580,y=60+corrimiento)
        self.widgets[0].append(self.label_frameInclinacion)


        corrimiento=120*2
        self.coefic =Label(master, text="Coeficiente de fricción\n del pavimento ",width=20,height=5,bg=color,fg='white')
        self.coefic.place(x=240,y=60+corrimiento)
        self.widgets[0].append(self.coefic)
        self.coeficienteFriccion = Entry(font=('Verdana',30),justify='center')
        self.coeficienteFriccion.insert(END,0.0)
        self.coeficienteFriccion.place(width=150,height=89,x=425,y=60+corrimiento)
        self.widgets[0].append(self.coeficienteFriccion)
        self.label_frameCoeficiente = Frame(width=80,height=89,bg=color)
        self.label_frameCoeficiente.pack_propagate(0)
        self.raya=Label(self.label_frameCoeficiente, font=('Verdana',17),text="-",bg=color,fg='white',anchor="center")
        self.raya.place(x=33,y=27)
        self.label_frameCoeficiente.place(x=580,y=60+corrimiento)
        self.widgets[0].append(self.label_frameCoeficiente)


        self.img1=Image.open("formula1.png")
        self.imageFormula =ImageTk.PhotoImage(self.img1)
        self.imagen1 =Label(master,image=self.imageFormula)
        self.imagen1.place(x=400,y=450)
        self.widgets[0].append(self.imagen1)

    
        ###
        self.img22=Image.open("carros.png")
        self.img22=self.img22.resize((245, 205))
        self.imagenCarros1 =ImageTk.PhotoImage(self.img22)
        self.imagen22 =Label(master,image=self.imagenCarros1)
        self.imagen22.place(x=680,y=60)
        self.widgets[0].append(self.imagen22)
        
        ###
    def vistafoto(self):
        id=1
        color= '#336B87'.upper() #Color azúl de botón
        color1= '#336B87'.upper() #Color azúl de botón
        over="#763626"
        master=self.master
        # crear label
        self.grilla = illuminancePictureFrame(widowsSizeX = 600, widowsSizeY = 400)
        self.grilla.grid( row = 0, column = 0,rowspan = 3, columnspan = 6, sticky = tk.W+tk.E+tk.N+tk.S)
        self.grilla.place(x=240,y=160)
        self.widgets[1].append(self.grilla)
        array = [0,0,0,0,0,0,0]
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
        self.altura_l =Label(master, text="Altura entrada:",width=20,height=2,bg=color,fg='white')
        self.altura_l.place(x=240,y=60+corrimiento)
        self.widgets[1].append(self.altura_l )

        self.altura = Entry(font=('Verdana',15),justify='center')
        self.altura.insert(END,0.0)
        self.altura.place(width=200,height=38,x=425,y=60+corrimiento)
        self.widgets[1].append(self.altura)

        self.label_frameAltura1 = Frame(width=80,height=38,bg=color)
        self.label_frameAltura1.pack_propagate(0)
        self.metros=Label(self.label_frameAltura1, font=('Verdana',13),text="metros",bg=color,fg='white',anchor="center")
        self.metros.place(x=8,y=4)
        self.label_frameAltura1.place(x=640,y=60+corrimiento)
        self.widgets[1].append(self.label_frameAltura1)
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
        self.radio_portal_entry.insert(END,90)
        self.radio_portal_entry.place(width=70,height=38,x=1020,y=60+corrimiento+corrimiento2*0)
        self.widgets[1].append(self.radio_portal_entry)

        self.radio_circulo_entry = Entry(font=('Verdana',15),justify='center')
        self.radio_circulo_entry.insert(END,55)
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
        self.nieve.place(x=850+100+100+100,y=y1)
        self.widgets[1].append(self.nieve)

        self.prados= Button(master, text="Prados",width=10,height=1,background=color,command=self.cambiarColorPrados, fg='white')
        self.prados.place(x=850,y=y1+40)
        self.widgets[1].append(self.prados)
        
        self.tunel = Button(master, text="Túnel",width=10,height=1,background=color,command=self.cambiarColorTunel, fg='white')
        self.tunel.place(x=850+100,y=y1+40)
        self.widgets[1].append(self.tunel)

        self.edificios= Button(master, text="Edificaciones",width=10,height=1,background=color,command=self.cambiarColorEdificios, fg='white')
        self.edificios.place(x=850+100+100,y=y1+40)
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
        self.LuminanciaTunel = Button(master, text="Luminancia Tunel",width=16,height=3,highlightbackground=color1,command=self.reboot)
        self.LuminanciaTunel.place(x=10,y=310+75)
        w = Canvas(master, width=1150, height=650)
        w.create_rectangle(0, 0, 1150, 650, fill="#90AFC5", outline = 'black')
        w.place(x=200,y=25)
    
    def l20_peque(self):
        color= '#336B87'.upper() #Color azúl de botón
        color1= '#336B87'.upper() #Color azúl de botón
        over="#763626"
        master = self.master
        self.subtitle = Label(master, text="Ingrese los parámetros \n conocidos:",width=35,height=3,bg=color,fg='white')
        self.subtitle.place(x=250,y=70)
        self.widgets[2].append(self.subtitle)

        corrimiento = 60
        self.lc_sub =Label(master, text="Lc",width=8,height=3,bg=color,fg='white')
        self.lc_sub.place(x=250,y=70+corrimiento)
        self.widgets[2].append(self.lc_sub )

        self.lc = Entry(font=('Verdana',15),justify='center')
        self.lc.insert(END,0.0)
        self.lc.place(width=180,height=50,x=320,y=70+corrimiento)
        self.widgets[2].append(self.lc)

        self.lc_frame = Frame(width=70,height=50,bg=color)
        self.lc_frame.pack_propagate(0)
        self.cd_m2=Label(self.lc_frame, font=('Verdana',10),text="cd/m^2",bg=color,fg='white',anchor="center")
        self.cd_m2.place(x=8,y=10)
        self.lc_frame.place(x=520,y=70+corrimiento)
        self.widgets[2].append(self.lc_frame)
        
        self.lr_sub =Label(master, text="Lr",width=8,height=3,bg=color,fg='white')
        self.lr_sub.place(x=250,y=70+corrimiento*2)
        self.widgets[2].append(self.lr_sub )

        self.lr = Entry(font=('Verdana',15),justify='center')
        self.lr.insert(END,0.0)
        self.lr.place(width=180,height=50,x=320,y=70+corrimiento*2)
        self.widgets[2].append(self.lr)

        self.lr_frame = Frame(width=70,height=50,bg=color)
        self.lr_frame.pack_propagate(0)
        self.cd_m2_1=Label(self.lr_frame, font=('Verdana',10),text="cd/m^2",bg=color,fg='white',anchor="center")
        self.cd_m2_1.place(x=8,y=10)
        self.lr_frame.place(x=520,y=70+corrimiento*2)
        self.widgets[2].append(self.lr_frame)

        self.le_sub =Label(master, text="Le",width=8,height=3,bg=color,fg='white')
        self.le_sub.place(x=250,y=70+corrimiento*3)
        self.widgets[2].append(self.le_sub )

        self.le = Entry(font=('Verdana',15),justify='center')
        self.le.insert(END,0.0)
        self.le.place(width=180,height=50,x=320,y=70+corrimiento*3)
        self.widgets[2].append(self.le)

        self.le_frame = Frame(width=70,height=50,bg=color)
        self.le_frame.pack_propagate(0)
        self.cd_m2_2=Label(self.le_frame, font=('Verdana',10),text="cd/m^2",bg=color,fg='white',anchor="center")
        self.cd_m2_2.place(x=8,y=10)
        self.le_frame.place(x=520,y=70+corrimiento*3)
        self.widgets[2].append(self.le_frame)

        self.calcular_lth_sub =Label(master, text="Calcular Lth",width=12,height=3,bg=color,fg='white')
        self.calcular_lth_sub.place(x=250,y=70+corrimiento*5)
        self.widgets[2].append(self.calcular_lth_sub )

        self.lth = Entry(font=('Verdana',15),justify='center')
        self.lth.insert(END,0.0)
        self.lth.place(width=180,height=50,x=360,y=70+corrimiento*5)
        self.widgets[2].append(self.lth)

    def distribucionDeLuminarias(self):
        color= '#336B87'.upper() #Color azúl de botón
        color1= '#336B87'.upper() #Color azúl de botón
        over="#763626"
        master = self.master
        self.seccionDelTunel =Label(master, text="Sección del\n Tunel",width=14,height=3,bg=color,fg='white')
        self.seccionDelTunel.place(x=250,y=50)
        self.widgets[3].append(self.seccionDelTunel)
        corrimiento=60
        
        self.alturaLuminarias =Label(master, text="Altura de\n luminarias",width=14,height=3,bg=color,fg='white')
        self.alturaLuminarias.place(x=250,y=50+corrimiento)
        self.widgets[3].append(self.alturaLuminarias)
        
        self.interDistancia =Label(master, text="Inter\n distancia",width=14,height=3,bg=color,fg='white')
        self.interDistancia.place(x=250,y=50+corrimiento*2)
        self.widgets[3].append(self.interDistancia)

        self.anchoDelCamino =Label(master, text="Ancho del\n camino",width=14,height=3,bg=color,fg='white')
        self.anchoDelCamino.place(x=250,y=50+corrimiento*3)
        self.widgets[3].append(self.anchoDelCamino)

        self.numeroCarriles =Label(master, text="# de carriles",width=14,height=3,bg=color,fg='white')
        self.numeroCarriles.place(x=250,y=50+corrimiento*4)
        self.widgets[3].append(self.numeroCarriles)

        self.fotometria =Label(master, text="fotometria",width=14,height=3,bg=color,fg='white')
        self.fotometria.place(x=250,y=50+corrimiento*5)
        self.widgets[3].append(self.fotometria)

        self.rotacionLuminaria =Label(master, text="Rotacion de\n luminaria",width=14,height=3,bg=color,fg='white')
        self.rotacionLuminaria.place(x=250,y=50+corrimiento*6)
        self.widgets[3].append(self.rotacionLuminaria)
        
        self.factorMantenimiento =Label(master, text="Factor de\n mantenimiento",width=14,height=3,bg=color,fg='white')
        self.factorMantenimiento.place(x=250,y=50+corrimiento*7)
        self.widgets[3].append(self.factorMantenimiento)
        corrimiento2=130
        numeroSecciones=5


        for i in range(numeroSecciones):
            self.seccion1 =Label(master, text="Sección "+str(i+1),width=14,height=3,bg=color,fg='white')
            self.seccion1.place(x=270+corrimiento2*(i+1),y=50)
            self.widgets[3].append(self.seccion1)
        for i in range(7):
            for j in range(numeroSecciones):
                self.entry1 = Entry(font=('Verdana',15),justify='center')
                if i!=4:
                    self.entry1.insert(END,0)
                else:
                    self.entry1.insert(END,"RUTA")
                self.entry1.place(width=70,height=38,x=270+corrimiento2*(j+1),y=60+corrimiento*(i+1))
                self.widgets[3].append(self.entry1)
                if i==6:
                    break

def main():
    root = Tk()
    v=Ventana(root)
    root.mainloop()


if __name__ == '__main__':
    main()
        