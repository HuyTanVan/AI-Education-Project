#Contains all the database models (tables) using SQLAlchemy.

from . import db
import uuid

# auto-generated last 12 digits of uuid4
def generate_uuid4_last12():
    return str(uuid.uuid4())[-12:]

class User(db.Model):
    """
    Represents a user in the system.

    Attributes:
        id (str): The unique identifier for the user.
        username (str): The user's username (unique).
        password_hash (str): The hashed password for the user.
        role (str): The role of the user ('student' or 'teacher').
    """
    id = db.Column(db.String(12), primary_key=True, default=generate_uuid4_last12, unique=True, nullable=False)
    user_name = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(10))  # 'student' or 'teacher'
    last_login = db.Column(db.DateTime, nullable = True)
    created_at = db.Column(db.DateTime, nullable = False)
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
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    teacher = db.relationship('User', backref='courses')

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
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))
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