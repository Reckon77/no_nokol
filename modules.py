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
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')

# Line we have to update outdated line:
chrome_options.add_argument(
    'userAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
browser = webdriver.Chrome(
    ChromeDriverManager().install(), options=chrome_options)


def findPlag(sentence_to_search):
    sentence_to_search = sentence_to_search.replace(' ', '+')
    url = f'https://www.google.com/search?q="{sentence_to_search}"&num10'

    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    result = soup.find('div', class_='card-section rQUFld')
    if result == None:
        try:
            link = soup.find('div', class_='yuRUbf').a['href']
            return link
        except:
            return ""
    else:
        return ''

def checkPlag(data):
    res={}
    for sentence in data:
        res[sentence]=findPlag(sentence)
    return res
