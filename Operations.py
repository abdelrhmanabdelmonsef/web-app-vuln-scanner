from pathlib import Path
import re
class Operations:


    @staticmethod
    def is_exist(path):
        file_path = Path(path)
        return file_path.exists()
    # Input: File Path 
    # Action: read file line by line then return list of lines 
    # Output: list of lines
    @staticmethod
    def get_file_content(file_path,str=' '):
        try:
            with open(file_path, 'r') as file:
                lines = []
                for line in file:
                    lines.append(line.strip(str))
            return lines
        except FileNotFoundError:
            return False
    @staticmethod   
    def dirsearch_extract_urls(file_path,str=' '):
        urls = []
        with open(file_path, 'r') as file:
            for line in file:
                # Check if the line starts with 30X
                if re.match(r'30\d', line):
                    match = re.search(r'REDIRECTS TO: (http[^\s]+)', line)
                    if match:
                        urls.append(match.group(1))
                # Check if the line starts with 200
                elif line.startswith('200'):
                    match = re.search(r'(http[^\s]+)', line)
                    if match:
                        
                        urls.append(match.group(1))
        return urls
    # Input: Operation: write => 'w' or append => 'a' ,File Path and List of items
    # action: save each item in a single line
    # Output: return true if operation success and False if failure
    @staticmethod
    def add_list_to_file(lst, file_path, operation):
        with open(file_path, operation) as file:
            file.write("\n".join(lst))
            return True
        return False
    
    # Input: Operation: write => 'w' or append => 'a' ,File Path ,Dictionary, Delimiter
    # action: save key in a single line then each item in a value save in a single line then delimitor + newline
    # Output: return true if operation success and False if failure
    @staticmethod
    def add_dic_to_file(dic, operation, file_path, prefix='', infix=':', postfix='\n',suffix='\n\n'):
        with open(file_path, operation) as file:
            for key, value in dic.items():
                result=prefix+key+infix+value+postfix
                file.write(result)
            file.write(suffix)
            return True
        return False
    
    # Input: List of Items
    # Output: Returns list of uniq Items
    @staticmethod
    def uniq_list(lst):
        result=[]
        for item in lst:
            if item not in result:
                result.append(item)
        result.sort()
        return result

    #input: {"key1":"value1","key2":"value2","key3":"value3"}
    #Output: "key1 value1 key2 value2 key3 value3" 
    @staticmethod
    def dic_to_str(dic,prefix='',infix=' ',postfix=''):
        result=""
        for key,value in dic.items():
            result+=f"{prefix}{key}{infix}{value}{postfix}"
        return result    
