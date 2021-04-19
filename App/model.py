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

                'instrumentalness': None,
                'liveness': None,
                'speechiness': None,
                'danceability': None,
                'valence': None,
                'loudness': None,
                'tempo': None,
                'acousticness': None,
                'energy': None,
                'mode': None,
                'key': None,

                "artist_id": None,
                "track_id":None
                }

    for key in analyzer.keys():

        if key == 'tracks': 
            analyzer[key] = lt.newList('SINGLE_LINKED', compareIds)

        else:
            analyzer[key] = om.newMap(omaptype='RBT',
                                comparefunction=compareValues)

    return analyzer

# Funciones para agregar informacion al catalogo
def addTrack(analyzer, track):
    """
    """
    for key in analyzer.keys():

        if key == "tracks":
            lt.addLast(analyzer[key], track)

        else:
            updateIndex(analyzer[key], track, key)

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
    addArtistIndex(datentry, track)
    return map

# Funciones para creacion de datos

def newDataEntry(track):
    """
    Crea una entrada en el indice por valor de característica, es decir en el arbol
    binario.
    """
    entry = {'artistIndex': None, 'lsttracks': None}
    entry['artistIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareArtists)

    entry['lsttracks'] = lt.newList('SINGLE_LINKED', compareValues)
    return entry


def addArtistIndex(datentry, track):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lsttracks']
    lt.addLast(lst, track)
    offenseIndex = datentry['artistIndex']
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
    Crea una entrada en el indice por artista, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'artist_id': None, 'lstartists': None}
    ofentry['artist_id'] = offensegrp
    ofentry['lstartists'] = lt.newList('SINGLELINKED', compareArtists)
    return ofentry

# Funciones de consulta

def tracksSize(analyzer):
    """
    Número de pistas
    """
    return lt.size(analyzer['tracks'])

def artistsSize(analyzer):
    """
    Número de artistas
    """
    return om.size(analyzer['artist_id'])


def uniquetracksSize(analyzer):
    """
    Número de pistas
    """
    return om.size(analyzer['track_id'])

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
    if (value1 == value2):
        return 0
    elif (value1 > value2):
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
