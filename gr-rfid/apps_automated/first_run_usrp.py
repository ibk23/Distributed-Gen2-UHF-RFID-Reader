import subprocess
import tempfile

with tempfile.TemporaryFile() as tempf:
    proc = subprocess.Popen(['sudo', 'sysctl', '-w', 'net.core.wmem_max=1048576'], stdout=tempf)
    proc.wait()
    print(tempf.read())
    proc = subprocess.Popen(['sudo', 'sysctl', '-w', 'net.core.rmem_max=50000000'], stdout=tempf)
    proc.wait()
    print(tempf.read())

