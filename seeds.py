from connect_db import session
from model import Student, Group, Grade, Teacher, Subject
import random
from faker import Faker
from random import randint


NUMBER_STUDENTS = 50
NUMBER_GROUPS = 3
NUMBER_SUBJECTS = 9
NUMBER_TEACHERS = 5
NUMBER_GRADES = 20

def insert_data_to_db() -> None:
    fake = Faker()
    g = Group()
    # Додавання груп
    for _ in range(NUMBER_GROUPS):
        group = Group(group_name=fake.word())
        session.add(group)
    # Додавання викладачів
    for _ in range(NUMBER_TEACHERS):
        teacher = Teacher(
            first_name=fake.first_name(),
            last_name=fake.last_name()
        )
        session.add(teacher)
    # Додавання предметів 
    for _ in range(NUMBER_SUBJECTS):
        subject = Subject(
            subject_name=fake.word(),
            teacher_id=random.randint(1, NUMBER_TEACHERS)
        )
        session.add(subject)
    # Додавання студентів і оцінок 
    for _ in range(NUMBER_STUDENTS):
        student = Student(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            group_id=random.randint(1, NUMBER_GROUPS)
        )
        session.add(student)
        for _ in range(NUMBER_GRADES):
            grade = Grade(
                student_id=random.randint(1, NUMBER_STUDENTS),
                subject_id=random.randint(1, NUMBER_SUBJECTS),
                grade=random.randint(0, 100),
                grade_date=fake.date_this_year()
            )
            session.add(grade)
    session.commit()

if __name__ == "__main__":
    insert_data_to_db()

