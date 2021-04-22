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

                "artist_id": None
}

    for key in analyzer.keys():

        if key == 'tracks': 
            analyzer[key] = lt.newList('SINGLE_LINKED', compareIds)

        else:
            analyzer[key] = om.newMap(omaptype='RBT',
                                comparefunction=compareValues)

    return analyzer





# Funciones para agregar informacion al catalogo

def addGenero(dict_generos, name, min, max):

    dict_generos[name] = {}

    dict_generos[name]["min"] = min

    dict_generos[name]["max"] = max

    return dict_generos
     


def events_load(analyzer):
    tracks=analyzer["tracks"]

    begin=6
    last=lt.size(tracks)-5

    first_last_tracks=lt.newList('SINGLE_LINKED')

    for i in range(5):
        first_element=lt.getElement(tracks,begin)
        last_element=lt.getElement(tracks, last)

        lt.addFirst(first_last_tracks,first_element)
        lt.addLast(first_last_tracks,last_element)

        begin-=1
        last+=1
    text = ""
    
    iterator=lt.iterator(first_last_tracks)

    max_size=80 #tamaño de impresion 
    upper="-"*(max_size+18)+"\n"
    
    pos=1
    for i in iterator:
        text += upper+"|{}|\n".format(("VIDEO "+str(pos)).center(max_size+16))+upper
        for j in i:
            a=str(j).center(15)
            b=str(i[j]).center(max_size)
            value="|{}|{}|\n".format(a,b)
            text+=value
            text+=upper    
        pos+=1                
        text+="\n"*3

    return text



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

    entry['lsttracks'] = lt.newList('SINGLE_LINKED', compareValues)
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


def newArtistDataEntry(track):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'ArtistIndex': None, 'lsttracks': None}
    entry['ArtistIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareArtists)
    entry['lsttracks'] = lt.newList('SINGLE_LINKED', compareValues)
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


def getReq3(analyzer, final_dict):

    tottracks_total = 0
    tottracks_map = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareArtists)

    sizetracks_map = m.newMap(numelements=30,
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

        m.put(tottracks_map, genre_name, lt.newList('SINGLE_LINKED'))

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

                
    #sizetracks_map ---- Hash Map cuya llave es el género y cuyo valor es la cantidad de tracks
    
    #sizetracks_map ---- Hash Map cuya llave es el género y cuyo valor una lista con los 10 ids de los primeros artistas en aparecer

    #TODO ----- Número de artistas únicos para todo lo buscado
    #TODO ----- Tracks únicos de todo lo buscado






##############################################################################################
################# FUNCIONES AUXILIARES #######################################################
##############################################################################################

def getTrackListByRange(analyzer, initialValue, finalValue, contentCharacteristic):

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

    random_list = lt.newList('SINGLE_LINKED', compareIds)

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

# Funciones de ordenamiento
