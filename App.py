from flask import Flask, render_template, Response, request, jsonify, session

from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField, DecimalRangeField, IntegerRangeField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired,NumberRange
import os

import cv2


from yoloWebCam import video_detection
app = Flask(__name__)

app.config['SECRET_KEY'] = 'Marck121'
app.config['UPLOAD_FOLDER'] = 'static/files'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit =  SubmitField("Run")

def generate_frame(path_x = ''):
    yolo_output = video_detection(path_x)

    for detection_ in yolo_output:
        ref, buffer = cv2.imencode('.jpg', detection_)

        frame = buffer.tobytes()
        yield(b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/', methods = ['GET','POST'])
@app.route('/home', methods = ['GET', 'POST'])
def hom():
    session.clear()
    return render_template('index.html')

@app.route('/webcam', methods=['GET', 'POST'])
def webcam():
    session.clear()
    return render_template('ui.html')

@app.route('/acerca')
def acerca():
    session.clear()
    return render_template('acerca.html')

@app.route('/recomendaciones')
def recomendaciones():
    session.clear()
    return render_template('recomendaciones.html')

@app.route('/FrontPage', methods = ['GET', 'POST'])
def front():
    form = UploadFileForm()
    if form.validate_on_submit():
        
        #la ruta del video se guarda aqui

        file = form.file.data
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename)))

        session['video_path'] = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],
                                             secure_filename(file.filename))
        
    return render_template('videoproject.html', form = form)


@app.route('/video')
def video():
    return Response(generate_frame(path_x=session.get('video_path',None)), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webapp')
def webapp():
    return Response(generate_frame(path_x=0), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')