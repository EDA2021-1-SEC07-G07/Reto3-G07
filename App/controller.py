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
 """

import config as cf
import model
import csv
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
from DISClib.ADT import list as lt

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


def getTracksByRange(analyzer, initialValue, finalValue, contentCharacteristic):
    """
    Retorna el total de crimenes en un rango de fechas
    """
    initialValue = float(initialValue)
    finalValue = float(finalValue)

    return model.getTracksByRange(analyzer, initialValue,
                                  finalValue, contentCharacteristic)


    


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