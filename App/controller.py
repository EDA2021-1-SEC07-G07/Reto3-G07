﻿"""
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
 """

import config as cf
import model
import csv
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
import datetime

import time
import tracemalloc
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de pistas

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos

def loadData(analyzer, tracksfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()


    sentimentsfile =  cf.data_dir + "sentiment_values.csv"
    input_sentiments = csv.DictReader(open(sentimentsfile, encoding="utf-8"),
                                delimiter=",")

    temporal_sentiment_dict = m.newMap(numelements=600,
                                     maptype='PROBING')

    for related_sentiment in input_sentiments:
        
        if not m.contains(temporal_sentiment_dict, related_sentiment["hashtag"]):
            m.put(temporal_sentiment_dict, related_sentiment["hashtag"], {})

        m.put(temporal_sentiment_dict, related_sentiment["hashtag"], related_sentiment)



    tracksfile = cf.data_dir + tracksfile
    input_file = csv.DictReader(open(tracksfile, encoding="utf-8"),
                                delimiter=",")
    for track in input_file:
        model.addTrack(analyzer, track)
    

    content_file = cf.data_dir + "context_content_features-small.csv"

    input_content = csv.DictReader(open(content_file, encoding="utf-8"),
                                delimiter=",")

    for content_track in input_content:

        track_id = content_track["track_id"]
        user_id = content_track["user_id"]
        created_at = content_track["created_at"]

        entry = om.get(analyzer["track_id"], track_id)
        dataentry = me.getValue(entry)

        subentry = m.get(dataentry["UserIndex"], user_id)
        datasubentry = me.getValue(subentry)
        
        track_list = datasubentry["lstUsers"]

        for track in lt.iterator(track_list):
            
            if track["created_at"] ==  created_at:
                 
                for column, row in content_track.items():

                    if column not in track.keys():

                        track[column] = row
            

                if m.contains(temporal_sentiment_dict, track["hashtag"]):

                    sentiment_entry = m.get(temporal_sentiment_dict, track["hashtag"])
                    sentiment_data = me.getValue(sentiment_entry)

                    for key, value in sentiment_data.items():
                        
                        track[key] = value

    model.iterateCompleteCatalog(analyzer)


    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)


    addTime(analyzer,delta_time,delta_memory,"carga")


def getReq1(analyzer, initialValue, finalValue, contentCharacteristic):
    """
    Retorna el total de crimenes en un rango de fechas
    """

    try:
        start=start_functions()
        initialValue = float(initialValue)
        finalValue = float(finalValue)

        value=model.getReq1(analyzer, initialValue,
                                    finalValue, contentCharacteristic)
        finish=finish_functions()
        calculus_of_memorytime(analyzer, start, finish, "Req1")
        
        return value
    except:
        return None

def getReq2(analyzer, energyMin, energyMax, danceMin, danceMax):

    try:
        energyMin = float(energyMin)
        energyMax = float(energyMax)

        danceMin = float(danceMin)
        danceMax = float(danceMax)
        
        start=start_functions()
        
        value=model.getReq2(analyzer, energyMin, energyMax, danceMin, danceMax)
        
        finish=finish_functions()
        calculus_of_memorytime(analyzer, start, finish, "Req2")
        
        return value 
    except:
        return None

def getReq3(analyzer, instrumentalnessMin, instrumentalnessMax, tempoMin, tempoMax):
    try:

        start=start_functions()
        
        value=model.getReq3(analyzer, instrumentalnessMin, instrumentalnessMax, tempoMin, tempoMax)
        
        finish=finish_functions()
        calculus_of_memorytime(analyzer, start, finish, "Req3")

        return value
    except:
        return None

def getReq4(analyzer, final_dict):
    try:
        start=start_functions()
        value=model.getReq4(analyzer, final_dict)
        finish=finish_functions()
        calculus_of_memorytime(analyzer, start, finish, "Req4")

        return value 
    except:
        return None

def getReq5(analyzer, initialDate, finalDate, final_dict):

    try:
        start=start_functions()

        initialDate = datetime.datetime.strptime(initialDate, '%H:%M:%S')
        finalDate = datetime.datetime.strptime(finalDate, '%H:%M:%S')
        value=model.getReq5(analyzer, initialDate, finalDate, final_dict)
        
        finish=finish_functions()
        calculus_of_memorytime(analyzer, start, finish, "Req5")

        return value
    except:
        return None


def events_load(analyzer):
    return model.events_load(analyzer)
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def tracksSize(analyzer):
    """
    Numero de pistas leidos
    """
    return model.tracksSize(analyzer)





def artistsSize(analyzer):
    """
    Numero de artistas leidos
    """
    return model.artistsSize(analyzer)

def uniquetracksSize(analyzer):
    """
    Numero de pistas leidos
    """
    return model.uniquetracksSize(analyzer)

def newGeneros():
     
    dict_generos = {

        "Reggae": {"min":60, "max":90},

        "Down-tempo":{"min":70, "max":100},

        "Chill-out": {"min":90, "max":120},

        "Hip-hop": {"min":85, "max":115},

        "Jazz and Funk": {"min":120, "max":125},

        "Pop": {"min":100, "max":130},

        "R&B": {"min":60, "max":80},

        "Rock": {"min":110, "max":140},

        "Metal": {"min":100, "max":160}
    }

    return dict_generos

def addGenero(dict_generos, name, min, max):
     
    return model.addGenero(dict_generos, name, min, max)

#funciones de impresion 

def print_singlelinked(single_list,title):
    return model.print_singlelinked(single_list,title)

def print_req4(tottracks_total, sizetracks_map, uniqueartists_map, tottracks_map):
    return model.print_req4(tottracks_total, sizetracks_map, uniqueartists_map, tottracks_map)


def print_req5(tot_plays, genre_list, top_genre, top_unique_tracks, track_id_sublist):
    return model.print_req5(tot_plays, genre_list, top_genre, top_unique_tracks, track_id_sublist)


# ======================================
# Funciones para medir tiempo y memoria
# ======================================
def addTime(analyzer,time,memory, label):
    return model.addTime(analyzer,time,memory,label)

def start_functions():
    # Funciones de tiempo para las graficas
    delta_time=-1.0
    delta_memory=-1.0
    tracemalloc.start()
    start_time=getTime()
    start_memory=getMemory()
    return  start_time, start_memory

def finish_functions():
    stop_time=getTime()
    stop_memory=getMemory()
    tracemalloc.stop()
    return stop_time, stop_memory

def calculus_of_memorytime(analyzer,start:tuple, finish:tuple, label):
    delta_time=finish[0]-start[0]
    delta_memory=deltaMemory(start[1], finish[1])
    
    print(delta_time,delta_memory)
    addTime(analyzer,delta_time,delta_memory,label)

    return analyzer

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory