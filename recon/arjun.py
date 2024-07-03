import os
import sys
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import methods
import threads

class arjun:
    def __init__(self,end_points):
        self.end_points=end_points
        self.end_points_with_params={}
        self.errors={'end_points':[],'general':[]}
	
    def split_endpoint(self,URL):
        return URL.split('/')[-1]
    
    def arjun_execute(self,str_flags):
        command = f"arjun {str_flags} 2> /dev/null"
        _,out,err=methods.execute_command(command)
        if not err:
            return out
        else:
            return False
    
    def str_flags(self,flags,end_point):
        file_name=self.split_endpoint(end_point)
        flags["-u"]=end_point
        flags["-oT"]= f"AR-{file_name}.txt"
        return methods.dic_to_str(flags,postfix=' ')
    
    def arjun(self,end_point,flags={}):
        arjun_result = self.arjun_execute(self.str_flags(flags,end_point))
        if arjun_result:
            self.end_points_with_params[end_point] = methods.get_file_content(flags["-oT"])
        else:
            self.errors[flags["-oT"]].append(end_point)

    def larjun(self,flags={}):
        print("[●] Vulnerabilities Scanning  -  Arjun")
        try:
            thread_objects = []
            for end_point in self.end_points:
                t = threads.thread(self.arjun,args=(end_point,flags))
                thread_objects.append(t)
            threads.join_threads(thread_objects)

        except Exception as e:
            self.errors['general'] = e     

# arj = arjun(['http://testhtml5.vulnweb.com','http://testphp.vulnweb.com','http://testasp.vulnweb.com'])
# arj.larjun()
# print(f'End point with params: {arj.end_points_with_params}')
# print(f'Errors: {arj.errors}')
