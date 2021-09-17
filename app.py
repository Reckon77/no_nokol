from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from os.path import join, dirname, realpath
from modules import *

app = Flask(__name__)
UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/')
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024 #File size limit 10mb


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        if request.files:
            file = request.files['file']
            print(file)


            if file.filename == "":
                return render_template('error.html')
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                path=f"./static/uploads/{filename}"
                data=extractText(path)
                # print(data)
                res={}
                try:
                    res=checkPlag(data)
                    # print(res)
                    return render_template('display.html',res=res)
                except:
                    return render_template('error.html')
            else:
                return render_template('error.html')
        else:
            return render_template('error.html')
    return render_template('index.html')

@app.route('/textdata',methods=['POST'])
def textdata():
    if request.method=='POST':
        data = request.form["input"]
        data = inputDataExtract(data)
        print(data)
        res={}
        try:
            res=checkPlag(data)
            # print(res)
            return render_template('display.html',res=res)
        except:
            return render_template('error.html')
            
@app.route('/assamese',methods=['GET','POST'])
def assamese():
    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            if file.filename == "":
                return render_template('error.html')
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                path=f"./static/uploads/{filename}"
                try:
                    data,assameseData=extractAssameseText(path)
                    res={}
                    res=checkPlag(data)
                    # print(res)
                    return render_template('display.html',res=res,assameseData=assameseData)
                except:
                    return render_template('error.html')
            else:
                return render_template('error.html')
        else:
            return render_template('error.html')
    return render_template('assamese.html')

@app.route('/assameseText',methods=['POST'])
def assameseText():
    if request.method=='POST':
        data = request.form["input"]
        try:
            data,assameseData= inputAssameseDataExtract(data)
            # print(data)
            res={}
            res=checkPlag(data)
            # print(res)
            return render_template('display.html',res=res,assameseData=assameseData)
        except:
            return render_template('error.html')


@app.errorhandler(413)
def too_large(e):
    return "File size is too large.", 413

if __name__ == "__main__":
    app.run(debug=True)