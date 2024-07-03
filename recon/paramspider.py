import os
import sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import methods
import threads

global_path = '/home/kali'

class paramspider:
    def __init__(self,URLs):
        self.URLs=URLs
        self.end_points_with_params={}
        self.errors={'urls':[],'general':[]}
	
    def split_domain(self,URL):
        return URL.split('//')[-1].split('/')[0]
    
    def paramspider_execute(self,str_flags):
        command = f"python3 '{global_path}/Web Vulnarability Scanner/ParamSpider/paramspider.py' {str_flags} 2> /dev/null"
        _,out,err=methods.execute_command(command)
        if not err:
            return out
        else:
            return False
    
    def str_flags(self,flags,URL):
        domain = self.split_domain(URL)
        flags["--domain"]=domain
        flags["--output"]= f"{domain}"
        return methods.dic_to_str(flags,postfix=' ')
    
    def paramspider(self,URL,flags={}):
        paramspider_result = self.paramspider_execute(self.str_flags(flags,URL))
        if paramspider_result:
            self.end_points_with_params[URL] = methods.get_file_content(f'output/{self.split_domain(URL)}')
        else:
            self.errors['urls'].append(URL)

    def lparamspider(self,flags={}):
        print("[●] Vulnerabilities Scanning  -  paramspider")
        try:
            thread_objects = []
            for URL in self.URLs:
                t = threads.thread(self.paramspider,args=(URL,flags))
                thread_objects.append(t)
            threads.join_threads(thread_objects)
            methods.rmdir('output',True)
        except Exception as e:
            self.errors['general'] = e     

# spider = paramspider(['http://testhtml5.vulnweb.com','http://testphp.vulnweb.com','http://testasp.vulnweb.com'])
# spider.lparamspider()
# print(f'End point with params: {spider.end_points_with_params}')
# print(f'Errors: {spider.errors}')
