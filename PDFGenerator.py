from create_table_fpdf2 import PDF
from LuminanceCalculator import LuminanceCalculator

class PDFGenerator():
    
    def exportLuminanceData(self, route="LuminanceData", sections=[LuminanceCalculator()]):
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


        for index, section in enumerate(sections):
            pdf.add_page()
            
            # Data Organization:
            inputDataArray = [
                ["Parametro", "Valor"], 
                ["Altura de luminarias", str(section.luminairesHeight)+" m"],
                ["Distancia entre luminarias", str(section.luminairesBetweenDistance)+" m"],
                ["Ancho de la carretera", str(section.roadWidth)+" m"],
                ["Numero de carriles", str(section.roadLanes)],
                ["Distribución de luminarias", "Distribución " + str(section.luminariesDistribution)],            
                ["Saliente de la luminaria sobre la calzada ", str(section.luminariesOverhang) + " m"],
                ["Rotacion de la luminaria ", str(-section.luminairesRotation) + "º"],
                ["Factor de mantenimiento", str(section.roadLanes)],
                ["Ruta de archivo fotométrico", section.IESroute[-20:]]
            ]
            
            # illuminanceMatrix
            illuminanceDataArray = [["" for i in range(3*section.roadLanes+1)] for j in range(section.N+1) ]
            illuminanceDataArray[0][0] = "C/Gamma?"

            for i in range(len(illuminanceDataArray[0])-1):
                illuminanceDataArray[0][i+1] = str(section.StepGamma*i) + "º"
            for i in range(len(illuminanceDataArray)-1):
                illuminanceDataArray[i+1][0] = str(section.StepC*i) + "º"
            for i in range(section.N):
                for j in range(3*section.roadLanes):
                    illuminanceDataArray[i+1][j+1] =  "{:.4f}".format(section.Illuminance[i][j]) + " lx?"

            # illuminance nutshell
            illuminanceNutshellArray = [
                ["Iluminancia maxima", "Iluminancia promedio", "Iluminancia minima", "Factor g1", "Factor g2", "Factor g3" ], 
                ["{:.4f}".format(section.Emax)+" lx?","{:.4f}".format(section.Eav)+" lx?", "{:.4f}".format(section.Emin)+" lx?", "{:.4f}".format(section.g1), "{:.4f}".format(section.g2), "{:.4f}".format(section.g3)]
            ]

            # Luminance
            luminanceDataArray = [[["" for i in range(3*section.roadLanes+1)] for j in range(section.N+1) ] for k in range(section.roadLanes)]
            for i in range(section.roadLanes):
                luminanceDataArray[i][0][0] = "C/Gamma?"

            for i in range(len(luminanceDataArray[0][0])-1):
                for j in range(section.roadLanes):
                    luminanceDataArray[j][0][i+1] = str(section.StepGamma*i) + "º"

            for i in range(len(luminanceDataArray[0])-1):
                for j in range(section.roadLanes):
                    luminanceDataArray[j][i+1][0] = str(section.StepC*i) + "º"

            for i in range(section.roadLanes):
                for j in range(section.N):
                    for k in range(3*section.roadLanes):
                        
                        luminanceDataArray[i][j+1][k+1] =  "{:.4f}".format(section.luminance[i][j][k]) + " cd/m2" 

            # Luminance nutshell

            luminanceNutshellArray = [None for i in range(section.roadLanes)]

            for i in range(section.roadLanes):
                luminanceNutshellArray[i]=[
                    ["Luminancia maxima", "Luminancia promedio", "Luminancia minima"],
                    ["{:.4f}".format(section.Lmax[i])+" lx?","{:.4f}".format(section.Lav[i])+" lx?", "{:.4f}".format(section.Lmin[i])]
                ] 
                
            

            # Section Title
            pdf.set_font("Times", "B", size=20)
            pdf.cell(80, 10, "Sección " + str(index) + ": " + sectionNamesArray[index], border = False)
            pdf.ln(h=10)
            pdf.line(pdf.x,pdf.y,pdf.x+180,pdf.y)
            pdf.ln(5)
            
            # Input Parameters
            pdf.set_font("Times", "B", size=15)
            pdf.cell(80, 10, "Parametros de entrada:", border = False)
            pdf.ln(h=15)

            pdf.set_font("Times", size=10)
            pdf.create_table(table_data = inputDataArray, cell_width="uneven", x_start=20)
            pdf.image("distributionImages/"+str(section.luminariesDistribution)+".jpg", pdf.x + 120, pdf.y - 60, 50)
            pdf.ln()

            # Road
            pdf.set_font("Times", "B", size=15)
            pdf.cell(80, 10, "Luminancia en el pavimento:", border = False)
            pdf.ln(h=15)

            pdf.set_font("Times", size=12)
            pdf.cell(80, 10, "    Matriz de Iluminancia:", border = False)
            pdf.ln(h=8)
            pdf.set_font("Times", size=6)
            pdf.create_table(table_data = illuminanceDataArray, cell_width="even", x_start=20, align_data = "C", align_header="C")
            pdf.ln()

            pdf.set_font("Times", size=12)
            pdf.cell(65, 10, "Resumen Iluminancia:", border = False, align="C")
            pdf.ln(h=8)
            pdf.set_font("Times", size=10)
            pdf.create_table(table_data = illuminanceNutshellArray, cell_width="uneven", x_start="C", align_data = "C", align_header="C")
            pdf.ln()


            for i in range(section.roadLanes):
                pdf.set_font("Times", size=12)
                pdf.cell(80, 10, "    Matriz de Luminancia del observador " + str(i) + ":", border = False)
                pdf.ln(h=8)
                pdf.set_font("Times", size=6)
                pdf.create_table(table_data = luminanceDataArray[i], cell_width="even", x_start=20, align_data = "C", align_header="C")
                pdf.ln()

                pdf.set_font("Times", size=12)
                pdf.cell(65, 10, "Resumen luminancia del observador "+ str(i) + ":", border = False, align="C")
                pdf.ln(h=8)
                pdf.set_font("Times", size=10)
                pdf.create_table(table_data = luminanceNutshellArray[i], cell_width="uneven", x_start="C", align_data = "C", align_header="C")
                pdf.ln()


            # Walls
            pdf.set_font("Times", "B", size=15)
            pdf.cell(80, 10, "Luminancia en las Paredes:", border = False) 
            pdf.ln(h=15)

            pdf.set_font("Times", "I", size=15)
            pdf.cell(80, 10, "      Pendiente por implementar", border = False)
            pdf.ln(h=20)

        pdf.output(route+".pdf")

def main():
    test = PDFGenerator()

    section = LuminanceCalculator(IESroute="Fotometrias/Sit2.ies", luminairesHeight = 4, luminairesBetweenDistance = 40, roadWidth = 10, roadLanes=2, luminairesRotation = 90, luminariesOverhang = 2, luminariesDistribution = 3, Fm= 0.8)
    array = [section,section,section,section,section]
    test.exportLuminanceData(sections= array)


if __name__ == '__main__':
    main()
        
