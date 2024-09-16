#! /usr/bin/python3

# 4 campioni per angolo
#from load_test01_S4_45g import cm_list, deg_list # OK
#from load_test02_S4_90g import cm_list, deg_list  # NO: v. foto & excel. confusa fra i due triangoli
#from load_test03_S4_180g import cm_list, deg_list # OK
#from load_test04_S4_225 import cm_list, deg_list # OK, da controllare meglio il grafico differenze-angoli
#from load_test05_S4_315 import cm_list, deg_list # OK, da controllare meglio il grafico differenze-angoli
#from load_test06_S4_345 import cm_list, deg_list  # OK, da controllare meglio il grafico differenze-angoli


#Scansioni di riferimento (da processare)
from stanza_wip.load_refcm_roomNoTria import cm_list_roomNoTria_ref_scan, deg_list_roomNoTria_ref_scan
from stanza_wip.load_refcm_roomTria   import cm_list_roomTria_ref_scan,   deg_list_roomTria_ref_scan

#Scansioni di riferimento processate
cm_list_roomNoTria_ref = list()
deg_list_roomNoTria_ref = list()
cm_list_roomTria_ref = list()
deg_list_roomTria_ref = list()

#Ipotetica stanza con tutti i triangoli agli angoli. Da gradi a distanza
deg2cm_tria = dict()
#Ipotetica stanza senza nessun triangolo agli angoli. Da gradi a distanza
deg2cm_notria = dict()

#Utilizzo delle misure di riferimento e trovo gli oggetti quando ci sono differenze nel pattern
#NOTA! SPEGNI GLI ALTRI SENSORI AD ULTRASUONI (V. API) FANNO INTERFERENZA!!!
# - Il pattern di una stanza completamente vuota, senza uscite
# - Il pattern di una stanza con i quattro angoli tutti occupati dai triangoli
# - Imposta gli angoli di start e stop di ogni triangolo (se una diff ricade in quegli angoli ==> potrebbe esserci un triangolo)
# Confrontando (diff) lo scan attuale con i due pattern dovresti capire dove sono le palline e le uscite

# Come memorizzare i dati di riferimento
# - Fai uno scan lento, in modo che prenda 4 campioni per ogni angolo.
# - Metti i log nel file excel per estrarre distanza e angolo
# - Memorizza i valori excel in load_refcm* (saranno processati da evac_subsamble e evac_smooth per ottenere i dati di riferimento)

# A runtime
# - fai lo scan, anche più veloce (TBC) che prenda almeno un sample per grado.
# - Dai in pasto questo scan a evac_subsamble e evac_smooth. 
# - Confronta il risultato con roomTria_ref per trovare le palline. 
# - Se non trovi nulla confronta con roomNoTria_ref per coprire i casi di palline in angoli dove non ci sono triangoli.

#Dimensione della pallina
sizePallinaCm = 4.5

#Sample da restituire
class Sample:
    def __init__(self, idx_max, idx_left, idx_right, cm_list, deg_list, cm_ref):
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
        self.angle = deg_list[self.idx_sampled] % 360
        # Distanza fra il sample e il riferimento
        self.dist_ref = abs(self.distance - cm_ref[self.idx_sampled])

    def dump(self):
        print("Sample: idx_max: ",self.idx_max,"; idx_left: ",self.idx_left,"; idx_right: ", self.idx_right,
              "; idx_sampled: ", self.idx_sampled, "; width: ", self.width, "; dist_ref: ", self.dist_ref, "; distance: ",self.distance,"; angle: ",self.angle)

#Costruisce i reference data a partire dai campionamenti di riferimento
def evac_build_ref_data():
    global cm_list_roomNoTria_ref
    global deg_list_roomNoTria_ref
    global cm_list_roomTria_ref
    global deg_list_roomTria_ref

    cm_list_roomNoTria_ref, deg_list_roomNoTria_ref = evac_subsamble(cm_list_roomNoTria_ref_scan, deg_list_roomNoTria_ref_scan)
    cm_list_roomNoTria_ref = evac_smooth(cm_list_roomNoTria_ref)

    cm_list_roomTria_ref, deg_list_roomTria_ref = evac_subsamble(cm_list_roomTria_ref_scan, deg_list_roomTria_ref_scan)
    cm_list_roomTria_ref = evac_smooth(cm_list_roomTria_ref)

    cm_list_roomNoTria_ref_scan.clear()
    deg_list_roomNoTria_ref_scan.clear()
    cm_list_roomTria_ref_scan.clear()
    deg_list_roomTria_ref_scan.clear()

    for i in range(len(deg_list_roomNoTria_ref)):
        deg2cm_notria[ deg_list_roomNoTria_ref[i] ] = cm_list_roomNoTria_ref[i]

    for i in range(len(deg_list_roomTria_ref)):
        deg2cm_tria[ deg_list_roomTria_ref[i] ] = cm_list_roomTria_ref[i]


    # print("### cm_list_roomNoTria_ref")
    # for i in range(len(cm_list_roomNoTria_ref)):
    #      print("distCm Angle: ", cm_list_roomNoTria_ref[i], " ", deg_list_roomNoTria_ref[i])

    # print("### cm_list_roomTria_ref")
    # for i in range(len(cm_list_roomTria_ref)):
    #      print("distCm Angle: ", cm_list_roomTria_ref[i], " ", deg_list_roomTria_ref[i])


#Restituisce cm_list e deg_list come liste di 451 elementi (da 0 gradi a 450 gradi)
#Un sample per grado. Media fra i campioni dello stesso grado
#Sottocampiona le distanze. Es. 4 campioni per grado x ==> media dei 4 per il grado x
def evac_subsamble(cm_list, deg_list):
    #Output
    NOVAL = 100000
    sizelist = 451
    cm_list_sampled = [NOVAL] * sizelist
    deg_list_sampled = range(sizelist)

    cm_list_avg = dict()
    for i in range(len(cm_list)):
        key = deg_list[i]
        cm_list_avg.setdefault(key, list())
        cm_list_avg[key].append(cm_list[i])

    for deg in cm_list_avg:
        dist_list = cm_list_avg[deg]
        cm_list_sampled[deg] = sum(dist_list)/len(dist_list)
        
    #Fill empty angles
    for i in range(0, len(cm_list_sampled)):
        if cm_list_sampled[i] == NOVAL:
            cm_list_sampled[i] = cm_list_sampled[i-1] if i >= 0 else 40

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


#Restituisce la pallina / uscita da raggiungere
SPIKE_POS = 0
SPIKE_NEG = 1
def evac_get_spikes(cm_list_ref, cm_list, deg_list, spike_type):

    #Output
    samples_sorted = None

    #In caso di detection delle uscite (SPIKE_NEG), inverto cm_list_ref e cm_list, in modo da 
    # lavorare sempre nel caso SPIKE_POS
    cm_list_ref_local = cm_list_ref
    cm_list_local = cm_list
    if spike_type == SPIKE_NEG:
        cm_list_ref_local = cm_list_local = list()
        dist_ref = cm_list_ref[0]
        for i in range(len(cm_list_ref)):
            cm_list_ref_local[i] = dist_ref + ( dist_ref - cm_list_ref[i])
        
        dist_ref = cm_list[0]
        for i in range(len(cm_list)):
            cm_list_local[i] = dist_ref + ( dist_ref - cm_list[i])
        

    #Analizzo il segnale se la distanza con il pattern di riferimento > soglia
    #soglia_sample_cm = sizePallinaCm
    soglia_sample_cm = 6

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


    num_elem = min(len(cm_list_local),len(cm_list_ref_local))
    cm_diff = list(range(num_elem))
    for i in range(0, num_elem, 1):
        cm_diff[i] = cm_list_ref_local[i] - cm_list_local[i]

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

            sample = Sample(max_idx, idx_left, idx_right, cm_list_local, deg_list,cm_list_ref_local)
            
            samples.append(sample)

            #Cancella questo sample e rifaccio la ricerca
            cm_diff[idx_left:idx_right+1] = [0] * (idx_right - idx_left + 1)


    print("Samples found: ")
    for i in range(0, len(samples), 1):
        samples[i].dump()

    #Choose best sample
    #samples_sorted = sorted(samples, key=lambda x: x.width, reverse=True )
    samples_sorted = sorted(samples, key=lambda x: x.dist_ref, reverse=True )

    print("Samples sorted: ")
    for i in range(0, len(samples_sorted), 1):
        samples_sorted[i].dump()

    return samples_sorted


# Trova pallina
def evac_get_ball(cm_list, deg_list):
    cm_list_sub, deg_list_sub = evac_subsamble(cm_list, deg_list)
    cm_list_smooth = evac_smooth(cm_list_sub)

    # print("### cm_list_smooth")
    # for i in range(len(cm_list_smooth)):
    #     print("distCm Angle: ", cm_list_smooth[i], " ", deg_list_sub[i])

    #Uso come dato di riferimento la stanza con i triangoli su tutti i corner
    samples_sorted = evac_get_spikes(cm_list_roomTria_ref, cm_list_smooth, deg_list_sub, SPIKE_POS)
    
    sample_to_return = samples_sorted[0] if len(samples_sorted) > 0 else None
    if sample_to_return != None:
        print("To return: ")
        sample_to_return.dump()
    else:
        print("No sample found")

    #@@@
    #Se non ho trovato nulla, confronta con il riferimento di stanza senza triangoli,
    # Ma escludi i risultati dove ci sono i triangoli
    # Gli angoli dei triangoli li conosci dalla parte di rilascio del rescue kit!

    return sample_to_return


# Trova uscite
def evac_get_exits(cm_list, deg_list):
    cm_list_sub, deg_list_sub = evac_subsamble(cm_list, deg_list)
    cm_list_smooth = evac_smooth(cm_list_sub)

    #Uso come dato di riferimento la stanza senza triangoli ai corner
    samples_sorted = evac_get_spikes(cm_list_roomNoTria_ref, cm_list_smooth, deg_list_sub, SPIKE_NEG)

    #Escludere le detection trovate sui triangoli (i gradi dei triangoli li conosci dalla parte di rescue kit)
    #Escludere anche l'entrata (trovata dalla funzione di raggiungi_centro_stanza)
    
    sample_to_return = samples_sorted[0] if len(samples_sorted) > 0 else None
    if sample_to_return != None:
        print("To return: ")
        sample_to_return.dump()
    else:
        print("No sample found")

    return sample_to_return



#BUILD REFERENCE DATA
#evac_build_ref_data()
#evac_get_ball_main(cm_list, deg_list)
