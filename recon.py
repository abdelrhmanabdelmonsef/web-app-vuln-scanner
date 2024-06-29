""" 
1. list domains
2.shodan --> dict {sub : ip }
3. subdomain enumeration --> resolver 
4.ip --> nmap 
5.subdomains --> resourse enum
6.endpoints & endpoints with parameters --> exploitation
"""
import os
import sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), 'recon/')))
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), 'recon/ip_resolver')))
import methods
import threads
import groc_ai

from subdomain_enum import SubdomainEnumerator
from resolver import resolver
from nmap import nmap
from my_shodan import shodan_class

def recon(domain):
    Shodan_opject=shodan_class(domain)
    Shodan_opject.shodan()
    shodan_result = Shodan_opject.domain_ip 
    shodan_ai_report = groc_ai.reporting(shodan_result,'')
    sub_enum = subdomain_enum(domain)
    sub_enum.enumerate()
    sub_enum_subdomains = sub_enum.subdomains
    sub_enum_live_subdomains = sub_enum.live_subdomains
    sub_enum_errors = sub_enum.errors
    sub_enum_pre_report = {"Subdomains":sub_enum_subdomains,"Live sub domaind":sub_enum_live_subdomains,"subdomain enumeration errors":sub_enum_errors}
    sub_enum_ai_report = groc_ai.reporting(sub_enum_pre_report,'')
    # sent result to ai
    resolver = resolver()
    resolver.resolve()
    resolver_ips=resolver.ips
    resolver_nss=resolver.nss
    resolver_vhs=resolver.virtual_hosts
    resolver_ai_report = groc_ai.reporting({"resolving process nameservers":resolver_nss,"resolving process virtual hosts":resolver_vhs},'')
    # sent result to ai
    # nmap_scanner = nmap(resolver_ips)
    # nmap_scanner.nmap()
    # nmap_scanner_reports = nmap_scanner.reports
    # nmap_scanner_errors = nmap_scanner.errors
    # nmap_scanner_ai_report = groc_ai.reporting({'nmap reports':nmap_scanner_reports,'nmap errors': nmap_scanner_errors},'')
    # sent result to ai
    return [sub_enum_ai_report,resolver_ai_report,shodan_ai_report]
    
print(recon('vulnweb.com'))