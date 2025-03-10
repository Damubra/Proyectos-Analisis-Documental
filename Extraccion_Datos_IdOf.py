import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

#--------------------PARTE 1. PROCESAMIENTO DE LA IMAGEN A TRABAJAR----------------------------------------------------------------

documento = None #INGRESAR LA RUTA DE LA IMAGEN (TIP: IMAGEN > DETALLES)

imagen = Image.open(documento) #DEFINIMOS LA VARIABLE IMAGEN
texto = pytesseract.image_to_string(imagen, lang="spa") # ESTO ES PARA EXTRAER EL TEXTO ("SPA" ES ESPAÑOL)
lineas = [linea.strip() for linea in texto.split("\n") if linea.strip()] #ORGANIZAMOS EL TEXTO POR LINEAS

#--------------------PARTE 2. BUSQUEDA DE LOS DATOS DE INTERES---------------------------------------------------------

for i, linea in enumerate(lineas):
    if "NOMBRE" in linea:
        # IDENTIFICA EL TEXTO DE LAS PRIMERAS TRES LINEAS DESPUES DE LA PALABRA NOMBRE
        nombre_completo = " ".join(lineas[i+1:i+4])
        break
#----------------PARTE 3. RESULTADOS---------------------------------------------------------------------

print("Nombre extraído:", nombre_completo)
