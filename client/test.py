from subprocess import Popen, PIPE


process = Popen(['powershell.exe', 'ipconfig'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate()
print(process.returncode)
print(stdout.decode())
