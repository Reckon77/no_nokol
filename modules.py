import re
from tika import parser
def extractText(path):
    raw = parser.from_file(path)
    data=raw['content']
    data = " ".join(data.split())
    data = re.sub(r'http\S+', '', data)
    data=data.split('. ') 
    for i in range (0,len(data)):
        data[i]="\""+data[i]+"\""
    return data