import dns.resolver

class DNS:
    # All Functions return List of items or exception if faliure
    
    @staticmethod
    def get_address(domain):
        try:
            answers = dns.resolver.resolve(domain, 'A')
            return [rdata.to_text() for rdata in answers]
        except Exception as e:
                return False
    @staticmethod   
    def get_name_server(domain):
        try:
            answers = dns.resolver.resolve(domain, 'NS')
            return [rdata.to_text() for rdata in answers]
        except Exception as e:
                return e  
    @staticmethod
    def get_txt(domain):
        try:
            answers = dns.resolver.resolve(domain, 'TXT')
            return [rdata.to_text() for rdata in answers]
        except Exception as e:
                return e  
    @staticmethod    
    def get_soa(domain):
        try:
            answers = dns.resolver.resolve(domain, 'SOA')
            return [rdata.to_text() for rdata in answers]
        except Exception as e:
                return e 
    @staticmethod    
    def get_cname(ip):
        try:
            answers = dns.resolver.resolve(ip, 'CNAME')
            return [rdata.to_text() for rdata in answers]
        except Exception as e:
                return False
