# import dns.resolver
# import subprocess

# class SubdomainEnumerator:
#     def __init__(self):
#         pass

#     def enumerate_subdomains(self, domain):
#         subdomains = []

#         # Method 1: Use DNS resolution to find subdomains
#         try:
#             answers = dns.resolver.resolve(domain, 'CNAME')
#             for rdata in answers:
#                 subdomains.append(rdata.target.to_text())
#         except:
#             pass

#         # Method 2: Use Subfinder to find subdomains
#         try:
#             subfinder_output = subprocess.check_output(["subfinder", "-d", domain]).decode("utf-8")
#             for line in subfinder_output.splitlines():
#                 subdomains.append(line.strip())
#         except (subprocess.CalledProcessError, FileNotFoundError):
#             pass
#         return subdomains
################################################

import dns.resolver

import subprocess

class SubdomainEnumerator:
    def _init_(self):
        pass

    def enumerate_subdomains( domain):
        subdomains = set()
        live_subdomains = []

        # Method 1: Use DNS resolution to find subdomains
        try:
            answers = dns.resolver.resolve(domain, 'CNAME')
            for rdata in answers:
                subdomains.add(rdata.target.to_text())
        except dns.resolver.NoAnswer:
            pass
        except dns.resolver.NXDOMAIN:
            pass
        except Exception as e:
            print(f"DNS resolution error: {e}")

        # Method 2: Use Subfinder to find subdomains
        try:
            subfinder_output = subprocess.check_output(["subfinder", "-d", domain]).decode("utf-8")
            for line in subfinder_output.splitlines():
                subdomains.add(line.strip())
        except subprocess.CalledProcessError:
            print("Subfinder execution failed.")
        except FileNotFoundError:
            print("Subfinder not found.")
        except Exception as e:
            print(f"Error running Subfinder: {e}")

        # Method 3: Use httpx to check live subdomains
        if subdomains:
            try:
                # Create a temporary file to store the subdomains
                with open('subdomains.txt', 'w') as f:
                    f.write('\n'.join(subdomains))
                
                httpx_output = subprocess.check_output(["httpx", "-l", 'subdomains.txt']).decode("utf-8")
                for line in httpx_output.splitlines():
                    live_subdomains.append(line.strip())
                
                # Remove the temporary file after use
                subprocess.call(["rm", 'subdomains.txt'])
            except subprocess.CalledProcessError:
                print("httpx execution failed.")
            except FileNotFoundError:
                print("httpx not found.")
            except Exception as e:
                print(f"Error running httpx: {e}")

        return live_subdomains
    

    print (enumerate_subdomains("vulnweb.com"))
