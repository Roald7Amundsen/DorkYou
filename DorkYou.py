from requests_html import HTMLSession
import re
import threading
import time
import os
import signal
import gc
import csv
import sys
from functools import partial
session = HTMLSession()
validador = re.compile(r'^[\d\,]{1,16}\d$')
from multiprocessing import Pool
#barra de carga
from tqdm.auto import tqdm
busqueda = [] 
categoria = []
arregloRetorno = []
#categorias GHDB
queryBusqueda = []
dorks = []
#arreglos para cargar respuestas
userPassword = []
sensibleDir = []
portals = []
onlineDevice = []
vulnserver = []
vulnScan = []
sensibleInfo = []
personalDork = []
escritura = []
CSE1 = "" 
CSE2 = ""
CSE = ""


#BANNER
banner = ''' 
    ██████╗░░█████╗░██████╗░██╗░░██╗  ░██      ██╗░░█████╗░ ██╗░░░░░██╗
    ██╔══██╗██╔══██╗██╔══██╗██║░██╔╝  ░░██    ██╔╝░██╔══██╗ ██║░░░░░██║
    ██║░░██║██║░░██║██████╔╝█████═╝░  ░░░██  ██╔╝░░██║░░██║ ██║░░░░░██║
    ██║░░██║██║░░██║██╔══██╗██╔═██╗░  ░░░░░██╔═╝░░░██║░░██║ ██╚═════██║
    ██████╔╝╚█████╔╝██║░░██║██║░╚██╗  ░░░░░██║░░░░░╚█████╔╝ ╚╗██████╔═╝
    ╚═════╝░░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝  ░░░░░╚═╝░░░░░░╚════╝░░░╚══════╝░░
    
    Made By: Javier Larrea (github.com/roald7amundsen) 
'''

#########################################################
##########                                     ##########
##########        Actualizar   Dorks           ##########
##########                                     ##########
#########################################################

#Funcion para ejecuar scraping de GHDB
def scraping(indice):
    #variables locales categoria y query 
    strCategoria = ""
    strBusqueda = ""
    try:
        #definiendo URL de GHDB
        url = ("https://www.exploit-db.com/ghdb/%d" % (indice))
        r = session.get(url)
        if (str(r)) == "<Response [200]>":
            strQuery = (r.html.find('title')[0].text)
            respuesta2 = (str(strQuery)).split(" - ")
            strCategoria = respuesta2[-1]
            strBusqueda = str(r.html.find('a[href^="https://www.google.com/search?q="]')[0].text)
        else:
            strBusqueda = "retirado"
            strCategoria = "retirado"
    except:
            strBusqueda = "error de Comunicacion"
            strCategoria = "error de Comunicacion"
    finally:
            busqueda.append(strBusqueda)
            categoria.append(strCategoria)
            
        
    return

#Funcion para escribir los nuevos Dorks
def escribir(dorkInicial,dorkFinal):
    i = 0
    file = open("DorksDB.txt", "a", encoding='utf-8')
    while (dorkInicial <= dorkFinal):
        file.write(str(dorkInicial)+"-separador-"+categoria[i]+"-separador-"+busqueda[i]+"\n")
        i=i+1
        dorkInicial=dorkInicial+1
    file.close()
 
        

#funcion encontrar indice ultimo Dork GHDB
def getIndexGHDB():
    session = HTMLSession()
    r = session.get("https://www.exploit-db.com/rss___ghdb.xml")
    page = (r.html.find('item', first=True))
    index = (str(page.find('link', first=True).html).split("/"))[-1]
    return (int(index))

#obtener ultimo indice de dork Local 
def getIndexLOCAL():
    try:
        leerFile = open ( "DorksDB.txt", "r", encoding='utf-8')
        indiceLocal = leerFile.readlines ()
        leerFile.close ()
        ultimaLinea = indiceLocal [len (indiceLocal) -1]
        return (int((str(ultimaLinea).split("-separador-"))[0]))
    except:
        return (0)
 
#funcion principal de actualizacion
def actualizarDorks():
    if (getIndexLOCAL() == 0):
        print ("Archivo base no encontrado")
    elif (getIndexGHDB() == getIndexLOCAL()):
        print ("Dorks Actualizados")
    else:
        totalDorks = (getIndexGHDB() - getIndexLOCAL())
        print ("Actualizando %d Google Dorks" % (totalDorks))
        for i in tqdm(range ((getIndexLOCAL()+1), (getIndexGHDB()+1))):
            scraping(i)                   
        escribir((getIndexLOCAL()+1),getIndexGHDB())
            
#########################################################
##########                                     ##########
##########           Agregar   Dorks           ##########
##########                                     ##########
#########################################################

#funcion escribir dorks personalizados
def escribirDorkPersonal(dorkPersonal):
    file = open("dorksPersonales.txt", "a", encoding='utf-8')
    file.write("NA"+"-separador-"+"Dork personalizado"+"-separador-"+dorkPersonal+"\n")
    file.close()
    
#funcion ingreso de dork personalizado   
def agregarDork():
    print("************Añadir nuevo Dork**************")
    print()
    choice = input("""
    1: Ingresar Dork Personalizado
    2: Salir
                    
    Ingresa tu respuesta: """)

    if choice == "1":
        dorkPersonal = input ("Ingresa tu Dork Personalizado: ")
        confirmacion = input ("El Dork [%s] es correcto ? Y/N  " %(dorkPersonal))
        if confirmacion == "Y" or confirmacion == "y":
            escribirDorkPersonal(dorkPersonal)
            print ("Dork ingresado correctamente")
            agregarDork()
        elif confirmacion == "N" or confirmacion == "n":
            agregarDork()        
    elif choice == "2":
        print(getIndexLOCAL())
        menuPrincipal()
    else:
        print("Debes seleccionar 1 o 2")
        print("Por favor intenta de nuevo")
        agregarDork()


#########################################################
##########                                     ##########
##########           Buscar    Dorks           ##########
##########                                     ##########
#########################################################

 #ingreso de cadenas CSE  
def buscarDork():
    global CSE1
    global CSE2
    global CSE
    print("************Buscar Dorks**************")
    while (True):
        CSE1 = input ("ingrese su primera cadena CSE:  ")
        if (validarCSE(CSE1) == True):
            break
        else:
            print ("Su entrada no corresponde con un enlace CSE")
    while (True):
        CSE2 = input ("ingrese su segunda cadena CSE:  ")
        if (validarCSE(CSE2) == True):
            break
        else:
            print ("Su entrada no corresponde con un enlace CSE")
    CSE = CSE1
    menuBusqueda()


#funcion de carga de dorks en memoria
def cargarDorks():
    clases = []
    archivo1 = open("DorksDB.txt", "r", encoding='utf-8')
    archivo2 = open("dorksPersonales.txt", "r", encoding='utf-8')
    for linea in archivo1.readlines():
        dorks.append(linea)        
    archivo1.close() 
    for linea in archivo2.readlines():
        dorks.append(linea)             
    archivo2.close() 
    #print (dorks)

#funcion de validacion de cadena CSE ingresada
def validarCSE(strCSE):
    validador = re.compile(r'^https\:\/\/cse\.google\.com\/cse\?cx\=[a-z-0-9]{17}$') 
    if (validador.search(strCSE) != None):
        return True
    else:
        return False
        
#funcion de busqueda de dorks por categorias  especificas     
def menuBusqueda():
    while (True):
        arregloRetorno.clear()
        seleccion = input ("""
        Seleccione la categoria de interes
        
        1 usuarios y passwords
        2 directorios sensibles
        3 portales de login
        4 dispositivos en linea
        5 servidores y directorios vulnerables
        6 escaneos de vulnerabilidades
        7 Información sensible
        8 Dorks personalizados
        9 Todos los dorks
        10 Salir

        Nota: puede seleccionar varias categorias separandolas por una coma, ejemplo: 1,5,7.
        
        opcion: """)
        
        if (seleccion == '10'):
            arregloRetorno.append('10')
            print("")
            print("        *****************************       ")
            print("        *       saliendo...         *       ")
            print("        *****************************       ")
            scrapingDork(arregloRetorno)
        elif (len(seleccion)==1):
            try:
                int(seleccion)
                arregloRetorno.append(seleccion)
                print(arregloRetorno)
                scrapingDork(arregloRetorno)
                
            except:
                print("solo se permiten numeros")
                pass
        elif (len(seleccion)>2):    
            if(validador.search(seleccion) != None):
                if '10' in (str(seleccion).split(",")):
                    print ("no se permite ingresar la opcion 10 en una cadena")
                else:
                    print (str(seleccion).split(","))
                    scrapingDork((str(seleccion).split(",")))
            else:
                print("ingrese la cadena de forma correcta")
        else:
            pass
        seleccion = ""

#limpiando arreglos de data cargados para mantener la informacion actualizada       
def limpiarData():
    userPassword.clear()
    sensibleDir.clear()
    portals.clear()
    onlineDevice.clear()
    vulnserver.clear()
    vulnScan.clear()
    sensibleInfo.clear()
    personalDork.clear()
 
#carga de arreglos basados en categorias de GHDB
def  scrapingDork(opciones):
    for opcion in opciones:
        if (opcion == '1'):
            limpiarData()
            cargarCategoria("Files Containing Usernames GHDB Google Dork",userPassword)
            cargarCategoria("Files Containing Passwords GHDB Google Dork",userPassword)
            scrapingCategoria("GHDB_User_Passwords",userPassword)
        if (opcion == '2'):
            limpiarData()
            cargarCategoria("Sensitive Directories GHDB Google Dork",sensibleDir)
            scrapingCategoria("GHDB_Directorios_Sensibles",sensibleDir)
        if (opcion == '3'):
            limpiarData()
            cargarCategoria("Pages Containing Login Portals GHDB Google Dork",portals)
            cargarCategoria("- Pages Containing Login Portals GHDB Google Dork",portals)
            scrapingCategoria("GHDB_Portales_Login",portals)
        if (opcion == '4'):
            limpiarData()
            cargarCategoria("Various Online Devices GHDB Google Dork",onlineDevice)
            scrapingCategoria("GHDB_Dispositivos_Online",onlineDevice)
        if (opcion == '5'):
            limpiarData()
            cargarCategoria("Vulnerable Files GHDB Google Dork",vulnserver)
            cargarCategoria("Vulnerable Servers GHDB Google Dork",vulnserver)
            cargarCategoria("Advisories and Vulnerabilities GHDB Google Dork",vulnserver)
            scrapingCategoria("GHDB_Servidores_Directorios_Vulnerables",vulnserver)
        if (opcion == '6'):
            limpiarData()
            cargarCategoria("Network or Vulnerability Data GHDB Google Dork",vulnScan)
            scrapingCategoria("GHDB_Escaneos_Vulnerabilidades",vulnScan)
        if (opcion == '7'):
            limpiarData()
            cargarCategoria("Files Containing Juicy Info GHDB Google Dork",sensibleInfo)
            cargarCategoria("Web Server Detection GHDB Google Dork",sensibleInfo)
            cargarCategoria("Error Messages GHDB Google Dork",sensibleInfo)
            cargarCategoria("Footholds GHDB Google Dork",sensibleInfo)
            cargarCategoria("Sensitive Online Shopping Info GHDB Google Dork",sensibleInfo)
            cargarCategoria("- Footholds GHDB Google Dork",sensibleInfo)
            scrapingCategoria("GHDB_Informacion_Sensible",sensibleInfo)
        if (opcion == '8'):
            limpiarData()
            cargarCategoria("Dork personalizado",personalDork)
            scrapingCategoria("Dorks_Personales",userPassword)
        if (opcion == '9'):
            limpiarData()
            cargarCategoria("Files Containing Usernames GHDB Google Dork",userPassword)
            cargarCategoria("Files Containing Passwords GHDB Google Dork",userPassword)
            cargarCategoria("Sensitive Directories GHDB Google Dork",sensibleDir)
            scrapingCategoria("GHDB_Directorios_Sensibles",sensibleDir)                    
            cargarCategoria("Pages Containing Login Portals GHDB Google Dork",portals)
            cargarCategoria("- Pages Containing Login Portals GHDB Google Dork",portals)
            scrapingCategoria("GHDB_Portales_Login",portals)
            cargarCategoria("Various Online Devices GHDB Google Dork",onlineDevice)
            scrapingCategoria("GHDB_Dispositivos_Online",onlineDevice)
            cargarCategoria("Vulnerable Files GHDB Google Dork",vulnserver)
            cargarCategoria("Vulnerable Servers GHDB Google Dork",vulnserver)
            cargarCategoria("Advisories and Vulnerabilities GHDB Google Dork",vulnserver)
            scrapingCategoria("GHDB_Servidores_Directorios_Vulnerables",vulnserver)
            cargarCategoria("Network or Vulnerability Data GHDB Google Dork",vulnScan)
            scrapingCategoria("GHDB_Escaneos_Vulnerabilidades",vulnScan)
            cargarCategoria("Files Containing Juicy Info GHDB Google Dork",sensibleInfo)
            cargarCategoria("Web Server Detection GHDB Google Dork",sensibleInfo)
            cargarCategoria("Error Messages GHDB Google Dork",sensibleInfo)
            cargarCategoria("Footholds GHDB Google Dork",sensibleInfo)
            cargarCategoria("Sensitive Online Shopping Info GHDB Google Dork",sensibleInfo)
            cargarCategoria("- Footholds GHDB Google Dork",sensibleInfo)
            scrapingCategoria("GHDB_Informacion_Sensible",sensibleInfo)
            cargarCategoria("Dork personalizado",personalDork)
            scrapingCategoria("GHDB_Informacion_Sensible",personalDork)
        if (opcion == '10'):
            print (banner)
            menuPrincipal()

            
#cargar dorks en un arreglo basado en los categorias de GHDB y las definidas localmente
def cargarCategoria(categoria,categoriaArray):
    for dork in dorks:
        dorkTMP = (str(dork).split("-separador-"))
        if (dorkTMP[1] == categoria):
            categoriaArray.append(dork) 


#busqueda y scraping de resultados por categoria seleccionada
def scrapingCategoria(categoria,categoriaArray):
    j = 0   
    categoriaDorkTMP = []
    resultados = []
    global CSE1
    global CSE2
    global escritura
    indiceTMP = ""
    categoriaTMP = ""
    queryTMPfinal = ""
    dorkInfo = ""
    test = CSE1
    contadorLocal = 0
    pool = Pool(processes=5)
    CSE = CSE1 
    #cargando arreglo temporal
    for linea in categoriaArray:
        contadorLocal = contadorLocal + 1
        if (contadorLocal >= 50):
            if (CSE == CSE1):
                CSE = CSE2
            else:
                CSE = CSE1
            contadorLocal = 0
        indiceTMP = str((str(linea).split("-separador-")[0]))
        categoriaTMP = (str(linea).split("-separador-"))[1]
        queryTMPfinal = CSE + "&q=" + (str(linea).split("-separador-"))[2]
        dorkInfo = indiceTMP + "-separador-" + categoriaTMP + "-separador-" + queryTMPfinal
        categoriaDorkTMP.append(dorkInfo)
    #creacion de procesos simultaneos dentro de la barra de progreso
    with tqdm(total=len(categoriaDorkTMP),position=0, leave=True) as pbar:        
        for _ in pool.imap_unordered(scrapingCSE, categoriaDorkTMP):
            pbar.update(1)  
            resultados.append(_)
        pool.close()
        pool.join()
        pbar.close()
    escribirCSV(categoria,resultados)   
    time.sleep(0.5)
    pool.close()
    pool.join()

    


#funcion de escritura archivo de resultados
def escribirCSV(nombre,arreglo):
    nombreArchivo = nombre + ".csv"
    i = 1
    with open(nombreArchivo, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["N", "Enlace de GHDB", "URLS Encontrados"])
        for linea in arreglo:
            if (str(linea).split("-separador-")[3] != ''):
                writer.writerow([i, ("https://www.exploit-db.com/ghdb/" + str((str(linea).split("-separador-")[0]))), (str(linea).split("-separador-")[3]).replace("-separadorURL-","\n")])
                i = i + 1
       
     
#scraping de CSE y renderizacion de la pagina web
def scrapingCSE(urlTMP):
    dorkURL = (str(urlTMP).split("-separador-"))[2]
    try:
        session = HTMLSession(browser_args=["--no-sandbox","--disable-setuid-sandbox"])
        r = session.get(dorkURL)
        r.html.render(timeout=10)
        urls = r.html.links
        session.close()
        r.close()
    except:
        urls = []
        session.close()
        r.close()
    urlTMP = urlTMP + "-separador-"
    for url in urls:
        if (str(url).find("google") == -1):        
            urlTMP = urlTMP + url + "-separadorURL-"
    return urlTMP



#########################################################
##########                                     ##########
##########           Menu Principal            ##########
##########                                     ##########
#########################################################


def menuPrincipal():
    while (True):
        seleccion = input ("""
        Seleccione una opcion
        
        1 Actualizar Dorks
        2 Agregar Dorks
        3 Ejecutar busqueda de Dorks
        4 Salir
     
        opcion: """)
        
        if (seleccion == '1'):
            actualizarDorks()
        if (seleccion == '2'):
            agregarDork()
        if (seleccion == '3'):
            buscarDork()
        if (seleccion == '4'):  
            sys.exit(0)


if __name__ == '__main__':  
    print (banner)
    cargarDorks()
    menuPrincipal()

