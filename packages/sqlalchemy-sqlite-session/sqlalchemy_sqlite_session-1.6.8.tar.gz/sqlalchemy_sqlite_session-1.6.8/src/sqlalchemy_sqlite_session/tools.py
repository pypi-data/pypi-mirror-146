"""SQLAlchemy 数据库 ORM 文件"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine():
    engine = create_engine('sqlite:///C:\\sqlite\\all.db')
    return engine


def get_session():
    engine = create_engine('sqlite:///C:\\sqlite\\all.db')
    Session = sessionmaker(bind=engine)
    session = Session()         # 创建Session类实例
    return session

if __name__ == '__main__':
    pass
