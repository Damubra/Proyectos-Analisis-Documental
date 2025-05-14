import pandas as pd
from pathlib import Path
import subprocess

excel = input("Introduce la ruta del excel que contiene el nombre de los expedientes: ").strip("'").strip('"') 
excel = excel.replace("\\", "/")

bd = pd.read_excel(excel)

if "ID SOLICITUD" not in bd.columns:
    print("Error: La columna 'ID SOLICITUD' no se encuentra en el archivo Excel.")
    exit()

lista1 = bd["ID SOLICITUD"].dropna().tolist() #----- No la utlicé por el momento ------
lista2 = bd["NOMBRE DEL EXPEDIENTE"].dropna().tolist()

carpeta = Path(input("Introduce la ruta de la carpeta que necesitas actualizar: ").strip("'").strip('"'))

archivos_ordenados = sorted(
    [f for f in carpeta.iterdir() if f.is_file()],
    key=lambda x: int(x.stem) if x.stem.isdigit() else x.stem  # Ordenamos nombres de menor a mayor
)

nombres_ordenados = [f.name for f in archivos_ordenados]

#-----

if len(nombres_ordenados) != len(lista2):
    raise ValueError("Cuidado: la cantidad de archivos en la carpeta no coincide con la cantidad de nombres nuevos")

# Preparamos las listas como arrays de PowerShell
originales_ps = "@(" + ", ".join(f'"{nombre}"' for nombre in nombres_ordenados) + ")"
nuevos_ps     = "@(" + ", ".join(f'"{nombre}"' for nombre in lista2) + ")"
carpeta_ps    = str(carpeta).replace("\\", "\\")

# Generamos el comando final de PowerShell
comando_ps = f"""
$originales = {originales_ps}
$nuevos = {nuevos_ps}
$carpeta = "{carpeta_ps}"

for ($i = 0; $i -lt $originales.Count; $i++) {{
    Rename-Item -Path (Join-Path $carpeta $originales[$i]) -NewName "$($nuevos[$i]).$($originales[$i].Split('.')[-1])"
}}
"""

ejecucion = subprocess.run(["powershell", "-Command", comando_ps], capture_output=True, text=True)
print(ejecucion.stdout)



### ---------------------------------------------------------###
### ---------------------------------------------------------###
### ----------- Creado por B. Daniel Muñoz Bravo ----------- ###
### -------------------- 05/05/2025  ------------------------###
### ---------------------------------------------------------###
### ---------------------------------------------------------###
### -------Administración Financiera Coma S.A. de C.V.-------###
### ---------------------------------------------------------###
### ---------------------------------------------------------###
### ---------------------------------------------------------###
### ---------------------------------------------------------###