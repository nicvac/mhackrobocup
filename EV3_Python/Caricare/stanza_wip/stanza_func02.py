#! /usr/bin/python3


# 1 campione per angolo
#from load_p090g import *  # 155
#from load_p090g_b import * # 85g
#from load_p120g import * # 114g
#from load_p125g import * # 0g
#from load_p128g import * # 120g
#from load_p129g import * # 113g
#from load_p050g import * # 57g

# 4 campioni per angolo
from load_S4p090g import *
#from load_S4p240g import *

from collections import defaultdict

from load_refcm import cm_list_ref, deg_list_ref

#Utilizzo delle misure di riferimento e trovo gli oggetti quando ci sono differenze nel pattern
#@@@ Misurare: SPEGNI GLI ALTRI SENSORI AD ULTRASUONI (V. API) FANNO INTERFERENZA!!!
# - Il pattern di una stanza completamente vuota, senza uscite
# - Il pattern di una stanza con i quattro angoli tutti occupati dai triangoli
# - Imposta gli angoli di start e stop di ogni triangolo (se una diff ricade in quegli angoli ==> potrebbe esserci un triangolo)
# Confrontando (diff) lo scan attuale con i due pattern dovresti capire dove sono le palline e le uscite

# Come memorizzare i dati di riferimento
# Fai uno scan lento, in modo che prenda 4 campioni per ogni angolo.
# Dai questo scan in pasto a evac_subsamble e evac_smooth per memorizzare i pattern di riferimento (stanza vuota e con angoli)
# A runtime fai lo scan, anche più veloce (TBC) che prenda almeno un sample per grado.
# Dai in pasto questo scan a evac_subsamble e evac_smooth. Confronta il risultato con i pattern di riferimento.

#Dimensione della pallina
sizePallinaCm = 4.5

#Sample da restituire
class Sample:
    def __init__(self, idx_max, idx_left, idx_right, cm_list, deg_list):
        # idx sample, distanza massima
        self.idx_max = idx_max
        # idx sample, quando la differenza è piccola a sinistra
        self.idx_left = idx_left
        # idx sample, quando la differenza è piccola a destra
        self.idx_right = idx_right
        # idx del sample scelto (media fra idx_left e idx_right)
        #self.idx_sampled = round((idx_left+idx_right)/2)
        self.idx_sampled = idx_max 
        # Larghezza della campana 
        self.width = idx_right - idx_left
        # Distanza misurata sul campione
        self.distance = cm_list[self.idx_sampled]
        # Angolo calcolato per questo campione
        self.angle = deg_list[self.idx_sampled]

    def dump(self):
        print("Sample: idx_max: ",self.idx_max,"; idx_left: ",self.idx_left,"; idx_right: ", self.idx_right,
              "; idx_sampled: ", self.idx_sampled, "; width", self.width, "; distance: ",self.distance,"; angle: ",self.angle)

#Un sample per grado. Media fra i campioni dello stesso grado
#Sottocampiona le distanze. Es. 4 campioni per grado x ==> media dei 4 per il grado x
def evac_subsamble(cm_list, deg_list):
    #Output
    cm_list_sampled = list()
    deg_list_sampled = list()

    cm_list_avg = defaultdict(list)
    for i in range(len(cm_list)):
        cm_list_avg[deg_list[i]].append(cm_list[i])

    for deg, dist_list in cm_list_avg.items():
        cm_list_sampled.append( sum(dist_list)/len(dist_list) )
        deg_list_sampled.append(deg)

    return cm_list_sampled, deg_list_sampled

#Smooth. Riduco il rumore. Ogni campione viene ottenuto dalla media di 5 elementi.
def evac_smooth(cm_list):
    #Output
    cm_list_smooth = [0, 0]

    i = 2
    while i <= len(cm_list)-1 -2:
        elems=[ cm_list[i-2], cm_list[i-1], cm_list[i], cm_list[i+1], cm_list[i+2] ]
        cm_list_smooth.append(sum(elems)/len(elems))
        i += 1

    #Completo gli elementi vuoti di elems
    cm_list_smooth[0] = cm_list_smooth[2]
    cm_list_smooth[1] = cm_list_smooth[2]
    cm_list_smooth.append(cm_list_smooth[-1])
    cm_list_smooth.append(cm_list_smooth[-1])

    return cm_list_smooth

    

#Restituisce la pallina da raggiungere
def evac_get_ball(cm_list, deg_list):

    #Output
    sample_to_return = None

    #Analizzo il segnale se la distanza con il pattern di riferimento > soglia
    soglia_sample_cm = sizePallinaCm

    #Stabilità fra campioni successivi nell'analisi discendente e ascendente
    soglia_campana_cm = 1

    #Funzioni di supporto
    def evac_get_campana():
        
        idx_left = max_idx
        stop = False
        while not stop:
            idx_left -= 1
            descending = False
            interesting = False
            inlist = (idx_left >= 0)
            if inlist:
                descending = cm_diff[idx_left] <= cm_diff[idx_left+1] + soglia_campana_cm
                interesting = (cm_diff[idx_left] >= soglia_sample_cm)

            stop = not inlist or not descending or not interesting
        idx_left += 1

        idx_right = max_idx
        stop = False
        while not stop:
            idx_right += 1
            descending = False
            interesting = False
            inlist = (idx_right <= len(cm_diff)-1)
            if inlist:
                descending = cm_diff[idx_right] <= cm_diff[idx_right-1] + soglia_campana_cm
                interesting = (cm_diff[idx_right] >= soglia_sample_cm)

            stop = not inlist or not descending or not interesting
        idx_right -= 1
        
        return idx_left, idx_right

    samples=list()


    num_elem = min(len(cm_list),len(cm_list_ref))
    cm_diff = list(range(num_elem))
    for i in range(0, num_elem, 1):
        cm_diff[i] = cm_list_ref[i] - cm_list[i]

    found = True
    while found:

        #Trovo la distanza più alta
        max_value = max(cm_diff)
        max_idx = cm_diff.index(max_value)

        #Se la differenza è maggiore della pallina può essere un sample interessante
        found = (max_value >= soglia_sample_cm)
        if found: 
            #Catturo tutta la campana, a destra e sinistra
            idx_left, idx_right = evac_get_campana()

            sample = Sample(max_idx, idx_left, idx_right, cm_list, deg_list)
            
            samples.append(sample)

            #Cancella questo sample e rifaccio la ricerca
            cm_diff[idx_left:idx_right+1] = [0] * (idx_right - idx_left + 1)


    print("Samples found: ")
    for i in range(0, len(samples), 1):
        samples[i].dump()

    #Choose best sample
    samples_sorted = sorted(samples, key=lambda x: x.width, reverse=True )

    print("Samples sorted: ")
    for i in range(0, len(samples_sorted), 1):
        samples_sorted[i].dump()

    sample_to_return = samples_sorted[0] if len(samples_sorted) > 0 else None
    if sample_to_return != None:
        print("To return: ")
        sample_to_return.dump()
    else:
        print("No sample found")

    return sample_to_return

# Trova pallina
def evac_get_ball_main():
    cm_list_sub, deg_list_sub = evac_subsamble(cm_list, deg_list)

    # for i in range(len(cm_list_sub)):
    #     print("distCm Angle: ", cm_list_sub[i], " ", deg_list_sub[i])

    cm_list_smooth = evac_smooth(cm_list_sub)
    evac_get_ball(cm_list_smooth, deg_list_sub)


evac_get_ball_main()

