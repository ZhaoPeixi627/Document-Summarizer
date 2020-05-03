import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
from pdfminer.pdfinterp import PDFPageInterpreter,PDFResourceManager
from pdfminer.converter import TextConverter,PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFPage

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
            no1 = request.form['no1']               
            if file.filename == '':
                print('No file selected')
                return redirect(request.url)
            else:
                if file.filename[-3:len(file.filename)] == 'pdf':
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                    fp = open(os.path.join(app.config['UPLOAD_FOLDER'], file.filename),'rb')
                    parser = PDFParser(fp)
                    doc = PDFDocument(parser=parser)
                    parser.set_document(doc=doc)
                    resource = PDFResourceManager()
                    laparam=LAParams()
                    device = PDFPageAggregator(resource,laparams=laparam)
                    interpreter = PDFPageInterpreter(resource,device)
                    for page in PDFPage.get_pages(fp):
                        interpreter.process_page(page)
                        layout = device.get_result()
                        for out in layout:
                            if hasattr(out,'get_text'): 
                                fw = open('old.txt','a')
                                fw.write(out.get_text())
                    fw.close()
                    tmp = open('temp.txt','w')
                    o = open('old.txt', 'r', encoding='utf8')
                    for line in o:
                        print(line)
                        for words in line:
                            if words == '\n':
                                tmp.write(' ')
                            else:
                                tmp.write(words)
                    tmp.close()
                    if fw:
                        process_file2(newname,no1)
                        os.remove('temp.txt')
                        os.remove('old.txt')
                        return redirect(url_for('uploaded_file', newname=newname))
                else:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        process_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename, newname,no1)
                        return redirect(url_for('uploaded_file', newname=newname))
        elif request.form['BTN']=='Download_Keywords':
            if 'file' not in request.files:
                print('No file attached in request')
                return redirect(request.url)
            file = request.files['file']
            keywords = request.form['keywords']
            no2 = request.form['no2']
            if file.filename == '':
                print('No file selected')
                return redirect(request.url)
            else:
                if file.filename[-3:len(file.filename)] == 'pdf':
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                    fp = open(os.path.join(app.config['UPLOAD_FOLDER'], file.filename),'rb')
                    parser = PDFParser(fp)
                    doc = PDFDocument(parser=parser)
                    parser.set_document(doc=doc)
                    resource = PDFResourceManager()
                    laparam=LAParams()
                    device = PDFPageAggregator(resource,laparams=laparam)
                    interpreter = PDFPageInterpreter(resource,device)
                    for page in PDFPage.get_pages(fp):
                        interpreter.process_page(page)
                        layout = device.get_result()
                        for out in layout:
                            if hasattr(out,'get_text'):                      
                                fw = open('old1.txt','a')
                                fw.write(out.get_text())
                    fw.close() 
                    tmp = open('temp1.txt','w')
                    o = open('old1.txt', 'r', encoding='utf8')
                    for line in o:
                        print(line)
                        for words in line:
                            if words == '\n':
                                tmp.write(' ')
                            else:
                                tmp.write(words)
                    tmp.close()
                    if fw:
                        process_file3(keywords,no2)
                        os.remove('temp1.txt')
                        os.remove('old1.txt')
                        return redirect(url_for('uploaded_file1', keywords=keywords))   
                else:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        process_file1(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename, keywords,no2)
                        return redirect(url_for('uploaded_file1', keywords=keywords))
    return render_template('main.html')

def process_file1(path,filename,keywords,no2):
    input_file = open(app.config['UPLOAD_FOLDER'] + filename)
    content = input_file.read()
    with open('input.txt','w') as f:
        f.write(str(content))
    f.close()
    args = 'python3 textrank.py -p input.txt -l '+str(no2)+' -t'+' '+str(keywords)
    os.system(args)

def process_file(path, filename, newname,no1):
    input_file = open(app.config['UPLOAD_FOLDER'] + filename)
    content = input_file.read()
    with open('new.txt','w') as f:
        f.write(str(content))
    f.close()
    args = 'python3 textrank.py -p new.txt -s -l '+str(no1)+' -t'+' '+str(newname)
    os.system(args)

def process_file2(newname,no1):
    args = 'python3 textrank.py -p temp.txt -s -l '+str(no1)+' -t'+' '+str(newname)
    os.system(args)

def process_file3(keywords,no2):
    args = 'python3 textrank.py -p temp1.txt -l '+str(no2)+' -t'+' '+str(keywords)
    os.system(args)

@app.route('/<newname>')
def uploaded_file(newname):
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), newname+'.txt', as_attachment=True)

@app.route('/<keywords>')
def uploaded_file1(keywords):
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), keywords+'.txt', as_attachment=True)


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)
