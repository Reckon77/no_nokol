from flask import Flask
from flask import render_template
from flask import request, redirect
from werkzeug.utils import secure_filename
import os
from os.path import join, dirname, realpath
from modules import *

app = Flask(__name__)
UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/')
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        if request.files:
            file = request.files["file"]
            if file.filename == "":
                return render_template('error.html')
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                path=f"./static/uploads/{filename}"
                data=extractText(path)
                # print(data)
                return render_template('display.html',data=data)
            else:
                return render_template('error.html')
        else:
            return render_template('error.html')
    return render_template('index.html')

if __name__ == "__main__":
    app.run()