
import sys
import dns.resolver
import subprocess
import requests
import concurrent.futures
import os
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), 'ip_resolver')))
print(sys.path)
from DNS import DNS
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import methods
class SubdomainEnumerator:
    def __init__(self,domain):
        self.subdomains = set()
        self.live_subdomains = set()
        self.domain=domain

    def dns_enumeration(self):
        result=DNS.get_cname(self.domain)
        if result:
            self.subdomains.union(set(result))
    

    def bruteforce_subdomains(self):
        subs=methods.get_file_content("/home/kali/Desktop/Web Vulnarability Scanner/n0kovo_subdomains_small.txt",'\n')
        print(type(subs))
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(self.check_subdomain, f"{sub}.{self.domain}") for sub in subs[-5:]]
            concurrent.futures.wait(futures)

    def check_subdomain(self, subdomain):
        try:
            if DNS.get_address(subdomain):
                self.subdomains.add(subdomain)
        except:
            pass

    def crt_sh_enumeration(self):
        url = f"https://crt.sh/?q=%.{self.domain}&output=json"
        try:
            response = requests.get(url)
            data = response.json()
            for entry in data:
                self.subdomains.add(entry['name_value'])
        except:
            pass
        
    def check_live_subdomains(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(self.check_live, subdomain) for subdomain in self.subdomains]
            concurrent.futures.wait(futures)

    def check_live(self, subdomain):
        try:
            response = requests.get(f"http://{subdomain}", timeout=5)
            if response.status_code == 200:
                self.live_subdomains.add(subdomain)
        except:
            try:
                response = requests.get(f"https://{subdomain}", timeout=5)
                if response.status_code == 200:
                    self.live_subdomains.add(subdomain)
            except:
                pass

    def enumerate_subdomains(self):
        self.dns_enumeration()
        self.bruteforce_subdomains()
        self.crt_sh_enumeration()
        self.check_live_subdomains()


enumerator = SubdomainEnumerator("microsoft.com")
enumerator.enumerate_subdomains()
print(enumerator.live_subdomains)    