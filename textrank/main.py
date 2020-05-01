import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

app = Flask(__name__, static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
# limit upload size upto 8mb
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['BTN']=='Download_Summary':
            if 'file' not in request.files:
                print('No file attached in request')
                return redirect(request.url)
            file = request.files['file']
            newname = request.form['newname']
            if file.filename == '':
                print('No file selected')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                process_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename, newname)
                return redirect(url_for('uploaded_file', newname=newname))
        elif request.form['BTN']=='Download_Keywords':
            if 'file' not in request.files:
                print('No file attached in request')
                return redirect(request.url)
            file = request.files['file']
            keywords = request.form['keywords']
            if file.filename == '':
                print('No file selected')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                process_file1(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename, keywords)
                return redirect(url_for('uploaded_file1', keywords=keywords)) 
    return render_template('main.html')

def process_file1(path,filename,keywords):
    input_file = open(app.config['UPLOAD_FOLDER'] + filename)
    content = input_file.read()
    with open('input.txt','w') as f:
        f.write(str(content))
    f.close()
    args = 'python3 textrank.py -p input.txt -l 10 -t'+' '+str(keywords)
    os.system(args)

def process_file(path, filename, newname):
    input_file = open(app.config['UPLOAD_FOLDER'] + filename)
    content = input_file.read()
    with open('new.txt','w') as f:
        f.write(str(content))
    f.close()
    args = 'python3 textrank.py -p new.txt -s -l 3 -t'+' '+str(newname)
    os.system(args)

@app.route('/<newname>')
def uploaded_file(newname):
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), newname+'.txt', as_attachment=True)

@app.route('/<keywords>')
def uploaded_file1(keywords):
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), keywords+'.txt', as_attachment=True)


if __name__ == '__main__':
    app.run(debug = True)
    # app.run(host = '0.0.0.0', port = 5000)