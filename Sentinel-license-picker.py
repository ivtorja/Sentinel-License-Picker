import urllib.request, urllib.parse, urllib.error
import xml.etree.ElementTree as ET
import re
import shutil
import os
import ctypes
from configparser import ConfigParser

# URL del Sentinel
url = 'http://localhost:6002/keyinfo.xml'

# Path del archivo init
default_ini_path = r"C:\nx_license_checker.ini"

# Parseamos el archivo init
config = ConfigParser()
config.read(default_ini_path)

# Path de las licencias
license_path = r"C:\NX\NX Lic"

# Path de NX
nx_path = r"C:\Siemens\NX\NXBIN\ugraf.exe"

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

# Cargamos las rutas del archivo init 
if os.path.exists(default_ini_path):
  license_path = config.get('paths', 'licensepath')
  nx_path = config.get('paths', 'nxpath')
  print(license_path)
  print(nx_path)
else:
    ctypes.windll.user32.MessageBoxW(0, "No encuentro el archivo de inicialización :(", "Errorcito", 1)

# Borramos el archivo "licencia.txt" si existe
if os.path.exists(license_path + "\\licencia.txt"):
  os.remove(license_path + "\\licencia.txt")
  print("Borrao")
else:
  print("The file does not exist")

# Buscamos dentro de la carpeta especificada la licencia que queremos activar
directory = os.listdir(license_path)
searchstring = licencia

for fname in directory:
    if os.path.isfile(license_path + os.sep + fname):
        # Full path
        f = open(license_path + os.sep + fname, 'r')

# Y la copiamos como "licencia.txt"
        if searchstring in f.read():
            print('%s' % fname)
            newPath = shutil.copy(license_path + '\\%s' % fname, license_path + "\\licencia.txt")

# Cerramos los archivos abiertos
f.close()

# Ejecutamos NX
os.startfile(nx_path)
        