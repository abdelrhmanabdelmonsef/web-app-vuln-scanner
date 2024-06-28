import subprocess
from Operations import Operations
from api import reporting
class nuclei_class:

    def __init__(self,endpoint=[]):
        self.end_points=endpoint

    def nuclei(self, flags={}):
        errors = []
        reports={}
        print("Starting nuclei ...\n=======================")
        for end_point in self.end_points:
            flags["-u"] = end_point
            str_flags = Operations.dic_to_str(flags, postfix=" ")
            command = f"nuclei {str_flags} -nc 1>nuclei_out.txt 2> /dev/null"
            try:
                proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, start_new_session=True)
                proc.communicate()
                file=Operations.get_file_content("nuclei_out.txt","\n")
                response=reporting(file,"for high , medium and low risk vuln mention all details ,create a markdown report")
                reports[end_point]=response
            except Exception as e:
               errors.append(end_point)
               # errors[file_name] = f"Exception: {str(e)}"
            #   print(f"Exception running XSStrike on {end_point}: {str(e)}")
        return [errors,reports]



nuc=nuclei_class(["https://0a6000aa03b6a227819c2130009d00a7.web-security-academy.net/image?filename=25.jpg"])
nucerr,nucrep=nuc.nuclei()
print(f"nuclei report: {nucrep} \n\n nuclei error: {nucerr}")