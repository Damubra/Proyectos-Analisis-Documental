import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe' #CON ESTA LINEA NOS EVITAMOS LO DEL PATH

#--------------------PARTE 1. PROCESAMIENTO DE LA IMAGEN A TRABAJAR----------------------------------------------------------------

documento = input("Introduce la ruta de la imagen: ").strip("'").strip('"') #INGRESAR LA RUTA DE LA IMAGEN (TIP: IMAGEN > DETALLES)
documento = documento.replace("\\", "/") #CON ESTO CORREGIMOS EL ERROR DE QUE NO SE PUEDEN LEER LAS RUTAS QUE TIENEN '\'
imagen_0 = Image.open(documento) #DEFINIMOS LA VARIABLE IMAGEN

ancho, alto = imagen_0.size #DEFINIMOS EL TAMAÑO DE LA IMAGEN
imagen = imagen_0.crop((0, 0, ancho*0.70, alto))  #RECORTAMOS HORIZONTALMENTE LA IMAGEN AL 70%

texto = pytesseract.image_to_string(imagen, lang="spa") # ESTO ES PARA EXTRAER EL TEXTO ("SPA" ES ESPAÑOL)
lineas = [linea.strip() for linea in texto.split("\n") if linea.strip()] #ORGANIZAMOS EL TEXTO POR LINEAS


#--------------------PARTE 2. BUSQUEDA DE LOS DATOS DE INTERES---------------------------------------------------------

for i, linea in enumerate(lineas):
    if "NOMBRE" in linea: # IDENTIFICA EL TEXTO DE LAS PRIMERAS TRES LINEAS DESPUES DE LA PALABRA NOMBRE
        nombre_completo = " ".join(lineas[i+1:i+4])
        break
        
for i, linea in enumerate(lineas):  # IDENTIFICA EL TEXTO DE LAS PRIMERAS TRES LINEAS DESPUES DE LA PALABRA DOMICILIO
    if "DOMICILIO" in linea:
        domicilio = " ".join(lineas[i+1:i+4])
        break
#----------------PARTE 3. RESULTADOS---------------------------------------------------------------------

print("Nombre:", nombre_completo)
print("Domicilio:", domicilio)