import os
from werkzeug.utils import secure_filename
from flask import Flask,flash,request,redirect,send_file,render_template
from flask import send_from_directory
from rembg.bg import remove
import numpy as np
import io
from PIL import ImageFile, Image

UPLOAD_FOLDER = 'uploads/'
PROCESS_FOLDER = "process/"
#app = Flask(__name__)
app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESS_FOLDER'] = PROCESS_FOLDER


def blend_value(under, over, a):
    return (over*a + under*(255-a)) / 255

def blend_rgba(under, over):
    return tuple([blend_value(under[i], over[i], over[3]) for i in (0,1,2)] + [255])


def image_process(filename):
    print(filename,"imageprocessicinde")
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    print(UPLOAD_FOLDER,filename)
    f = np.fromfile(UPLOAD_FOLDER + filename)
    result = remove(f,
                    alpha_matting=True,
                    alpha_matting_foreground_threshold=240,
                    alpha_matting_background_threshold=10,
                    alpha_matting_erode_structure_size=6)
    img = Image.open(io.BytesIO(result)).convert("RGB")#.convert("RGBA")
    print(img.format,img.mode)

    # https://stackoverflow.com/questions/9166400/convert-rgba-png-to-rgb-with-pil/9459208#9459208
    #img.save("process/background_subtract"+filename,'JPEG', quality=80)
    img.save("process/background_subtract.jpg")
    print("Resim kaydedildi")
    return img


# Upload API
@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return send_from_directory(app.config['UPLOAD_PATH'], filename)
            
            #return redirect(request.url)
        else:
#            return send_from_directory(app.config['UPLOAD_PATH'], filename)
            print(file)
            filename = secure_filename(file.filename) # <FileStorage: 'bjarne.jpg' ('image/jpeg')>
            print(filename) # bjarne...
            print(app.config['UPLOAD_FOLDER']) # uploads/

            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            print("saved file successfully")
            #send file name as parameter to downlad
            
            imageproc = image_process(filename)
            
            #imageproc.save(os.path.join(app.config['PROCESS_FOLDER'], filename))
            #return redirect('/downloadfile/'+ PROCESS_FOLDER + "background_subtract.jpg")
            #return redirect('/downloadfile/'+ PROCESS_FOLDER + filename )
            return send_file(PROCESS_FOLDER + "background_subtract.jpg" )

    return render_template('upload_file.html')

# Download API
@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    return render_template('index.html',value=filename)

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    file_path = UPLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
