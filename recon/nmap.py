import sys
import os 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import methods  # Assuming methods.py contains utility functions
class nmap:

    def __init__(self, targets):
        self.targets = targets
        self.reports = {}
        self.errors = {'targets': [], 'General': []}

    def scan(self, target):
        print('in scan')
        command = f"nmap -sV -sC -A --open --script vuln -T5 -iL {target} -oG Nmap_out_put"
        print('Command: ',command)
        _,stdout, stderr = methods.execute_command(command)
        if stderr:
            return False, stderr
        else:
            return True, stdout

    def nmap(self):
        print('in nmap')
        ips_file = 'target_file'
        methods.add_list_to_file(self.targets,ips_file,'w','\n')
        self.scan(ips_file)
        methods.rm(ips_file)
    
