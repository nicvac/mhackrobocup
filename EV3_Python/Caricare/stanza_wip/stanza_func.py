#! /usr/bin/python3

# Varianza e standard deviation
# https://stackoverflow.com/questions/35583302/how-can-i-calculate-the-variance-of-a-list-in-python

# Vedi dati su 
# https://docs.google.com/spreadsheets/d/1zzRqJC8Go7ISH45u8RZzTldJTufcHLqrFenuDwdnGmc/edit?usp=sharing

# @@@ IDEA: Se non trova nulla (o lo stable count è piccolo), puoi invertire cm_list ed eseguire questo algoritmo in senso inverso

#from statistics import variance
#from statistics import stdev

#from load_p090g import *
#from load_p090g_b import * # <<--- NO
from load_p120g import *
#from load_p125g import *
#from load_p128g import *
#from load_p129g import *
#from load_p050g import *


def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/n # in Python 2 use sum(data)/float(n)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def stddev(data, ddof=0):
    """Calculates the population standard deviation
    by default; specify ddof=1 to compute the sample
    standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/(n-ddof)
    return pvar**0.5

class Sample:
    def __init__(self, idx_spike_down):
        # idx sample quando il segnale va giù (più vicino) 
        self.idx_spike_down = idx_spike_down
        # idx sample quando il segnale risale (si allontana)
        self.idx_spike_up = 0
        # idx del sample scelto (idx_spike_down o media fra idx_spike_down e idx_spike_up)
        self.idx_sampled = idx_spike_down
        # quanti campioni stabili ci sono fra idx_spike_down e idx_spike_up (differenza fra i due idx)
        self.stable_curr = 0
        # quanti campioni stabili ho prima dello spike down
        self.stable_prev = 0
        # Distanza misurata sul campione
        self.distance = 0
        # Angolo calcolato per questo campione
        self.angle = 0


    def dump(self):
        print("Sample: idx_spike_down: ",self.idx_spike_down,"; idx_spike_up: ",self.idx_spike_up,"; idx_sampled: ", self.idx_sampled,
              "; stable_curr: ", self.stable_curr, "; stable_prev: ",self.stable_prev,"; distance: ",self.distance,"; angle: ",self.angle)

def evac_get_sample(cm_list, deg_list):

    #Output
    sample_to_return = None

    #La distanza fra due campioni entro cui riterli stabili
    soglia_stabile_cm = 2
    #Rumore: Dimensione della finestra da analizzare
    win_size = 5
    #Rumore: Se la deviazione standard di win_size campioni supera questa soglia => rumore
    soglia_devstd = 2.5
    #Rumore: Se vado tre volte su e giù => zigzag, rumore
    soglia_updown = 3
    #Durande la detection dello spike di risalita, la distanza fra due campioni entro cui riterli stabili
    soglia_stabile_risalita_cm = 2
    #Durande la detection dello spike di risalita, la distanza fra l'ultimo campione stabile e lo spike di risalita
    soglia_spike_risalita_cm = 3.5

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
        sd = stddev(data)

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
                samples.append(Sample(idx_sample))
            i +=1

        print("After noise check: i: ", i)


    #Calcolo per ogni sample trovato il contatore di stabilità sui sample precedenti
    for idx_s in range(0, len(samples), 1):
        j_curr = samples[idx_s].idx_spike_down - 1
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

        samples[idx_s].stable_prev = stable_count



    # Per ogni sample trovato calcolo la risalita (e nel caso ricalcolo idx_sampled)
    for i in range(0, len(samples), 1):
        sample = samples[i]
        idx = sample.idx_spike_down
        found = False
        while not found and idx+1 < len(cm_list):
            sample_curr = cm_list[idx]
            sample_next = cm_list[idx+1]
            sample_curr_idx = idx
            found = abs(sample_curr - sample_next) > soglia_stabile_risalita_cm
            idx += 1
        
        if found:
            if sample_next >= sample_curr + soglia_spike_risalita_cm:
                sample.idx_spike_up = sample_curr_idx
                sample.idx_sampled = round( (sample.idx_spike_up + sample.idx_spike_down) /2)
            else:
                sample.idx_spike_up = -1
        else:
            sample.idx_spike_up = -1

    # Per ogni sample trovato recupero l'algolo e calcolo self.stable_curr
    for i in range(0, len(samples), 1):
        sample = samples[i]
        sample.stable_curr = sample.idx_spike_up - sample.idx_spike_down
        sample.distance = cm_list[sample.idx_sampled]
        sample.angle = deg_list[sample.idx_sampled]

    print("\nCONF: ",
    "soglia_stabile_cm: ",soglia_stabile_cm,
    "; win_size: ", win_size,
    "; soglia_devstd: ", soglia_devstd,
    "; soglia_updown: ", soglia_updown,
    "; soglia_stabile_risalita_cm: ", soglia_stabile_risalita_cm,
    "; soglia_spike_risalita_cm: ", soglia_spike_risalita_cm
    )

    print("Samples found: ")
    for i in range(0, len(samples), 1):
        samples[i].dump()

    #Choose best sample
    samples_sorted = sorted(samples, key=lambda x: x.stable_curr, reverse=True )

    print("Samples sorted: ")
    for i in range(0, len(samples_sorted), 1):
        samples_sorted[i].dump()

    found = False
    sample = None
    i=0
    while not found and i<len(samples_sorted):
        sample = samples_sorted[i]
        found = sample.idx_spike_up != -1
        i += 1

    sample_to_return = sample
    if sample_to_return != None:
        print("To return: ")
        sample.dump()
    else:
        print("No sample found")

    return sample_to_return

evac_get_sample(cm_list, deg_list)
