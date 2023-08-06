from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_sqlite_session.tools import get_engine, get_session


Base = declarative_base()


def database_toast(issue: int, name_cn: str, name: str, key: str, value: str):
    """数据表属性 写入成功提示"""
    print(f">>> 合并数据成功，期号: {issue}，表名: {name_cn}-{name}: {key} - {value}")


def get_session_ssq():
    session = get_session()
    return session


def get_engine_ssq():
    engine = get_engine()
    return engine


class ExpertBase(Base):
    """
    many_r
    save_r
    many_b
    save_b
    """
    __abstract__ = True
    # __name__ = 'ssq_edahongdazi'
    # _name_ = '大红大紫'
    issue = Column(Integer, primary_key=True)

    # attributes
    many_r = Column(String)  # 红球
    save_r = Column(String)  # 红胆
    many_b = Column(String)  # 篮球
    save_b = Column(String)  # 蓝胆

    # verify attributes
    v_many_r = Column(String)
    v_save_r = Column(String)
    v_many_b = Column(String)
    v_save_b = Column(String)

    @classmethod
    def set_attribute(cls, issue: int, attribute_name: str, data: str):
        """set_attribute
        @param issue: 期号 \n
        @param attribute_name: 属性名称 \n
        @param data: 属性的数据
        """
        # 获取表的字段名称集合
        # total_names = [str(x) for x in cls.metadata.tables[cls.__tablename__].columns]
        # attributes = [x.replace(f'{cls.__tablename__}.', '') for x in total_names]
        session = get_session_ssq()
        ins = cls()
        ins.issue = issue
        # 选择属性
        if attribute_name == 'issue':
            pass
        elif attribute_name == 'many_r':
            ins.many_r = data
        elif attribute_name == 'save_r':
            ins.save_r = data
        elif attribute_name == 'many_b':
            ins.many_b = data
        elif attribute_name == 'save_b':
            ins.save_b = data
        elif attribute_name == 'v_many_r':
            ins.v_many_r = data
        elif attribute_name == 'v_save_r':
            ins.v_save_r = data
        elif attribute_name == 'v_many_b':
            ins.v_many_b = data
        elif attribute_name == 'v_save_b':
            ins.v_save_b = data
        else:
            raise Exception(f">>> 数据表《{cls._name_}》属性名称错误!!!")
        database_toast(issue, cls._name_, cls.__tablename__, attribute_name, data)
        session.merge(ins)
        session.commit()
        session.close()

    @classmethod
    def get_verify(cls):
        return f'{cls.v_many_r}{cls.v_save_r}{cls.v_many_b}{cls.v_save_b}'


class DaHongDaZi(ExpertBase):
    __tablename__ = 'ssq_edahongdazi'
    _name_ = '大红大紫'


class GaoShanLiuShui(ExpertBase):
    __tablename__ = 'ssq_egaoshanliushui'
    _name_ = '高山流水'


class HongLanNongFu(ExpertBase):
    __tablename__ = 'ssq_ehonglannongfu'
    _name_ = '红蓝农夫'


class HuaQiRenShen(ExpertBase):
    __tablename__ = 'ssq_ehuaqirenshen'
    _name_ = '花旗人参'


class JingZhuangXia(ExpertBase):
    __tablename__ = 'ssq_ejingzhuangxia'
    _name_ = '精装侠'


class LaoHuoLiangTang(ExpertBase):
    __tablename__ = 'ssq_elaohuoliangtang'
    _name_ = '老火靓汤'


class LiangLaoTang(ExpertBase):
    __tablename__ = 'ssq_elianglaotang'
    _name_ = '靓佬汤'


class ShanZhaiWang(ExpertBase):
    __tablename__ = 'ssq_eshanzhaiwang'
    _name_ = '山寨王'


class TongLuoWan(ExpertBase):
    __tablename__ = 'ssq_etongluowan'
    _name_ = '铜锣湾'


class YouZhanWang(ExpertBase):
    __tablename__ = 'ssq_eyouzhanwang'
    _name_ = '油沾旺'


class XingYunBoShi(ExpertBase):
    __tablename__ = 'ssq_exingyunboshi'
    _name_ = '幸运博士'


class HaoYunLaiLe(ExpertBase):
    __tablename__ = 'ssq_ehaoyunlaile'
    _name_ = '好运来了'


class ShanDongDaXia(ExpertBase):
    __tablename__ = 'ssq_eshandongdaxia'
    _name_ = '山东大侠'


class ChongQingHuoGuo(ExpertBase):
    __tablename__ = 'ssq_echongqinghuoguo'
    _name_ = '重庆火锅'


class HuiShang(ExpertBase):
    __tablename__ = 'ssq_ehuishang'
    _name_ = '徽商'


class JinLaoXi(ExpertBase):
    __tablename__ = 'ssq_ejinlaoxi'
    _name_ = '晋老西合伙制'


class MengGuBao(ExpertBase):
    __tablename__ = 'ssq_emenggubao'
    _name_ = '蒙古包'


class YaoKong(ExpertBase):
    __tablename__ = 'ssq_eyaokong'
    _name_ = '遥控'


class ZhongLe(ExpertBase):
    __tablename__ = 'ssq_ezhongle'
    _name_ = '中了没商量'


class BanErYe(ExpertBase):
    __tablename__ = 'ssq_ebanerye'
    _name_ = '板儿爷'


class SiDaShu(ExpertBase):
    __tablename__ = 'ssq_esidashu'
    _name_ = '斯达舒'


class DaLianHaiXian(ExpertBase):
    __tablename__ = 'ssq_edalianhaixian'
    _name_ = '大连海鲜'


class MaTouQin(ExpertBase):
    __tablename__ = 'ssq_ematouqin'
    _name_ = '马头琴'


class NumberSSQ(Base):
    __tablename__ = 'number_ssq'

    def __init__(self, data_list: list):
        self.session = get_session_ssq()
        self.issue, self.num1, self.num2, self.num3, self.num4, self.num5, self.num6, self.num7 = data_list

    issue = Column(Integer, primary_key=True)
    num1 = Column(Integer, nullable=False)
    num2 = Column(Integer, nullable=False)
    num3 = Column(Integer, nullable=False)
    num4 = Column(Integer, nullable=False)
    num5 = Column(Integer, nullable=False)
    num6 = Column(Integer, nullable=False)
    num7 = Column(Integer, nullable=False)

    @classmethod
    def get_numbers(cls):
        """
        根据名称获取对应的设置项的值
        :param name: 设置项名称
        :return: 根据值的属性，返回对应的数据类型
        """
        session = get_session_ssq()
        data = session.query(cls).all()
        session.close()
        result = [[x.issue, x.num1, x.num2, x.num3, x.num4, x.num5, x.num6, x.num7] for x in data]
        return result

    @classmethod
    def get_one(cls, issue_number: int):
        """
        根据名称获取对应的设置项的值
        :type issue_number: issue
        """
        session = get_session_ssq()
        d = session.query(cls).get(issue_number)
        session.close()
        return [d.issue, d.num1, d.num2, d.num3, d.num4, d.num5, d.num6, d.num7]

    @classmethod
    def get_issues(cls):
        """get issues"""
        session = get_session_ssq()
        i = session.query(cls).all()
        session.close()
        return [x.issue for x in i]

    @classmethod
    def add_number(cls, p_issue: str, p_numbers: list):
        """添加一条记录"""
        session = get_session()
        ins = cls([p_issue] + p_numbers)
        session.merge(ins)
        session.commit()
        session.close()
        print(f">>> SSQ merge:{p_issue} - {p_numbers}")


class PredictSSQ(Base):
    """ numbers@sd.db """
    __tablename__ = 'cjcp_cz89'

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
    red25 = Column(String, nullable=True)
    red20 = Column(String, nullable=True)
    red12 = Column(String, nullable=True)
    red10 = Column(String, nullable=True)
    red_save1 = Column(String, nullable=True)
    red_save2 = Column(String, nullable=True)
    red_save3 = Column(String, nullable=True)
    red_kill3 = Column(String, nullable=True)
    red_kill6 = Column(String, nullable=True)
    red_begin2 = Column(String, nullable=True)
    red_end2 = Column(String, nullable=True)
    blue_kill5 = Column(String, nullable=True)
    blue_save2 = Column(String, nullable=True)
    blue_save3 = Column(String, nullable=True)
    blue_save4 = Column(String, nullable=True)
    blue_save5 = Column(String, nullable=True)


if __name__ == "__main__":
    # WelfareVerify.add_score('20212882945', 2021288, 2, '945', 'y', 0.49)
    # print(WelfareNumber.get_next3_issues(2021287))
    # generate tables
    engine = get_engine()
    Base.metadata.create_all(engine)
    pass
