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
    print("7- Indicar el género musical más escuchado en un tiempo determinado")
    print("0- Salir")

tracksfile = 'user_track_hashtag_timestamp-small.csv'
catalog = None
final_dict = controller.newGeneros()

def iterAddGenre(dict_generos):

    for genero in dict_generos.keys():

        print("-{}".format(genero))

    add_genre = input("¿Desea añadir un nuevo género? S / N: ")

    if add_genre.lower() == "s":

        new_name = input("El nuevo nombre de su género será: ")
        new_min = input("El BPM mínimo de su género será: ")
        new_max = input("El BPM máximo de su género será: ")
            
        new_dict = controller.addGenero(dict_generos, new_name, new_min, new_max)

        return iterAddGenre(new_dict)

    return dict_generos

def print_singlelinked(single_list, title):
    text=controller.print_singlelinked(single_list, title)
    print(text)


"""
Menu principal
"""


def Req1():

    print("\n"*2)
    print(("*"*15+"Requerimiento 1"+"*"*15).center(50),"\n"*2+"Buscando eventos de escucha en un rango determinado para una característica:".center(50),"\n"*5)
    contentCharacteristic = input("Ingrese la caracterítica de contenido sobre la que desea indagar: ").lower()
    initialValue = input("Valor mínimo de la característica escogida: ")
    finalValue = input("Valor máximo de la característica escogida: ")

    total = controller.getReq1(catalog, initialValue, finalValue, contentCharacteristic)
    if total!=None:
        print("\nTotal de eventos de escucha en el rango de valores para la característica elegida: " + str(total[0]))
        print("\nTotal de artistas únicos en el rango de valores para la característica elegida: " + str(total[1]))

    else:
        print("\n"*5,"Error seleccionando los eventos de escucha, intente nuevamente")
        Req1()
             

def Req2():
    print("Buscando pistas únicas para festejar...")

    minEnergy = input("Valor mínimo de la característica energy: ")
    maxEnergy = input("Valor máximo de la característica energy: ")

    minDance = input("Valor mínimo de la característica danceability: ")
    maxDance = input("Valor máximo de la característica danceability: ")

    total = controller.getReq2(catalog, minEnergy, maxEnergy ,  minDance, maxDance)
    if total!=None:
        pistas_unicas_size = total[0]
        pistas_aleatorias = total[1]

        print("Total de pistas únicas dentro de los parametros establecidos: {}".format(pistas_unicas_size), "\n"*3)

        text_total=print_singlelinked(pistas_aleatorias,"Pistas")
        print(text_total)
    else:
        print("\n"*5,"Error seleccionando las pistas para festejar, intente nuevamente")
        Req2()


def Req3():
    print("\n"*2)
    print(("*"*40+"Requerimiento 3"+"*"*40).center(80),"\n"*2+"Buscando eventos de escucha en un rango determinado para Instrumentalness and Tempo:".center(50),"\n"*5)


    minInstrumentalness = input("Valor mínimo de la característica Instrumentalness: ")
    maxInstrumentalness = input("Valor máximo de la característica Instrumentalness: ")

    minTempo = input("Valor mínimo de la característica Tempo: ")
    maxTempo = input("Valor máximo de la característica Tempo: ")

    total = controller.getReq3(catalog, minInstrumentalness,maxInstrumentalness,minTempo,maxTempo)
    if total!=None:
        pistas_unicas_size = total[0]
        pistas_aleatorias = total[1]

        print("Total de pistas únicas dentro de los parametros establecidos: {}".format(pistas_unicas_size), "\n"*3)

        text_total=print_singlelinked(pistas_aleatorias,"Pista Instrumentalness and Tempo")
        print(text_total)

    else:
        print("\n"*5,"Error seleccionando los rangos de Instrumentalness and Tempo  pistas para festejar, intente nuevamente")
        Req3()



    

def Req4():

    search_dict = {}

    dict_generos = controller.newGeneros()
    print("Preparandose para estudiar los géneros musicales en el catalogo...")

    print("Géneros musicales dispobles para realizar su búsqueda: ")

    new_dict = iterAddGenre(dict_generos)

    genre_names = input("Por favor ingrese los géneros sobre los que desea buscar separados por una coma: ")

    genre_list = genre_names.split(",")

    for genre in genre_list:

        genre = genre.strip()

        if genre in new_dict.keys():

            search_dict[genre] = new_dict[genre]
            

    total = controller.getReq4(catalog, search_dict)

    #TODO- BORRAR-##########################
    if total!=None:

        text=controller.print_req4(total[0],total[1],total[2],total[3])
        print(text)

    else:
        print("Error")
    ###############################

def Req5():

    print("\n"*2)
    print(("*"*40+"Requerimiento 5"+"*"*40).center(80),"\n"*2+"Buscando el género musical más escuchado en un tiempo determinado:".center(50),"\n"*5)
    
    initialDate = input("Hora Inicial (H:M:S): ")
    finalDate = input("Hora Final (H:M:S): ")

    total = controller.getReq5(catalog, initialDate, finalDate, final_dict)

    if total !=None:

        pass

    else:
        print("Error escribir hora inicial y final nievamente")
        Req5()







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
        print('Artistas únicos cargados: ' + str(controller.artistsSize(catalog)))
        print('Pistas de audio únicas cargadas: ' + str(controller.uniquetracksSize(catalog)))

        text_load=controller.events_load(catalog)
        print("\n",text_load)


    elif int(inputs[0]) == 3:
        Req1()
        
    elif int(inputs[0]) == 4:
        Req2()

    elif int(inputs[0]) == 5:
        Req3()

    elif int(inputs[0]) == 6:
        Req4()

    elif int(inputs[0]) == 7:
        Req5()



    else:
        sys.exit(0)
sys.exit(0)



            