from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///resume_user_data.db')

Base=declarative_base()

class Resume(Base):
    __tablename__ = 'resume'

    id = Column(Integer, primary_key=True,nullable=False)
    user_id = Column(Integer)
    job_title= Column(String(50))
    name = Column(String(50))
    resume_location= Column(String(20))

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def GetResume(resume_location):
    try:
         return session.query(Resume).filter(Resume.resume_location==resume_location).first()
    except:
        return None
    
def PutResume(user_id,job_title,name,resume_location):
    new_resume = Resume(user_id=user_id,job_title=job_title,name=name,resume_location=resume_location)
    session.add(new_resume)
    session.commit()