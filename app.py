from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

## Configuration

app = Flask(__name__)
# database_uri_mysql = "mysql://sql9343372:M9n5hMmtQP@sql9.freemysqlhosting.net:3306/sql9343372"
database_uri_postgres = "postgres://kqpakbfg:HKfT25s4G3yf89SxJQXkH-pxVmIwsWnS@ruby.db.elephantsql.com:5432/kqpakbfg"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri_postgres
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

db = SQLAlchemy(app)

## Tables

class Doctor(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    reviews = db.relationship('Review', backref='doctor', lazy=True)

    #returns dictionary output of doctor and all reviews of that doctor
    def as_dict(self):
        ans = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        ans["reviews"] = [review.as_dict() for review in self.reviews]
        return ans


class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(120), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    #returns dictionary of review object
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


##Routes

# Create a doctor
@app.route('/doctors', methods=['POST'])
def add_doctor():

    #data: dict where data['name'] = doctor name
    data = request.get_json()
    doctor = Doctor(name=data['name'])
    db.session.add(doctor)
    db.session.commit()

    return "Added doctor " + str(data['name'])

# Add a review to existing doctor
@app.route('/doctors/<doctor_id>/reviews', methods=['POST'])
def add_review(doctor_id):

    #data: dict where data['description'] = text of review
    data = request.get_json()

    review = Review(description=data['description'], doctor_id=doctor_id)
    db.session.add(review)
    db.session.commit()

    #map the review under the existing doctor
    doctor = Doctor.query.filter_by(id=doctor_id).first()
    doctor.reviews.append(review)

    return "Added review \"" + str(data['description']) + "\" " \
            "to doctor " + doctor.name + " (id: " + str(doctor.id) + ")"

# List all doctors and their reviews
@app.route('/doctors', methods=['GET'])
def get_all_doctors():

    doctors = Doctor.query.all()
    return jsonify([doctor.as_dict() for doctor in doctors])

# List a doctor and the review(s)
@app.route('/doctors/<doctor_id>', methods=['GET'])
def get_doctor(doctor_id):

    doctor = Doctor.query.filter_by(id=doctor_id).first()
    return jsonify(doctor.as_dict())

# Delete a review from a doctor
@app.route('/doctors/<doctor_id>/reviews/<review_id>', methods=['DELETE'])
def delete_review(doctor_id, review_id):

    doctor = Doctor.query.filter_by(id=doctor_id).first()
    review = Review.query.filter_by(id=review_id).first()
    db.session.delete(review) #removes the review from the doctor as well
    db.session.commit()

    return "Deleted review \"" + str(review.description) + "\" " \
            "from doctor " + doctor.name + " (id: " + str(doctor.id) + ")"

# Delete a doctor
@app.route('/doctors/<doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):

    doctor = Doctor.query.filter_by(id=doctor_id).first()

    #delete all of the doctor's reviews
    for review in doctor.reviews:
        db.session.delete(review)
    
    #then remove the doctor
    db.session.delete(doctor)
    db.session.commit()

    return "Deleted doctor " + doctor.name + " (id: " + str(doctor.id) + ")"

#flask run -h localhost -p 3000

# from application import create_app

# app = create_app()

# if __name__ == "__main__":
#     app.run(host='0.0.0.0')

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/cars_api"