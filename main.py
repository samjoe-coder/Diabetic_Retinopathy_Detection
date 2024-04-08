from flask import request, render_template, redirect, url_for, session
from config import app, db
from models import User, Prediction, Report
import os
from uniqueCode import generate_unique_code
from tensorflow.keras.models import Model
from detection_model.drModel import predict, load_model
from report import generate_pdf_report

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return redirect(url_for('prediction'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('prediction'))
    return render_template('login.html')

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if 'user_id' not in session:
        return redirect(url_for('signup')) ## change to login
    if request.method == 'POST':
        if 'image' not in request.files:
            return 'No file part', 400
        
        drImage = request.files['image']
        if drImage.filename == '':
            return 'No selected file'
        
        if drImage:
            #generate a unique code for the image
            #save the image with the unique code
            #save the unique code in the database

            code = generate_unique_code()
            _, file_extension = os.path.splitext(drImage.filename)
            fileName = code + file_extension

            fn = os.path.join(app.config['UPLOAD_FOLDER'], fileName)
            drImage.save(fn)

            x,y = load_model()
            model = Model(inputs=x, outputs=y, name='Resnet18')
            model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
            model.load_weights("retina_weights.hdf5")

            imageToPredict = os.path.join(app.config['UPLOAD_FOLDER'], fileName)
            result = predict(imageToPredict, model)

            prediction = Prediction(user_id=session['user_id'], image=fileName, prediction=result)
            db.session.add(prediction)
            db.session.commit()

            # Generate PDF report
            generate_pdf_report(imageToPredict, result, code)
            
            
            return result

    return render_template('prediction.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)

