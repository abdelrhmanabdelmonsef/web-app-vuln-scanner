import os
import sys
from DNS import DNS
from sectrails  import Sectrails 
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import methods 
class resolver:
    def __init__(self,subdomains,sectrails_cookie=''):
        # Define Attributes
        self.subdomains = subdomains
        self.subdomains_ips_mapper = {}
        self.subdomains_ns_mapper = {}
        self.ips = []
        self.nss = []
        self.virtual_hosts={}
        self.errors={"ips":{},"nss":{},"virtual_hosts":None}
        self.sec_trails_cookie=sectrails_cookie
        self.sectrails=Sectrails(c2=self.sec_trails_cookie)


    def get_ips(self):
        for subdomain in self.subdomains:
            try:
                result = DNS.get_address(subdomain)
                if isinstance(result, list):
                    self.ips += result
                    
                else:
                    self.errors['ips'][subdomain] = result
                Sectrails_result=self.sectrails.get_using_sectrails(subdomain,"ip4")
                if Sectrails_result[0] :
                    self.ips+=Sectrails_result[1]  
                    result +=  Sectrails_result[1]
                self.subdomains_ips_mapper[subdomain] = result
            except Exception as e:
                self.errors['ips'][subdomain] = str(e)

        self.ips = methods.uniq_list(self.ips)

    def get_name_servers(self):

        for subdomain in self.subdomains:
            try:
                result = DNS.get_name_server(subdomain)
                if isinstance(result, list):
                    self.nss += result
                    self.subdomains_ns_mapper[subdomain] = result
                else:
                    self.errors['nss'][subdomain] = result
                Sectrails_result=self.sectrails.get_using_sectrails(subdomain,"ns")
                if Sectrails_result[0] :
                    self.nss+=Sectrails_result[1]
            except Exception as e:
                self.errors['nss'][subdomain] = str(e)
        
        self.nss = methods.uniq_list(self.nss)


    def get_virtual_hosts(self):
        self.errors['virtual_hosts'] = {}
        for ip in self.ips:
            try:
                subdomains = [key for key, value in self.subdomains_ips_mapper.items() if ip in value]
                self.virtual_hosts[ip] = subdomains
            except Exception as e:
                self.errors['virtual_hosts'][ip] = str(e)


    def resolve(self):
        self.get_ips()
        self.get_name_servers()
        self.get_virtual_hosts()

