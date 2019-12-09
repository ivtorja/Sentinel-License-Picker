import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import re
import shutil
import os
import ctypes

# URL del Sentinel
url = 'http://localhost:6002/keyinfo.xml'

# Path del archivo init
default_ini_path = "C:\\nx_license_checker.ini"

# Path de las licencias
user_input = "C:\\NX\\NX Lic"

# Cargar el archivo XML en memoria
uh = urllib.request.urlopen(url)
data = uh.read()

# Buscamos el TAG "KeyDetails" dentro del XML
tree = ET.fromstring(data)
lst = tree.findall('KeyDetails')

# Buscamos el tag "SerialNumber"
counts = tree.findall('.//SerialNumber')

# Extraemos el serial number del Sentinel insertado sin los ceros iniciales
for each in counts:
    string = each.text
    licencia = re.sub(r"\b0{3}","",string)

# Como cada usuario tiene las licencias en una carpeta distinta, 
# creamos o buscamos un archivo de inicialización con esa ruta    

if os.path.exists(default_ini_path):
  init = open(default_ini_path,"r")
  # Tomamos la ruta como variable
  user_input = init.read()
  init.close()
  print(user_input)
else:
    ctypes.windll.user32.MessageBoxW(0, "No encuentro el archivo de inicialización :(", "Errorcito", 1)

# Borramos el archivo "licencia.txt" si existe
if os.path.exists(user_input + "\\licencia.txt"):
  os.remove(user_input + "\\licencia.txt")
  print("Borrao")
else:
  print("The file does not exist")

# Buscamos dentro de la carpeta especificada la licencia que queremos activar
directory = os.listdir(user_input)
searchstring = licencia

for fname in directory:
    if os.path.isfile(user_input + os.sep + fname):
        # Full path
        f = open(user_input + os.sep + fname, 'r')

# Y la copiamos como "licencia.txt"
        if searchstring in f.read():
            print('%s' % fname)
            newPath = shutil.copy(user_input + '\\%s' % fname, user_input + "\\licencia.txt")

# Cerramos los archivos abiertos
f.close()
        