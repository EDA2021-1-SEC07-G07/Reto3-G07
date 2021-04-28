"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
from DISClib.Algorithms.Sorting import mergesort as merge
import datetime
import random
assert config
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos


def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todas las pistas
    Se crean indices (Maps) por los siguientes criterios:
    
    -instrumentalness
    -liveness
    -speechiness
    -danceability
    -valence
    -loudness
    -tempo
    -acousticness
    -energy
    -mode
    -key

    Retorna el analizador inicializado.
    """
    analyzer = {'tracks': None,
                "track_id": None, #

                "instrumentalness": None,
                "liveness": None,
                "speechiness": None,
                "danceability": None,
                "valence": None,
                "loudness": None,
                "tempo": None,
                "acousticness": None,
                "energy": None,
                "mode": None,
                "key": None,

                "created_at": None,
                "artist_id": None
}

    for key in analyzer.keys():

        if key == 'tracks': 
            analyzer[key] = lt.newList('ARRAY_LIST', compareIds)

        elif key == "created_at":
            analyzer[key] = om.newMap(omaptype='RBT',
                                comparefunction=compareDates)

        else:
            analyzer[key] = om.newMap(omaptype='RBT',
                                comparefunction=compareValues)

    return analyzer


# funciones para imprimir
def events_load(analyzer):
    tracks=analyzer["tracks"]

    begin=6
    last=lt.size(tracks)-5

    first_last_tracks=lt.newList('ARRAY_LIST')

    for i in range(5):
        first_element=lt.getElement(tracks,begin)
        last_element=lt.getElement(tracks, last)

        lt.addFirst(first_last_tracks,first_element)
        lt.addLast(first_last_tracks,last_element)

        begin-=1
        last+=1

    
    
    return print_singlelinked(first_last_tracks,"PISTAS ")



def print_singlelinked(single_list,title):
    iterator= lt.iterator(single_list)

    max_size=80 #tamaño de impresion 
    upper="-"*(max_size+18)+"\n"
    text = ""
    pos=1

    for i in iterator:
        text += upper+"|{}|\n".format((str(title)+str(pos)).center(max_size+16))+upper
        for j in i:
            a=str(j).center(15)
            b=str(i[j]).center(max_size)
            value="|{}|{}|\n".format(a,b)
            text+=value
            text+=upper    
        pos+=1                
        text+="\n"*3

    return text   



# Funciones para agregar informacion al catalogo

def addGenero(dict_generos, name, min, max):

    dict_generos[name] = {}

    dict_generos[name]["min"] = min

    dict_generos[name]["max"] = max

    return dict_generos
     






def addTrack(analyzer, track, updateId = True):
    """
    """
    for key in analyzer.keys():

        if key == "tracks":
            #Tracks será añadido luego cuando todos los archivos hayan sido fusionados
            pass

        elif key == "track_id" and updateId == True:
            updateIndex(analyzer[key], track, key)

        else:

            try:
                
                if key == "created_at":
                   
                    updateDateIndex(analyzer[key], track, key)

                else:
                    updateArtistIndex(analyzer[key], track, key)

            except Exception:
                pass


    return analyzer


def updateIndex(map, track, characteristic):
    """
    Se toma el valor de la característica de la pista y se busca si ya existe en el arbol
    dicho valor.  Si es asi, se adiciona a su lista de pistas
    y se actualiza el indice de tipos de pistas.

    Si no se encuentra creado un nodo para ese valor en el arbol
    se crea y se actualiza el indice de tipos de pistas
    """
    characteristic_value = track[characteristic]
    entry = om.get(map, characteristic_value)
    if entry is None:
        datentry = newDataEntry(track)
        om.put(map, characteristic_value, datentry)
    else:
        datentry = me.getValue(entry)
    addUserIndex(datentry, track)
    return map

# Funciones para creacion de datos

def newDataEntry(track):
    """
    Crea una entrada en el indice por valor de característica, es decir en el arbol
    binario.
    """
    entry = {'UserIndex': None, 'lsttracks': None}
    entry['UserIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareUsers)

    entry['lsttracks'] = lt.newList('ARRAY_LIST', compareValues)
    return entry


def addUserIndex(datentry, track):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lsttracks']
    lt.addLast(lst, track)
    offenseIndex = datentry['UserIndex']
    offentry = m.get(offenseIndex, track['user_id'])
    if (offentry is None):
        entry = newUserEntry(track['user_id'], track)
        lt.addLast(entry['lstUsers'], track)
        m.put(offenseIndex, track['user_id'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstUsers'], track)

    return datentry

def newUserEntry(offensegrp, crime):
    """
    Crea una entrada en el indice por Usera, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'user_id': None, 'lstUsers': None}
    ofentry['user_id'] = offensegrp
    ofentry['lstUsers'] = lt.newList('SINGLELINKED', compareUsers)
    return ofentry


##### Extra Functions (Después de cargar ambas bases de datos) #################################

def iterateCompleteCatalog(analyzer):

    node_list = om.valueSet(analyzer["track_id"])

    for node in lt.iterator(node_list):

        user_list = m.valueSet(node["UserIndex"])

        for user in lt.iterator(user_list):
        
            track_list = user["lstUsers"]

            for track in lt.iterator(track_list):
                
                lt.addLast(analyzer["tracks"], track)

                addTrack(analyzer, track, False)

            

def updateArtistIndex(map, track, key):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    value = track[key]
  
    entry = om.get(map, value)
    if entry is None:
        datentry = newArtistDataEntry(track)
        om.put(map, value, datentry)
    else:
        datentry = me.getValue(entry)
    addArtistIndex(datentry, track)
    return map


def updateDateIndex(map, track, key):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """

    value = track[key].split()[1]
    
    value = datetime.datetime.strptime(value, '%H:%M:%S')


    entry = om.get(map, value)

    if entry is None:
        datentry = newHashtagDataEntry(track)
        om.put(map, value, datentry)
    else:
        datentry = me.getValue(entry)
    addHashtagIndex(datentry, track)
    return map


def addHashtagIndex(datentry, track):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lsttracks']
    lt.addLast(lst, track)
    offenseIndex = datentry['HashtagIndex']
    offentry = m.get(offenseIndex, track['hashtag'])
    if (offentry is None):
        entry = newHashtagEntry(track['hashtag'], track)
        lt.addLast(entry['lsthashtags'], track)
        m.put(offenseIndex, track['hashtag'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lsthashtags'], track)
    return datentry



def addArtistIndex(datentry, track):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lsttracks']
    lt.addLast(lst, track)
    offenseIndex = datentry['ArtistIndex']
    offentry = m.get(offenseIndex, track['artist_id'])
    if (offentry is None):
        entry = newArtistEntry(track['artist_id'], track)
        lt.addLast(entry['lstartists'], track)
        m.put(offenseIndex, track['artist_id'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstartists'], track)
    return datentry


def newArtistEntry(offensegrp, crime):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'artist_id': None, 'lstartists': None}
    ofentry['artist_id'] = offensegrp
    ofentry['lstartists'] = lt.newList('SINGLELINKED', compareArtists)
    return ofentry


def newHashtagEntry(offensegrp, crime):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'hashtag': None, 'lsthashtags': None}
    ofentry['hashtag'] = offensegrp
    ofentry['lsthashtags'] = lt.newList('SINGLELINKED', compareArtists)
    return ofentry

def newHashtagDataEntry(track):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'HashtagIndex': None, 'lsttracks': None}
    entry['HashtagIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareArtists)
    entry['lsttracks'] = lt.newList('ARRAY_LIST', compareValues)
    return entry


def newArtistDataEntry(track):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'ArtistIndex': None, 'lsttracks': None}
    entry['ArtistIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareArtists)
    entry['lsttracks'] = lt.newList('ARRAY_LIST', compareValues)
    return entry

# Funciones de consulta

def tracksSize(analyzer):
    """
    Número de pistas
    """
    return lt.size(analyzer['tracks'])

def artistsSize(analyzer):
    """
    Número de Useras
    """
    return om.size(analyzer['artist_id'])


def uniquetracksSize(analyzer):
    """
    Número de pistas
    """
    return om.size(analyzer['track_id'])

############################################################################################
# FUNCIONES DE REQUERIMIENTOS #############################################################
###########################################################################################

def getReq1(analyzer, initialValue, finalValue, contentCharacteristic):
    """
    Retorna el numero de eventos de escucha en un rago de fechas.
    """
    node_list = getTrackListByRange(analyzer, initialValue, finalValue, contentCharacteristic)

    sizes = getTreeMapSize(node_list)

    return sizes


def getReq2(analyzer, energyMin, energyMax, danceMin, danceMax):
    """
    Retorna el numero de eventos de escucha en un rago de fechas.
    """
    node_list_energy = getTrackListByRange(analyzer, energyMin, energyMax, "energy")

    node_list_dance = getTrackListByRange(analyzer, danceMin, danceMax, "danceability")

    unique_energy = UniqueMap(node_list_energy)

    unique_dance = UniqueMap(node_list_dance)

    fusion_map = fusionMaps(unique_energy, unique_dance)

    #Gets the number of unique tracks
    fusion_map_size = m.size(fusion_map)

    #Gets 5 random tracks
    random_list = randomSubListFromMap(fusion_map, 5)
    
    return  fusion_map_size, random_list





def getReq3(analyzer, instrumentalnessMin, instrumentalnessMax, tempoMin, tempoMax):
    """
    Retorna el numero de eventos de escucha en un rago de Instrumentalness and Tempo
    """

    node_list_instrumentalness=getTrackListByRange(analyzer,instrumentalnessMin, instrumentalnessMax, "instrumentalness")
    node_list_tempo=getTrackListByRange(analyzer,tempoMin, tempoMax, "tempo")

    unique_instrumentalness=UniqueMap(node_list_instrumentalness)
    unique_tempo=UniqueMap(node_list_tempo)

    fusion_map = fusionMaps(unique_instrumentalness, unique_tempo)

    #Gets the number of unique tracks
    fusion_map_size = m.size(fusion_map)

    #Gets 5 random tracks
    random_list = randomSubListFromMap(fusion_map, 5)
    
    return  fusion_map_size, random_list






def getReq4(analyzer, final_dict):

    tottracks_total = 0
    tottracks_map = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareArtists)

    sizetracks_map = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareArtists)

    uniqueartists_map = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareArtists)

    for key in final_dict.keys():

        genre_name = key

        genre_min = final_dict[key]["min"]
        genre_max = final_dict[key]["max"]

        node_list_tempo = getTrackListByRange(analyzer, genre_min, genre_max, "tempo")

        sizes = getTreeMapSize(node_list_tempo)

        #Primer valor a mostrar -Total de eventos de escucha (por genero)
        tottracks_genre = sizes[0]


        #Total de artistas únicos por género
        uniqueartists_genre = sizes[1]
        m.put(uniqueartists_map, genre_name, uniqueartists_genre)


        m.put(tottracks_map, genre_name, lt.newList('ARRAY_LIST'))

        m.put(sizetracks_map, genre_name, tottracks_genre)


        #Se suma al total de los tracks para los géneros buscados
        tottracks_total += tottracks_genre 

        #Se obtiene el ID de los primeros 10 artistas
        artist_count = 0
        
        for lstdate in lt.iterator(node_list_tempo):
            artist_lst =  m.keySet(lstdate["ArtistIndex"])

            for artist_id in lt.iterator(artist_lst):
            
                entry = m.get(tottracks_map, genre_name)
                datentry = me.getValue(entry)

                lt.addLast(datentry, artist_id)
                artist_count += 1

                if artist_count >= 10:
                    break
            
            if artist_count >= 10:
                break
    
                
    #tottracks_map ---- Hash Map cuya llave es el género y cuyo valor una lista con los 10 ids de los primeros artistas en aparecer 
    
    #sizetracks_map ---- Hash Map cuya llave es el género y cuyo valor es la cantidad de eventos de escucha por género

    #uniqueartists_map ----- Número de artistas únicos para todo lo buscado

    #tottracks_total ----- Eventos de escucha totales

    return tottracks_total, sizetracks_map, uniqueartists_map, tottracks_map
    

def getReq5(analyzer, initialDate, finalDate, final_dict):

    tot_plays = 0

    genre_map = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareArtists)

    genre_list = lt.newList("ARRAY_LIST")
    
    node_list_date = getTrackListByDate(analyzer,initialDate, finalDate, "created_at")

    unique_map =  m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareArtists)


    #Se entra al arbol (ordenado por valor)
    for node in lt.iterator(node_list_date):

        #Se entra a los valores del mapa (lista con tracks)
        track_lst =  node["lsttracks"]

        for track in lt.iterator(track_lst):
            #Se accede a cada track 
            tot_plays += 1

            try:
                tempo = track["tempo"]
            except:
                #En dado caso de que no exista información referente a tempo de un track, se ignora y se pasa al siguiente
                continue

            for key in final_dict.keys():

                if float(tempo) >= final_dict[key]["min"] and float(tempo) <= final_dict[key]["max"]:

                    if m.contains(genre_map, key):

                        entry = m.get(genre_map, key)

                        datentry = me.getValue(entry)

                        datentry += 1

                        m.put(genre_map, key, datentry)

                    else:
                        m.put(genre_map, key, 0)

    

    for genre in lt.iterator(m.keySet(genre_map)):

        mini_list =  lt.newList("ARRAY_LIST")
        
        #Se añade el género como elemento 1 a la mini lista
        lt.addLast(mini_list, genre)

        #Se añade el valor del género como elemento 2 de la minilista
        entry = m.get(genre_map, genre)
        datentry = me.getValue(entry)
        lt.addLast(mini_list, datentry)

        #Se añade la mini lista a la lista con todos los géneros (lista para ser organizada)
        lt.addLast(genre_list, mini_list)

        #Se organiza la lista de generos
        genre_list = listSort(genre_list, "ListItems")


    #Se accede al primer elemento de la lista (género con más reproducciones)
    entry = lt.getElement(genre_list, 1)
    top_genre = lt.getElement(entry, 1)

    #Se itera sobre los tracks del primer género y se encuentran los tracks únicos
    for node in lt.iterator(node_list_date):

        #Se entra a los valores del mapa (lista con tracks)
        hashtag_lst =  m.valueSet(node["HashtagIndex"])

        for hashtag in lt.iterator(hashtag_lst):

            track_list = hashtag["lsthashtags"]

            for track in lt.iterator(track_list):

                try:
                    tempo = track["tempo"]
                except:
                    #En dado caso de que no exista información referente a tempo de un track, se ignora y se pasa al siguiente
                    continue

                track_id = track["track_id"]
                hash_value = track["hashtag"]

                if float(tempo) >= final_dict[top_genre]["min"] and float(tempo) <= final_dict[top_genre]["max"]:

                    #Se revisa si ese track_id ya es la llave del unique_map
                    if not m.contains(unique_map, track_id):

                        #En dado caso de que no lo contenga, añadimos un track a esa llave
                        m.put(unique_map, track_id, lt.newList("ARRAY_LIST"))
                        
                        #Se añade el hash_map como primer valor de la lista dentro del mapa
                        hash_map = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareArtists)
                        entry = m.get(unique_map, track_id)
                        datentry = me.getValue(entry)
                        lt.addFirst(datentry, hash_map)

                

                    entry = m.get(unique_map, track_id)
                    datentry = me.getValue(entry)


                    #Se accede al hash_map (primer elemento)
                    hash_map = lt.getElement(datentry, 1)
                    

                    #Se revisa si el track con hash único ya fue añadido y si este tiene información del vader
                    if not m.contains(hash_map, hash_value):

                        m.put(hash_map, hash_value, None)
                        lt.addLast(datentry, track)
                        

    top_unique_tracks = m.size(unique_map)


    #Ahora unique_map tiene como llave cada track único y dentro una lista con los eventos de reproducción que tienen hashtag distinto
    #Por lo tanto para encontrar el tamaño de esta lista interna determinará cuál tiene más hashtags únicos

    #Se pasa el unique_map a una lista organizable
    track_id_list = m.valueSet(unique_map)

    #Se organiza esa lista por el valor de el tamaño de sus sub-listas
    track_id_list = listSort(track_id_list)

    #Se divide el track_id_list y se obtiene una lista con sus 10 primera canciones
    track_id_sublist = lt.subList(track_id_list, 1, 10)

    #tot_plays ------- Total de reproducciones
    #genre_list ------- Lista ORDENADA con los géneros y sus reproducciones
    #top_genre ------- Nombre del género con más reproducciones
    #top_unique_tracks ------ Número de tracks únicos en el género con más reproducciones

    print(genre_list)
    print(top_genre)
    print(top_unique_tracks)
    print(track_id_sublist)
    #TODO-----Obtener top genre y sacar el top 10 de tracks por número de canciones

##############################################################################################
################# FUNCIONES AUXILIARES #######################################################
##############################################################################################

def getTrackListByRange(analyzer, initialValue, finalValue, contentCharacteristic):

    lst = om.values(analyzer[contentCharacteristic], initialValue, finalValue)

    return lst

def getTrackListByDate(analyzer, initialValue, finalValue, contentCharacteristic):

    lst = om.values(analyzer[contentCharacteristic], initialValue, finalValue)
    return lst



def getTreeMapSize(track_list):

    tottracks = 0
    totartists = 0

    temporal_artist_map =  m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareArtists)

    for lstdate in lt.iterator(track_list):

        #Se buscan los artistas en una nueva tabla de hash para filtrar efectivamente los artistas únicos
        artist_lst =  m.keySet(lstdate["ArtistIndex"])

        for artist_id in lt.iterator(artist_lst):
            
            m.put(temporal_artist_map, artist_id, None)

        #Se obiene el tamaño (artistas únicos) del mapa temporal creado
        totartists = m.size(temporal_artist_map)

        tottracks += lt.size(lstdate['lsttracks'])

    return tottracks, totartists


def UniqueMap(lst):

    unique_map =  m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareArtists)

    #Se entra al arbol (ordenado por valor)
    for node in lt.iterator(lst):

        #Se entra a los valores del mapa (lista con tracks)
        track_lst =  node["lsttracks"]

        for track in lt.iterator(track_lst):
            #Se accede al track ID de cada track 
            track_id = track["track_id"]

            #Se revisa si ese track_id ya es la llave del unique_map

            if not m.contains(unique_map, track_id):

                #En dado caso de que no lo contenga, añadimos un track a esa llave
                m.put(unique_map, track_id, track)

    #De esta forma se retorna un diccionario cuyas llaves son los track_id y dentro de estas existe la información de un track único
    return unique_map

    
def fusionMaps(map1, map2):
    #Fusiona mapas que tienen el mismo tipo de llave en un nuevo mapa único

    fusion_map =  m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareArtists)

    map1_keys = m.keySet(map1)

    for key in lt.iterator(map1_keys):

        if m.contains(map2, key):
            
            common_key = key 
            
            entry = m.get(map2, key)

            common_value = me.getValue(entry)

            m.put(fusion_map, common_key, common_value)

    return fusion_map


def randomSubListFromMap(map, numelements):

    value_list = m.valueSet(map)
    map_size = m.size(map)

    random_list = lt.newList('ARRAY_LIST', compareIds)

    for n in range(numelements):

        random_pos = random.randint(1,map_size)

        random_item = lt.getElement(value_list, random_pos)

        lt.addLast(random_list, random_item)

    return random_list

# Funciones utilizadas para comparar elementos dentro de una lista
def compareIds(id1, id2):
    """
    Compara dos pistas
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareValues(value1, value2):
    """
    Compara dos valores de una característica específica
    """
    try:
        value1 = float(value1) 
        value2 = float(value2) 

    except Exception:
        pass


    if (value1 == value2):
        return 0
    elif (value1 > value2):
        return 1
    else:
        return -1

def compareUsers(User1, User2):
    """
    Compara dos tipos de crimenes
    """
    offense = me.getKey(User2)
    if (User1 == offense):
        return 0
    elif (User1 > offense):
        return 1
    else:
        return -1

def compareArtists(artist1, artist2):
    """
    Compara dos tipos de crimenes
    """
    offense = me.getKey(artist2)
    if (artist1 == offense):
        return 0
    elif (artist1 > offense):
        return 1
    else:
        return -1

def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareListItems(i1, i2):

    item1 = lt.getElement(i1, 2)
    item2 =  lt.getElement(i2, 2)

    return float(item1) > float(item2)


def compareListSize(i1, i2):

    item1 = lt.size(i1)
    item2 =  lt.size(i2)

    return float(item1) > float(item2)



# Funciones de ordenamiento
def listSort(lst, comparefunction = None):

    if comparefunction == "ListItems":

        sorted_list = merge.sort(lst,compareListItems)
    
    else:
        sorted_list = merge.sort(lst,compareListSize)

    return sorted_list