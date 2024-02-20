from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, CheckConstraint, select, and_, desc, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column, relationship

# sqlalchemy.url = sqlite:///data_sql.db
# engine = create_engine('sqlite:///data_sql.db', echo=False)  
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

Base = declarative_base()

class Group(Base):
    __tablename__ = 'groups'
    id: Mapped[int] = mapped_column(primary_key=True)
    group_name: Mapped[str] = mapped_column(String(150))


class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))
    group_id: Mapped[int] = mapped_column('group_id', ForeignKey('groups.id', ondelete='CASCADE'))
    group = relationship("Group", backref="students")

    @hybrid_property
    def fullname(self):
        return self.first_name + " " + self.last_name


class Teacher(Base):
    __tablename__ = 'teachers'
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(150))
    last_name: Mapped[str] = mapped_column(String(150))

    @hybrid_property
    def fullname(self):
        return self.first_name + " " + self.last_name


class Subject(Base):
    __tablename__ = 'subjects'
    id: Mapped[int] = mapped_column(primary_key=True)
    subject_name: Mapped[str] = mapped_column(String(175))
    teacher_id: Mapped[int] = mapped_column('teacher_id', ForeignKey('teachers.id', ondelete='CASCADE'))
    teacher = relationship("Teacher", backref="subjects")


class Grade(Base):
    __tablename__ = 'grades'
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column('student_id', ForeignKey('students.id', ondelete='CASCADE'))
    student = relationship("Student", backref="grades")
    subject_id: Mapped[int] = mapped_column('subject_id', ForeignKey('subjects.id', ondelete='CASCADE'))
    subject = relationship("Subject", backref="grades")
    grade: Mapped[int] = mapped_column(CheckConstraint('grade >= 0 AND grade <= 100'))
    grade_date: Mapped[Date] = mapped_column(Date, nullable=False)


# Base.metadata.create_all(engine)
