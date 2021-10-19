#Importing required libs
import re
#Tika is used to import text data from pdf,docx,txt files
from tika import parser
import tika
tika.initVM()
#API keys
from dotenv import load_dotenv
import os
load_dotenv() 
API_KEY=os.getenv("API_KEY")
LOCATION=os.getenv("LOCATION")

from nltk.tokenize import sent_tokenize

#function to translate input language into english (Microsoft Translation API)
import requests, uuid, json
def translate(text,language):
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
        'from': language,
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
def extractData(path):
    raw = parser.from_file(path)
    data=raw['content']
    return data

def cleanData(data):
    #remove extra space
    data = " ".join(data.split())
    #remove links
    data = re.sub(r'http\S+', '', data)
    return data
#function to extract the english text data from files and return it
def extractText(path):
    #extract
    data=extractData(path)
    #clean
    data = cleanData(data)
    #break into sentences
    data=sent_tokenize(data)
    # data=data.split('. ') 
    #return array of sentences
    return data
#Extract and tokenize assamese text
def extractAssameseText(path):
    #extract
    data=extractData(path)
    #clean
    data = cleanData(data)
    #break into sentences
    data=data.split('। ')
    # data=data.split('. ') 
    #return array of sentences
    return data

#function to extract the multilingual text data from files and return it
def extractMultilingualText(path,language):
    data=extractData(path)
    data = cleanData(data)
    #since MS API support translation upto 5000 characters only
    if len(data)>=5000:
        raise "text limit exceeded"
    translatedData=translate(data,language)
    translatedData=sent_tokenize(translatedData)
    # translatedData=translatedData.split('. ')
    return translatedData,data
#function to extract the multilingual text data from text area input and return it
def inputMultilingualDataExtract(data,language):
    data = cleanData(data)
    if len(data)>=5000:
        raise "text limit exceeded"
    translatedData=translate(data,language)
    translatedData=sent_tokenize(translatedData)
    # translatedData=translatedData.split('. ')
    return translatedData,data
#function to extract the english text data from text area input and return it
def inputDataExtract(data):
    data = cleanData(data)
    data=sent_tokenize(data)
    # textData=textData.split('. ') 
    return data
def assameseInputDataExtract(data):
    data = cleanData(data)
    # data=sent_tokenize(data)
    data=data.split('। ') 
    # print(data)
    return data

#file validation function
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
#function that return a link if exact match of the query is found
def findPlag(text,sourceFilter=""):
    #text = text.replace(" ","+")
    # print(text)
    url = f'https://www.bing.com/search?q=%2B"{text}"&qs=n&form=QBRE&sp=-1&pq=%2B"{text.lower()}"'
    # Crafting the proper request 
    header = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'}
    page = requests.get(url, headers= header, allow_redirects=True)
    content = BeautifulSoup(page.content, 'html.parser')
    #print(content.prettify())
    #return content
    # link= content.find('h2')
    try:
        element=content.find('li',class_='b_algo').h2
        link= element.find('a')['href']
        if link == sourceFilter:
            return ""
        else:
            return link
    except:
        return ""
#function that return a link for relevant match of the query is found
def findPlagNormal(text,sourceFilter=""):
    #text = text.replace(" ","+")
    # print(text)
    url = f'https://www.bing.com/search?q="{text}"&qs=n&form=QBRE&sp=-1&pq="{text.lower()}"' 
    header = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'}
    page = requests.get(url, headers= header, allow_redirects=True)
    content = BeautifulSoup(page.content, 'html.parser')
    #print(content.prettify())
    #return content
    # link= content.find('h2')
    try:
        element=content.find('li',class_='b_algo').h2
        link= element.find('a')['href']
        if link == sourceFilter:
            return ""
        else:
            return link
        return link
    except:
        return ""

#function that takes array of sentences as input and returns associated links, plagiarism count
#total sentences, mostProbable sentences using exact match function
from collections import defaultdict,Counter
def checkPlag(data,sourceFilter=""):
    res={}
    websites=defaultdict(int)
    plagCount=0
    total=0
    for sentence in data:
        link=findPlag(sentence,sourceFilter)
        res[sentence]=link
        total+=1
        if link!='':
            websites[link]+=1
        if res[sentence]!='':
            plagCount+=1
    k = Counter(websites)
    mostProbable = k.most_common(3)
    return res,plagCount,total,mostProbable
#function that takes array of sentences as input and returns associated links, plagiarism count
#total sentences, mostProbable sentences using relevant match function
def checkPlagNormal(data,sourceFilter=""):
    res={}
    websites=defaultdict(int)
    plagCount=0
    total=0
    for sentence in data:
        link=findPlagNormal(sentence,sourceFilter)
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
#function that takes a word as input and returns the most common synonym
#if the word is a noun or adjective
def findSynonym(word):
    synonyms = []
    if len(word)==0:
        return ""
    wordList=[]
    wordList.append(word)
    #checking for noun or adjective (NLTK POS tagging)
    tagged = nltk.pos_tag(wordList)
    allowed=["NN","NNS","JJ","JJR","JJS"]
    POS=tagged[0][1]
    if POS not in allowed:
        return word
    #getting all the synonyms of a word
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
    if len(synonyms)==0:
        return word
    synonyms=set(synonyms)
    synonyms=list(synonyms)
    maxFreq=freqs[synonyms[0]]
    wrd=synonyms[0]
    #getting the synonym with maximum frequency using brown corpus of NLTK
    for synWord in synonyms:
        if freqs[synWord]>maxFreq:
            wrd=synWord
            maxFreq=freqs[synWord]
    if word.upper()==wrd.upper():
        return word
    if word[0].isupper():
        return wrd.capitalize()
    return wrd
# function to apply the findSynonym() function in a sentence and return it
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
# function to apply the transformSentence(text) function in an array of sentences and return it
def transformToSynonyms(data):
    synonymSentences=[]
    for s in data:
        synonymSentences.append(transformSentence(s))
    return synonymSentences,data

def checkPlagIntelligent(data,sourceFilter=""):
    res={}
    websites=defaultdict(int)
    plagCount=0
    total=0
    for sentence in data:
        tranformedText=transformSentence(sentence)
        link=findPlagNormal(tranformedText,sourceFilter)
        res[sentence]=[tranformedText,link]
        total+=1
        if link!='':
            websites[link]+=1
        if res[sentence][1]!='':
            plagCount+=1
    k = Counter(websites)
    mostProbable = k.most_common(3)
    return res,plagCount,total,mostProbable