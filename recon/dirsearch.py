import os
import sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import methods
import threads
import re

global_path = '/home/kali/Desktop/'

class DirSearch:
    def __init__(self,URLs):
        self.URLs=URLs
        self.end_points={}
        self.errors={'urls':[],'general':[]}
	
    def split_domain(self,URL):
        return URL.split('//')[-1].split('/')[0]
    
    def dirsearch_execute(self,str_flags):
        command = f"python3 '{global_path}/Web dirsearch.py' {str_flags} 2> /dev/null"
        _,out,err=methods.execute_command(command)
        if not err:
            return out
        else:
            return False
    
    def str_flags(self,flags,URL):
        domain = self.split_domain(URL)
        flags['-o'] = domain
        flags['-u'] = URL
        return methods.dic_to_str(flags,postfix=' ')
    
    def extract_urls(self,file_path):
        lines = methods.get_file_content(file_path)
        if lines:
            urls=set()
            for line in lines:
                result = re.findall(r'(http[^\s]+)', line)
                if result:
                    urls.add(result[-1]) 
            return urls        
        else:
            return False
    
    def dirsearch(self,URL,flags={}):
        dirsearch_result = self.dirsearch_execute(self.str_flags(flags,URL))
        if dirsearch_result:
            extract_result = self.extract_urls(self.split_domain(URL))
            self.end_points[URL] = extract_result
            methods.rm(self.split_domain(URL))
        else:
            self.errors['urls'].append(URL)

    def ldirsearch(self,flags={}):
        print("[●] Vulnerabilities Scanning  -  dirsearch")
        try:
            thread_objects = []
            for URL in self.URLs:
                t = threads.thread(self.dirsearch,args=(URL,flags))
                thread_objects.append(t)
            threads.join_threads(thread_objects)
        except Exception as e:
            self.errors['general'] = e     

# dir_search = DirSearch(['http://testhtml5.vulnweb.com','http://testphp.vulnweb.com','http://testasp.vulnweb.com'])
# dir_search.ldirsearch({'-w':'word.txt'})
# print(f'Output: {dir_search.end_points}')
# print(f'Errors: {dir_search.errors}')
