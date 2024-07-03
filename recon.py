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
import threads
from groc_ai import groq
from subdomain_enum import subdomain_enum
from resolver import resolver
from nmap import nmap
from my_shodan import shodan_class
from dirsearch import DirSearch
from paramspider import paramspider
from arjun import arjun


class recon():

    def __init__(self, domain):
        self.domain = domain
        self.reports = {'shodan': [], 'subdomain_enum': [], 'resolver':[],'dirsearch': [], 'paramspider': [], 'arjun':[] ,'nmap': []}
        self.subdomains=[]
        self.alive_subdomains=[]
        self.ips=[]
        self.endpoints=[]
        self.endpoint_with_params=[]
        self.groc_ai = groq()

    def run_shodan(self):
        domain = self.domain.split('//')[-1]
        my_shodan = shodan_class(domain)
        my_shodan.shodan()
        my_shodan_outputs = my_shodan.domain_ip
        self.ips += my_shodan_outputs
        my_shodan_long_ai_report = self.groc_ai.reporting(my_shodan_outputs,'This is the shodan tool ouptut Create the markdown file that includes all detailed information')
        my_shodan_short_ai_report =  self.groc_ai.reporting(my_shodan_outputs,'This is the shodan tool ouptut Create the short markdown file that includes important informations')
        self.reports['shodan'].append(my_shodan_long_ai_report)
        self.reports['shodan'].append(my_shodan_short_ai_report)
        
    def run_subdomain_enum(self):
        my_subdomain_enum = subdomain_enum(self.domain)
        my_subdomain_enum.enumerate()
        my_subdomain_enum_output = my_subdomain_enum.subdomains
        self.subdomains += list(my_subdomain_enum_output)
        self.alive_subdomains += my_subdomain_enum.live_subdomains
        my_subdomain_enum_long_ai_report = self.groc_ai.reporting(my_subdomain_enum_output,'This is the subdomain enumeration tool ouptut Create the markdown file that includes all detailed information')
        my_subdomain_enum_short_ai_report =  self.groc_ai.reporting(my_subdomain_enum_output,'This is the subdomain enumeration tool ouptut Create the short markdown file')
        self.reports['subdomain_enum'].append(my_subdomain_enum_long_ai_report)
        self.reports['subdomain_enum'].append(my_subdomain_enum_short_ai_report)

    def run_resolver(self):
        my_resolver = resolver(self.subdomains)
        my_resolver.resolve()
        my_resolver_output = {'subdomains_ips_mapper':my_resolver.subdomains_ips_mapper, 'subdomains_ns_mapper':my_resolver.subdomains_ns_mapper, 'ips':my_resolver.ips, 'name_server':my_resolver.nss, 'virtual_hosts':my_resolver.virtual_hosts}
        resolver_long_ai_report = self.groc_ai.reporting(my_resolver_output,'This is the resolving tool ouptut Create the markdown file that includes all detailed information')
        resolver_short_ai_report =  self.groc_ai.reporting(my_resolver_output,'This is the resolving tool ouptut Create the short markdown file')
        self.reports['resolver'].append(resolver_long_ai_report)
        self.reports['resolver'].append(resolver_short_ai_report)

    def run_dirsearch(self):
        my_dirsearch = DirSearch(self.alive_subdomains)
        my_dirsearch.ldirsearch()
        my_dirsearch_ouputs = my_dirsearch.end_points
        self.endpoints += my_dirsearch_ouputs
        my_dirsearch_long_ai_report = self.groc_ai.reporting(my_dirsearch_ouputs,'This is the dirsearch tool ouptut Create the markdown file that includes all detailed information')
        my_dirsearch_short_ai_report =  self.groc_ai.reporting(my_dirsearch_ouputs,'This is the dirsearch tool ouptut Create the short markdown file')
        self.reports['dirsearch'].append(my_dirsearch_long_ai_report)
        self.reports['dirsearch'].append(my_dirsearch_short_ai_report)

    def run_paramspider(self):
        my_paramspider = paramspider(self.domain)
        my_paramspider.lparamspider()
        my_paramspider_output = my_paramspider.end_points_with_params
        self.endpoint_with_params += my_paramspider_output
        my_paramspider_long_ai_report = self.groc_ai.reporting(my_paramspider_output,'This is the paramspider tool ouptut Create the markdown file that includes all detailed information')
        my_paramspider_short_ai_report =  self.groc_ai.reporting(my_paramspider_output,'This is the paramspider tool ouptut Create the short markdown file')
        self.reports['paramspider'].append(my_paramspider_long_ai_report)
        self.reports['paramspider'].append(my_paramspider_short_ai_report)

    def run_arjun(self):
        my_arjun = arjun(self.domain)
        my_arjun.larjun()
        my_arjun_ouptut = my_arjun.end_points_with_params
        self.endpoint_with_params += my_arjun_ouptut
        my_arjun_long_ai_report = self.groc_ai.reporting(my_arjun_ouptut,'This is the resolving tool ouptut Create the markdown file that includes all detailed information')
        my_arjun_short_ai_report =  self.groc_ai.reporting(my_arjun_ouptut,'This is the resolving tool ouptut Create the short markdown file')
        self.reports['arjun'].append(my_arjun_long_ai_report)
        self.reports['arjun'].append(my_arjun_short_ai_report)

    def run_nmap(self):
        my_nmap = nmap(self.domain)
        my_nmap.nmap()
        my_nmap_ouptut = my_nmap.reports
        my_nmap_long_ai_report = self.groc_ai.reporting(my_nmap_ouptut,'This is the nmap tool ouptut Create the markdown file that includes all detailed information')
        my_nmap_short_ai_report =  self.groc_ai.reporting(my_nmap_ouptut,'This is the nmap tool ouptut Create the short markdown file')
        self.reports['nmap'].append(my_nmap_long_ai_report)
        self.reports['nmap'].append(my_nmap_short_ai_report)

#self.reports = {'shodan': [], 'subdomain_enum': [], 'dirsearch': [], 'paramspider': [], 'arjun':[] ,'nmap': []}
    def recon(self,lst):
        thread_objects = []
        if 'nmap' in lst:
            t = threads.thread(self.run_nmap,())
            thread_objects.append(t)

        if 'shodan' in lst:
            t = threads.thread(self.run_shodan,())
            thread_objects.append(t)

        if 'subdomain_enum' in lst:
            t = threads.thread(self.run_subdomain_enum,())
            thread_objects.append(t)
        
            if 'resolver' in lst:
                t = threads.thread(self.run_resolver,())
                thread_objects.append(t)
            
            if 'dirsearch' in lst:
                t = threads.thread(self.run_dirsearch,())
                thread_objects.append(t)
            
            if 'paramspider' in lst:
                    t = threads.thread(self.run_paramspider,())
                    thread_objects.append(t)
                
            if 'arjun' in lst:
                    t = threads.thread(self.run_arjun,())
                    thread_objects.append(t)
        threads.join_threads(thread_objects)