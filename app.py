from flask import Flask, request, render_template, send_file
from tensorflow.keras.models import Model
import os
from model.drModel import predict, load_model
from report.pdfReport import generate_pdf_report

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        print(name, email, password)
        return render_template('home.html')








    return render_template('signup.html')

@app.route('/predict', methods=['POST'])
def drPredict():
    if 'image' not in request.files:
        return 'No file part', 400
    
    drImage = request.files['image']
    
    if drImage.filename == '':
        return 'No selected file'

    if drImage:
        fn = os.path.join(app.config['UPLOAD_FOLDER'], drImage.filename)
        drImage.save(fn)

        x,y = load_model()

        model = Model(inputs=x, outputs=y, name='Resnet18')
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        model.load_weights("retina_weights.hdf5")

        imageToPredict = os.path.join(app.config['UPLOAD_FOLDER'], drImage.filename)
        result = predict(imageToPredict, model)

        # Generate PDF report
        pdf_filename = generate_pdf_report(imageToPredict, result)

        # Return the PDF file to the user
        return send_file(pdf_filename, as_attachment=True)

    return 'Error in prediction', 400

if __name__ == '__main__':
    app.run(debug=True)
