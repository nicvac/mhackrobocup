#! /usr/bin/python3

# Varianza e standard deviation
# https://stackoverflow.com/questions/35583302/how-can-i-calculate-the-variance-of-a-list-in-python

# Vedi dati su 
# https://docs.google.com/spreadsheets/d/1zzRqJC8Go7ISH45u8RZzTldJTufcHLqrFenuDwdnGmc/edit?usp=sharing

from statistics import variance
from statistics import stdev

from load_p117g import *
#from load_p090g import *

samples = list()

i=0
while i < len(cm_list):
    is_smooth = True
    while is_smooth and i<len(cm_list)-1:
        refcm = cm_list[i]
        nextcm = cm_list[i+1]
        is_smooth = (abs(refcm - nextcm) <= 1)
        i += 1

    i -= 1
    print("smooth fino a ", i)

    #Individuata una differenza di 1 cm
    #Faccio una analisi in avanti per controllare se si tratta di rumore 

    #Analizzo una finestra in avanti di 5 campioni.
    w = 5
    idx_start = i+1
    idx_stop = idx_start + w -1

    if not idx_stop < len(cm_list): break

    #1. Calcolo la deviazione standard sui 5 campioni
    data = list()
    for j in range(idx_start, idx_stop+1, 1):
        data.append( cm_list[j] )
    sample_prev = cm_list[ idx_start-1 ] if idx_start-1 >= 0 else cm_list[ idx_start ]
    sd = stdev(data)

    #2. Se sd alta, controllo se il segnale fa su e giù
    diff = data[0] - sample_prev
    to_up = (diff > 0)
    upanddown = 1 # La prima discesa è data per la prima distanza rilevante con sample_prev rilevata
    for j in range(0, len(data)-1, 1):
        diff_prev = diff
        to_up_prev = to_up
        diff = data[j+1] - data[j]
        to_up = (diff > 0)

        if abs(diff) > 1: #1.5:
            if to_up != to_up_prev:
                upanddown += 1

    #isnoise = (sd >= 1.5)
    isnoise = (sd >= 1.5 and upanddown >= 3)

    print("Sd in [",idx_start,",", idx_stop ,"]: ", sd, "; upanddown", upanddown, "=> isNoise: ", isnoise)

    if isnoise:
        i = idx_stop+1
    else:
        idx_sample = i+1 #tranquillo con gli indici ne ho almeno w davanti, per costruzione
        diff = cm_list[idx_sample-1] - cm_list[idx_sample] 
        if diff >= 5:
            #prima del sample scelto voglio almeno x misurazioni stabili
            s_prev_1 = cm_list[idx_sample-1] if idx_sample-1 >= 0 else cm_list[idx_sample]
            s_prev_2 = cm_list[idx_sample-2] if idx_sample-2 >= 0 else cm_list[idx_sample]
            if abs(s_prev_2 - s_prev_1) <= 1:
                samples.append(idx_sample)
            else:
                print("Sample ",idx_sample, " scartato perchè i due sample precedenti instabili")
        i +=1

    print("After noise check: i: ", i)

print("Risultato: ", samples)
