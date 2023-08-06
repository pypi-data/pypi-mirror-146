from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String
from sqlalchemy_sqlite_session.tools import get_session

Base = declarative_base()


class HappyFollow(Base):
    __tablename__ = 'kl8_follow'

    issue = Column(Integer, primary_key=True)
    n01 = Column(Integer, nullable=False)
    n02 = Column(Integer, nullable=False)
    n03 = Column(Integer, nullable=False)
    n04 = Column(Integer, nullable=False)
    n05 = Column(Integer, nullable=False)
    n06 = Column(Integer, nullable=False)
    n07 = Column(Integer, nullable=False)
    n08 = Column(Integer, nullable=False)
    n09 = Column(Integer, nullable=False)
    n10 = Column(Integer, nullable=False)
    n11 = Column(Integer, nullable=False)
    n12 = Column(Integer, nullable=False)
    n13 = Column(Integer, nullable=False)
    n14 = Column(Integer, nullable=False)
    n15 = Column(Integer, nullable=False)
    n16 = Column(Integer, nullable=False)
    n17 = Column(Integer, nullable=False)
    n18 = Column(Integer, nullable=False)
    n19 = Column(Integer, nullable=False)
    n20 = Column(Integer, nullable=False)
    nt01 = Column(Integer)
    nt02 = Column(Integer)
    nt03 = Column(Integer)
    nt04 = Column(Integer)
    nt05 = Column(Integer)
    nt06 = Column(Integer)
    nt07 = Column(Integer)
    nt08 = Column(Integer)
    nt09 = Column(Integer)
    nt10 = Column(Integer)
    nt11 = Column(Integer)
    nt12 = Column(Integer)
    nt13 = Column(Integer)
    nt14 = Column(Integer)
    nt15 = Column(Integer)
    nt16 = Column(Integer)
    nt17 = Column(Integer)
    nt18 = Column(Integer)
    nt19 = Column(Integer)
    nt20 = Column(Integer)
    f01 = Column(Integer)
    f02 = Column(Integer)
    f03 = Column(Integer)
    f04 = Column(Integer)
    f05 = Column(Integer)
    f06 = Column(Integer)
    f07 = Column(Integer)
    f08 = Column(Integer)
    f09 = Column(Integer)
    f10 = Column(Integer)
    f11 = Column(Integer)
    f12 = Column(Integer)
    f13 = Column(Integer)
    f14 = Column(Integer)
    f15 = Column(Integer)
    f16 = Column(Integer)
    f17 = Column(Integer)
    f18 = Column(Integer)
    f19 = Column(Integer)
    f20 = Column(Integer)
    f21 = Column(Integer)
    f22 = Column(Integer)
    f23 = Column(Integer)
    f24 = Column(Integer)
    f25 = Column(Integer)
    f26 = Column(Integer)
    f27 = Column(Integer)
    f28 = Column(Integer)
    f29 = Column(Integer)
    f30 = Column(Integer)
    f31 = Column(Integer)
    f32 = Column(Integer)
    f33 = Column(Integer)
    f34 = Column(Integer)
    f35 = Column(Integer)
    f36 = Column(Integer)
    f37 = Column(Integer)
    f38 = Column(Integer)
    f39 = Column(Integer)
    f40 = Column(Integer)
    f41 = Column(Integer)
    f42 = Column(Integer)
    f43 = Column(Integer)
    f44 = Column(Integer)
    f45 = Column(Integer)
    f46 = Column(Integer)
    f47 = Column(Integer)
    f48 = Column(Integer)
    f49 = Column(Integer)
    f50 = Column(Integer)
    f51 = Column(Integer)
    f52 = Column(Integer)
    f53 = Column(Integer)
    f54 = Column(Integer)
    f55 = Column(Integer)
    f56 = Column(Integer)
    f57 = Column(Integer)
    f58 = Column(Integer)
    f59 = Column(Integer)
    f60 = Column(Integer)
    f61 = Column(Integer)
    f62 = Column(Integer)
    f63 = Column(Integer)
    f64 = Column(Integer)
    f65 = Column(Integer)
    f66 = Column(Integer)
    f67 = Column(Integer)
    f68 = Column(Integer)
    f69 = Column(Integer)
    f70 = Column(Integer)
    f71 = Column(Integer)
    f72 = Column(Integer)
    f73 = Column(Integer)
    f74 = Column(Integer)
    f75 = Column(Integer)
    f76 = Column(Integer)
    f77 = Column(Integer)
    f78 = Column(Integer)
    f79 = Column(Integer)
    f80 = Column(Integer)
    c01 = Column(Float)
    c02 = Column(Float)
    c03 = Column(Float)
    c04 = Column(Float)
    c05 = Column(Float)
    c06 = Column(Float)
    c07 = Column(Float)
    c08 = Column(Float)
    c09 = Column(Float)
    c10 = Column(Float)
    c11 = Column(Float)
    c12 = Column(Float)
    c13 = Column(Float)
    c14 = Column(Float)
    c15 = Column(Float)
    c16 = Column(Float)
    c17 = Column(Float)
    c18 = Column(Float)
    c19 = Column(Float)
    c20 = Column(Float)
    c21 = Column(Float)
    c22 = Column(Float)
    c23 = Column(Float)
    c24 = Column(Float)
    c25 = Column(Float)
    c26 = Column(Float)
    c27 = Column(Float)
    c28 = Column(Float)
    c29 = Column(Float)
    c30 = Column(Float)
    c31 = Column(Float)
    c32 = Column(Float)
    c33 = Column(Float)
    c34 = Column(Float)
    c35 = Column(Float)
    c36 = Column(Float)
    c37 = Column(Float)
    c38 = Column(Float)
    c39 = Column(Float)
    c40 = Column(Float)
    c41 = Column(Float)
    c42 = Column(Float)
    c43 = Column(Float)
    c44 = Column(Float)
    c45 = Column(Float)
    c46 = Column(Float)
    c47 = Column(Float)
    c48 = Column(Float)
    c49 = Column(Float)
    c50 = Column(Float)
    c51 = Column(Float)
    c52 = Column(Float)
    c53 = Column(Float)
    c54 = Column(Float)
    c55 = Column(Float)
    c56 = Column(Float)
    c57 = Column(Float)
    c58 = Column(Float)
    c59 = Column(Float)
    c60 = Column(Float)
    c61 = Column(Float)
    c62 = Column(Float)
    c63 = Column(Float)
    c64 = Column(Float)
    c65 = Column(Float)
    c66 = Column(Float)
    c67 = Column(Float)
    c68 = Column(Float)
    c69 = Column(Float)
    c70 = Column(Float)
    c71 = Column(Float)
    c72 = Column(Float)
    c73 = Column(Float)
    c74 = Column(Float)
    c75 = Column(Float)
    c76 = Column(Float)
    c77 = Column(Float)
    c78 = Column(Float)
    c79 = Column(Float)
    c80 = Column(Float)

    def __init__(self, issue_num_list: list) -> None:
        super().__init__()
        self.issue = issue_num_list[0]
        self.n01 = issue_num_list[1]
        self.n02 = issue_num_list[2]
        self.n03 = issue_num_list[3]
        self.n04 = issue_num_list[4]
        self.n05 = issue_num_list[5]
        self.n06 = issue_num_list[6]
        self.n07 = issue_num_list[7]
        self.n08 = issue_num_list[8]
        self.n09 = issue_num_list[9]
        self.n10 = issue_num_list[10]
        self.n11 = issue_num_list[11]
        self.n12 = issue_num_list[12]
        self.n13 = issue_num_list[13]
        self.n14 = issue_num_list[14]
        self.n15 = issue_num_list[15]
        self.n16 = issue_num_list[16]
        self.n17 = issue_num_list[17]
        self.n18 = issue_num_list[18]
        self.n19 = issue_num_list[19]
        self.n20 = issue_num_list[20]

    @classmethod
    def get_follow_dict(cls):
        session = get_session()
        data = session.query(cls).all()
        result = {}
        for t in data:
            result[t.issue] = [
                t.f01,
                t.f02,
                t.f03,
                t.f04,
                t.f05,
                t.f06,
                t.f07,
                t.f08,
                t.f09,
                t.f10,
                t.f11,
                t.f12,
                t.f13,
                t.f14,
                t.f15,
                t.f16,
                t.f17,
                t.f18,
                t.f19,
                t.f20,
                t.f21,
                t.f22,
                t.f23,
                t.f24,
                t.f25,
                t.f26,
                t.f27,
                t.f28,
                t.f29,
                t.f30,
                t.f31,
                t.f32,
                t.f33,
                t.f34,
                t.f35,
                t.f36,
                t.f37,
                t.f38,
                t.f39,
                t.f40,
                t.f41,
                t.f42,
                t.f43,
                t.f44,
                t.f45,
                t.f46,
                t.f47,
                t.f48,
                t.f49,
                t.f50,
                t.f51,
                t.f52,
                t.f53,
                t.f54,
                t.f55,
                t.f56,
                t.f57,
                t.f58,
                t.f59,
                t.f60,
                t.f61,
                t.f62,
                t.f63,
                t.f64,
                t.f65,
                t.f66,
                t.f67,
                t.f68,
                t.f69,
                t.f70,
                t.f71,
                t.f72,
                t.f73,
                t.f74,
                t.f75,
                t.f76,
                t.f77,
                t.f78,
                t.f79,
                t.f80
            ]
        return result

    @classmethod
    def get_change_dict(cls):
        session = get_session()
        data = session.query(cls).all()
        result = {}
        for t in data:
            result[t.issue] = [
                t.c01,
                t.c02,
                t.c03,
                t.c04,
                t.c05,
                t.c06,
                t.c07,
                t.c08,
                t.c09,
                t.c10,
                t.c11,
                t.c12,
                t.c13,
                t.c14,
                t.c15,
                t.c16,
                t.c17,
                t.c18,
                t.c19,
                t.c20,
                t.c21,
                t.c22,
                t.c23,
                t.c24,
                t.c25,
                t.c26,
                t.c27,
                t.c28,
                t.c29,
                t.c30,
                t.c31,
                t.c32,
                t.c33,
                t.c34,
                t.c35,
                t.c36,
                t.c37,
                t.c38,
                t.c39,
                t.c40,
                t.c41,
                t.c42,
                t.c43,
                t.c44,
                t.c45,
                t.c46,
                t.c47,
                t.c48,
                t.c49,
                t.c50,
                t.c51,
                t.c52,
                t.c53,
                t.c54,
                t.c55,
                t.c56,
                t.c57,
                t.c58,
                t.c59,
                t.c60,
                t.c61,
                t.c62,
                t.c63,
                t.c64,
                t.c65,
                t.c66,
                t.c67,
                t.c68,
                t.c69,
                t.c70,
                t.c71,
                t.c72,
                t.c73,
                t.c74,
                t.c75,
                t.c76,
                t.c77,
                t.c78,
                t.c79,
                t.c80
            ]
        return result

    @classmethod
    def get_nums(cls):
        """
        [[issue, n01, n02, n03],...]
        """
        session = get_session()
        data = session.query(cls).all()
        session.close()
        result = [[
            x.issue,
            x.n01,
            x.n02,
            x.n03,
            x.n04,
            x.n05,
            x.n06,
            x.n07,
            x.n08,
            x.n09,
            x.n10,
            x.n11,
            x.n12,
            x.n13,
            x.n14,
            x.n15,
            x.n16,
            x.n17,
            x.n18,
            x.n19,
            x.n20
        ]
            for x in data]
        return result

    @classmethod
    def get_issue_and_next(cls):
        """
        [[issue, nt01, nt02, nt03, ..., nt20],...]
        """
        session = get_session()
        data = session.query(cls).all()
        session.close()
        result = [[
            x.issue,
            x.nt01,
            x.nt02,
            x.nt03,
            x.nt04,
            x.nt05,
            x.nt06,
            x.nt07,
            x.nt08,
            x.nt09,
            x.nt10,
            x.nt11,
            x.nt12,
            x.nt13,
            x.nt14,
            x.nt15,
            x.nt16,
            x.nt17,
            x.nt18,
            x.nt19,
            x.nt20
        ]
            for x in data]
        return result

    @classmethod
    def get_next(cls, issue):
        """
        [data.nt01, data.nt02, ...... data.nt20]
        """
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        result = [
            data.nt01,
            data.nt02,
            data.nt03,
            data.nt04,
            data.nt05,
            data.nt06,
            data.nt07,
            data.nt08,
            data.nt09,
            data.nt10,
            data.nt11,
            data.nt12,
            data.nt13,
            data.nt14,
            data.nt15,
            data.nt16,
            data.nt17,
            data.nt18,
            data.nt19,
            data.nt20
        ]
        return result

    @classmethod
    def get_issues(cls):
        """get issues"""
        session = get_session()
        data = session.query(cls).all()
        session.close()
        result = [x.issue for x in data]
        result.sort()
        return result


class HappyNumber(Base):
    """ numbers@p3.db """
    __tablename__ = 'number_kl8'

    issue = Column(Integer, primary_key=True)
    n01 = Column(Integer, nullable=False)
    n02 = Column(Integer, nullable=False)
    n03 = Column(Integer, nullable=False)
    n04 = Column(Integer, nullable=False)
    n05 = Column(Integer, nullable=False)
    n06 = Column(Integer, nullable=False)
    n07 = Column(Integer, nullable=False)
    n08 = Column(Integer, nullable=False)
    n09 = Column(Integer, nullable=False)
    n10 = Column(Integer, nullable=False)
    n11 = Column(Integer, nullable=False)
    n12 = Column(Integer, nullable=False)
    n13 = Column(Integer, nullable=False)
    n14 = Column(Integer, nullable=False)
    n15 = Column(Integer, nullable=False)
    n16 = Column(Integer, nullable=False)
    n17 = Column(Integer, nullable=False)
    n18 = Column(Integer, nullable=False)
    n19 = Column(Integer, nullable=False)
    n20 = Column(Integer, nullable=False)

    def __init__(self, issue: int, data_list: list):
        if len(data_list) != 20:
            raise Exception(">>>>>> ERROR DATA")
        self.issue = issue
        self.n01 = data_list[0]
        self.n02 = data_list[1]
        self.n03 = data_list[2]
        self.n04 = data_list[3]
        self.n05 = data_list[4]
        self.n06 = data_list[5]
        self.n07 = data_list[6]
        self.n08 = data_list[7]
        self.n09 = data_list[8]
        self.n10 = data_list[9]
        self.n11 = data_list[10]
        self.n12 = data_list[11]
        self.n13 = data_list[12]
        self.n14 = data_list[13]
        self.n15 = data_list[14]
        self.n16 = data_list[15]
        self.n17 = data_list[16]
        self.n18 = data_list[17]
        self.n19 = data_list[18]
        self.n20 = data_list[19]

    @classmethod
    def get_n01(cls, issue):
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        return data.n01

    @classmethod
    def get_n02(cls, issue):
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        return data.n02

    @classmethod
    def get_n03(cls, issue):
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        return data.n03

    @classmethod
    def get_n04(cls, issue):
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        return data.n04

    @classmethod
    def get_n05(cls, issue):
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        return data.n05

    @classmethod
    def get_n06(cls, issue):
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        return data.n06

    @classmethod
    def get_n07(cls, issue):
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        return data.n07

    @classmethod
    def get_n08(cls, issue):
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        return data.n08

    @classmethod
    def get_n09(cls, issue):
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        return data.n09

    @classmethod
    def get_n10(cls, issue):
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        return data.n10

    @classmethod
    def get_n11(cls, issue):
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        return data.n11

    @classmethod
    def get_n12(cls, issue):
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        return data.n12

    @classmethod
    def get_n13(cls, issue):
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        return data.n13

    @classmethod
    def get_n14(cls, issue):
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        return data.n14

    @classmethod
    def get_n15(cls, issue):
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        return data.n15

    @classmethod
    def get_n16(cls, issue):
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        return data.n16

    @classmethod
    def get_n17(cls, issue):
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        return data.n17

    @classmethod
    def get_n18(cls, issue):
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        return data.n18

    @classmethod
    def get_n19(cls, issue):
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        return data.n19

    @classmethod
    def get_n20(cls, issue):
        session = get_session()
        data = session.query(cls).get(issue)
        session.close()
        return data.n20

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
    def get_previous3_issues(cls, issue_now):
        all_issues = cls.get_issues()
        issue_now = int(issue_now)
        index_now = all_issues.index(issue_now)
        return all_issues[index_now - 3: index_now]

    @classmethod
    def get_next3_issues(cls, issue_now):
        all_issues = cls.get_issues()
        issue_now = int(issue_now)
        index_now = all_issues.index(issue_now)
        return all_issues[index_now + 1: index_now + 4]

    @classmethod
    def get_all(cls):
        """get all [[issue, n01, n02, n03,...... n20]... ]"""
        session = get_session()
        data = session.query(cls).all()
        session.close()
        return [[
            x.issue,
            x.n01,
            x.n02,
            x.n03,
            x.n04,
            x.n05,
            x.n06,
            x.n07,
            x.n08,
            x.n09,
            x.n10,
            x.n11,
            x.n12,
            x.n13,
            x.n14,
            x.n15,
            x.n16,
            x.n17,
            x.n18,
            x.n19,
            x.n20
        ] for x in data]

    @classmethod
    def get_one(cls, issue_number: int):
        """获取对应 issue 的号码列表 [issue, n01, n02, n03, ......n20]"""
        session = get_session()
        data = session.query(cls).get(issue_number)
        session.close()
        return [
            data.issue,
            data.n01,
            data.n02,
            data.n03,
            data.n04,
            data.n05,
            data.n06,
            data.n07,
            data.n08,
            data.n09,
            data.n10,
            data.n11,
            data.n12,
            data.n13,
            data.n14,
            data.n15,
            data.n16,
            data.n17,
            data.n18,
            data.n19,
            data.n20
        ]

    @classmethod
    def add_number(cls, p_issue: str, p_numbers: list):
        """添加一条记录"""
        session = get_session()
        ins = cls(p_issue, p_numbers)
        session.merge(ins)
        session.commit()
        session.close()
        print(f">>> KL8 merge:{p_issue} - {p_numbers}")


class HappyVerify(Base):
    __tablename__ = "kl8_verifies"

    inumabc = Column(String, primary_key=True)
    issue = Column(Integer)
    num = Column(Integer)
    abc = Column(String)
    result = Column(String)
    score = Column(Float)
    verify = Column(String)
    n01 = Column(Integer)
    n02 = Column(Integer)
    n03 = Column(Integer)
    n04 = Column(Integer)
    n05 = Column(Integer)
    n06 = Column(Integer)
    n07 = Column(Integer)
    n08 = Column(Integer)
    n09 = Column(Integer)
    n10 = Column(Integer)
    n11 = Column(Integer)
    n12 = Column(Integer)
    n13 = Column(Integer)
    n14 = Column(Integer)
    n15 = Column(Integer)
    n16 = Column(Integer)
    n17 = Column(Integer)
    n18 = Column(Integer)
    n19 = Column(Integer)
    n20 = Column(Integer)

    def __init__(self, inumabc, issue, num, abc, result, score):
        super().__init__()
        self.inumabc = inumabc
        self.issue = issue
        self.num = num
        self.abc = abc
        self.result = result
        self.score = score

    @classmethod
    def get_result_score_or_false(cls, issue_num_abc: str):
        sess = get_session()
        data = sess.query(cls).get(issue_num_abc)
        sess.close()
        if data:
            return {'label': data.result, 'predicts': data.score}
        else:
            return False

    @classmethod
    def add_score(cls, inumabc, issue, num, abc, result, score):
        sess = get_session()
        ins = cls(inumabc, issue, num, abc, result, score)
        issues_all = HappyNumber.get_issues()
        if issue in issues_all:
            numbers = HappyNumber.get_one(issue)
            ins.n01 = numbers[1]
            ins.n02 = numbers[2]
            ins.n03 = numbers[3]
            ins.n04 = numbers[4]
            ins.n05 = numbers[5]
            ins.n06 = numbers[6]
            ins.n07 = numbers[7]
            ins.n08 = numbers[8]
            ins.n09 = numbers[9]
            ins.n10 = numbers[10]
            ins.n11 = numbers[11]
            ins.n12 = numbers[12]
            ins.n13 = numbers[13]
            ins.n14 = numbers[14]
            ins.n15 = numbers[15]
            ins.n16 = numbers[16]
            ins.n17 = numbers[17]
            ins.n18 = numbers[18]
            ins.n19 = numbers[19]
            ins.n20 = numbers[20]
            if int(num) in numbers[1:]:
                if result == 'y':
                    ins.verify = 'y'
                else:
                    ins.verify = 'n'
            else:
                if result == 'y':
                    ins.verify = 'n'
                else:
                    ins.verify = 'y'
        else:
            ins.verify = None
        sess.merge(ins)
        sess.commit()
        sess.close()
        print(
            f">>> {cls.__tablename__}: add score: inumabc: {inumabc}, issue: {issue}, num: {num}, abc: {abc}, result: {result}, score: {score}, verify: {ins.verify}")

    @classmethod
    def whether_needs_retrained(cls, num_abc: str, last_num: int, min_right: int):
        """检查模型最后几期的准确率, 判断是否合格

        Args:
            num_abc (str): num + abc [1008]
            last_num (int): 检查最后几期
            min_right (int): 最小正确数

        Returns:
            [type]: [description]
        """
        # 检查模型最后几期的准确率，判断是否合格
        if min_right > last_num:
            raise Exception(">>> ERROR PARAM: min_right > last_num")
        if len(num_abc) != 4:
            raise Exception(">>> ERROR PARAM: num_abc", num_abc)
        num_abc = str(num_abc)
        whether_train = True
        num = num_abc[:2]
        sess = get_session()
        issue_all = HappyNumber.get_issues()
        issue_last = issue_all[-last_num:]
        coll_verify = []
        coll_verify_all = []
        for i_target in issue_last:
            i_num_abc = f'{i_target}{num_abc}'
            v = sess.query(cls).get(i_num_abc)
            coll_verify.append(v.verify)
            temp_dict = {
                'num123': HappyNumber.get_one(i_target),
                'result': v.result,
                'verify': v.verify
            }
            coll_verify_all.append(temp_dict)
            print(f'model: {num_abc}, result: {temp_dict}')

        # 检查 y 的数量
        if coll_verify.count('y') >= min_right:
            whether_train = False

            # 检查 出号必y
            for one_coll in coll_verify_all:
                if num in one_coll['num123']:
                    if one_coll['verify'] == 'n':
                        whether_train = True

        print(f">>> whether_needs_retrained: {num_abc} - {whether_train}")
        return whether_train


if __name__ == "__main__":
    # generate tables
    from tools import get_engine
    engine = get_engine()
    Base.metadata.create_all(engine)
