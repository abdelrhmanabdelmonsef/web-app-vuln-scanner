
import sys
import dns.resolver
import subprocess
import requests
import concurrent.futures
import os
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), 'ip_resolver')))
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DNS import DNS
import methods
class SubdomainEnumerator:
    def __init__(self,domain):
        self.subdomains = set()
        self.live_subdomains = set()
        self.domain=domain
        self.errors={'CNAME':None, 'A':None, 'crt':None, 'lives':None, 'subfinder':None, 'sublister': None, 'httpx':None}

    def dns_enumeration(self):
        result=DNS.get_cname(self.domain)
        if result:
            self.subdomains.union(set(result))
        else:
            self.errors['CNAME']=True

    def bruteforce_subdomains(self):
        subs=methods.get_file_content("/home/kali/Desktop/Web Vulnarability Scanner/recon/word.txt",'\n')
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(self.check_subdomain, f"{sub}.{self.domain}") for sub in subs[:5]]
            concurrent.futures.wait(futures)

    def check_subdomain(self, subdomain):
        try:
            if DNS.get_address(subdomain):
                self.subdomains.add(subdomain)
        except:
            self.errors['A']=True

    def crt_sh_enumeration(self):
        url = f"https://crt.sh/?q=%.{self.domain}&output=json"
        try:
            response = requests.get(url)
            data = response.json()
            for item in data:
                subdomains = set(item['name_value'].split('\n'))
                self.subdomains.update(subdomains)
        except:
            self.errors['crt']=True
        
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
                self.errors['lives']=True

    def subfinder(self):
        try:
            subfinder_output = subprocess.check_output(["subfinder", "-d", self.domain]).decode("utf-8")
            for line in subfinder_output.splitlines():
                self.subdomains.add(line.strip())
        except:
                self.errors['subfinder']=True

    def sublister(self):
        try:
            sublister_output = subprocess.check_output(["sublist3r", "-d", self.domain]).decode("utf-8")
            for line in sublister_output.splitlines():
                self.subdomains.add(line.strip())
        except:
                self.errors['sublister']=True

    def httpx(self):
        if self.subdomains:
            try:
                # Create a temporary file to store the subdomains
                with open('subdomains.txt', 'w') as f:
                    f.write('\n'.join(self.subdomains))
                
                httpx_output = subprocess.check_output(["httpx", "-l", 'subdomains.txt','-t',200]).decode("utf-8")
                for line in httpx_output.splitlines():
                    self.live_subdomains.append(line.strip())
                
                subprocess.call(["rm", 'subdomains.txt'])
                # Remove the temporary file after use
            except:
                self.errors['httpx']=True

    def enumerate(self):
        self.dns_enumeration()
        self.bruteforce_subdomains()
        self.crt_sh_enumeration()
        # self.subfinder()
        # self.sublister()
        self.check_live_subdomains()


su=SubdomainEnumerator('vulnweb.com')
su.enumerate()

print(su.live_subdomains )
print(su.subdomains)


