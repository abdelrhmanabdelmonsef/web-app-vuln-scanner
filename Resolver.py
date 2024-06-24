from DNS import DNS
from Operations import Operations
from sectrails  import Sectrails 



class Resolver:
    def __init__(self):
        # Define Attributes
        self.subdomains = []
        self.ips = []
        self.subdomains_ips_mapper = {}
        self.nss = []
        self.subdomains_ns_mapper = {}
        self.virtual_hosts={}
        self.errors={"ips":{},"nss":{}}
        self.sec_trails_cookie="tvQWHwv9WO47nlAnWu0aI7wqiPyA5etdHn3JMiBxLsM-1719140615-1.0.1.1-7AYTqtueESPDHK9MO5d_us656Tg69U6wmsm.UjblbnMXBqi35ga5m0iDoJMwotC2r4ogTlAEOSHa3i.RIFAX0A"
        self.sectrails=Sectrails(c2=self.sec_trails_cookie)




    # def get_ips(self):
    #     for subdomain in self.subdomains:
    #         result=DNS.get_address(subdomain)
    #         if type(result) is list:
    #             self.ips+=result
    #             self.subdomains_ips_mapper[subdomain]=result
    #         else:
    #             self.errors['ips'][subdomain]=result
    #     Operations.uniq_list(self.ips.sort())

    def get_ips(self):
        """
        
        Resolves IP addresses for each subdomain in self.subdomains
        and updates self.ips and self.subdomains_ips_mapper accordingly.
        Errors are stored in self.errors['ips'].
        
        """
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

        self.ips = Operations.uniq_list(self.ips)



    # def get_name_servers(self):
    #     for subdomain in self.subdomains:
    #         result=DNS.get_name_server(subdomain)
    #         if type(result) is list:
    #             self.nss+=result
    #             self.subdomains_ns_mapper[subdomain]=result
    #         else:
    #             self.errors['nss'][subdomain]=result
    #     Operations.uniq_list(self.nss.sort())
    def get_name_servers(self):
        """
        Resolves name servers for each subdomain in self.subdomains
        and updates self.nss and self.subdomains_ns_mapper accordingly.
        Errors are stored in self.errors['nss'].
        """
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
        
        self.nss = Operations.uniq_list(self.nss)

        
    # def get_virtual_hosts(self):
    #     for ip in self.ips:
    #         subdomains=[]
    #         for key,value in self.subdomains_ips_mapper.items():
    #             if ip in value:
    #                 subdomains+=[key]
    #         self.virtual_hosts[ip]=subdomains

    # def get_virtual_hosts(self):
    #     """
    #     Maps each IP address in self.ips to its associated subdomains based on self.subdomains_ips_mapper.
    #     Updates self.virtual_hosts with the IP-subdomain mappings.
    #     """
    #     for ip in self.ips:
    #         subdomains = [key for key, value in self.subdomains_ips_mapper.items() if ip in value]
    #         self.virtual_hosts[ip] = subdomains

    def get_virtual_hosts(self):
        """
        Maps each IP address in self.ips to its associated subdomains based on self.subdomains_ips_mapper.
        Updates self.virtual_hosts with the IP-subdomain mappings.
        Errors are stored in self.errors['virtual_hosts'].
        """
        self.errors['virtual_hosts'] = {}
        
        for ip in self.ips:
            try:
                subdomains = [key for key, value in self.subdomains_ips_mapper.items() if ip in value]
                self.virtual_hosts[ip] = subdomains
            except Exception as e:
                self.errors['virtual_hosts'][ip] = str(e)

# Example usage in main class 
resolver = Resolver()
resolver.subdomains=["google.com","facebook.com","amazon.com"]
print(resolver.subdomains)
resolver.get_ips()
resolver.get_name_servers()
resolver.get_virtual_hosts()
print(f"IPS: {resolver.ips}\n")
print(f"IP Mapper: {resolver.subdomains_ips_mapper} \n")
print(f"NSs: {resolver.nss}\n")
print(f"Virtual Hosts: {resolver.virtual_hosts}\n")
print(f"Errors: {resolver.errors}\n")

