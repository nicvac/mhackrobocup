#! /usr/bin/python3

# Varianza e standard deviation
# https://stackoverflow.com/questions/35583302/how-can-i-calculate-the-variance-of-a-list-in-python

# Vedi dati su 
# https://docs.google.com/spreadsheets/d/1zzRqJC8Go7ISH45u8RZzTldJTufcHLqrFenuDwdnGmc/edit?usp=sharing

# @@@ IDEA: Se non trova nulla (o lo stable count è piccolo), puoi invertire cm_list ed eseguire questo algoritmo in senso inverso
# @@@ MIGLIORAMENTO
# @@@ Ora mi restituisce ad esempio Best samples:  {17: 103, 4: 109, 8: 118}.
#     Significa che il sample 103 ha 17 campioni stabili prima dello spike, ecc...
#     Da questi best sample bisogna individuare il migliore.
#     Alcuni criteri: - il campione con la distanza più vicina con una stabilità sufficientemente grande
#                     - il campione con la stabilità maggiore
#                ---> - il campione la cui distanza risale *stabilmente* di almeno 5 centimetri. 
#                       Restituire il campione nel mezzo fra lo spike detection e lo spike inverso di risalita.

from statistics import variance
from statistics import stdev

from load_p117g import *
#from load_p090g import *

#La distanza fra due campioni entro cui riterli stabili
soglia_stabile_cm = 1
#Rumore: Dimensione della finestra da analizzare
win_size = 5
#Rumore: Se la deviazione standard di win_size campioni supera questa soglia => rumore
soglia_devstd = 1.5
#Rumore: Se vado tre volte su e giù => zigzag, rumore
soglia_updown = 3


samples = list()

i=0
while i < len(cm_list):
    is_smooth = True
    while is_smooth and i<len(cm_list)-1:
        refcm = cm_list[i]
        nextcm = cm_list[i+1]
        is_smooth = (abs(refcm - nextcm) <= soglia_stabile_cm)
        i += 1

    i -= 1
    print("smooth fino a ", i)

    #Individuata una differenza di 1 cm
    #Faccio una analisi in avanti per controllare se si tratta di rumore 

    #Analizzo una finestra in avanti di 5 campioni.
    idx_start = i+1
    idx_stop = idx_start + win_size -1

    if not idx_stop < len(cm_list): break

    #1. Calcolo la deviazione standard sui 5 campioni
    data = list()
    for j in range(idx_start, idx_stop+1, 1):
        data.append( cm_list[j] )
    sample_prev = cm_list[ idx_start-1 ] if idx_start-1 >= 0 else cm_list[ idx_start ]
    sd = stdev(data)

    #2. Controllo inoltre se il segnale fa su e giù (va a zigzag)
    diff = data[0] - sample_prev
    to_up = (diff > 0)
    upanddown = 1 # La prima discesa è data per la prima distanza rilevante con sample_prev rilevata
    for j in range(0, len(data)-1, 1):
        diff_prev = diff
        to_up_prev = to_up
        diff = data[j+1] - data[j]
        to_up = (diff > 0)

        if abs(diff) > soglia_stabile_cm:
            if to_up != to_up_prev:
                upanddown += 1

    isnoise = (sd >= soglia_devstd and upanddown >= soglia_updown)

    print("Sd in [",idx_start,",", idx_stop ,"]: ", sd, "; upanddown", upanddown, "=> isNoise: ", isnoise)

    if isnoise:
        i = idx_stop+1
        # Non butto via tutti i 5 sample della finestra data. Recupero i sample finali se questi si raccordano con il sample dopo la finetra
        procedi = True
        while procedi:
            cm_next = cm_list[i] if i < len(cm_list) else cm_list[-1]
            cm_curr = cm_list[i-1]
            procedi = (abs(cm_next - cm_curr) <= soglia_stabile_cm ) #Questa condizione sarà falsa almeno una volta entro la finetra data (perchè noise=true)
            i = i-1
        
    else:
        idx_sample = i+1 #tranquillo con gli indici, ne ho almeno win_size davanti, per costruzione
        diff = cm_list[idx_sample-1] - cm_list[idx_sample] 
        #Se la differenza la il sample precedente e quello corrente è >= size pallina ==> buon candidato
        if diff >= 5:
            samples.append(idx_sample)
        i +=1

    print("After noise check: i: ", i)

print("Risultato: ", samples)

#Catalogo i sample in base alla loro distanza e alla stabilità dei sample precedenti
samples_best_stable = dict()
samples_best_near = dict()
for idx_s in range(0, len(samples), 1):
    j_curr = samples[idx_s] - 1
    sample_curr = cm_list[j_curr] if j_curr >= 0 else cm_list[0]
    
    is_stable=True
    stable_count = -1 #La prima volta prev e curr combaciano
    while is_stable and j_curr >= 0:
        sample_prev = sample_curr
        sample_curr = cm_list[j_curr]
        is_stable = abs(sample_prev - sample_curr) <= soglia_stabile_cm
        if is_stable:
            stable_count += 1
        j_curr -= 1

    samples_best_stable[stable_count] = samples[idx_s]
    samples_best_near[ samples[idx_s] ] = stable_count


print("Best samples: ", samples_best_stable)

