#coding:cp1250

class data_frame:
    """Class for managing data input, required value is file path and optional values are"""
    """header, separator and instant load"""

    
    def __init__(self,path, **kwargs):
       options = {
               'header' : 'T',
               'sep' : ',',
               'instant_load' : 'T'
               }
       options.update(kwargs)

       
       if options['instant_load']=='T':
            raw_data = self.load_data(path)
            self.initialize_data(raw_data,options['sep'],options['header'])
                        

    def load_data(self,path):
        """method for loading raw data, specify path to file"""
        
        data=open('data.csv','r')
        raw_data=[]
        for line in data:
            raw_data.append(line)
            
        data.close()
        return raw_data

    def initialize_data(self,raw_data,sep,header):
        """Initializes data into program readable format"""
        try:
            if header=='T':
                self.header=raw_data.pop(0)
                self.header=self.header.rstrip()
                self.header=self.header.split(sep)
                
            data = []
            for row in raw_data:
                data.append(row.split(sep))
            self.data=data
            return "Success"
        except:
            return "Unexpected error"

class analysis:
    """Class made for doing some analysis stuff"""
    
    def __init__(self, data , *args, **kwargs):
        options = {
            'header' : []
            }
        options.update(kwargs)
        self.data=data
        self.header = options['header']
        if ((len(self.header)!=len(self.data[0])) and len(self.header)!=0):
            print "Warning, different length of header and data!"

class report:
    """Makes neat output files"""

    def __init__(self):
        print 'Empty at the moment'
            
    
if __name__ == "__main__":
    x=data_frame("data.csv")
    y=analysis(x.data,header = x.header)
