import pandas as pd
from pathlib import Path
import subprocess

excel = input("Introduce la ruta del excel que contiene el nombre de los expedientes: ").strip("'").strip('"') 
excel = excel.replace("\\", "/")

bd = pd.read_excel(excel)

nuevas_filas = []

for _, row in bd.iterrows():
    for version in ["E01", "E03", "E05"]:
        nueva = row.copy()
        nueva["NOMBRE DEL EXPEDIENTE"] = nueva["NOMBRE DEL EXPEDIENTE"].replace("E01", version)
        nuevas_filas.append(nueva)

bd_final = pd.DataFrame(nuevas_filas)

if "NOMBRE DEL EXPEDIENTE" not in bd_final.columns:
    raise ValueError(f"La columna NOMBRE DEL EXPEDIENTE no se encuentra en el Excel. Verifica que sea el archivo sea correcto")

lista = bd_final["NOMBRE DEL EXPEDIENTE"].dropna().tolist()

#-----

carpeta = Path(input("Introduce la ruta de la carpeta que necesitas actualizar: ").strip("'").strip('"'))

archivos_ordenados = sorted(
    [f for f in carpeta.iterdir() if f.is_file()],
    key=lambda x: x.stat().st_mtime
)

nombres_ordenados = [f.name for f in archivos_ordenados]

#-----

if len(nombres_ordenados) != len(lista):
    raise ValueError("Cuidado: la cantidad de archivos en la carpeta no coincide con la cantidad de nombres nuevos")

# Preparar las listas como arrays de PowerShell
originales_ps = "@(" + ", ".join(f'"{nombre}"' for nombre in nombres_ordenados) + ")"
nuevos_ps     = "@(" + ", ".join(f'"{nombre}"' for nombre in lista) + ")"
carpeta_ps    = str(carpeta).replace("\\", "\\")

# Generar el comando final de PowerShell
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
