from dataclasses import dataclass
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
database_uri_mysql = "mysql://sql9343372:M9n5hMmtQP@sql9.freemysqlhosting.net:3306/sql9343372"
database_uri_postgres = "postgres://kqpakbfg:HKfT25s4G3yf89SxJQXkH-pxVmIwsWnS@ruby.db.elephantsql.com:5432/kqpakbfg"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri_postgres
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

db = SQLAlchemy(app)


class Doctor(db.Model):
    # __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    reviews = db.relationship('Review', backref='doctor', lazy=True)

    def as_dict(self):
        ans = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        ans["reviews"] = [review.as_dict() for review in self.reviews]
        return ans


class Review(db.Model):
    # __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# Create a doctor
@app.route('/doctors', methods=['POST'])
def add_doctor():

    data = request.get_json()  # data: dict
    doctor = Doctor(name=data['name'])
    db.session.add(doctor)
    db.session.commit()

    return "Added doctor " + str(data['name'])

# Add a review to existing doctor
@app.route('/doctors/<doctorid>/reviews', methods=['POST'])
def add_review(doctorid):

    data = request.get_json()

    review = Review(description=data['description'], doctor_id=doctorid)
    db.session.add(review)
    db.session.commit()

    doctor = Doctor.query.filter_by(id=doctorid).first()
    doctor.reviews.append(review)

    return "Added review \"" + str(data['description']) + "\" " \
            "to doctor " + doctor.name + " (id: " + str(doctor.id) + ")"

# List all doctors and their reviews
@app.route('/doctors', methods=['GET'])
def get_all_doctors():

    doctors = Doctor.query.all()
    return jsonify([doctor.as_dict() for doctor in doctors])

# List a doctor and the review(s)
@app.route('/doctors/<doctorid>', methods=['GET'])
def get_doctor(doctorid):

    doctor = Doctor.query.filter_by(id=doctorid).first()
    return jsonify(doctor.as_dict())

# Delete a review from a doctor
@app.route('/doctors/<doctor_id>/reviews/<review_id>', methods=['DELETE'])
def delete_review():
    if request.method == 'DELETE':

        data = request.get_json()

        print('Data Received: "{data}"'.format(data=data))
        return "Request Processed.\n"

# Delete a doctor
@app.route('/doctors/<doctor_id>', methods=['DELETE'])
def delete_doctor():
    if request.method == 'DELETE':

        data = request.get_json()

        print('Data Received: "{data}"'.format(data=data))
        return "Request Processed.\n"

#flask run -h localhost -p 3000

# from application import create_app

# app = create_app()

# if __name__ == "__main__":
#     app.run(host='0.0.0.0')

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/cars_api"