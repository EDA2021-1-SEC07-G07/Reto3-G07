import matplotlib.pyplot as plt
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp


def print_execution_time(catalog):

    
    times=catalog["times"]
    iterator=lt.iterator(times)
    fig1 = plt.figure("Tiempo y memoria de ejecución distintos procesos")
    fig1.subplots_adjust(hspace=0.5, wspace=0.5)


    list_names=[]
    list_times=[]
    list_memory=[]


    memory_load=0
    time_load=0
    for info in iterator:
        label=info["label"]
        time=info["time"]
        memory=info["memory"]

        if label!="carga":
            list_names.append(label)
            list_times.append(time)
            list_memory.append(memory)

        else:
            memory_load=memory
            time_load=time



    width=0.35 #tamaño barra 

    ax=fig1.add_subplot(2, 1, 1)
    ax.pie([time_load, memory_load],labels=["Time load (ms)\n"+str(time_load), "Memory load (kb)\n"+str(memory_load)])
    ax.set_title("Time and Memory of load ")


    ax = fig1.add_subplot(2, 2, 3)
    ax.bar(list_names,list_times,width)
    ax.set_xlabel("Requerimientos")
    ax.set_ylabel("Time (ms)")
    ax.set_title("Times of execution")
    ax.grid(color='gray', linestyle='dashed', linewidth=1, alpha=0.4)
    # Pintar los ejes pasando por (0,0)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_xticks(list_names)


    ax = fig1.add_subplot(2, 2, 4)
    ax.bar(list_names,list_memory,width)
    ax.set_xlabel("requerimientos")
    ax.set_ylabel("Memory (kb)")
    ax.set_title("Memory of execution")
    ax.grid(color='gray', linestyle='dashed', linewidth=1, alpha=0.4)
    # Pintar los ejes pasando por (0,0)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.set_xticks(list_names)
    plt.show()

