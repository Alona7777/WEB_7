from sqlalchemy import func, desc, select, and_, join
from model import Student, Group, Grade, Teacher, Subject
from connect_db import session


# 1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1() -> list:
    result = session.query(
        Student.id, 
        Student.fullname, 
        func.round(func.avg(Grade.grade), 2).label('average_grade')
        ).join(Grade).group_by(Student.id).order_by(desc('average_grade')).limit(5).all()
    
    res = []
    for item in result:
        line_res = f'Student ID: {item[0]}, Student FULLNAME: {item[1]}, Avarage SCORE: {item[2]}'
        res.append(line_res)
    return res

# 2. Знайти студента із найвищим середнім балом з певного предмета.
def select_2(subject_id: int) -> list:
    subj = session.query(Subject.subject_name).filter(Subject.id == subject_id).first()[0]
    result = session.query(
        Student.id, 
        Student.fullname, 
        func.round(func.avg(Grade.grade),2).label('average_grade')
        ).select_from(Grade).join(Student).filter(Grade.student_id == subject_id).group_by(Student.id).order_by(
        desc('average_grade')).limit(1).all()
    
    res = []
    for item in result:
        line_res = f'SUBJECT: {subj}, Student ID: {item[0]}, Student FULLNAME: {item[1]}, Avarage SCORE: {item[2]}'
        res.append(line_res)
    return res

# 3. Знайти середній бал у групах з певного предмета.
def select_3(subject_id: int) -> list:
    result = session.query(
        Subject.subject_name,
        Group.group_name,
        func.round(func.avg(Grade.grade),2).label('average_grade')
        ).select_from(Grade).join(Student).join(Group).join(Subject).filter(Subject.id == subject_id).group_by(Group.group_name).all()
    res= []
    for item in result:
        line_res = f'SUBJECT: {item[0]}, GROUP NAME: {item[1]}, Avarage SCORE: {item[2]}'
        res.append(line_res)
    return res

# 4. Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4() -> str:
    result = session.query(
       func.round(func.avg(Grade.grade),2).label('average_grade')
       ).select_from(Grade).first()
    
    line_res = f'Avarage SCORE: {result[0]}'
    return line_res

# 5. Знайти які курси читає певний викладач.
def select_5(tech_id: int) -> list:
    result = session.query(
        Teacher.fullname,
        Subject.id,
        Subject.subject_name
        ).select_from(Subject).join(Teacher).filter(Subject.teacher_id == tech_id).group_by(Subject.subject_name).all()
    res= []
    for item in result:
        line_res = f'TEACHER FULLNAME: {item[0]}, SUBJECT ID: {item[1]}, SUBJECT NAME: {item[2]}'
        res.append(line_res)
    return res

# 6. Знайти список студентів у певній групі.
def select_6(group_id: int) -> list:
    group_name = session.query(Group.group_name).filter(Group.id == group_id).first()[0]
    result = session.query(
        Student.id,
        Student.fullname
        ).select_from(Student).join(Group).filter(Group.id == group_id).group_by(Student.id).all()
    res = []
    res.append(f'GROUP NAME: {group_name}')
    for item in result:
        line_res = f'Student ID: {item[0]}, Student FULLNAME: {item[1]}'
        res.append(line_res)
    return res
    
# 7. Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(group_id: int, subj_id: int) -> list:
    group_name = session.query(Group.group_name).filter(Group.id == group_id).first()[0]
    subj_name = session.query(Subject.subject_name).filter(Subject.id == subj_id).first()[0]
    result = session.query(
        Student.fullname,
        Grade.grade
        ).select_from(Grade).join(Student).join(Group).join(Subject).filter(and_(Group.id == group_id, Subject.id == subj_id)).order_by(desc(Grade.grade)).all()
    res = []
    res.append(f'GROUP NAME: {group_name}, SUBJECT NAME: {subj_name}')
    for item in result:
        # line_res = f'Student FULLNAME: {item[0]}, Student GRADE: {item[1]}'
        line_res = f'Student FULLNAME and GRADE: {item[0]}, {item[1]}'
        res.append(line_res)
    return res

# 8.Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teach_id: int) -> list:
    teacher_name = session.query(Teacher.fullname).filter(Teacher.id==teach_id).first()[0]
    result = session.query(
        Subject.subject_name,
        func.round(func.avg(Grade.grade),2).label('average_grade')
        ).select_from(Subject).join(Grade).join(Teacher).filter(Teacher.id == teach_id).group_by(Subject.subject_name).all()
    res = []
    res.append(f'TEACHER NAME: {teacher_name}')
    for item in result:
        line_res = f'SUBJECT NAME: {item[0]}, Avarage SCORE: {item[1]}'
        res.append(line_res)
    return res

# 9. Знайти список курсів, які відвідує студент.
def select_9(student_id: int) -> list:
    student_name = session.query(Student.fullname).filter(Student.id==student_id).first()[0]
    result = session.query(
        Subject.subject_name,
    ).select_from(Student).join(Grade).join(Subject).filter(Student.id == student_id).distinct().all()
    res = []
    res.append(f'Student FULLNAME: {student_name}')
    for item in result:
        line_res = f'SUBJECT NAME: {item[0]}'
        res.append(line_res)
    return res

# 10. Список курсів, які певному студенту читає певний викладач.
def select_10(student_id: int, teach_id: int) -> list:
    student_name = session.query(Student.fullname).filter(Student.id==student_id).first()[0]
    teacher_name = session.query(Teacher.fullname).filter(Teacher.id==teach_id).first()[0]
    result = session.query(
        Subject.subject_name
        ).select_from(Student).join(Grade).join(Subject).join(Teacher).filter(and_(Student.id == student_id, Teacher.id == teach_id)).distinct().all()
    res = []
    res.append(f'STUDENT FULLNAME: {student_name}, TEACHER FULLNAME: {teacher_name}')
    for item in result:
        line_res = f'SUBJECT NAME: {item[0]}'
        res.append(line_res)
    return res

# 11. Середній бал, який певний викладач ставить певному студентові.
def select_11(student_id: int, teach_id: int) -> list:
    student_name = session.query(Student.fullname).filter(Student.id==student_id).first()[0]
    teacher_name = session.query(Teacher.fullname).filter(Teacher.id==teach_id).first()[0]
    result = session.query(
        func.round(func.avg(Grade.grade),2).label('average_grade')
    ).select_from(Student).join(Grade).join(Subject).join(Teacher).filter(and_(Student.id == student_id, Teacher.id == teach_id)).all()
    res = []
    res.append(f'STUDENT FULLNAME: {student_name}, TEACHER FULLNAME: {teacher_name}')
    for item in result:
        line_res = f'Avarage SCORE: {item[0]}'
        res.append(line_res)
    return res

# 12.Оцінки студентів у певній групі з певного предмета на останньому занятті.
def select_12(group_id: int, subj_id: int) -> list:

    subquery = (select(func.max(Grade.grade_date)).join(Student).filter(and_(
        Grade.subject_id == subj_id, Student.group_id == group_id
    ))).scalar_subquery()

    result = session.query(
        Student.fullname, 
        Grade.grade,
        Grade.grade_date 
        ).select_from(Grade).join(Student).filter(
            and_(Grade.subject_id == subj_id, Student.group_id == group_id, Grade.grade_date == subquery)).all()


    return result
    

if __name__ == '__main__':
    print(select_1())
    print(select_2(subject_id=1))
    print(select_3(subject_id=3))
    print(select_4())
    print(select_5(tech_id=1))
    print(select_6(group_id=2))
    print(select_7(group_id=3, subj_id=3))
    print(select_8(teach_id=2))
    print(select_9(student_id=7))
    print(select_10(student_id=7, teach_id=1))
    print(select_11(student_id=1, teach_id=2))
    print(select_12(subj_id=2, group_id=3))
