from __future__ import print_function
import subprocess
import tempfile
import re
import csv
import numpy as np
import sys

#header csv file
with open("calibration_data.csv","ab") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['freq_1','freq_2','tx_power_1','tx_power_2', 'tag_power_from_SA'])


freq_1='910'
freq_2='910'
power_1='5'
power_2='5'

def power_sweep(start, fin, no_steps):
    print("Running test with params",freq_1,freq_2,power_1,power_2)
    for power in np.linspace(start, fin, no_steps):
        power=str(power)
        if usrp_no==1:
            print("power_1 is ",power)
            run_test(freq_1,freq_2,power,power_2)
        if usrp_no==2:
            print("power_2 is ",power)
            run_test(freq_1,freq_2,power_1,power)


def run_test(freq_1,freq_2,power_1,power_2):
    print('\n',freq_1,freq_2,power_1,power_2, end='')
    with tempfile.TemporaryFile() as tempf:
        if (900<float(freq_1)<931 and
                900<float(freq_2)<931 and
                float(power_1)<15 and
                float(power_2)<15):

            proc = subprocess.Popen(['sudo', 'GR_SCHEDULER=STS', 'nice', '-n', '-20',
                                     'python', 'reader11_automatable.py',
                                     freq_1, freq_2,power_1, power_2], stdout=tempf)
            proc.wait()
            with open("calibration_data.csv","ab") as csvfile:
                writer = csv.writer(csvfile)
                power_read_SA = input("Enter the peak power seen by the signal analyser -> ")
                if usrp_no==1:
                    writer.writerow([freq_1, '', power_1, '',power_read_SA])
                elif usrp_no==2:
                    writer.writerow(['', freq_2, '', power_2,power_read_SA])
        else:
            print("Looks like freq or power is wrong, skipping.",freq_1,freq_2,power_1,power_2)
            

usrp_no=0
while not (usrp_no==1 or usrp_no==2):
    usrp_no = int(input("Which USRP is connected (1/2) ->"))
    print(usrp_no,type(usrp_no))
#print("Running power sweep from 0 to 15 and back")
#power_sweep(0,15,31)
for a in [5,14.5]:
    run_test('910','910','5',str(a))

