import subprocess
import os
from Operations import Operations
import json

class exploitation1:
    def __init__(self, end_points=[], requests=None):
        self.end_points = end_points
        self.requests = requests
        

    def XSpear(self, flags={}):
        errors = {}
        output_dir = "exploitation/XSpear"
        Operations.mkdir(output_dir)  # Ensure output directory exists
        print("Starting XSpear ...\n=======================")
        reports=[]
        for end_point in self.end_points:
            domain_name = end_point.split('//')[-1].split('/')[0]
            flags["-u"] = f'"{end_point}"'
            flags["-v"]= "0"
            flags["-o"]="json"
            report={}
            str_flags = Operations.dic_to_str(flags, postfix=" ")
            file_name = domain_name + "_" + end_point.split('/')[-1]
            output_file = os.path.join(output_dir, f"{file_name}.txt")
            
            command = f"echo '{end_point}' 1>> {output_file} ; XSpear {str_flags} 1>> {output_file} 2> /dev/null"
            print(f"[+] End_point: {end_point}")
            
            
            try:
                proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, start_new_session=True)
                stdout, stderr = proc.communicate()
                
                if proc.returncode != 0:
                    errors[file_name] = f"Sub Process Error: {stderr.decode().strip()}"
            #        print(f"Error running XSStrike on {end_point}: {stderr.decode().strip()}")       
            except Exception as e:
                errors[file_name] = f"Exception: {str(e)}"
            #    print(f"Exception running XSStrike on {end_point}: {str(e)}")
            result=Operations.get_file_content(output_file,"\n")[1]
            report[end_point]=json.loads(result)
            reports.append(report)
        return [errors,reports]





# Example endpoints
endpoints = ["http://testphp.vulnweb.com/search.php?test=query1"]

# Create an instance of the exploitation class
exploit = exploitation1(end_points=endpoints)

# Run the XSStrike method
errors ,reports= exploit.XSpear()

# Check for any errors
if errors:
    print("Errors encountered:")
    for file_name, error in errors.items():
        print(f"{file_name}: {error}")
        
else:
    print("XSStrike executed successfully for all endpoints.")
    print(f"{list(reports[0].values())[0]["starttime"]}")