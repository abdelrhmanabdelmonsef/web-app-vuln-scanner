import subprocess
from Operations import Operations

class ResourcesEnumeration:
    def __init__(self):
        self.URLs=[] # urls is stripped from previous process
        self.end_points=[]
        self.end_points_with_params=[]

    # dirsearch.py -e php,html,js -u https://target -w /path/to/wordlist
    # tool output:
    def dirsearch(self,flags={}):
        errors={}
        end_points=[]
        print("Starting Dirsearch ...\n=======================")
        for URL in self.URLs:
            domain_name=URL.split('//')[-1].split('/')[0]
            flags["-o"]= f"{domain_name}.txt" # dirsearch/{host}.txt
            flags["-u"]=URL
            str_flags=Operations.dic_to_str(flags,postfix=" ")
            command = f"python3 /home/mahmoud/dirsearch/dirsearch.py {str_flags} 2> /dev/null"
            print(f"[+]URL: {URL}")
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, start_new_session=True)
            proc.wait()
            #stdout, stderr = proc.communicate()
            #proc.wait()
            # shell return 0 if success, otherwise if fault 
            if not proc.returncode:
                is_exist=Operations.is_exist(flags["-o"])
                # check if a file is been created by dirsearch, if success get file content
                if is_exist:
                    end_points+=Operations.dirsearch_extract_urls(flags["-o"])
                else:
                    errors[URL]="No End Points Found!!"
            else:
                errors[URL]="Sub Process Error!!"
            # if errors[URL]:
            #     print(f"ERROR: {errors[URL]}")
            # else:
            #     print(f"EndPoints Found.")
        self.end_points+=Operations.uniq_list(end_points)
        print()
        return errors
    
    # paramspider.py --domain bugcrowd.com --exclude woff,css,js,png,svg,php,jpg --output bugcrowd.txt
    def paramspider(self,flags={}):
        endpoints_with_params=[]
        print("Starting paramspider ...\n=======================")

        for URL in self.URLs:
            host=URL.split('//')[-1].split('/')[0]
            errors={}
            flags["--domain"]=host
            flags["--output"]= f"{host}.txt"
            print(f"[+]Host: {host}")
            str_flags=Operations.dic_to_str(flags,postfix=" ")
            command = f'python3 "/home/mahmoud/Web Vulnarability Scanner/ParamSpider/paramspider.py" {str_flags} 2> /dev/null'
            #proc = subprocess.run(command, shell=True)
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, start_new_session=True)
            proc.wait()
    
            if not proc.returncode:
                is_exist=Operations.is_exist(flags["--output"])
                # check if a file is been created by dirsearch, if success get file content
                if is_exist:
                    endpoints_with_params+=Operations.get_file_content(f"output/{flags['--output']}")
                else:
                    errors[host]="No params Found!!"
            else:
                errors[host]="Sub Process Error!!"
            # #if errors[host]:
            #     print(f"{URL} => {errors[URL]}")
            # else:
            #     print(f"{URL} ==> EndPoints Found.")
    
        self.end_points_with_params+=Operations.uniq_list(endpoints_with_params)
        print()
        return errors

    # arjun -u https://api.example.com/endpoint -m POST -oT result.txt
    def arjun(self,flags={}):
        end_point_with_params=[]
        errors={}
        print("Starting arjun ...\n=====================")

        for end_point in self.end_points:
            file_name=end_point.split('/')[-1]
            flags["-u"]=end_point
            flags["-oT"]= f"AR-{file_name}.txt"
            print(f"[+] End_Point: {end_point}")

            str_flags=Operations.dic_to_str(flags,postfix=" ")
            command = f"arjun {str_flags} 2> /dev/null"
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, start_new_session=True)
            proc.wait()
            if not proc.returncode:
                is_exist=Operations.is_exist(flags["-oT"])
                # check if a file is been created by dirsearch, if success get file content
                if is_exist:
                    end_point_with_params+=Operations.get_file_content(flags["-oT"])
                else:
                    errors[file_name]="No params Found!!"
            else:
                errors[file_name]="Sub Process Error!!"
        self.end_points_with_params+=Operations.uniq_list(end_point_with_params)
        print()
        return errors

# # Example usage in main class 
re_enum=ResourcesEnumeration()
re_enum.URLs=['http://testhtml5.vulnweb.com','http://testphp.vulnweb.com']
dirsearch_errors=re_enum.dirsearch({"-w":"wordlist.txt"})
paramspider_errors=re_enum.paramspider()
arjun_errors=re_enum.arjun()
print(f"URLS \n=============\n{re_enum.URLs}\n")
print(f"End_points \n=============\n{re_enum.end_points}\n")
print(f"End_Points_with_Params \n=============\n{re_enum.end_points_with_params}\n")


