#! /usr/bin/python3

# Varianza e stddev: https://stackoverflow.com/questions/35583302/how-can-i-calculate-the-variance-of-a-list-in-python

from statistics import variance
from statistics import stdev

from load import *

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
    w = 5
    idx_start = i+1
    idx_stop = idx_start + w -1

    if not idx_stop < len(cm_list): break

    data = list()
    for j in range(idx_start, idx_stop+1, 1):
        data.append( cm_list[j] )
    sd = stdev(data)

    isnoise = (sd >= 1.5)
    print("Sd in [",idx_start,",", idx_stop ,"]: ", sd, "; isNoise: ", isnoise)

    if isnoise:
        i = idx_stop+1
    else:
        diff = cm_list[i] - cm_list[i+1] #ne ho almeno w davanti
        if diff > 5:
            samples.append(i+1)
        i +=1

    print("After noise check: i: ", i)

print("Risultato: ", samples)
