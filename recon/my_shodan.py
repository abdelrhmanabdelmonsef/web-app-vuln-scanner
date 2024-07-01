import os
import subprocess
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
import methods

class shodan_class:
    def __init__(self,target) :
        self.target=target
        self.domain_ip={}

    def shodan(self):
        command=f"shodan domain {self.target} 1> shodan_out.txt 2>/dev/null"
        methods.execute_command(command=command)
        lines=methods.get_file_content("shodan_out.txt","\n")
        for line in lines:
            if 'A' in line:
                temp=" ".join(line.split())
                self.domain_ip[f"{temp.split(' A ')[0]}.{self.target}"] = temp.split(" A ")[-1]
        methods.rm("shodan_out.txt")
