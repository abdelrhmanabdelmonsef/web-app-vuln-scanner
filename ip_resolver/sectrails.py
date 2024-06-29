import requests 
from bs4 import BeautifulSoup
#/_next/data/982e4e5e/domain/google.com/dns.json?domain=google.com 
class Sectrails:
    def __init__(self,c2=None):
        self.headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"}
        # Custom cookies
        if c2 is None:
            c2=".C3Z25NpSN0GUqX86bEec97FgrnPTWB3bNn7JapRT_8-1719135680-1.0.1.1-2zlRgygLR5rJLt_jaMUDLwuT9VMqpqvX1voxfs70KQXeqKXUwm4cKuadE6U7QgwNI.eiX6VGxFCXj.629bVR.w"
        self.cookies = {
        "cf_clearance":c2}
        # Check if the request was successful



    def get_using_sectrails(self,domain,rec):

        self.response=requests.get(f'https://securitytrails.com/domain/{domain}/dns', headers=self.headers, cookies=self.cookies)   
        
        map={"ip4":0,"ip6":1,"mx":2,"ns":3,"soa":4,"cname":6}
        success=False
        results=[]
        if self.response.status_code == 200:
            print("Start using Security Trails crawling")
            # Step 2: Parse the response content
            soup = BeautifulSoup(self.response.content, 'html.parser')        
            parent_node = soup.find_all('div', class_='bg-white dark:bg-black-90 rounded-2xl pt-2 pb-4')[map[rec]]
            
            children=parent_node.find_all('a')
            results =[child.get_text() for child in children ]
            success=True
        return [success,results] 


