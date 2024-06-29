import subprocess
import time
import os 
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
import threads
import methods  # Assuming methods.py contains utility functions
class NmapScanner:

    def __init__(self, targets):
        self.targets = targets
        self.reports = {}
        self.errors = {'targets': [], 'General': []}

    def execute_command(self, command):
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = proc.communicate()
        return [stdout.decode("utf-8"), stderr.decode("utf-8")]

    def scan(self, target):
        command = f"sudo nmap -sV -O -sC -A --open --script vuln -T3 -iL {target} -oG Nmap_out_put"
        command=f"nmap -iL {target} -Pn -oG Namp_out_put"
        print(command)
        stdout, stderr = self.execute_command(command)
        if stderr:
            return False, stderr
        else:
            return True, stdout

    def run_scans(self):
        print("[+] Initiating Nmap Scanning...")
        try:
            try:
                file="nmap_targets.txt"
                methods.add_list_to_file(self.targets,file,'w','\n')
                threads.thread(self.scan, (file,))
            except Exception as e:
                self.errors['targets'].append(e)
        except Exception as e:
            self.errors['General'] = str(e)
    


# Example Usage
if __name__ == "__main__":
    targets = ['microsoft.com']
    nmap_scanner = NmapScanner(targets)
    nmap_scanner.run_scans()
    print("Errors:", nmap_scanner.errors)
    print("Reports:", nmap_scanner.reports)