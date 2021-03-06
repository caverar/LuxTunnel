from create_table_fpdf2 import PDF
from LuminanceCalculator import LuminanceCalculator
from L20Calculator import L20Calculator

import numpy as np

class PDFGenerator():
    
    def exportData(self, l20=L20Calculator(), route="LuminanceData.pdf", luminanceTunnelEntranceImageRoute="L20DefaultImage.jpg", sections=[LuminanceCalculator()]):
        """
        Export Luminance Data to a PDF file
        """

        # Call to PDF library
        pdf = PDF(format = "A4", unit="mm")
        pdf.set_left_margin(15)
        pdf.set_right_margin(15)
        pdf.alias_nb_pages()
        pdf.set_auto_page_break(auto=True, margin=15)
        

        sectionNamesArray = ["Zona de acceso",
                             "Zona de umbral",
                             "Zona de transición",
                             "Zona del interior",
                             "Zona de salida"]

        # L20
        pdf.add_page()

        # Data Organization:
        # L20 Input
        mountainTarrain = ["No", "Si"]
        cardinalDirection = ["Norte", "Occidente", "Sur", "Oriente"]
        L20InputDataArray = [
            ["Parametro", "Valor"], 
            ["Velocidad maxima en la entrada del túnel", str(l20.maxSpeed)+" km/h"],
            ["Pendiente de la carretera", str(l20.slope)+"º"],
            ["Terreno montañoso", mountainTarrain[l20.MountainousTerrain]],
            ["Orientación hacia el túnel", cardinalDirection[l20.cardinalDirection]],
            ["Hemisferio", cardinalDirection[2*l20.Hemisphere]],
            ["Porcentaje de area de cielo","{:.2f}".format(l20.percentArray[0]*100) +" %"],
            ["Porcentaje de area de pavimento","{:.2f}".format(l20.percentArray[1]*100) +" %"],
            ["Porcentaje de area de rocas","{:.2f}".format(l20.percentArray[2]*100) +" %"],
            ["Porcentaje de area de construcciones","{:.2f}".format(l20.percentArray[3]*100) +" %"],
            ["Porcentaje de area de nieve","{:.2f}".format(l20.percentArray[4]*100) +" %"],
            ["Porcentaje de area de vegetacion","{:.2f}".format(l20.percentArray[5]*100) +" %"],
        ]

        L20OutputDataArray = [
            ["Parametro", "Valor"],
            ["Distancia de parada","{:.4f}".format(l20.SD) + " m"],
            ["Factor k","{:.2f}".format(l20.k)],
            ["Fricción sobre el pavimento mojado","{:.2f}".format(l20.f)],
            ["Luminancia cielo (Lc)", "{:.4f}".format(l20.Lc) + " cd/m2"],
            ["Luminancia carretera (Lr)", "{:.4f}".format(l20.Lr) + " cd/m2"],
            ["Luminancia rocas (LeR)", "{:.4f}".format(l20.LeRocks) + " cd/m2"],
            ["Luminancia construcciones (LeB)", "{:.4f}".format(l20.LeBuildings) + " cd/m2"],
            ["Luminancia nieve (LeS)", "{:.4f}".format(l20.LeSnow) + " cd/m2"],
            ["Luminancia vegetacion (LeM)", "{:.4f}".format(l20.LeMeadows) + " cd/m2"],
            ["Luminancia umbral, entrada del túnel (Lth)", "{:.4f}".format(l20.Lth) + " cd/m2"],


              
        
        ]



        # Section Title
        pdf.set_font("Times", "B", size=20)
        pdf.cell(80, 10, "L20: Calculo de Luminancia Umbral", border = False)
        pdf.ln(h=10)
        pdf.line(pdf.x,pdf.y,pdf.x+180,pdf.y)
        pdf.ln(5)
        
        # Input Parameters
        pdf.set_font("Times", "B", size=15)
        pdf.cell(80, 10, "Parametros de entrada:", border = False)
        pdf.ln(h=15)
        pdf.set_font("Times", size=9)
        pdf.create_table(table_data = L20InputDataArray, cell_width="uneven", x_start=20)
        pdf.image(luminanceTunnelEntranceImageRoute, pdf.x + 105, pdf.y - 70, 70)
        pdf.ln()

        # Output Parameters
        pdf.set_font("Times", "B", size=15)
        pdf.cell(80, 10, "Resultados:", border = False)
        pdf.ln(h=15)
        pdf.set_font("Times", size=9)
        pdf.create_table(table_data = L20OutputDataArray, cell_width="uneven", x_start=20)
        pdf.ln()


        # Tunnel Sections
        for index, section in enumerate(sections):
            pdf.add_page()
            
            # Data Organization:

            

            # luminanceInput
            inputDataArray = [
                ["Parametro", "Valor"], 
                ["Altura de luminarias", str(section.luminairesHeight)+" m"],
                ["Distancia entre luminarias", str(section.luminairesBetweenDistance)+" m"],
                ["Ancho de la carretera", str(section.roadWidth)+" m"],
                ["Numero de carriles", str(section.roadLanes)],
                ["Distribución de luminarias", "Distribución " + str(section.luminariesDistribution)],            
                ["Saliente de la luminaria sobre la calzada ", str(section.luminariesOverhang) + " m"],
                ["Rotacion de la luminaria ", str(-section.luminairesRotation) + "º"],
                ["Factor de mantenimiento", str(section.Fm)],
                ["Ruta de archivo fotométrico", section.IESroute[-20:]]
            ]
            
            # illuminanceMatrix
            illuminanceDataArray = [["" for i in range(3*section.roadLanes+1)] for j in range(section.N+1) ]
            illuminanceDataArray[0][0] = "x/y"

            for i in range(len(illuminanceDataArray[0])-1):
                illuminanceDataArray[0][i+1] = str(section.StepGamma*i) + " m"
            for i in range(len(illuminanceDataArray)-1):
                illuminanceDataArray[i+1][0] = str(section.StepC*i) + " m"
            for i in range(section.N):
                for j in range(3*section.roadLanes):
                    illuminanceDataArray[i+1][j+1] =  "{:.4f}".format(section.Illuminance[i][j]) + " lx"

            # illuminance nutshell
            illuminanceNutshellArray = [
                ["Iluminancia maxima", "Iluminancia promedio", "Iluminancia minima", "g1(Uh)  minimo/promedio", "g2 minimo/maximo", "g3 promedio/maximo" ], 
                ["{:.4f}".format(section.Emax)+" lx","{:.4f}".format(section.Eav)+" lx", "{:.4f}".format(section.Emin)+" lx", "{:.4f}".format(section.g1) +" lx",
                 "{:.4f}".format(section.g2) +" lx", "{:.4f}".format(section.g3) + " lx"]
            ]

            # Luminance
            luminanceDataArray = [[["" for i in range(3*section.roadLanes+1)] for j in range(section.N+1) ] for k in range(section.roadLanes)]
            for i in range(section.roadLanes):
                luminanceDataArray[i][0][0] = "x/y"

            for i in range(len(luminanceDataArray[0][0])-1):
                for j in range(section.roadLanes):
                    luminanceDataArray[j][0][i+1] = "{:.2f}".format(section.Py[0][i]) + " m"

            for i in range(len(luminanceDataArray[0])-1):
                for j in range(section.roadLanes):
                    luminanceDataArray[j][i+1][0] = "{:.2f}".format(section.Px[i][0]) + " m"

            for i in range(section.roadLanes):
                for j in range(section.N):
                    for k in range(3*section.roadLanes):
                        
                        luminanceDataArray[i][j+1][k+1] =  "{:.4f}".format(section.luminance[i][j][k]) + " cd/m2" 

            # Luminance nutshell

            luminanceNutshellArray = [None for i in range(section.roadLanes)]

            for i in range(section.roadLanes):
                luminanceNutshellArray[i]=[
                    ["Luminancia maxima", "Luminancia promedio", "Luminancia minima", "g1(Uo)  min/promedio", "g2    min/maximo", "g3 promedio/max", "U. Longitudinal (Ul)"],
                    ["{:.4f}".format(section.Lmax[i])+" cd/m2","{:.4f}".format(section.Lav[i])+" cd/m2", "{:.4f}".format(section.Lmin[i]) +" cd/m2", 
                     "{:.4f}".format(section.Lg1[i])+ " cd/m2", "{:.4f}".format(section.Lg2[i])+ " cd/m2", "{:.4f}".format(section.Lg3[i]) + " cd/m2",
                     "{:.4f}".format(section.ul[i]) + " cd/m2"]
                ] 
            
            
            globalLuminanceNutshellArray =[
                ["Luminancia maxima", "Luminancia promedio", "Luminancia minima", "g1(Uo)  min/promedio", "g2    min/maximo", "g3 promedio/max", "U. Longitudinal (Ul)"],
                ["{:.4f}".format(np.mean(section.Lmax))+" cd/m2","{:.4f}".format(np.mean(section.Lav))+" cd/m2", "{:.4f}".format(np.mean(section.Lmin)) +" cd/m2", 
                 "{:.4f}".format(np.mean(section.Lg1) )+ " cd/m2", "{:.4f}".format(np.mean(section.Lg2))+ " cd/m2", "{:.4f}".format(np.mean(section.Lg3)) + " cd/m2",
                 "{:.4f}".format(np.mean(section.ul)) + " cd/m2"]
            ]

            

            # Section Title
            pdf.set_font("Times", "B", size=20)
            pdf.cell(80, 10, "Sección " + str(index+1) + ": " + sectionNamesArray[index], border = False)
            pdf.ln(h=10)
            pdf.line(pdf.x,pdf.y,pdf.x+180,pdf.y)
            pdf.ln(5)
            
            # Input Parameters
            pdf.set_font("Times", "B", size=15)
            pdf.cell(80, 10, "Parametros de entrada:", border = False)
            pdf.ln(h=15)

            pdf.set_font("Times", size=10)
            pdf.create_table(table_data = inputDataArray, cell_width="uneven", x_start=20)
            pdf.image("distributionImages/"+str(section.luminariesDistribution)+".jpg", pdf.x + 110, pdf.y - 65, 70)
            pdf.ln()

            # Road
            pdf.set_font("Times", "B", size=15)
            pdf.cell(80, 10, "Resultados de iluminación:", border = False)
            pdf.ln(h=15)

            pdf.set_font("Times", size=12)
            pdf.cell(80, 10, "    Matriz de Iluminancia:", border = False)
            pdf.ln(h=8)
            pdf.set_font("Times", size=6)
            pdf.create_table(table_data = illuminanceDataArray, cell_width="even", x_start=20, align_data = "C", align_header="C")
            pdf.set_font("Times", "I", size=7)
            pdf.multi_cell(0, 10, "\"x\" = coordenadas longitudinales, depende de la distancia entre luminarias y su distribución. \"y\" =  coordenadas transversales, depende del ancho de la carretera.", border = False,  align="C")
            pdf.ln(h=1)



            pdf.set_font("Times", size=12)
            pdf.cell(45, 10, "Resumen Iluminancia:", border = False, align="C")
            pdf.ln(h=8)
            pdf.set_font("Times", size=10)
            pdf.create_table(table_data = illuminanceNutshellArray, cell_width="even", x_start="C", align_data = "C", align_header="C")
            pdf.set_font("Times", "I", size=7)
            pdf.multi_cell(0, 10, "\"g1\", \"g2\" y  \"g3\"  son la relación de uniformidad, calculada con concientes entre la iluminancia minima, maxima y promedio.", border = False,  align="C")
            pdf.ln(h=1)


            for i in range(section.roadLanes):
                pdf.set_font("Times", size=12)
                pdf.cell(80, 10, "    Matriz de Luminancia del observador " + str(i+1) + ":", border = False)
                pdf.ln(h=8)
                pdf.set_font("Times", size=6)
                pdf.create_table(table_data = luminanceDataArray[i], cell_width="even", x_start=20, align_data = "C", align_header="C")
                pdf.set_font("Times", "I", size=7)
                pdf.multi_cell(0, 10, "\"x\" = coordenadas longitudinales, depende de la distancia entre luminarias y su distribución. \"y\" =  coordenadas transversales, depende del ancho de la carretera.", border = False,  align="C")
                pdf.ln(h=1)

                pdf.set_font("Times", size=12)
                pdf.cell(75, 10, "Resumen Luminancia del observador "+ str(i+1) + ":", border = False, align="C")
                pdf.ln(h=8)
                pdf.set_font("Times", size=10)
                pdf.create_table(table_data = luminanceNutshellArray[i], cell_width="even", x_start="C", align_data = "C", align_header="C")
                pdf.set_font("Times", "I", size=7)
                pdf.multi_cell(0, 10, "\"g1\", \"g2\" y  \"g3\"  son la relación de uniformidad, calculada con concientes entre la luminancia minima, maxima y promedio.", border = False,  align="C")
                pdf.ln(h=1)


            pdf.set_font("Times", size=12)
            pdf.cell(60, 10, "Promedio de los observadores:", border = False, align="C")
            pdf.ln(h=8)
            pdf.set_font("Times", size=10)
            pdf.create_table(table_data = globalLuminanceNutshellArray, cell_width="even", x_start="C", align_data = "C", align_header="C")
            pdf.set_font("Times", "I", size=7)
            pdf.multi_cell(0, 10, "\"g1\", \"g2\" y  \"g3\"  son la relación de uniformidad, calculada con concientes entre la luminancia minima, maxima y promedio.", border = False,  align="C")
            pdf.ln(h=1)
            

            # Walls
            pdf.set_font("Times", "B", size=15)
            pdf.cell(80, 10, "Luminancia en las Paredes:", border = False) 
            pdf.ln(h=15)

            pdf.set_font("Times", "I", size=15)
            pdf.cell(80, 10, "      Pendiente por implementar", border = False)
            pdf.ln(h=20)

        pdf.output(route)

def main():
    test = PDFGenerator()
    l20 = L20Calculator(maxSpeed = 60, slope = 0.5, fiftyPercentThreshold= False,  cardinalDirection = 0, Hemisphere = 0, 
                        percentArray = [0.10,0.10,0.10,0.10,0.10,0.20,0.30])
    section0 = LuminanceCalculator(IESroute="Fotometrias/Sit1.ies", luminairesHeight = 4, luminairesBetweenDistance = 20, roadWidth = 10, roadLanes=2, luminairesRotation = 90, luminariesOverhang = 2, luminariesDistribution = 1, Fm= 0.8)
    section1 = LuminanceCalculator(IESroute="Fotometrias/Sit2.ies", luminairesHeight = 4, luminairesBetweenDistance = 40, roadWidth = 10, roadLanes=2, luminairesRotation = 90, luminariesOverhang = 2, luminariesDistribution = 3, Fm= 0.8)
    section2 = LuminanceCalculator(IESroute="Fotometrias/Sit2.ies", luminairesHeight = 4, luminairesBetweenDistance = 40, roadWidth = 10, roadLanes=2, luminairesRotation = 0, luminariesOverhang = 2, luminariesDistribution = 3, Fm= 0.8)
    section3 = LuminanceCalculator(IESroute="Fotometrias/Sit2.ies", luminairesHeight = 4, luminairesBetweenDistance = 40, roadWidth = 10, roadLanes=2, luminairesRotation = 90, luminariesOverhang = 2, luminariesDistribution = 2, Fm= 0.8)
    section4 = LuminanceCalculator(IESroute="Fotometrias/Sit2.ies", luminairesHeight = 4, luminairesBetweenDistance = 40, roadWidth = 10, roadLanes=2, luminairesRotation = 90, luminariesOverhang = 2, luminariesDistribution = 3, Fm= 0.8)

    array = [section0,section1,section2,section3,section4]
    test.exportData(l20=l20,sections= array)


if __name__ == '__main__':
    main()
        
