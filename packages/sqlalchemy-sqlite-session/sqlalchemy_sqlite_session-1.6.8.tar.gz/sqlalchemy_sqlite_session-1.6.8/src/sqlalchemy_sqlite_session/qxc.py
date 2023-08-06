from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_sqlite_session.tools import get_session
Base = declarative_base()


class QixingcaiNumber(Base):
    """ number_qlc """
    __tablename__ = 'number_qxc'

    issue = Column(Integer, primary_key=True)
    num1 = Column(Integer, nullable=False)
    num2 = Column(Integer, nullable=False)
    num3 = Column(Integer, nullable=False)
    num4 = Column(Integer, nullable=False)
    num5 = Column(Integer, nullable=False)
    num6 = Column(Integer, nullable=False)
    num7 = Column(Integer, nullable=False)

    def __init__(self, data_list: list):
        self.issue, self.num1, self.num2, self.num3, self.num4, self.num5, self.num6, self.num7 = data_list

    @classmethod
    def get_issues(cls):
        """get issues[list]"""
        session = get_session()
        i = session.query(cls).all()
        session.close()
        result = [x.issue for x in i]
        result.sort()
        return result

    @classmethod
    def get_all(cls):
        """get all [[issue, num1, num2, num3]... ]"""
        session = get_session()
        data = session.query(cls).all()
        session.close()
        return [[x.issue, x.num1, x.num2, x.num3, x.num4, x.num5, x.num6, x.num7] for x in data]

    @classmethod
    def get_one(cls, issue_number: int):
        """获取对应 issue 的号码列表 [issue, num1, num2, num3]"""
        session = get_session()
        data = session.query(cls).get(issue_number)
        session.close()
        return [data.issue, data.num1, data.num2, data.num3, data.num4, data.num5, data.num6, data.num7]

    @classmethod
    def add_number(cls, p_issue: str, p_numbers: list):
        """添加一条记录"""
        session = get_session()
        ins = cls([p_issue] + p_numbers)
        session.merge(ins)
        session.commit()
        session.close()
        print(f">>> QXC merge:{p_issue} - {p_numbers}")


if __name__ == "__main__":
    from sqlalchemy_sqlite_session.tools import get_engine
    engine = get_engine()
    Base.metadata.create_all(engine)
    pass
