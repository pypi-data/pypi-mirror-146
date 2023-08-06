from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_sqlite_session.tools import get_engine, get_session

Base = declarative_base()


class GroupTen(Base):
    """ table group10 """
    __tablename__ = 'group10'
    channel_group_issue = Column(String, primary_key=True)
    channel = Column(String)
    group = Column(String)
    issue = Column(Integer)
    num10 = Column(String)

    def __init__(self, channel, group, issue, num10):
        self.channel_group_issue = f'{channel}_{group}_{issue}'
        self.channel = channel
        self.group = group
        self.issue = issue
        self.num10 = num10

    @classmethod
    def merge_one(cls, channel, group, issue, num10):
        """get issues[list]"""
        session = get_session()
        ins = cls(channel, group, issue, num10)
        session.merge(ins)
        session.commit()
        session.close()
        print(f">>>>>> merge one: {channel} - {group} - {issue} - {num10}")


class Power(Base):
    """ table powers """
    __tablename__ = 'powers'
    channel_power_issue = Column(String, primary_key=True)
    channel = Column(String)
    power = Column(String)
    issue = Column(Integer)
    num10 = Column(String)

    def __init__(self, channel, power, issue, num10):
        self.channel_power_issue = f'{channel}_{power}_{issue}'
        self.channel = channel
        self.power = power
        self.issue = issue
        self.num10 = num10

    @classmethod
    def merge_one(cls, channel, power, issue, num10):
        """get issues[list]"""
        session = get_session()
        ins = cls(channel, power, issue, num10)
        session.merge(ins)
        session.commit()
        session.close()
        print(f">>>>>> merge one: {channel} - {power} - {issue} - {num10}")


class Power3(Base):
    """ table powers """
    __tablename__ = 'power3'
    channel_power_issue = Column(String, primary_key=True)
    channel = Column(String)
    power = Column(String)
    issue = Column(Integer)
    num10 = Column(String)

    def __init__(self, channel, power, issue, num10):
        self.channel_power_issue = f'{channel}_{power}_{issue}'
        self.channel = channel
        self.power = power
        self.issue = issue
        self.num10 = num10

    @classmethod
    def merge_one(cls, channel, power, issue, num10):
        """get issues[list]"""
        session = get_session()
        ins = cls(channel, power, issue, num10)
        session.merge(ins)
        session.commit()
        session.close()
        print(f">>>>>> merge one: {channel} - {power} - {issue} - {num10}")

class Power5(Base):
    """ table powers """
    __tablename__ = 'power5'
    channel_power_issue = Column(String, primary_key=True)
    channel = Column(String)
    power = Column(String)
    issue = Column(Integer)
    num10 = Column(String)

    def __init__(self, channel, power, issue, num10):
        self.channel_power_issue = f'{channel}_{power}_{issue}'
        self.channel = channel
        self.power = power
        self.issue = issue
        self.num10 = num10

    @classmethod
    def merge_one(cls, channel, power, issue, num10):
        """get issues[list]"""
        session = get_session()
        ins = cls(channel, power, issue, num10)
        session.merge(ins)
        session.commit()
        session.close()
        print(f">>>>>> merge one: {channel} - {power} - {issue} - {num10}")


class Group(Base):
    """ table groups history"""
    __tablename__ = 'groups'
    c_i_r_s = Column(String, primary_key=True)
    channel = Column(String)
    issue = Column(Integer)
    range = Column(Integer)
    spin = Column(Integer)
    result_index = Column(String)
    result_count = Column(String)
    result_index_except_last = Column(String)
    result_count_except_last = Column(String)

    def __init__(self, channel, issue, range, spin):
        self.c_i_r_s = f'{channel}_{issue}_{range}_{spin}'
        self.channel = channel
        self.issue = issue
        self.range = range
        self.spin = spin

    @classmethod
    def merge_one(cls, channel, issue, range, spin, result_index, result_count):
        """get issues[list]"""
        session = get_session()
        ins = cls(channel, issue, range, spin)
        ins.result_index = result_index
        ins.result_count = result_count
        temp_index = result_index.split('-')[:-1]
        temp_count = result_count.split('-')[:-1]
        ins.result_index_except_last = ''.join([x for sub in temp_index for x in sub])
        ins.result_count_except_last = ''.join([x for sub in temp_count for x in sub])
        session.merge(ins)
        session.commit()
        session.close()
        print(
            f">>>>>> merge one: {channel} - {issue} - {range} - {spin} - {result_index} - {result_count} - {ins.result_index_except_last} - {ins.result_count_except_last}")


if __name__ == "__main__":
    # generate tables
    engine = get_engine()
    Base.metadata.create_all(engine)
    pass
