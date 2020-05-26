from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:103Mojonera@localhost:5432/doctor_api"

db = SQLAlchemy(app)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    reviews = db.relationship('Review', backref='doctor',lazy = True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(120), nullable=False)
    doctor = db.Column(db.Integer, db.ForeignKey('doctor.id'),nullable=False)


@app.route('/post', methods=['POST'])
def post_route():
    if request.method == 'POST':

        data = request.get_json()
        print(type(data))
        x = dict(data)
        print('dict x: ', x)

        print('Data Received: "{data}"'.format(data=data))
        return "Request Processed.\n"

#flask run -h localhost -p 3000

# from application import create_app

# app = create_app()

# if __name__ == "__main__":
#     app.run(host='0.0.0.0')

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/cars_api"