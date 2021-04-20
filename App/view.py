"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Inicializar catalogo")
    print("2- Cargar información en el catálogo")
    print("3- Conocer eventos de escucha basandose en una característica de contenido y rango determinado")
    print("4- Encontrar pistas para festejar según su rango de energía y bailabilidad")
    print("5- Encontrar pistas para estudiar según su rango de tempo e instrumentalidad")
    print("6- Estudiar los géneros musicales en el catálogo")
    print("0- Salir")

tracksfile = 'user_track_hashtag_timestamp-small.csv'
catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:

        print("\nInicializando....")
        # catalog es el controlador que se usará de acá en adelante
        catalog = controller.init()


    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")
        controller.loadData(catalog, tracksfile)
        
        print('Eventos de escucha cargados: ' + str(controller.tracksSize(catalog)))
        #print('Artistas únicos cargados: ' + str(controller.artistsSize(catalog)))
        print('Pistas de audio únicas cargadas: ' + str(controller.uniquetracksSize(catalog)))


    elif int(inputs[0]) == 3:
        print("Buscando eventos de escucha en un rango determinado para una característica:")

        contentCharacteristic = input("Ingrese la caracterítica de contenido sobre la que desea indagar: ")
        initialValue = input("Valor mínimo de la característica escogida: ")
        finalValue = input("Valor máximo de la característica escogida: ")

        total = controller.getTracksByRange(catalog, initialValue, finalValue, contentCharacteristic)
        print("\nTotal de eventos de escucha en el rango de valores para la característica elegida: " + str(total))


    else:
        sys.exit(0)
sys.exit(0)
