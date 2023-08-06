from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_sqlite_session.tools import get_session

Base = declarative_base()
# generate tables

class PredictDaletou(Base):
    """ numbers@sd.db """
    __tablename__ = 'cjcp_predict_daletou'

    issue_name = Column(String, primary_key=True)
    issue = Column(Integer, nullable=True)
    name = Column(String, nullable=True)
    num1 = Column(Integer, nullable=True)
    num2 = Column(Integer, nullable=True)
    num3 = Column(Integer, nullable=True)
    num4 = Column(Integer, nullable=True)
    num5 = Column(Integer, nullable=True)
    num6 = Column(Integer, nullable=True)
    num7 = Column(Integer, nullable=True)
    front25 = Column(String, nullable=True)
    front20 = Column(String, nullable=True)
    front10 = Column(String, nullable=True)
    front_save1 = Column(String, nullable=True)
    front_save2 = Column(String, nullable=True)
    front_save3 = Column(String, nullable=True)
    front_kill3 = Column(String, nullable=True)
    front_kill6 = Column(String, nullable=True)
    front_begin2 = Column(String, nullable=True)
    front_end2 = Column(String, nullable=True)
    behind_kill3 = Column(String, nullable=True)
    behind_save6 = Column(String, nullable=True)
    behind_save1 = Column(String, nullable=True)
    behind_save2 = Column(String, nullable=True)


class PredictSport(Base):
    """ numbers@sd.db """
    __tablename__ = 'cjcp_predict_pl3'

    issue_name = Column(String, primary_key=True)
    issue = Column(Integer, nullable=True)
    num1 = Column(Integer, nullable=True)
    num2 = Column(Integer, nullable=True)
    num3 = Column(Integer, nullable=True)
    name = Column(String, nullable=True)
    save1 = Column(String, nullable=True)
    save2 = Column(String, nullable=True)
    save3 = Column(String, nullable=True)
    save5 = Column(String, nullable=True)
    save6 = Column(String, nullable=True)
    save7 = Column(String, nullable=True)
    kill1 = Column(String, nullable=True)
    kill2 = Column(String, nullable=True)
    v_save1 = Column(Integer, nullable=True)
    v_save2 = Column(Integer, nullable=True)
    v_save3 = Column(Integer, nullable=True)
    v_save5 = Column(Integer, nullable=True)
    v_save6 = Column(Integer, nullable=True)
    v_save7 = Column(Integer, nullable=True)
    v_kill1 = Column(String, nullable=True)
    v_kill2 = Column(String, nullable=True)


class DaletouNumber(Base):
    """ numbers@p3.db """
    __tablename__ = 'number_dlt'

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
    def get_numbers(cls):
        """get all [[issue, num1, num2, num3]... ]"""
        session = get_session()
        data = session.query(cls).all()
        session.close()
        return [[x.issue, x.num1, x.num2, x.num3, x.num4, x.num5, x.num6, x.num7] for x in data]

    @classmethod
    def get_one(cls, issue_number: int):
        """获取对应 issue 的号码列表 [issue, num1, num2, num3]"""
        session = get_session()
        d = session.query(cls).get(issue_number)
        session.close()
        return [d.issue, d.num1, d.num2, d.num3, d.num4, d.num5, d.num6, d.num7]

    @classmethod
    def add_number(cls, p_issue: str, p_numbers: list):
        """添加一条记录"""
        session = get_session()
        ins = cls([p_issue] + p_numbers)
        session.merge(ins)
        session.commit()
        session.close()
        print(f">>> DLT merge:{p_issue} - {p_numbers}")


if __name__ == "__main__":
    # WelfareVerify.add_score('20212882945', 2021288, 2, '945', 'y', 0.49)
    # print(WelfareNumber.get_next3_issues(2021287))
    # generate tables
    from tools import get_engine
    engine = get_engine()
    Base.metadata.create_all(engine)
    pass
