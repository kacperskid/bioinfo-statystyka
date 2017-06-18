import os.path

def file_test(file_name):
    """Checks if file exists"""
    if os.path.isfile(file_name):
        print ("File "+file_name+" exists")
    else:
        print ("File "+file_name+" does not exists")

        
def close_test(var):
    """Checks if  files are closed"""
    
    if var.closed:
        print ("File is closed")
        return True
    else:
        print ("File is not closed")
        return False
    

def instance_test(object,method_list=["data","results","headers_of_numeric_columns","report_file_html","report_file"]):
    """Testing to check for presence of attributes, returns results"""
    
    results=[]
    for item in method_list:
        if hasattr(object,item):
            print ("Attribute "+item+" present")
            results.append(True)
        else:
            print ("No attribute "+item+" !!")
            results.append(False)
    return results