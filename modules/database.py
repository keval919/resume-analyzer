from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///users.db')

Base=declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True,nullable=False)
    username = Column(String(50))
    password = Column(String(100))

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
def user_exist(username):
    user_exist = session.query(User).filter(User.username==username).first()
    if(user_exist):
        return 1
    else:
        return 0
    
def add_user(username,password):
    new_user = User(username=username,password=password)
    session.add(new_user)
    session.commit()

def get_user_by_username(username):
    user=session.query(User).filter(User.username==username).first()
    userdata={
        "id":user.id,
        "username":user.username,
        "password":user.password
    }
    return userdata

def get_user_by_id(id):
    user=session.query(User).filter(User.id==id).first()
    userdata={
        "id":user.id,
        "username":user.username,
        "password":user.password
    }
    return userdata

'''
new_user = User(id=9,username='hello',password='password')
session.add(new_user)
session.commit()

all_users = session.query(User).all()
print(all_users[0].id,all_users[2].id)
'''

        
