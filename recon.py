""" 
1. list domains
2.shodan --> dict {sub : ip }
3. subdomain enumeration --> resolver 
4.ip --> nmap 
5.subdomains --> resourse enum
6.endpoints & endpoints with parameters --> exploitation
"""
import os
import methods
import threads
import sys

sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), 'recon/')))

from my_shodan import shodan_class
def recon(domains=[]):
    Shodan_opject=shodan_class(domains)
    Shodan_opject.shodan()
    print(Shodan_opject.domain_ip)


recon(['vulnweb.com'])