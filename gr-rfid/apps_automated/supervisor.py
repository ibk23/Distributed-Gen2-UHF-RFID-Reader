from __future__ import print_function
import subprocess
import tempfile
import re 
import csv
import numpy as np
import epc_finder_gate

#delete csv file
with open("dataoutput.csv","w") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['freq_1', 'freq_2', 'power_1', 'power_2', 'run1_success', 'run2_s','run3_s','run1_attempts','run2_a','run3_a'])


freq_1='910'
freq_2='910'
power_1='5'
power_2='0'


def frequency_sweep(start, fin, no_steps):
    print("Running test with params",freq_1,power_1,power_2)
    for freq_2 in np.linspace(start, fin, no_steps):
        freq_2=str(freq_2)
        print("freq_2 is ",freq_2)
        run_test(freq_1,freq_2,power_1,power_2)

def power_sweep(start, fin, no_steps):
    print("Running test with params",freq_1,freq_2,power_1)
    for power_2 in np.linspace(start, fin, no_steps):
        power_2=str(power_2)
        print("power_2 is ",power_2)
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
    for run in range(1):
        print('\n',freq_1,freq_2,power_1,power_2,"Run:",run, end='')
        with tempfile.TemporaryFile() as tempf:
            if not (900<float(freq_1)<931 and 
                    900<float(freq_2)<931 and 
                    float(power_1)<15 and 
                    float(power_2)<15):
                print("Looks like freq or power is wrong, quitting.",freq_1,freq_2,power_1,power_2)
                break
            proc = subprocess.Popen(['sudo', 'GR_SCHEDULER=STS', 'nice', '-n', '-20', 
                                     'python', 'reader11_automatable.py', 
                                     freq_1, freq_2,power_1, power_2], stdout=tempf)
            proc.wait()
            tempf.seek(0)
            if re.search("Number of queries\/queryreps sent : (.*)", tempf.read()):
                tempf.seek(0)
                attempts.append(re.findall("Number of queries\/queryreps sent : (.*)", tempf.read())[0])
                tempf.seek(0)
                successes.append(re.findall("Correctly decoded EPC : (.*)", tempf.read())[0])
                rn16_plus_epc.append(epc_finder_gate.count())
    print([suc for suc in successes],[at for at in attempts])
    with open("dataoutput.csv","ab") as csvfile:
        if successes and attempts:
            writer = csv.writer(csvfile)
            writer.writerow([freq_1, freq_2, power_1, power_2]+[suc for suc in successes]+[at for at in attempts]+[rn for rn in rn16_plus_epc])


#twod_sweep(910,915,6,5,10,6)
#run_test('910','910','7','7')
#twod_sweep(910,915,10,3,6,10)
#twod_sweep(910,915,5,6,10,5)
#twod_sweep_tx1_only(910,915,6,10,12.5,6)
#frequency_sweep(910,916,2)
#frequency_sweep(915,918,18)
power_sweep(9.3,11,1)
#power_sweep(8.6,9.4,15)
#power_sweep(8.5,10.5,30)

