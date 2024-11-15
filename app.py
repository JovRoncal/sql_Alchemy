from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    course = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def dictionary(self):
        return {"student_id": self.student_id, "name": self.name, "course": self.course, "age": self.age}



with app.app_context():
    db.create_all()


@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()
    new_student = student(name=data['name'], course=data['course'], age=data['age'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify(new_student.dictionary()), 201


@app.route('/students', methods=['GET'])
def get_students():
    students = student.query.all()
    return jsonify([student.dictionary() for student in students])


@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    result = student.query.get_or_404(student_id)
    return jsonify(result.dictionary())


@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    result = student.query.get_or_404(student_id)
    result.name = data.get('name', result.name)
    result.course = data.get('course', result.course)
    result.age = data.get('age', result.age)
    db.session.commit()
    return jsonify(result.dictionary())


@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    result = student.query.get_or_404(student_id)
    db.session.delete(result)
    db.session.commit()
    return jsonify({"message": "student deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)
