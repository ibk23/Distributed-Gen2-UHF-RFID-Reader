import subprocess
import tempfile
import re 
import csv
import numpy as np

csvfile = open("dataoutput.csv","w")
writer = csv.writer(csvfile)

freq_1='910'
freq_2='915'
power_1='7.0'
power_2='9.29'
writer.writerow(['freq_1', 'freq_2', 'power_1', 'power_2', 'run1_success', 'run2_s','run3_s','run1_attempts','run2_a','run3_a'])

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

def run_test(freq_1,freq_2,power_1,power_2):
    attempts=[]
    successes=[]
    for run in range(3):
        print("Run",run)
        with tempfile.TemporaryFile() as tempf:
            if not (900<float(freq_1)<920 and 
                    900<float(freq_2)<920 and 
                    float(power_1)<15 and 
                    float(power_2)<15):
                print("Looks like freq or power is wrong, quitting.",freq_1,freq_2,power_1,power_2)
                break
            proc = subprocess.Popen(['sudo', 'GR_SCHEDULER=STS', 'nice', '-n', '-20', 
                                     'python', 'reader11_automatable.py', 
                                     freq_1, freq_2,power_1, power_2], stdout=tempf)
            proc.wait()
            tempf.seek(0)
            attempts.append(re.findall("Number of queries\/queryreps sent : (.*)", tempf.read())[0])
            tempf.seek(0)
            successes.append(re.findall("Correctly decoded EPC : (.*)", tempf.read())[0])
    writer.writerow([freq_1, freq_2, power_1, power_2]+[suc for suc in successes]+[at for at in attempts])

#frequency_sweep(910,915,30)
#frequency_sweep(915,918,18)
power_sweep(7,10,15)
power_sweep(8.9,9.2,15)
csvfile.close()
