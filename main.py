from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func

DATABASE_URI = ''
engine = create_engine(DATABASE_URI)

Base = declarative_base()


student_class = Table(
    'student_class',
    Base.metadata,
    Column('student_id', Integer, ForeignKey('students.student_id')),
    Column('class_id', Integer, ForeignKey('classes.class_id'))
)

class Student(Base):
    __tablename__ = 'students'
    student_id = Column(Integer, primary_key=True)
    student_name = Column(String)
    scores = relationship('Score', back_populates='student')

class Class(Base):
    __tablename__ = 'classes'
    class_id = Column(Integer, primary_key=True)
    class_name = Column(String)
    students = relationship('Student', secondary=student_class)

class Subject(Base):
    __tablename__ = 'subjects'
    subject_id = Column(Integer, primary_key=True)
    subject_name = Column(String)

class Score(Base):
    __tablename__ = 'scores'
    score_id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.student_id'))
    class_id = Column(Integer, ForeignKey('classes.class_id'))
    subject_id = Column(Integer, ForeignKey('subjects.subject_id'))
    score = Column(Float)
    student = relationship('Student', back_populates='scores')
    subject = relationship('Subject')
    school_class = relationship('Class')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

students_data = [
    Student(student_name="Dara"),
    Student(student_name="Aiya"),
    Student(student_name="Dauren"),
    Student(student_name="Botakoz"),
    Student(student_name="Zhumatai"),
    Student(student_name="Dias"),
    Student(student_name="Qamidesh"),
    Student(student_name="Aizere"),
    Student(student_name="Damili"),
    Student(student_name="Tairkhan")
]
session.add_all(students_data)

classes_data = [
    Class(class_name="Класс 1"),
    Class(class_name="Класс 2"),
    Class(class_name="Класс 3"),
    Class(class_name="Класс 4"),
    Class(class_name="Класс 5")
]
session.add_all(classes_data)

subjects_data = [
    Subject(subject_name="Math"),
    Subject(subject_name="Physics"),
    Subject(subject_name="History"),
]
session.add_all(subjects_data)

scores_data = [
    Score(student_id=1, class_id=1, subject_id=1, score=90.0),
    Score(student_id=2, class_id=2, subject_id=1, score=85.0),
    Score(student_id=3, class_id=3, subject_id=1, score=95.0),
    Score(student_id=4, class_id=4, subject_id=1, score=87.0),
    Score(student_id=5, class_id=5, subject_id=1, score=91.0),
    Score(student_id=6, class_id=1, subject_id=1, score=88.0),
    Score(student_id=7, class_id=2, subject_id=1, score=99.0),
    Score(student_id=8, class_id=3, subject_id=1, score=87.0),
    Score(student_id=9, class_id=4, subject_id=1, score=97.0),
    Score(student_id=10, class_id=5, subject_id=1, score=88.0),
    Score(student_id=1, class_id=1, subject_id=2, score=80.0),
    Score(student_id=2, class_id=2, subject_id=2, score=95.0),
    Score(student_id=3, class_id=3, subject_id=2, score=85.0),
    Score(student_id=4, class_id=4, subject_id=2, score=97.0),
    Score(student_id=5, class_id=5, subject_id=2, score=81.0),
    Score(student_id=6, class_id=1, subject_id=2, score=98.0),
    Score(student_id=7, class_id=2, subject_id=2, score=89.0),
    Score(student_id=8, class_id=3, subject_id=2, score=97.0),
    Score(student_id=9, class_id=4, subject_id=2, score=87.0),
    Score(student_id=10, class_id=5, subject_id=2, score=98.0),
    Score(student_id=1, class_id=1, subject_id=3, score=89.0),
    Score(student_id=2, class_id=2, subject_id=3, score=99.0),
    Score(student_id=3, class_id=3, subject_id=3, score=88.0),
    Score(student_id=4, class_id=4, subject_id=3, score=97.0),
    Score(student_id=5, class_id=5, subject_id=3, score=86.0),
    Score(student_id=6, class_id=1, subject_id=3, score=95.0),
    Score(student_id=7, class_id=2, subject_id=3, score=84.0),
    Score(student_id=8, class_id=3, subject_id=3, score=93.0),
    Score(student_id=9, class_id=4, subject_id=3, score=82.0),
    Score(student_id=10, class_id=5, subject_id=3, score=91.0)
]
session.add_all(scores_data)

session.commit()

average_scores = session.query(Student.student_name, func.avg(Score.score).label('average_score')) \
    .join(Score) \
    .group_by(Student.student_name) \
    .all()

print("Средний балл каждого ученика:")
for student_name, average_score in average_scores:
    print(f'Ученик: {student_name}, Средний балл: {average_score:.2f}')

average_scores = session.query(Class.class_name, func.avg(Score.score).label('average_score')) \
    .join(Score) \
    .group_by(Class.class_name) \
    .all()

print("\nСредний балл каждого класса:")
for class_name, average_score in average_scores:
    print(f'Класс: {class_name}, Средний балл: {average_score:.2f}')

top_students = session.query(Student.student_name, func.avg(Score.score).label('average_score')) \
    .join(Score) \
    .group_by(Student.student_name) \
    .order_by(func.avg(Score.score).desc()) \
    .limit(3) \
    .all()

print("\nЛучшие 3 ученика:")
for rank, (student_name, average_score) in enumerate(top_students, start=1):
    print(f'Место {rank}: Ученик: {student_name}, Средний балл: {average_score:.2f}')

top_classes = session.query(Class.class_name, func.avg(Score.score).label('average_score')) \
    .join(Score) \
    .group_by(Class.class_name) \
    .order_by(func.avg(Score.score).desc()) \
    .limit(3) \
    .all()

print("\nЛучшие 3 класса:")
for rank, (class_name, average_score) in enumerate(top_classes, start=1):
    print(f'Место {rank}: Класс: {class_name}, Средний балл: {average_score:.2f}')

session.close()
