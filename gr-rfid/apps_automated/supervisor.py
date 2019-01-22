import subprocess
import tempfile
import re 
import csv
import numpy as np

csvfile = open("dataoutput.csv","w")
writer = csv.writer(csvfile)

freq_1='910'
freq_2='910'
power_1='7.0'
power_2='9.2'
writer.writerow(['freq_1', 'freq_2', 'power_1', 'power_2', 'run1_success', 'run2_s','run3_s','run1_attempts','run2_a','run3_a'])

for power_2 in np.linspace(0,5.0,10):
    power_2=str(power_2)
    print("Power_2 is ",power_2)
    attempts=[]
    successes=[]
    for run in range(3):
        print("Run",run)
        with tempfile.TemporaryFile() as tempf:

            if (900<freq_1<920 and 900<freq_2<920 and power_1<15 and power_2<15):
                print("Looks like freq or power is wrong, quitting.")
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


csvfile.close()
