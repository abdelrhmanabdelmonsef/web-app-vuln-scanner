
import dns.resolver
import subprocess
import requests
import concurrent.futures
import os

class SubdomainEnumerator:
    def __init__(self):
        self.subdomains = set()
        self.live_subdomains = set()

    def dns_enumeration(self, domain):
        record_types = ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT']
        for record in record_types:
            try:
                answers = dns.resolver.resolve(domain, record)
                for rdata in answers:
                    if record == 'CNAME':
                        self.subdomains.add(str(rdata.target))
                    elif record == 'MX':
                        self.subdomains.add(str(rdata.exchange))
                    elif record == 'NS':
                        self.subdomains.add(str(rdata))
            except:
                pass

    def bruteforce_subdomains(self, domain):
        with open('wordlist.txt', 'r') as f:
            subdomains = f.read().splitlines()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(self.check_subdomain, f"{sub}.{domain}") for sub in subdomains]
            concurrent.futures.wait(futures)

    def check_subdomain(self, subdomain):
        try:
            dns.resolver.resolve(subdomain, 'A')
            self.subdomains.add(subdomain)
        except:
            pass

    def crt_sh_enumeration(self, domain):
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        try:
            response = requests.get(url)
            data = response.json()
            for entry in data:
                self.subdomains.add(entry['name_value'])
        except:
            print("Error in crt.sh enumeration")

    def run_tool(self, tool, domain):
        try:
            output = subprocess.check_output([tool, "-d", domain]).decode("utf-8")
            for line in output.splitlines():
                self.subdomains.add(line.strip())
        except subprocess.CalledProcessError:
            print(f"{tool} execution failed.")
        except FileNotFoundError:
            print(f"{tool} not found.")
        except Exception as e:
            print(f"Error running {tool}: {e}")

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

    def enumerate_subdomains(self, domain):
        print(f"Starting subdomain enumeration for {domain}")

        # DNS enumeration
        print("Performing DNS enumeration...")
        self.dns_enumeration(domain)

        # Bruteforce subdomains
        print("Performing bruteforce subdomain enumeration...")
        self.bruteforce_subdomains(domain)

        # crt.sh enumeration
        print("Performing crt.sh enumeration...")
        self.crt_sh_enumeration(domain)

        # Run external tools
        tools = ['subfinder', 'amass', 'assetfinder', 'findomain']
        for tool in tools:
            print(f"Running {tool}...")
            self.run_tool(tool, domain)

        print(f"Total subdomains found: {len(self.subdomains)}")

        # Check live subdomains
        print("Checking for live subdomains...")
        self.check_live_subdomains()

        print(f"Live subdomains found: {len(self.live_subdomains)}")
        return list(self.live_subdomains)

# Usage
if __name__ == "__main__":
    enumerator = SubdomainEnumerator()
    live_subdomains = enumerator.enumerate_subdomains("google.com")
    print("\nLive subdomains:")
    for subdomain in live_subdomains:
        print(subdomain)