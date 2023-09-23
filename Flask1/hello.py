from flask import Flask, flash, render_template, request
from werkzeug.utils import secure_filename
import os
import cv2
import os
import replicate

#Set the REPLICATE_API_TOKEN environment variable
os.environ["REPLICATE_API_TOKEN"] = "r8_4mzrd8fmOlbhcZuuzQuggfOUrYu3hHb2EixMP"

UPLOAD_FOLDER = "Images"
ALLOWED_EXTENSIONS = {'png','jpeg','jpg','svg','webp','gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def processImage(filename, operation):
    print(f"Operation is {operation} and Image is {filename}")
    img = cv2.imread(f"Images/{filename}")
    img2=(f"Images/{filename}")
    match operation:
        case "grayscale":
            image_proc = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            new_file = f"static/{filename}"
            cv2.imwrite(f"static/{filename}", image_proc)
            return new_file
        case "webp":
            new_file = (f"static/{filename.split('.')[0]}.webp")
            cv2.imwrite(new_file, img)
            return new_file
        case "png":
            new_file = (f"static/{filename.split('.')[0]}.png")
            cv2.imwrite(new_file, img)
            return new_file
        case "jpg":
            new_file = (f"static/{filename.split('.')[0]}.jpg")
            cv2.imwrite(new_file, img)
            return new_file
        case "upscale":
            new_file = replicate.run(
                "tencentarc/gfpgan:9283608cc6b7be6b65a8e44983db012355fde4132009bf99d976b2f0896856a3",
                input={"img": open(img2, "rb")}
            )
            print(new_file)
            return new_file

@app.route("/")
def hello_world():
    return render_template("index.html")
@app.route("/about")
def aboutPage():
    return render_template("about.html")

@app.route("/edit", methods=["GET","POST"])
def editImage():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('Image Not Found')
            return "Error"
        file = request.files['file']
        operation = request.form.get('operation')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            new_images = processImage(filename, operation)
            flash(f"Image is proccessed, you can downlaod it <a href='{new_images}' target=_blank>here</a> ")
            
            return render_template('index.html')


app.run(debug=True, port=5001)