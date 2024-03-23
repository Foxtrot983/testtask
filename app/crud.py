from app.models import UserData
from app import app, db

from sqlalchemy.exc import NoResultFound

def post_data(title: str, text:str, user_id:int):
    try:
        with db.session() as session:
            data = UserData(title=title, text=text, user_id=user_id)
            session.add(data)
            session.commit()
    except Exception as e:
        print(e)
        

def get_data(user_id: int) -> list:
    with db.session() as session:
        data = session.query(UserData).filter(UserData.user_id==user_id).all()
    return data


def get_one_article(user_id:int, data_id:int):
    with db.session() as session:
        try:
            data = session.query(UserData).filter(UserData.id==data_id, UserData.user_id==user_id).one()
            return [data.title, data.text]
        except NoResultFound:
            return ['', '']


def update_data(data_id:int, title:str, text: str, user_id: int):
    with db.session() as session:
        try:
            data = session.query(UserData).filter(UserData.id==data_id, UserData.user_id==user_id).one()
            data.title = title
            data.text = text
            session.add(data)
            session.commit()
            return True
        except NoResultFound:
            return False


def delete_data(user_id:int, data_id:int):
    with db.session() as session:
        try:
            data = session.query(UserData).filter(UserData.id==data_id, UserData.user_id==user_id).one()
            session.delete(data)
            session.commit()
        except NoResultFound:
            pass
        except Exception as e:
            print(e)
            pass