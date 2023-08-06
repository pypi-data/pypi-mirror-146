from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_sqlite_session.tools import get_session, get_engine
import json

Base = declarative_base()


def database_toast(issue: int, name_cn: str, name: str, key: str, value: str):
    """数据表属性 写入成功提示"""
    print(f">>> 合并数据成功，期号：{issue}，表名：{name_cn}-{name}: {key} - {value}")


def get_session_sport():
    session = get_session()
    return session


def get_engine_sport():
    engine = get_engine()
    return engine


class SportNumber(Base):
    """ numbers@p3.db """
    __tablename__ = 'number_p3'

    issue = Column(Integer, primary_key=True)
    num1 = Column(Integer, nullable=False)
    num2 = Column(Integer, nullable=False)
    num3 = Column(Integer, nullable=False)

    def __init__(self, data_list: list):
        self.issue, self.num1, self.num2, self.num3 = data_list

    @classmethod
    def get_num1(cls, issue_number: int):
        """获取对应 issue 的号码 num1"""
        session = get_session_sport()
        data = session.query(cls).get(issue_number)
        session.close()
        return data.num1

    @classmethod
    def get_num2(cls, issue_number: int):
        """获取对应 issue 的号码 num2"""
        session = get_session_sport()
        data = session.query(cls).get(issue_number)
        session.close()
        return data.num2

    @classmethod
    def get_num3(cls, issue_number: int):
        """获取对应 issue 的号码 num3"""
        session = get_session_sport()
        data = session.query(cls).get(issue_number)
        session.close()
        return data.num3

    @classmethod
    def get_issues(cls):
        """get issues[list]"""
        session = get_session_sport()
        i = session.query(cls).all()
        session.close()
        result = [x.issue for x in i]
        result.sort()
        return result

    @classmethod
    def get_previous_issues_by_num(cls, issue_now, num):
        all_issues = cls.get_issues()
        issue_now = int(issue_now)
        if issue_now in all_issues:
            index_now = all_issues.index(issue_now)
            return all_issues[index_now - num: index_now]
        else:
            return all_issues[- num:]

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
        """get all [[issue, num1, num2, num3]... ]"""
        session = get_session_sport()
        data = session.query(cls).all()
        session.close()
        return [[x.issue, x.num1, x.num2, x.num3] for x in data]

    @classmethod
    def get_numbers(cls):
        """get numbers [[issue, num1, num2, num3]... ]"""
        session = get_session_sport()
        data = session.query(cls).all()
        session.close()
        result = [[x.issue, x.num1, x.num2, x.num3] for x in data]
        return result

    @classmethod
    def get_one(cls, issue_number: int):
        """获取对应 issue 的号码列表 [issue, num1, num2, num3]"""
        session = get_session_sport()
        data = session.query(cls).get(issue_number)
        session.close()
        return [data.issue, data.num1, data.num2, data.num3]

    @classmethod
    def add_number(cls, p_issue: str, p_numbers: list):
        """添加一条记录"""
        session = get_session_sport()
        ins = SportNumber([p_issue] + p_numbers)
        session.merge(ins)
        session.commit()
        session.close()
        print(f">>> P3 merge:{p_issue} - {p_numbers}")


class ExpertSummary(Base):
    """
    save_a
    save_b
    save_c
    kills
    he
    span
    mix5
    mix6
    mix7
    multi6
    multi3
    """
    __abstract__ = True
    issue = Column(Integer, primary_key=True)

    def set_attribute(self, issue: int, attribute_name: str, data: str):
        """获取表的字段名称集合, 并更新
        """
        # 获取表的字段名称集合
        total_names = [str(x) for x in self.metadata.tables[self.__tablename__].columns]
        attributes = [x.replace(f'{self.__tablename__}.', '') for x in total_names]
        session = get_session_sport()
        self.issue = issue
        # 选择属性
        if attribute_name == 'issue':
            pass
        elif attribute_name in attributes:
            exec_string = f'self.{attribute_name} = data'
            exec(exec_string)
        else:
            raise Exception(f">>> 数据表《{self._name_}》属性名称错误!!!")
        database_toast(issue, self._name_, self.__tablename__, attribute_name, data)
        session.merge(self)
        session.commit()
        session.close()

    def get_verify(self):
        return [
            '√' if self.v_save_a.find('正确') > -1 else 'x',
            '√' if self.v_save_b.find('正确') > -1 else 'x',
            '√' if self.v_save_c.find('正确') > -1 else 'x',
            '√' if self.v_kills.find('正确') > -1 else 'x',
            '√' if self.v_he.find('正确') > -1 else 'x',
            '√' if self.v_span.find('正确') > -1 else 'x',
            '√' if self.v_mix5.find('正确') > -1 else 'x',
            '√' if self.v_mix6.find('正确') > -1 else 'x',
            '√' if self.v_mix7.find('正确') > -1 else 'x',
            '√' if self.v_multi6.find('正确') > -1 else 'x',
            '√' if self.v_multi3.find('正确') > -1 else 'x'
        ]

    @classmethod
    def get_next_issue(cls):
        sess = get_session_sport()
        all = sess.query(cls).all()
        i = all[-1].issue
        return i

    @classmethod
    def gen_mix_7(cls, issue_p):
        sess = get_session_sport()
        nums = sess.query(SportNumber).get(issue_p)
        n1, n2, n3 = nums.num1, nums.num2, nums.num3
        mix7 = sess.query(cls).get(issue_p).mix7
        mix7_list = mix7.split(',')
        mix_list = [int(x) for x in mix7_list]
        counter_right = 0
        if n1 in mix_list:
            counter_right += 1
        if n2 in mix_list:
            counter_right += 1
        if n3 in mix_list:
            counter_right += 1
        sess.close()
        return counter_right


class CaiYanShi(ExpertSummary):
    """
    save_a
    save_b
    save_c
    kills
    he
    span
    mix5
    mix6
    mix7
    multi6
    multi3
    """
    __tablename__ = 'p3_caiyanshi'
    _name_ = '彩研师'
    issue = Column(Integer, primary_key=True)

    # attributes
    save_a = Column(String)  # 金胆
    save_b = Column(String)  # 银胆
    save_c = Column(String)  # 铜胆
    kills = Column(String)  # 排除
    he = Column(String)  # 和值
    span = Column(String)  # 跨度
    mix5 = Column(String)  # 五码复式
    mix6 = Column(String)  # 六码复式
    mix7 = Column(String)  # 七码复式
    multi6 = Column(String)  # 组选推荐
    multi3 = Column(String)  # 组三推荐

    # verify attributes
    v_save_a = Column(String)
    v_save_b = Column(String)
    v_save_c = Column(String)
    v_kills = Column(String)
    v_he = Column(String)
    v_span = Column(String)
    v_mix5 = Column(String)
    v_mix6 = Column(String)
    v_mix7 = Column(String)
    v_multi6 = Column(String)
    v_multi3 = Column(String)

    def get_verify(self):
        return [
            '√' if self.v_save_a.find('正确') > -1 else 'x',
            '√' if self.v_save_b.find('正确') > -1 else 'x',
            '√' if self.v_save_c.find('正确') > -1 else 'x',
            '√' if self.v_kills.find('正确') > -1 else 'x',
            '√' if self.v_he.find('正确') > -1 else 'x',
            '√' if self.v_span.find('正确') > -1 else 'x',
            '√' if self.v_mix5.find('正确') > -1 else 'x',
            '√' if self.v_mix6.find('正确') > -1 else 'x',
            '√' if self.v_mix7.find('正确') > -1 else 'x',
            '√' if self.v_multi6.find('正确') > -1 else 'x',
            '√' if self.v_multi3.find('正确') > -1 else 'x'
        ]


class DaiTouDaGe(ExpertSummary):
    __tablename__ = 'p3_daitoudage'
    _name_ = '带头大哥'
    issue = Column(Integer, primary_key=True)

    # attributes
    kills = Column(String)  # 杀码推荐
    save1 = Column(String)  # 独胆预测
    save2 = Column(String)  # 双胆预测
    save3 = Column(String)  # 三胆预测
    mix5 = Column(String)  # 五码复式
    mix6 = Column(String)  # 六码复式
    mix7 = Column(String)  # 七码复式
    he = Column(String)  # 推荐和值
    span = Column(String)  # 推荐跨度
    multi6 = Column(String)  # 组选推荐
    result_many = Column(String)  # 直选推荐

    # verify attributes
    v_kills = Column(String)
    v_save1 = Column(String)
    v_save2 = Column(String)
    v_save3 = Column(String)
    v_mix5 = Column(String)
    v_mix6 = Column(String)
    v_mix7 = Column(String)
    v_he = Column(String)
    v_span = Column(String)
    v_multi6 = Column(String)
    v_result_many = Column(String)

    def get_verify(self):
        return [
            '√' if self.v_kills.find('正确') > -1 else 'x',
            '√' if self.v_save1.find('正确') > -1 else 'x',
            '√' if self.v_save2.find('正确') > -1 else 'x',
            '√' if self.v_save3.find('正确') > -1 else 'x',
            '√' if self.v_mix5.find('正确') > -1 else 'x',
            '√' if self.v_mix6.find('正确') > -1 else 'x',
            '√' if self.v_mix7.find('正确') > -1 else 'x',
            '√' if self.v_he.find('正确') > -1 else 'x',
            '√' if self.v_span.find('正确') > -1 else 'x',
            '√' if self.v_multi6.find('正确') > -1 else 'x',
            '√' if self.v_result_many.find('正确') > -1 else 'x'
        ]


class HuaWuQue(ExpertSummary):
    __tablename__ = 'p3_huawuque'
    _name_ = '花无缺'
    issue = Column(Integer, primary_key=True)

    # attributes
    save_location = Column(String)  # 定位胆码
    position1 = Column(String)  # 百位
    position2 = Column(String)  # 十位
    position3 = Column(String)  # 个位
    mix5 = Column(String)  # 5码复试
    mix6 = Column(String)  # 6码复式
    mix7 = Column(String)  # 7码复式
    multi36 = Column(String)  # 组选推荐

    # verify attribute
    v_save_location = Column(String)
    v_position1 = Column(String)
    v_position2 = Column(String)
    v_position3 = Column(String)
    v_mix5 = Column(String)
    v_mix6 = Column(String)
    v_mix7 = Column(String)
    v_multi36 = Column(String)

    def get_verify(self):
        return [
            '√' if self.v_save_location.find('正确') > -1 else 'x',
            '√' if self.v_position1.find('正确') > -1 else 'x',
            '√' if self.v_position2.find('正确') > -1 else 'x',
            '√' if self.v_position3.find('正确') > -1 else 'x',
            '√' if self.v_mix5.find('正确') > -1 else 'x',
            '√' if self.v_mix6.find('正确') > -1 else 'x',
            '√' if self.v_mix7.find('正确') > -1 else 'x',
            '√' if self.v_multi36.find('正确') > -1 else 'x'
        ]


class QingQiuJuShi(ExpertSummary):
    __tablename__ = 'p3_qingqiujushi'
    _name_ = '清秋居士'
    issue = Column(Integer, primary_key=True)

    # attributes
    save1 = Column(String)  # 独胆
    save2 = Column(String)  # 双胆
    save3 = Column(String)  # 三胆
    kill1 = Column(String)  # 杀一码
    kill2 = Column(String)  # 杀二码
    kill3 = Column(String)  # 杀三码
    mix5 = Column(String)  # 五码
    mix6 = Column(String)  # 六码
    position_x = Column(String)  # 定位
    he = Column(String)  # 和值
    span = Column(String)  # 跨度
    multi6 = Column(String)  # 组选

    # verify attributes
    v_save1 = Column(String)
    v_save2 = Column(String)
    v_save3 = Column(String)
    v_kill1 = Column(String)
    v_kill2 = Column(String)
    v_kill3 = Column(String)
    v_mix5 = Column(String)
    v_mix6 = Column(String)
    v_position_x = Column(String)
    v_he = Column(String)
    v_span = Column(String)
    v_multi6 = Column(String)

    def get_verify(self):
        return [
            '√' if self.v_save1.find('正确') > -1 else 'x',
            '√' if self.v_save2.find('正确') > -1 else 'x',
            '√' if self.v_save3.find('正确') > -1 else 'x',
            '√' if self.v_kill1.find('正确') > -1 else 'x',
            '√' if self.v_kill2.find('正确') > -1 else 'x',
            '√' if self.v_kill3.find('正确') > -1 else 'x',
            '√' if self.v_mix5.find('正确') > -1 else 'x',
            '√' if self.v_mix6.find('正确') > -1 else 'x',
            '√' if self.v_position_x.find('正确') > -1 else 'x',
            '√' if self.v_he.find('正确') > -1 else 'x',
            '√' if self.v_span.find('正确') > -1 else 'x',
            '√' if self.v_multi6.find('正确') > -1 else 'x'
        ]


class ShiNaJiuWen(ExpertSummary):
    __tablename__ = 'p3_shinajiuwen'
    _name_ = '十拿九稳'
    issue = Column(Integer, primary_key=True)

    # attributes
    save3 = Column(String)  # 胆码
    mix4 = Column(String)  # 四码
    mix5 = Column(String)  # 五码复式
    mix6 = Column(String)  # 六码复式
    mix7 = Column(String)  # 七码复式
    position1 = Column(String)  # 百位定位推荐
    position2 = Column(String)  # 十位定位推荐
    position3 = Column(String)  # 个位定位推荐
    result_many = Column(String)  # 直选精选
    multi36 = Column(String)  # 组选大底

    # verify attribute
    v_save3 = Column(String)
    v_mix4 = Column(String)
    v_mix5 = Column(String)
    v_mix6 = Column(String)
    v_mix7 = Column(String)
    v_position1 = Column(String)
    v_position2 = Column(String)
    v_position3 = Column(String)
    v_result_many = Column(String)
    v_multi36 = Column(String)

    def get_verify(self):
        return [
            '√' if self.v_save3.find('正确') > -1 else 'x',
            '√' if self.v_mix4.find('正确') > -1 else 'x',
            '√' if self.v_mix5.find('正确') > -1 else 'x',
            '√' if self.v_mix6.find('正确') > -1 else 'x',
            '√' if self.v_mix7.find('正确') > -1 else 'x',
            '√' if self.v_position1.find('正确') > -1 else 'x',
            '√' if self.v_position2.find('正确') > -1 else 'x',
            '√' if self.v_position3.find('正确') > -1 else 'x',
            '√' if self.v_result_many.find('正确') > -1 else 'x',
            '√' if self.v_multi36.find('正确') > -1 else 'x'
        ]


class WanCaiLaoTou(ExpertSummary):
    __tablename__ = 'p3_wancailaotou'
    _name_ = '玩彩老头'
    issue = Column(Integer, primary_key=True)

    # attributes
    save1 = Column(String)  # 独胆
    save2 = Column(String)  # 双胆
    save3 = Column(String)  # 三胆
    mix5 = Column(String)  # 五码
    mix6 = Column(String)  # 六码
    mix7 = Column(String)  # 七码
    he = Column(String)  # 和值
    span = Column(String)  # 跨度
    multi6 = Column(String)  # 组六号码推荐

    # verify attributes
    v_save1 = Column(String)
    v_save2 = Column(String)
    v_save3 = Column(String)
    v_mix5 = Column(String)
    v_mix6 = Column(String)
    v_mix7 = Column(String)
    v_he = Column(String)
    v_span = Column(String)
    v_multi6 = Column(String)

    def get_verify(self):
        return [
            '√' if self.v_save1.find('正确') > -1 else 'x',
            '√' if self.v_save2.find('正确') > -1 else 'x',
            '√' if self.v_save3.find('正确') > -1 else 'x',
            '√' if self.v_mix5.find('正确') > -1 else 'x',
            '√' if self.v_mix6.find('正确') > -1 else 'x',
            '√' if self.v_mix7.find('正确') > -1 else 'x',
            '√' if self.v_he.find('正确') > -1 else 'x',
            '√' if self.v_span.find('正确') > -1 else 'x',
            '√' if self.v_multi6.find('正确') > -1 else 'x'
        ]


class XiaoYanZi(ExpertSummary):
    __tablename__ = 'p3_xiaoyanzi'
    _name_ = '小燕子'
    issue = Column(Integer, primary_key=True)

    # attributes
    save1 = Column(String)  # 独胆预测
    save2 = Column(String)  # 双胆预测
    save3 = Column(String)  # 三胆预测
    mix5 = Column(String)  # 五码复式
    mix6 = Column(String)  # 六码复式
    mix7 = Column(String)  # 七码复式
    he = Column(String)  # 推荐和值
    span = Column(String)  # 推荐跨度
    kills = Column(String)  # 排除号码
    multi6 = Column(String)  # 组选号码

    # verify attributes
    v_save1 = Column(String)
    v_save2 = Column(String)
    v_save3 = Column(String)
    v_mix5 = Column(String)
    v_mix6 = Column(String)
    v_mix7 = Column(String)
    v_he = Column(String)
    v_span = Column(String)
    v_kills = Column(String)
    v_multi6 = Column(String)

    def get_verify(self):
        return [
            '√' if self.v_save1.find('正确') > -1 else 'x',
            '√' if self.v_save2.find('正确') > -1 else 'x',
            '√' if self.v_save3.find('正确') > -1 else 'x',
            '√' if self.v_mix5.find('正确') > -1 else 'x',
            '√' if self.v_mix6.find('正确') > -1 else 'x',
            '√' if self.v_mix7.find('正确') > -1 else 'x',
            '√' if self.v_he.find('正确') > -1 else 'x',
            '√' if self.v_span.find('正确') > -1 else 'x',
            '√' if self.v_kills.find('正确') > -1 else 'x',
            '√' if self.v_multi6.find('正确') > -1 else 'x'
        ]


class YueYeFeiLong(ExpertSummary):
    __tablename__ = 'p3_yueyefeilong'
    _name_ = '月夜飞龙'
    issue = Column(Integer, primary_key=True)

    # attributes
    save1 = Column(String)  # 独胆
    save2 = Column(String)  # 双胆
    save3 = Column(String)  # 三胆
    kill1 = Column(String)  # 杀一码
    kill2 = Column(String)  # 杀二码
    kill3 = Column(String)  # 杀三码
    mix5 = Column(String)  # 五码
    mix6 = Column(String)  # 六码
    position_x = Column(String)  # 定位
    he = Column(String)  # 和值
    span = Column(String)  # 跨度
    multi6 = Column(String)  # 组选

    # verify attributes
    v_save1 = Column(String)
    v_save2 = Column(String)
    v_save3 = Column(String)
    v_kill1 = Column(String)
    v_kill2 = Column(String)
    v_kill3 = Column(String)
    v_mix5 = Column(String)
    v_mix6 = Column(String)
    v_position_x = Column(String)
    v_he = Column(String)
    v_span = Column(String)
    v_multi6 = Column(String)

    def get_verify(self):
        return [
            '√' if self.v_save1.find('正确') > -1 else 'x',
            '√' if self.v_save2.find('正确') > -1 else 'x',
            '√' if self.v_save3.find('正确') > -1 else 'x',
            '√' if self.v_kill1.find('正确') > -1 else 'x',
            '√' if self.v_kill2.find('正确') > -1 else 'x',
            '√' if self.v_kill3.find('正确') > -1 else 'x',
            '√' if self.v_mix5.find('正确') > -1 else 'x',
            '√' if self.v_mix6.find('正确') > -1 else 'x',
            '√' if self.v_position_x.find('正确') > -1 else 'x',
            '√' if self.v_he.find('正确') > -1 else 'x',
            '√' if self.v_span.find('正确') > -1 else 'x',
            '√' if self.v_multi6.find('正确') > -1 else 'x'
        ]


class ZiYunJian(ExpertSummary):
    """
    position5_1
    position5_2
    position5_3
    position3_1
    position3_2
    position3_3
    save3
    mix4
    mix5
    multi36
    """
    __tablename__ = 'p3_ziyunjian'
    _name_ = '紫云涧'
    issue = Column(Integer, primary_key=True)

    # attributes
    position5_1 = Column(String)  # 555复式 百位
    position5_2 = Column(String)  # 555复式 十位
    position5_3 = Column(String)  # 555复式 个位
    position3_1 = Column(String)  # 333复式 百位
    position3_2 = Column(String)  # 333复式 十位
    position3_3 = Column(String)  # 333复式 个位
    save3 = Column(String)  # 三胆
    mix4 = Column(String)  # 四码
    mix5 = Column(String)  # 五码
    multi36 = Column(String)  # 直,组推荐

    # verify attributes
    v_position5_1 = Column(String)
    v_position5_2 = Column(String)
    v_position5_3 = Column(String)
    v_position3_1 = Column(String)
    v_position3_2 = Column(String)
    v_position3_3 = Column(String)
    v_save3 = Column(String)
    v_mix4 = Column(String)
    v_mix5 = Column(String)
    v_multi36 = Column(String)

    def get_verify(self):
        return [
            '√' if self.v_position5_1.find('正确') > -1 else 'x',
            '√' if self.v_position5_2.find('正确') > -1 else 'x',
            '√' if self.v_position5_3.find('正确') > -1 else 'x',
            '√' if self.v_position3_1.find('正确') > -1 else 'x',
            '√' if self.v_position3_2.find('正确') > -1 else 'x',
            '√' if self.v_position3_3.find('正确') > -1 else 'x',
            '√' if self.v_save3.find('正确') > -1 else 'x',
            '√' if self.v_mix4.find('正确') > -1 else 'x',
            '√' if self.v_mix5.find('正确') > -1 else 'x',
            '√' if self.v_multi36.find('正确') > -1 else 'x'
        ]


class SportVerifyBase(Base):
    __abstract__ = True

    inumabc = Column(String, primary_key=True)
    issue = Column(Integer)
    num = Column(Integer)
    abc = Column(String)
    result = Column(String)
    score = Column(Float)
    num1 = Column(Integer)
    num2 = Column(Integer)
    num3 = Column(Integer)
    verify = Column(String)

    @classmethod
    def get_result_score_or_false(cls, issue_num_abc: str):
        with get_session_sport() as sess:
            # sess = get_session_sport()
            data = sess.query(cls).get(issue_num_abc)
            if data:
                return {'label': data.result, 'predicts': data.score}
            else:
                return False

    @classmethod
    def get_model_score(cls, path_json: str) -> dict:
        """
        检查表 verifies 最后5期的数据，得出所有模型的得分，并写入指定的json文件，并返回结果
        base                         s1     1
        verify == 'y' & 不包含开奖号  s2     1
        verify == 'y' & 又包含开奖号  s3     2
        verify == 'n'                       0
        """
        s1 = 1
        s2 = 1
        s3 = 2

        sess = get_session_sport()
        # 获取最后5期的期号
        num_all = sess.query(SportNumber).order_by(SportNumber.issue).all()
        num_last5 = num_all[-5:]
        issue_begin = num_last5[0].issue

        # 获取最后5期的 verifies 表数据
        data_verifies = sess.query(cls).filter(cls.issue >= issue_begin).all()
        dict_verifies = {x.inumabc: x for x in data_verifies}
        result = dict()

        # 循环模型名称
        for num in range(10):
            for p1 in range(10):
                for p2 in range(10):
                    for p3 in range(10):
                        num_a_b_c = f'{num}{p1}{p2}{p3}'
                        result[num_a_b_c] = s1
                        # 循环最后5期的数据
                        for n in num_last5:
                            i = n.issue
                            nums = [n.num1, n.num2, n.num3]
                            i_num_a_b_c = f'{i}{num_a_b_c}'
                            ins = dict_verifies.get(i_num_a_b_c)
                            if ins.verify == 'y':
                                if ins.num in nums:
                                    result[num_a_b_c] = result[num_a_b_c] + s3
                                else:
                                    result[num_a_b_c] = result[num_a_b_c] + s2
        # result
        with open(path_json, 'w') as file_write:
            json.dump(result, file_write)
        print(">>> json result has been written at:", path_json)
        return result

    @classmethod
    def add_score(cls, inumabc, issue, num, abc, result, score):
        sess = get_session_sport()
        ins = cls(inumabc, issue, num, abc, result, score)
        issues_all = SportNumber.get_issues()
        if issue in issues_all:
            numbers = SportNumber.get_one(issue)
            ins.num1 = numbers[1]
            ins.num2 = numbers[2]
            ins.num3 = numbers[3]
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
        """检查模型最后几期的准确率，判断是否合格

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
        num = num_abc[0]
        sess = get_session_sport()
        issue_all = SportNumber.get_issues()
        issue_last = issue_all[-last_num:]
        coll_verify = []
        coll_verify_all = []
        for i_target in issue_last:
            i_num_abc = f'{i_target}{num_abc}'
            v_ins = sess.query(cls).get(i_num_abc)
            coll_verify.append(v_ins.verify)
            temp_dict = {
                'num123': f'{v_ins.num1}{v_ins.num2}{v_ins.num3}',
                'result': v_ins.result,
                'verify': v_ins.verify
            }
            coll_verify_all.append(temp_dict)
            print(f'model: {num_abc}, result: {temp_dict}')

        # 检查 y 的数量
        if coll_verify.count('y') >= min_right:
            whether_train = False

            # 检查 出号必y
            for one_coll in coll_verify_all:
                if one_coll['num123'].find(str(num)) > -1:
                    if one_coll['verify'] == 'n':
                        whether_train = True

        print(f">>> whether_needs_retrained: {num_abc} - {whether_train}")
        return whether_train


class SportVerifyN(SportVerifyBase):
    __tablename__ = "p3_verifyn"

    def __init__(self, inumabc, issue, num, abc, result, score):
        super().__init__()
        self.inumabc = inumabc
        self.issue = issue
        self.num = num
        self.abc = abc
        self.result = result
        self.score = score


class SportNumber5(Base):
    """ numbers@p3.db """
    __tablename__ = 'number_p5'

    issue = Column(Integer, primary_key=True)
    num1 = Column(Integer, nullable=False)
    num2 = Column(Integer, nullable=False)
    num3 = Column(Integer, nullable=False)
    num4 = Column(Integer, nullable=False)
    num5 = Column(Integer, nullable=False)

    def __init__(self, data_list: list):
        self.issue, self.num1, self.num2, self.num3, self.num4, self.num5 = data_list

    @classmethod
    def get_issues(cls):
        """get issues[list]"""
        session = get_session_sport()
        i = session.query(cls).all()
        result = [x.issue for x in i]
        result.sort()
        session.close()
        return result

    @classmethod
    def get_all(cls):
        """get all [[issue, num1, num2, num3, num4, num5]... ]"""
        session = get_session_sport()
        data = session.query(cls).all()
        session.close()
        return [[x.issue, x.num1, x.num2, x.num3, x.num4, x.num5] for x in data]

    @classmethod
    def get_numbers(cls):
        """get numbers [[issue, num1, num2, num3, num4, num5]... ]"""
        session = get_session_sport()
        data = session.query(cls).all()
        session.close()
        result = [[x.issue, x.num1, x.num2, x.num3, x.num4, x.num5] for x in data]
        return result

    @classmethod
    def get_one(cls, issue_number: int):
        """获取对应 issue 的号码列表 [issue, num1, num2, num3, num4, num5]"""
        session = get_session_sport()
        data = session.query(cls).get(issue_number)
        session.close()
        return [data.issue, data.num1, data.num2, data.num3, data.num4, data.num5]

    @classmethod
    def add_number(cls, p_issue: str, p_numbers: list):
        """添加一条记录"""
        session = get_session_sport()
        ins = cls([p_issue] + p_numbers)
        session.merge(ins)
        session.commit()
        session.close()
        print(f">>> P5 merge:{p_issue} - {p_numbers}")

    @classmethod
    def get_num1(cls, issue_number: int):
        """获取对应 issue 的号码 num1"""
        session = get_session_sport()
        data = session.query(cls).get(issue_number)
        session.close()
        return data.num1

    @classmethod
    def get_num2(cls, issue_number: int):
        """获取对应 issue 的号码 num2"""
        session = get_session_sport()
        data = session.query(cls).get(issue_number)
        session.close()
        return data.num2

    @classmethod
    def get_num3(cls, issue_number: int):
        """获取对应 issue 的号码 num3"""
        session = get_session_sport()
        data = session.query(cls).get(issue_number)
        session.close()
        return data.num3

    @classmethod
    def get_num4(cls, issue_number: int):
        """获取对应 issue 的号码 num4"""
        session = get_session_sport()
        data = session.query(cls).get(issue_number)
        session.close()
        return data.num4

    @classmethod
    def get_num5(cls, issue_number: int):
        """获取对应 issue 的号码 num5"""
        session = get_session_sport()
        data = session.query(cls).get(issue_number)
        session.close()
        return data.num5

    @classmethod
    def get_previous3_issues(cls, issue_now):
        all_issues = cls.get_issues()
        all_issues.sort()
        issue_now = int(issue_now)
        index_now = all_issues.index(issue_now)
        return all_issues[index_now - 3: index_now]

    @classmethod
    def get_previous_issues_by_num(cls, issue_now, num):
        all_issues = cls.get_issues()
        all_issues.sort()
        issue_now = int(issue_now)
        index_now = all_issues.index(issue_now)
        return all_issues[index_now - num: index_now]

    @classmethod
    def get_next3_issues(cls, issue_now):
        all_issues = cls.get_issues()
        issue_now = int(issue_now)
        index_now = all_issues.index(issue_now)
        return all_issues[index_now + 1: index_now + 4]


class SportFollowX(Base):
    __abstract__ = True

    issue = Column(Integer, primary_key=True)
    num = Column(Integer, nullable=False)
    next1 = Column(Integer)
    next2 = Column(Integer)
    next3 = Column(Integer)
    f0 = Column(Integer)
    f1 = Column(Integer)
    f2 = Column(Integer)
    f3 = Column(Integer)
    f4 = Column(Integer)
    f5 = Column(Integer)
    f6 = Column(Integer)
    f7 = Column(Integer)
    f8 = Column(Integer)
    f9 = Column(Integer)
    c0 = Column(Float)
    c1 = Column(Float)
    c2 = Column(Float)
    c3 = Column(Float)
    c4 = Column(Float)
    c5 = Column(Float)
    c6 = Column(Float)
    c7 = Column(Float)
    c8 = Column(Float)
    c9 = Column(Float)

    # def __init__(self, issue, num) -> None:
    #     super().__init__()
    #     self.issue = issue
    #     self.num = num

    @classmethod
    def get_follow_09(cls):
        session = get_session_sport()
        data = session.query(cls).all()
        result = {}
        for t in data:
            result[t.issue] = [t.f0, t.f1, t.f2, t.f3, t.f4, t.f5, t.f6, t.f7, t.f8, t.f9]
        return result

    @classmethod
    def get_change_09(cls):
        session = get_session_sport()
        data = session.query(cls).all()
        result = {}
        for t in data:
            result[t.issue] = [t.c0, t.c1, t.c2, t.c3, t.c4, t.c5, t.c6, t.c7, t.c8, t.c9]
        return result

    @classmethod
    def get_follow_change_09(cls):
        session = get_session_sport()
        data = session.query(cls).all()
        result = {}
        for t in data:
            result[t.issue] = [t.f0, t.f1, t.f2, t.f3, t.f4, t.f5, t.f6, t.f7, t.f8,
                               t.f9, t.c0, t.c1, t.c2, t.c3, t.c4, t.c5, t.c6, t.c7, t.c8, t.c9]
        return result

    @classmethod
    def get_nums(cls):
        """
        [[issue, num],...]
        """
        session = get_session_sport()
        data = session.query(cls).all()
        session.close()
        result = [[x.issue, x.num] for x in data]
        return result

    @classmethod
    def get_number_and_next(cls):
        """
        [[issue, num, next1, next2, next3],...]
        """
        session = get_session_sport()
        data = session.query(cls).all()
        session.close()
        result = [[x.issue, x.num, x.next1, x.next2, x.next3] for x in data]
        return result

    @classmethod
    def get_all(cls):
        """
        获取所有的数据
        """
        session = get_session_sport()
        data = session.query(cls).all()
        session.close()
        result = [[
            x.issue,
            x.num,
            x.f0,
            x.f1,
            x.f2,
            x.f3,
            x.f4,
            x.f5,
            x.f6,
            x.f7,
            x.f8,
            x.f9,
            x.c0,
            x.c1,
            x.c2,
            x.c3,
            x.c4,
            x.c5,
            x.c6,
            x.c7,
            x.c8,
            x.c9
        ] for x in data]
        return result

    @classmethod
    def get_issues(cls):
        """get issues"""
        session = get_session_sport()
        data = session.query(cls).all()
        session.close()
        result = [x.issue for x in data]
        result.sort()
        return result


class SportFollowA(SportFollowX):
    __tablename__ = 'p5_followa'

    def __init__(self, issue, num) -> None:
        super().__init__()
        self.issue = issue
        self.num = num


class SportFollowB(SportFollowX):
    __tablename__ = 'p5_followb'

    def __init__(self, issue, num) -> None:
        super().__init__()
        self.issue = issue
        self.num = num


class SportFollowC(SportFollowX):
    __tablename__ = 'p5_followc'

    def __init__(self, issue, num) -> None:
        super().__init__()
        self.issue = issue
        self.num = num


class SportFollowD(SportFollowX):
    __tablename__ = 'p5_followd'

    def __init__(self, issue, num) -> None:
        super().__init__()
        self.issue = issue
        self.num = num


class SportFollowE(SportFollowX):
    __tablename__ = 'p5_followe'

    def __init__(self, issue, num) -> None:
        super().__init__()
        self.issue = issue
        self.num = num


class SportVerifyX(Base):
    __abstract__ = True

    inumabc = Column(String, primary_key=True)
    issue = Column(Integer)
    num = Column(Integer)
    abc = Column(String)
    result = Column(String)
    score = Column(Float)
    num1 = Column(Integer)
    num2 = Column(Integer)
    num3 = Column(Integer)
    num4 = Column(Integer)
    num5 = Column(Integer)
    verify = Column(String)

    @classmethod
    def get_result_score_or_false(cls, issue_num_abc: str):
        with get_session_sport() as sess:
            # sess = get_session_sport()
            data = sess.query(cls).get(issue_num_abc)
            if data:
                return {'label': data.result, 'predicts': data.score}
            else:
                return False

    @classmethod
    def get_model_score(cls, path_json: str) -> dict:
        """
        检查表 verifies 最后5期的数据，得出所有模型的得分，并写入指定的json文件，并返回结果
        base                         s1     1
        verify == 'y' & 不包含开奖号  s2     1
        verify == 'y' & 又包含开奖号  s3     2
        verify == 'n'                       0
        """

        channel = cls.__tablename__[-1]
        s1 = 1
        s2 = 1
        s3 = 2

        sess = get_session_sport()
        # 获取最后5期的期号
        num_all = sess.query(SportNumber5).order_by(SportNumber5.issue).all()
        num_last5 = num_all[-5:]
        issue_begin = num_last5[0].issue

        # 获取最后5期的 verifies 表数据
        data_verifies = sess.query(cls).filter(cls.issue >= issue_begin).all()
        dict_verifies = {x.inumabc: x for x in data_verifies}
        result = dict()

        # 循环模型名称
        for num in range(10):
            for p1 in range(10):
                for p2 in range(10):
                    for p3 in range(10):
                        num_a_b_c = f'{num}{p1}{p2}{p3}'
                        result[num_a_b_c] = s1
                        # 循环最后5期的数据
                        for n in num_last5:
                            i = n.issue
                            nums = {'a': n.num1, 'b': n.num2, 'c': n.num3, 'd': n.num4, 'e': n.num5}.get(channel)
                            i_num_a_b_c = f'{i}{num_a_b_c}'
                            ins = dict_verifies.get(i_num_a_b_c)
                            if ins.verify == 'y':
                                if ins.num == nums:
                                    result[num_a_b_c] = result[num_a_b_c] + s3
                                else:
                                    result[num_a_b_c] = result[num_a_b_c] + s2
        # result
        with open(path_json, 'w') as file_write:
            json.dump(result, file_write)
        print(">>> json result has been written at:", path_json)
        return result

    @classmethod
    def add_score(cls, inumabc, issue, num, abc, result, score):
        """add score

        Args:
            inumabc (str): issue + num + abc
            issue (int): issue
            num (int): num 0 - 9
            abc (str): 000 - 555
            result (str): 'n' or 'y'
            score (float): float result
            channel (str): 'a' or 'b' or 'c' or 'd' or 'e'
        """
        channel = cls.__tablename__[-1]
        if channel not in ['a', 'b', 'c', 'd', 'e']:
            raise Exception(f">>> class: {cls.__class__.__name__}, method: add_score")
        sess = get_session_sport()
        ins = cls(inumabc)
        ins.issue = issue
        ins.num = num
        ins.abc = abc
        ins.result = result
        ins.score = score
        issues_all = SportNumber5.get_issues()
        if issue in issues_all:
            num_channel = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}.get(channel)
            numbers = SportNumber5.get_one(issue)
            ins.num1 = numbers[1]
            ins.num2 = numbers[2]
            ins.num3 = numbers[3]
            ins.num4 = numbers[4]
            ins.num5 = numbers[5]
            if int(num) == numbers[num_channel]:
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
            f">>> {cls.__tablename__}: add score channel:{channel}: inumabc: {inumabc}, issue: {issue}, num: {num}, abc: {abc}, result: {result}, score: {score}, verify: {ins.verify}")

    @classmethod
    def whether_needs_retrained(cls, num_abc: str, last_num: int, min_right: int):
        """检查模型最后几期的准确率，判断是否合格

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
        num = num_abc[0]
        sess = get_session_sport()
        issue_all = SportNumber5.get_issues()
        issue_last = issue_all[-last_num:]
        coll_verify = []
        coll_verify_all = []
        for i_target in issue_last:
            i_num_abc = f'{i_target}{num_abc}'
            # print("i_num_abc: ", i_num_abc)
            v_ins = sess.query(cls).get(i_num_abc)
            coll_verify.append(v_ins.verify)
            if cls.__tablename__ == 'p5_verifya':
                temp_num123 = str(v_ins.num1)
            elif cls.__tablename__ == 'p5_verifyb':
                temp_num123 = str(v_ins.num2)
            elif cls.__tablename__ == 'p5_verifyc':
                temp_num123 = str(v_ins.num3)
            elif cls.__tablename__ == 'p5_verifyd':
                temp_num123 = str(v_ins.num4)
            elif cls.__tablename__ == 'p5_verifye':
                temp_num123 = str(v_ins.num5)
            else:
                raise(">>> ERROR TABLENAME")
            temp_dict = {
                'num123': temp_num123,
                'result': v_ins.result,
                'verify': v_ins.verify
            }
            coll_verify_all.append(temp_dict)
            print(f'model: {num_abc}, result: {temp_dict}')

        # 检查 y 的数量
        if coll_verify.count('y') >= min_right:
            whether_train = False

            # 检查 出号必y
            for one_coll in coll_verify_all:
                if one_coll['num123'] == str(num):
                    if one_coll['verify'] == 'n':
                        whether_train = True

        print(f">>>Table: {cls.__tablename__} whether_needs_retrained: {num_abc} - {whether_train}")
        return whether_train


class SportVerifyA(SportVerifyX):
    __tablename__ = "p5_verifya"

    def __init__(self, inumabc) -> None:
        super().__init__()
        self.inumabc = inumabc


class SportVerifyB(SportVerifyX):
    __tablename__ = "p5_verifyb"

    def __init__(self, inumabc) -> None:
        super().__init__()
        self.inumabc = inumabc


class SportVerifyC(SportVerifyX):
    __tablename__ = "p5_verifyc"

    def __init__(self, inumabc) -> None:
        super().__init__()
        self.inumabc = inumabc


class SportVerifyD(SportVerifyX):
    __tablename__ = "p5_verifyd"

    def __init__(self, inumabc) -> None:
        super().__init__()
        self.inumabc = inumabc


class SportVerifyE(SportVerifyX):
    __tablename__ = "p5_verifye"

    def __init__(self, inumabc) -> None:
        super().__init__()
        self.inumabc = inumabc


class SportFollowN(Base):
    __tablename__ = 'p3_follown'

    issue = Column(Integer, primary_key=True)
    num1 = Column(Integer, nullable=False)
    num2 = Column(Integer, nullable=False)
    num3 = Column(Integer, nullable=False)
    next1 = Column(Integer)
    next2 = Column(Integer)
    next3 = Column(Integer)
    f0 = Column(Integer)
    f1 = Column(Integer)
    f2 = Column(Integer)
    f3 = Column(Integer)
    f4 = Column(Integer)
    f5 = Column(Integer)
    f6 = Column(Integer)
    f7 = Column(Integer)
    f8 = Column(Integer)
    f9 = Column(Integer)
    c0 = Column(Float)
    c1 = Column(Float)
    c2 = Column(Float)
    c3 = Column(Float)
    c4 = Column(Float)
    c5 = Column(Float)
    c6 = Column(Float)
    c7 = Column(Float)
    c8 = Column(Float)
    c9 = Column(Float)

    def __init__(self, issue_and_num123: list) -> None:
        super().__init__()
        self.issue = issue_and_num123[0]
        self.num1 = issue_and_num123[1]
        self.num2 = issue_and_num123[2]
        self.num3 = issue_and_num123[3]

    @classmethod
    def get_follow_09(cls):
        session = get_session_sport()
        data = session.query(cls).all()
        result = {}
        for t in data:
            result[t.issue] = [t.f0, t.f1, t.f2, t.f3, t.f4, t.f5, t.f6, t.f7, t.f8, t.f9]
        return result

    @classmethod
    def get_follow_change_09(cls):
        session = get_session_sport()
        data = session.query(cls).all()
        result = {}
        for t in data:
            result[t.issue] = [t.f0, t.f1, t.f2, t.f3, t.f4, t.f5, t.f6, t.f7, t.f8,
                               t.f9, t.c0, t.c1, t.c2, t.c3, t.c4, t.c5, t.c6, t.c7, t.c8, t.c9]
        return result

    @classmethod
    def get_nums(cls):
        """
        [[issue, num1, num2, num3],...]
        """
        session = get_session_sport()
        data = session.query(cls).all()
        session.close()
        result = [[x.issue, x.num1, x.num2, x.num3] for x in data]
        return result

    @classmethod
    def get_number_and_next(cls):
        """
        [[issue, num1, num2, num3, next1, next2, next3],...]
        """
        session = get_session_sport()
        data = session.query(cls).all()
        session.close()
        result = [[x.issue, x.num1, x.num2, x.num3, x.next1, x.next2, x.next3] for x in data]
        return result

    @classmethod
    def get_all(cls):
        """
        获取所有的数据
        """
        session = get_session_sport()
        data = session.query(cls).all()
        session.close()
        result = [[
            x.issue,
            x.num1,
            x.num2,
            x.num3,
            x.next1,
            x.next2,
            x.next3,
            x.f0,
            x.f1,
            x.f2,
            x.f3,
            x.f4,
            x.f5,
            x.f6,
            x.f7,
            x.f8,
            x.f9,
            x.c0,
            x.c1,
            x.c2,
            x.c3,
            x.c4,
            x.c5,
            x.c6,
            x.c7,
            x.c8,
            x.c9
        ] for x in data]
        return result

    @classmethod
    def get_issues(cls):
        """get issues"""
        session = get_session_sport()
        data = session.query(cls).all()
        session.close()
        result = [x.issue for x in data]
        result.sort()
        return result


class KillSport(Base):
    """
    issue
    name
    issue_name
    save
    v_save
    """
    __tablename__ = 'p3_kill_sports'
    issue_name = Column(String, primary_key=True)  # 期号_专家名

    # attributes
    issue = Column(String)  # 期号
    name = Column(String)  # 专家名
    save = Column(String)  # 组选

    # verify attributes
    v_save = Column(String)  # 组选成绩

    @classmethod
    def set_attributes_except_v(cls, issue_name, issue, name, save):
        """更新数据库内容: 除了验证项目

        Args:
            issue_name(str): issue + _ + name
            issue(str): 期号
            name(str): name
            save(str): save
            path(str): 数据库保存目录
        Returns: None
        """
        # create instance
        session = cls.get_session()
        ins = cls()
        ins.issue_name = issue_name
        ins.issue = issue
        ins.name = name
        ins.save = save
        print(f">>> 合并数据成功, 期号_专家名: {issue_name}, save: {save}")
        session.merge(ins)
        session.commit()
        session.close()

    @classmethod
    def set_attribute(cls, issue_name, attribute_name, data, path):
        """更新数据库的某项

        Args:
            issue_name(str): issue + _ + name, 定位数据表的某条数据
            attribute_name(str): 数据表的列
            data(str): 保存的数据
            path(str): 数据库保存目录
        Returns: None
        """
        # 获取表的字段名称集合
        # total_names = [str(x) for x in cls.metadata.tables[cls.__tablename__].columns]
        # attributes = [x.replace(f'{cls.__tablename__}.', '') for x in total_names]
        session = cls.get_session()
        ins = cls()
        ins.issue_name = issue_name
        # 选择属性
        if attribute_name == 'issue_name':
            pass
        elif attribute_name == 'issue':
            ins.issue = data
        elif attribute_name == 'name':
            ins.name = data
        elif attribute_name == 'save':
            ins.save = data
        elif attribute_name == 'v_save':
            ins.v_save = data
        else:
            raise Exception(f">>> 数据表《{cls._name_}》属性名称错误!!!")
        print(f">>> 合并数据成功: {issue_name}，{attribute_name}: {data}")
        session.merge(ins)
        session.commit()
        session.close()

    @classmethod
    def get_verify(cls):
        return cls.v_save

    @staticmethod
    def get_engine():
        db_engine = get_engine_sport()
        return db_engine

    @staticmethod
    def get_session():
        session = get_session_sport()
        return session


if __name__ == "__main__":
    # generate tables
    # engine = create_engine("mysql+pymysql://root:Wangchenyu2012@localhost:3306/p3")
    # Base.metadata.create_all(engine)
    pass
    # SportVerifyA.add_score('20212993123', 2021299, '3', '235', 'y', 0.56, 'a')
