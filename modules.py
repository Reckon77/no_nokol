import re
from tika import parser
import tika
tika.initVM()
#API keys
from dotenv import load_dotenv
import os
load_dotenv() 
API_KEY=os.getenv("API_KEY")
LOCATION=os.getenv("LOCATION")

#translation
import requests, uuid, json
def translate(text):
    # Add your subscription key and endpoint
    subscription_key = API_KEY
    endpoint = "https://api.cognitive.microsofttranslator.com"

    # Add your location, also known as region. The default is global.
    # This is required if using a Cognitive Services resource.
    location = LOCATION

    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'as',
        'to': ['en']
    }
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

# You can pass more than one object in body.
    body = [{
        'text': text
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    return response[0]['translations'][0]['text']
def extractText(path):
    raw = parser.from_file(path)
    data=raw['content']
    data = " ".join(data.split())
    data = re.sub(r'http\S+', '', data)
    data=data.split('. ') 
    return data
def extractAssameseText(path):
    raw = parser.from_file(path)
    data=raw['content']
    data = " ".join(data.split())
    data = re.sub(r'http\S+', '', data)
    if len(data)>=5000:
        raise "text limit exceeded"
    translatedData=translate(data)
    translatedData=translatedData.split('. ')
    return translatedData,data
def inputAssameseDataExtract(data):
    data = " ".join(data.split())
    data = re.sub(r'http\S+', '', data)
    if len(data)>=5000:
        raise "text limit exceeded"
    translatedData=translate(data)
    translatedData=translatedData.split('. ')
    return translatedData,data
def inputDataExtract(textData):
    textData=" ".join(textData.split())
    textData = re.sub(r'http\S+', '', textData)
    textData=textData.split('. ') 
    return textData
def allowed_file(filename):

    # We only want files with a . in the filename
    if not "." in filename:
        return False

    # Split the extension from the filename
    ext = filename.rsplit(".", 1)[1]

    # Check if the extension is in allowed
    allowed=["PDF", "TXT", "DOCX", "ODT"]
    if ext.upper() in allowed:
        return True
    else:
        return False



# Scrapper
from bs4 import BeautifulSoup

# def findPlag(text):
#     text = text.replace(" ","+")
#     # print(text)
#     url = f'https://www.bing.com/search?q="{text}"&qs=n&form=QBRE&sp=-1&pq={text.lower()}"' # f'https://www.google.com?q="{text}&oq={text}&sourceid=chrome&ie=UTF-8"'  # "https://dataquestio.github.io/web-scraping-pages/simple.html"
#     # Crafting the proper request to fool Google
#     header = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'}
#     page = requests.get(url, headers= header, allow_redirects=True)
#     content = BeautifulSoup(page.content, 'html.parser')
#     # print(content.prettify())
#     # return content
#     # link= content.find('h2')
#     try:
#         element=content.find('li',class_='b_algo').h2
#         link= element.find('a')['href']
#         return link
#     except:
#         return ""
def findPlag(text):
    #text = text.replace(" ","+")
    # print(text)
    url = f'https://www.bing.com/search?q=%2B"{text}"&qs=n&form=QBRE&sp=-1&pq=%2B"{text.lower()}"' # f'https://www.google.com?q="{text}&oq={text}&sourceid=chrome&ie=UTF-8"'  # "https://dataquestio.github.io/web-scraping-pages/simple.html"
    # Crafting the proper request to fool Google
    header = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'}
    page = requests.get(url, headers= header, allow_redirects=True)
    content = BeautifulSoup(page.content, 'html.parser')
    #print(content.prettify())
    #return content
    # link= content.find('h2')
    try:
        element=content.find('li',class_='b_algo').h2
        link= element.find('a')['href']
        return link
    except:
        return ""
def findPlagAssamese(text):
    #text = text.replace(" ","+")
    # print(text)
    url = f'https://www.bing.com/search?q="{text}"&qs=n&form=QBRE&sp=-1&pq="{text.lower()}"' # f'https://www.google.com?q="{text}&oq={text}&sourceid=chrome&ie=UTF-8"'  # "https://dataquestio.github.io/web-scraping-pages/simple.html"
    # Crafting the proper request to fool Google
    header = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'}
    page = requests.get(url, headers= header, allow_redirects=True)
    content = BeautifulSoup(page.content, 'html.parser')
    #print(content.prettify())
    #return content
    # link= content.find('h2')
    try:
        element=content.find('li',class_='b_algo').h2
        link= element.find('a')['href']
        return link
    except:
        return ""
from collections import defaultdict,Counter
def checkPlag(data):
    res={}
    websites=defaultdict(int)
    plagCount=0
    total=0
    for sentence in data:
        link=findPlag(sentence)
        res[sentence]=link
        total+=1
        if link!='':
            websites[link]+=1
        if res[sentence]!='':
            plagCount+=1
    k = Counter(websites)
    mostProbable = k.most_common(3)
    return res,plagCount,total,mostProbable

def checkPlagAssamese(data):
    res={}
    websites=defaultdict(int)
    plagCount=0
    total=0
    for sentence in data:
        link=findPlagAssamese(sentence)
        res[sentence]=link
        total+=1
        if link!='':
            websites[link]+=1
        if res[sentence]!='':
            plagCount+=1
    k = Counter(websites)
    mostProbable = k.most_common(3)
    return res,plagCount,total,mostProbable
#Intelligent Plagiarism checker
import nltk
from nltk.corpus import wordnet
from nltk.corpus import brown
freqs = nltk.FreqDist(w.lower() for w in brown.words())

def findSynonym(word):
    synonyms = []
    if len(word)==0:
        return ""
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
    if len(synonyms)==0:
        return word
    synonyms=set(synonyms)
    synonyms=list(synonyms)
    maxFreq=freqs[synonyms[0]]
    wrd=synonyms[0]
    for synWord in synonyms:
        if freqs[synWord]>maxFreq:
            wrd=synWord
            maxFreq=freqs[synWord]
    if word.upper()==wrd.upper():
        return word
    if word[0].isupper():
        return wrd.capitalize()
    return wrd

def transformSentence(text):
    text = nltk.word_tokenize(text)
    synonyms=[]
    for w in text:
        synonyms.append(findSynonym(w))
    res=" ".join(synonyms)
    res2=""
    if len(res)==0:
        return res
    res2+=res[0]
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for x in range(1, len(res)):
        if res[x] in punctuations and res[x-1]==' ':
            res2 = res2[:-1]
        res2+=res[x]
    return res2

def transformToSynonyms(data):
    synonymSentences=[]
    for s in data:
        synonymSentences.append(transformSentence(s))
    return synonymSentences,data