#Contains all the database models (tables) using SQLAlchemy.

from . import db
import uuid
from datetime import datetime
# auto-generated last 12 digits of uuid4
def generate_uuid4_last12():
    return str(uuid.uuid4())[-12:]

class User(db.Model):
    """
    Represents a user in the system.

    Attributes:
        id (str): The unique identifier for the user.
        user_name (str): The user's username (unique).
        first_name (str): The user's first name.
        last_name (str): The user's last name.
        email (str): The user's email (unique).
        password_hash (str): The hashed password for the user.
        role (str): The role of the user ('student', 'teacher' or 'admin').
        last_login (DateTime): The last time user logged in.
        created_at (DateTime): when the user account was created.
        updated_at (DateTime): The last time the user’s information was updated.
    """
    id = db.Column(db.String(12), primary_key=True, default=generate_uuid4_last12, unique=True, nullable=False)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10))  # 'student' or 'teacher'
    last_login = db.Column(db.DateTime, nullable = True)
    created_at = db.Column(db.DateTime, nullable = False, default=datetime.now)
    updated_at =  db.Column(db.DateTime, nullable = True)

    def __repr__(self) -> str:
        return f"<Username: {self.user_name}>"

class Course(db.Model):
    """
    Represents a course in the system.

    Attributes:
        id (int): The unique identifier for the course.
        course_name (str): The name of the course.
        teacher_id (int): The ID of the teacher for this course.
        teacher (User): The relationship to the User model for the teacher.
    """
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(120), nullable=False)
    teacher_id = db.Column(db.String(12), db.ForeignKey('user.id'))

    teacher = db.relationship('User', backref='courses')

class Enrollment(db.Model):
    """
    Represents a course in the system.

    Attributes:
        id (int): The unique identifier for the enrollment.
        student_id (int): The ID of the student.
        course_id (int): The ID of the course.
        status (str) : The status of current enrollment ('enrolled', 'cancelled', 'pending')        
        enrollment_date (DateTime): When enrollment was made.
        student (User): The relationship to the User model for the student.
        course (Course): The relationship to the Course model for the course.
    """
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(12), db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Enum('enrolled', 'cancelled', 'pending'),default='pending', nullable=False)
    enrollment_date = db.Column(db.DateTime,default=datetime.now, nullable = True)

    student = db.relationship('User', backref='courses')
    course = db.relationship('Course', backref='courses')

class Exam(db.Model):
    """
    Represents an exam in the system.

    Attributes:
        id (int): The unique identifier for the exam.
        course_id (int): The ID of the course this exam belongs to.
        exam_title (str): The title of the exam.
        course (Course): The relationship to the Course model.
    """
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    exam_title = db.Column(db.String(120), nullable=False)
    exam_description = db.Column(db.String(255), nullable=True)
    course = db.relationship('Course', backref='exams')

class Question(db.Model):
    """
    Represents a question in an exam.

    Attributes:
        id (int): The unique identifier for the question.
        exam_id (int): The ID of the exam this question belongs to.
        question_text (str): The text of the question.
        exam (Exam): The relationship to the Exam model.
    """
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'))
    question_text = db.Column(db.Text, nullable=False)
    exam = db.relationship('Exam', backref='questions')

class Answer(db.Model):
    """
    Represents a student's answer to a question.

    Attributes:
        id (int): The unique identifier for the answer.
        question_id (int): The ID of the question this answer is for.
        student_id (int): The ID of the student who provided this answer.
        answer_text (str): The text of the student's answer.
        question (Question): The relationship to the Question model.
        student (User): The relationship to the User model for the student.
    """
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    student_id = db.Column(db.String(12), db.ForeignKey('user.id'))
    answer_text = db.Column(db.Text, nullable=False)
    question = db.relationship('Question', backref='answers')
    student = db.relationship('User', backref='answers')

class AIEvaluation(db.Model):
    """
    Represents an AI-generated evaluation of a student's answer.

    Attributes:
        id (int): The unique identifier for the evaluation.
        answer_id (int): The ID of the answer being evaluated.
        score (int): The score given by the AI (0, 1, or 2).
        feedback (str): The feedback provided by the AI.
        answer (Answer): The relationship to the Answer model.
    """
    id = db.Column(db.Integer, primary_key=True)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    score = db.Column(db.Integer)  # 0, 1, or 2
    feedback = db.Column(db.Text)
    answer = db.relationship('Answer', backref='evaluations')