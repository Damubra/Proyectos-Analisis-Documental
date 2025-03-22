import pytesseract
from PIL import Image
from pdf2image import convert_from_path

# Configura la ruta de Tesseract-OCR
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

#--------------------PARTE 1. PROCESAMIENTO DEL PDF A IMAGEN----------------------------------------------------------------

# Solicita la ruta del archivo PDF
documento = input("Introduce la ruta del archivo: ").strip("'").strip('"')
documento = documento.replace("\\", "/")  # Corrige las rutas con '\'

# Convierte el PDF a una lista de imágenes
jpg = convert_from_path(documento)

# Selecciona la primera página del PDF (puedes iterar sobre todas las páginas si es necesario)
imagen_0 = jpg[0]

#--------------------PARTE 2. PROCESAMIENTO DE LA IMAGEN A TEXTO----------------------------------------------------------------

ancho, alto = imagen_0.size  # Define el tamaño de la imagen
imagen = imagen_0.crop((0, 0, ancho//2, alto))  # Recorta horizontalmente la imagen al 70%

# Extrae el texto de la imagen
texto = pytesseract.image_to_string(imagen, lang="spa")

# Organiza el texto por líneas
lineas = [linea.strip() for linea in texto.split("\n") if linea.strip()]

#--------------------PARTE 3. BUSQUEDA DE LOS DATOS DE INTERES---------------------------------------------------------

nombre_completo = "No Encontrado"
for i, linea in enumerate(lineas):
    if "NOMBRE" in linea:  # Identifica el texto de las primeras tres líneas después de la palabra NOMBRE
        nombre_completo = " ".join(lineas[i+1:i+4])
        break
        
domicilio = "No Encontrado"
for i, linea in enumerate(lineas):  # Identifica el texto de las primeras tres líneas después de la palabra DOMICILIO
    if "DOMICILIO" in linea:
        domicilio = " ".join(lineas[i+1:i+4])
        break

#--------------------PARTE 4. RESULTADOS---------------------------------------------------------------------

print("Nombre:", nombre_completo)
print("Domicilio:", domicilio)