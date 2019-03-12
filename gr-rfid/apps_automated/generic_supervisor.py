from __future__ import print_function
from pprint import pprint 
import subprocess
import tempfile
import re 
import csv
import numpy as np



import epc_finder_filter
import epc_finder_gate


def add_file_headers():
    if RN16s_only:
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
    for delay_samples in np.linspace(start, fin, no_steps):
        arguments['-d'] = str(int(delay_samples))
        run_test()

def frequency_sweep(start, fin, no_steps):
    for freq_2 in np.linspace(start, fin, no_steps):
        arguments['-f2'] =str(freq_2)
        run_test()

def twod_power_sweep(start_1, fin_1, no_steps_1,start_2, fin_2, no_steps_2):
    for power_1 in np.linspace(start_1, fin_1, no_steps_1):
        arguments['-p1']=str(power_1)
        power_sweep(start_2, fin_2, no_steps_2)

def power_sweep(start, fin, no_steps):
    for power_2 in np.linspace(start, fin, no_steps):
        arguments['-p2']=str(power_2)
        run_test()

def twod_sweep(start_f,end_f,steps_f,start_p,end_p,steps_p):
    for freq_2 in np.linspace(start_f, end_f, steps_f):
        arguments['-f2'] =str(freq_2)
        power_sweep(start_p, end_p, steps_p)

def power_sweep_tx1_only(start, fin, no_steps):
    for power_1 in np.linspace(start, fin, no_steps):
        arguments['-p1']=str(power_1)
        run_test()

def twod_sweep_tx1_only(start_f,end_f,steps_f,start_p,end_p,steps_p):
    arguments['-single_tx']='False'
    for freq_1 in np.linspace(start_f, end_f, steps_f):
        arguments['-f1']=str(freq_1)
        power_sweep_tx1_only(start_p, end_p, steps_p)



def run_test():
    print('\n')
    pprint(arguments)
    attempts=[]
    successes=[]
    rn16_plus_epc=[]
    for run in range(no_repeats):
        print("\nRun:%i "%run,end='')
        with tempfile.TemporaryFile() as tempf:
            if not (900<float(arguments['-f1'])<931 and 
                    900<float(arguments['-f2'])<931 and 
                    float(arguments['-p1'])<15 and 
                    float(arguments['-p2'])<15):
                print("Looks like freq or power is wrong, quitting.",freq_1,freq_2,power_1,power_2)
                break

            arglist=[]
            for key, value in arguments.iteritems():
                arglist+=[key+'='+value]
            command = ['sudo', 'GR_SCHEDULER=STS', 'nice', '-n', '-20', 
                       'python', 'generic_reader.py']+arglist

            proc = subprocess.Popen(command, stdout=tempf)
            proc.wait()
            if not RN16s_only:
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
                if EPC_FINDER_METHOD=="GATE":
                    no_rn16s = epc_finder_gate.count()
                elif EPC_FINDER_METHOD=="FILTER":
                    no_rn16s = epc_finder_filter.count()
                else:
                    print("EPC Finder not specified, setting epc value to -1.")
                    no_rn16s = -1
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
        writer.writerow([arguments['-f1'], arguments['-f2'], arguments['-p1'], arguments['-p2'],arguments['-d']]+[suc for suc in successes]+[at for at in attempts]+[rn for rn in rn16_plus_epc])


RN16s_only = True
no_repeats=1
add_file_headers()

EPC_FINDER_METHOD="FILTER" # "FILTER" or "GATE"

arguments = {'-f1':'910', 
            '-f2':'911', 
            '-p1':'8', 
            '-p2':'8',
            '-single_tx':'False', 
            '-fd':'2', 
            '-cw':'False', 
            '-d':'0'}

#power_sweep_tx1_only(10,12,21)
#twod_power_sweep(7,14,8,0,14,15)
#delay_sweep(0,20,21)
twod_sweep(910.5,915,10,6,11,11)
#twod_sweep(912.5,914.5,5,7,12,11)
#run_test()
#twod_sweep(910,915,10,3,6,10)
#twod_sweep(915,915,1,10,11,1)
#twod_sweep_tx1_only(910,915,6,10,12.5,6)
#frequency_sweep(910,916,2)
#frequency_sweep(915,918,18)
#power_sweep(4,8,5)
#power_sweep(5.6,5.4,5)
#power_sweep(8.6,9.4,15)
#power_sweep(8.5,10.5,30)

