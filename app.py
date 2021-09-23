#Importing required libs
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from os.path import join, dirname, realpath
from modules import *
import shutil
#flask config
app = Flask(__name__)
#setting the absolute path for file upload folder
path_file = os.getcwd() #Gets current working directory path
path_final_name = path_file + '/static/uploads/'
UPLOADS_PATH = path_final_name #Passing it to variable store for config
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024 #File size limit 20mb

#English plag check route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.files:
            #getting the uploaded file
            file = request.files['file']
            if not os.path.exists(path_final_name):
                os.mkdir(path_final_name)
            #empty file name returns error
            if file.filename == "":
                return render_template('error.html')
            #file validation
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                    #adding the file in the uploads folder
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    #getting the file path
                path=f"./static/uploads/{filename}"
                    #extracting text from data
                data=extractText(path)
                    # print(data)
                res={}
                try:
                    if os.path.exists(path_final_name):
                        shutil.rmtree(path_final_name)
                    #getting the links and other attributes
                    res,plagCount,total,mostProbable=checkPlag(data)
                    # print(res)
                    return render_template('display.html',res=res,plagCount=plagCount,total=total,mostProbable=mostProbable)
                except:
                    if os.path.exists(path_final_name):
                        shutil.rmtree(path_final_name)
                    return render_template('error.html')
            else:
                if os.path.exists(path_final_name):
                        shutil.rmtree(path_final_name)
                return render_template('error.html')
        else:
            if os.path.exists(path_final_name):
                        shutil.rmtree(path_final_name)
            return render_template('error.html')
    return render_template('index.html')
#English text area post route
@app.route('/textdata',methods=['POST'])
def textdata():
    if request.method=='POST':
        try:
            #getting the text data
            data = request.form["input"]
            if data == "":
                return render_template('error.html')
            #breaking it into sentences
            data = inputDataExtract(data)
            res={}
            #getting the links
            res,plagCount,total,mostProbable=checkPlag(data)
            # print(res)
            return render_template('display.html',res=res,plagCount=plagCount,total=total,mostProbable=mostProbable)
        except:
            return render_template('error.html')
#Assamese plag check route          
@app.route('/assamese',methods=['GET','POST'])
def assamese():
    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            if not os.path.exists(path_final_name):
                os.mkdir(path_final_name)
            if file.filename == "":
                return render_template('error.html')
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                path=f"./static/uploads/{filename}"
                data,assameseData=extractAssameseText(path)
                res={}
                try:
                    if os.path.exists(path_final_name):
                        shutil.rmtree(path_final_name)
                    res,plagCount,total,mostProbable=checkPlagNormal(data)
                    # print(res)
                    return render_template('display.html',res=res,plagCount=plagCount,total=total,assameseData=assameseData,mostProbable=mostProbable)
                except:
                    if os.path.exists(path_final_name):
                        shutil.rmtree(path_final_name)
                    return render_template('error.html')
            else:
                if os.path.exists(path_final_name):
                        shutil.rmtree(path_final_name)
                return render_template('error.html')
        else:
            if os.path.exists(path_final_name):
                        shutil.rmtree(path_final_name)
            return render_template('error.html')
    return render_template('assamese.html')
#Assamese text area post route
@app.route('/assameseText',methods=['POST'])
def assameseText():
    if request.method=='POST':
        try:
            data = request.form["input"]
            if data == "":
                return render_template('error.html')
            data,assameseData= inputAssameseDataExtract(data)
            # print(data)
            res={}
            res,plagCount,total,mostProbable=checkPlagNormal(data)
            # print(res)
            return render_template('display.html',res=res,plagCount=plagCount,total=total,assameseData=assameseData,mostProbable=mostProbable)
        except:
            return render_template('error.html')
#Intelligent plag check route
@app.route("/intelligent",methods=['GET','POST'])
def intelligent():
    if request.method == "POST":
        if request.files:
            file = request.files['file']
            if not os.path.exists(path_final_name):
                os.mkdir(path_final_name)
            if file.filename == "":
                return render_template('error.html')
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                path=f"./static/uploads/{filename}"
                data=extractText(path)
                #getting the synonym transformed sentences
                # data,original=transformToSynonyms(data)
                res={}
                try:
                    if os.path.exists(path_final_name):
                        shutil.rmtree(path_final_name)
                    res,plagCount,total,mostProbable=checkPlagIntelligent(data)
                    # print(res)
                    return render_template('displayIntelligent.html',res=res,plagCount=plagCount,total=total,mostProbable=mostProbable)
                except:
                    if os.path.exists(path_final_name):
                        shutil.rmtree(path_final_name)
                    return render_template('error.html')
            else:
                if os.path.exists(path_final_name):
                        shutil.rmtree(path_final_name)
                return render_template('error.html')
        else:
            if os.path.exists(path_final_name):
                        shutil.rmtree(path_final_name)
            return render_template('error.html')
    return render_template('intelligent.html')

#Intelligent text area post route
@app.route('/intelligentTextdata',methods=['POST'])
def intelligentTextdata():
    if request.method=='POST':
        try:
            data = request.form["input"]
            if data == "":
                return render_template('error.html')
            data = inputDataExtract(data)
            #getting the synonym transformed sentences
            # data,original=transformToSynonyms(data)
            res={}
            res,plagCount,total,mostProbable=checkPlagIntelligent(data)
            # print(res)
            return render_template('displayIntelligent.html',res=res,plagCount=plagCount,total=total,mostProbable=mostProbable)
        except:
            return render_template('error.html')

@app.errorhandler(413)
def too_large(e):
    return "File size is too large.", 413

if __name__ == "__main__":
    app.run()