from pathlib import Path
import os
import shutil
import subprocess
import sys

def mkdir(path):
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        return False

def rmdir(path, with_children=False):
    try:
        if with_children:
            shutil.rmtree(path)
        else:
            os.rmdir(path)
        return True
    except Exception as e:
        return False

def rm(file_path):
    if is_exist(file_path):
        os.remove(file_path)
        
def is_exist(path):
    return Path(path).exists()

def get_file_content(file_path,str=' '):
    if is_exist(file_path):
        with open(file_path, 'r') as file:
            lines = []
            for line in file:
                lines.append(line.strip(str))
        return lines
    else:
        return False

def add_list_to_file(lst, file_path, operation, str):
    with open(file_path, operation) as file:
        file.write(str.join(lst))

def add_dic_to_file(dic, operation, file_path, prefix='', infix=':', postfix='\n',suffix='\n\n'):
    with open(file_path, operation) as file:
        for key, value in dic.items():
            result=prefix+key+infix+value+postfix
            file.write(result)
        file.write(suffix)

def uniq_list(lst):
    result=[]
    for item in lst:
        if item not in result:
            result.append(item)
    result.sort()
    return result

def dic_to_str(dic,prefix='',infix=' ',postfix=''):
    result=""
    for key,value in dic.items():
        result+=f"{prefix}{key}{infix}{value}{postfix}"
    return result    

def qsreplace(end_point,value):
    splitor = end_point.split('?')
    domain=splitor[0]
    params = splitor[-1].split('&')
    new_params = [f'{param.split("=")[0]}={value}' for param in params]
    return f"{domain}?{'&'.join(new_params)}"

def execute_command(command):
    proc= subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, start_new_session=True)
    stdout,stderr=proc.communicate()
    return [proc,stdout.decode("utf-8"),stderr.decode("utf-8")]
