import subprocess
import tempfile
import re 
import csv

csvfile = open("dataoutput.csv","w")
writer = csv.writer(csvfile)

freq_1=910
freq_2=914
power_1=7.0
power_2=9.2


attempts=[]
successes=[]
for run in range(3):
    print("Run",run)
    with tempfile.TemporaryFile() as tempf:
        proc = subprocess.Popen(['sudo', 'GR_SCHEDULER=STS', 'nice', '-n', '-20', 
                                 'python', 'reader11_automatable.py', 
                                 freq_1, freq_2,power_1, power_2], stdout=tempf)
        proc.wait()
        tempf.seek(0)
        attempts[run] = re.findall("Number of queries\/queryreps sent : (.*)", tempf.read())[0]
        tempf.seek(0)
        successes[run] = re.findall("Correctly decoded EPC : (.*)", tempf.read())[0]
writer.writerow([successes[0], attempts[0], successes[1], attempts[1], successes[2], attempts[2]])


csvfile.close()
