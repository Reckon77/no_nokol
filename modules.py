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

def allowed_file(filename):

    # We only want files with a . in the filename
    if not "." in filename:
        return False

    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    # Check if the extension is in allowed
    allowed=["PDF", "TXT", "DOCX"]
    if ext.upper() in allowed:
        return True
    else:
        return False