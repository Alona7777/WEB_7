from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///data_sql.db")
Session = sessionmaker(bind=engine)
session = Session()