# NO_NOKOL Plagiarism-Checker

A web application to check if a documents contents are plagiarised with multiple options availaible based upon the requirements.

## To run the app

1. run command "pip install -r requirements.txt"
2. run command "python app.py" in the terminal

### Note1 : Make sure that Java is installed in your machine to use the tika package

### Note2 : To use the Assamese Plag-Check, follow these steps :

1. Get your API key and location to use the Microsoft translation API ( refer [here](https://azure.microsoft.com/en-in/services/cognitive-services/translator/))
2. Create a .env file and write this code (replace "yourAPIkey" and "yourLocation" with the one that you obtained in step i.)

```
API_KEY=yourAPIkey
LOCATION=yourLocation
```

## How it works

- Based on the requirements there are three approaches to this project.
- It searches online using web scarapper designed to utilize Bing serarch engine for some queries. Queries are extracted from the source txt/pdf/odt/txt file.
- First approach works on English extracted data.
- Second approach works on Assamese data translated using [Microsoft Translator api](https://docs.microsoft.com/en-us/azure/cognitive-services/translator/quickstart-translator?tabs=python#translate-text) and then translated data is fed to scrapper for match.
- Third approach works in a way extracted data is fed to a logic where synonyms are recoginized using NLTK Synset and then we replace the nouns and adjectives with its most commonly used synonym (obtained from NLTK brown corpus) after that matches are found using the same method.
- Resulting URL, matched contents are checked for similarity with given text query.
- Finally the most probable source is displayed on views with information showning plagiarised percentage and sentences.

## Required Libraries

- The project uses tika module to extract text from files.
- Other required libraries are:
  - beautifulsoup4==4.10.0
  - bs4==0.0.1
  - certifi==2021.5.30
  - charset-normalizer==2.0.6
  - click==8.0.1
  - colorama==0.4.4
  - Flask==2.0.1
  - idna==3.2
  - itsdangerous==2.0.1
  - Jinja2==3.0.1
  - joblib==1.0.1
  - MarkupSafe==2.0.1
  - nltk==3.6.3
  - python-dotenv==0.19.0
  - regex==2021.8.28
  - requests==2.26.0
  - soupsieve==2.2.1
  - tika==1.24
  - tqdm==4.62.3
  - urllib3==1.26.6
  - Werkzeug==2.0.1

## Folder Structure

- [Static/](https://github.com/Reckon77/no_nokol/tree/main/static) : Contains views functionallity logics, script and styles.
- [Templates/](https://github.com/Reckon77/no_nokol/tree/main/templates) : Contains html files for rendering on views.
- [app.py](https://github.com/Reckon77/no_nokol/blob/main/app.py) : Main script file for running FLask application.
- [modules.py](https://github.com/Reckon77/no_nokol/blob/main/modules.py) : Consists of scrapper logic and required modules like tika logic for extracting text.

## License 

This project is licensed under the [MIT License](https://github.com/Reckon77/no_nokol/blob/main/LICENSE).
