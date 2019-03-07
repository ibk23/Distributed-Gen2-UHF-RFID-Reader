from __future__ import print_function
import subprocess
import tempfile
import re 
import csv
import numpy as np
import epc_finder_filter

#delete csv file



freq_1='910'
freq_2='912'
power_1='8'
power_2='3'
no_repeats=1
delay='0'
SINGLE_USRP=True

#Ensure this is set in reader*.py as well. 
TX_FAKE_DATA = True

if TX_FAKE_DATA:
    with open("dataoutput.csv","w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['freq_1', 'freq_2', 'power_1', 'power_2','delay']+
                        ["RN16s_run"+str(d+1) for d in range(no_repeats)])
else:
    with open("dataoutput.csv","w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['freq_1', 'freq_2', 'power_1', 'power_2','delay']+
                        ["run"+str(d+1)+"_successes" for d in range(no_repeats)]+
                        ["run"+str(d+1)+"_attempts" for d in range(no_repeats)]+
                        ["RN16s_run"+str(d+1) for d in range(no_repeats)])

def delay_sweep(start, fin, no_steps):
    global delay
    for delay_samples in np.linspace(start, fin, no_steps):
        delay = str(int(delay_samples))
        run_test(freq_1,freq_2,power_1,power_2)

def frequency_sweep(start, fin, no_steps):
    print("Running test with params",freq_1,power_1,power_2)
    for freq_2 in np.linspace(start, fin, no_steps):
        freq_2=str(freq_2)
        print("freq_2 is ",freq_2)
        run_test(freq_1,freq_2,power_1,power_2)

def twod_power_sweep(start_1, fin_1, no_steps_1,start_2, fin_2, no_steps_2):
    global power_1
    for power_1 in np.linspace(start_1, fin_1, no_steps_1):
        power_1=str(power_1)
        power_sweep(start_2, fin_2, no_steps_2)

def power_sweep(start, fin, no_steps):
    print("Running test with params",freq_1,freq_2,power_1)
    for power_2 in np.linspace(start, fin, no_steps):
        power_2=str(power_2)
        #print("power_2 is %s"%power_2)
        run_test(freq_1,freq_2,power_1,power_2)

def twod_sweep(start_f,end_f,steps_f,start_p,end_p,steps_p):
    global freq_2
    for freq_2 in np.linspace(start_f, end_f, steps_f):
        freq_2=str(freq_2)
        print("freq_2 is ",freq_2)
        power_sweep(start_p, end_p, steps_p)

def power_sweep_tx1_only(start, fin, no_steps):
    #print("Running test with params",freq_1,freq_2,power_1)
    for power_1 in np.linspace(start, fin, no_steps):
        power_1=str(power_1)
        #print("power_2 is ",power_1)
        run_test(freq_1,freq_2,power_1,power_2)

def twod_sweep_tx1_only(start_f,end_f,steps_f,start_p,end_p,steps_p):
    global freq_1
    for freq_1 in np.linspace(start_f, end_f, steps_f):
        freq_1=str(freq_1)
        #print("freq_1 is ",freq_1)
        power_sweep_tx1_only(start_p, end_p, steps_p)



def run_test(freq_1,freq_2,power_1,power_2):
    attempts=[]
    successes=[]
    rn16_plus_epc=[]
    for run in range(no_repeats):
        print('\n',freq_1,freq_2,power_1,power_2,"Run:",run ,"Delay:",delay)
        with tempfile.TemporaryFile() as tempf:
            if not (900<float(freq_1)<931 and 
                    900<float(freq_2)<931 and 
                    float(power_1)<15 and 
                    float(power_2)<15):
                print("Looks like freq or power is wrong, quitting.",freq_1,freq_2,power_1,power_2)
                break
            if SINGLE_USRP:
              proc = subprocess.Popen(['sudo', 'GR_SCHEDULER=STS', 'nice', '-n', '-20', 
                                     'python', 'single_tx_reader.py', 
                                     freq_1, freq_2,power_1, power_2, delay], stdout=tempf)
            else:
              proc = subprocess.Popen(['sudo', 'GR_SCHEDULER=STS', 'nice', '-n', '-20', 
                                     'python', 'CW_reader.py', 
                                     freq_1, freq_2,power_1, power_2, delay], stdout=tempf)
            proc.wait()
            if not TX_FAKE_DATA:
                tempf.seek(0)
                if re.search("Number of queries\/queryreps sent : (.*)", tempf.read()):
                    tempf.seek(0)
                    attempts.append(re.findall("Number of queries\/queryreps sent : (.*)", tempf.read())[0])
                    tempf.seek(0)
                    successes.append(re.findall("Correctly decoded EPC : (.*)", tempf.read())[0])
                else:
                    attempts.append("")
                    successes.append("")
            try:
                no_rn16s = epc_finder_filter.count()
                rn16_plus_epc.append(no_rn16s)
                #if 2<no_rn16s<198:
                #    epc_finder_filter.count(plot=True)
                  
            except Exception as e: 
                print(e)
                print("Error with the gate file")
                rn16_plus_epc.append("")
          
    print([suc for suc in successes],[at for at in attempts],[rn for rn in rn16_plus_epc])
    with open("dataoutput.csv","ab") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([freq_1, freq_2, power_1, power_2,delay]+[suc for suc in successes]+[at for at in attempts]+[rn for rn in rn16_plus_epc])

delay='0'

power_1='8'
power_2='3'
twod_power_sweep(8,14,7,0,0,1)
#delay_sweep(0,20,21)
#twod_sweep(915.5,917.5,5,8.5,10,11)
#twod_sweep(912.5,914.5,5,7,12,11)
#run_test('910','912','9','-100')
#twod_sweep(910,915,10,3,6,10)
#twod_sweep(915,915,1,10,11,1)
#twod_sweep_tx1_only(910,915,6,10,12.5,6)
#frequency_sweep(910,916,2)
#frequency_sweep(915,918,18)
#power_sweep(4,8,5)
#power_sweep(5.6,5.4,5)
#power_sweep(8.6,9.4,15)
#power_sweep(8.5,10.5,30)

