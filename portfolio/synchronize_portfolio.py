#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from sqlalchemy import Column, Integer, String, JSON, DATETIME, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base1 = declarative_base()
Base2 = declarative_base()


class MPortfolio(Base1):
    __tablename__ = 'portfolio'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    integral = Column(Integer)
    expired_time = Column(Integer)
    status = Column(Integer)
    create_time = Column(DATETIME)
    update_time = Column(DATETIME)

    def __repr__(self):
        return "<MPortfolio(id='%s', name='%s', integral='%s', expired_time='%s', " \
               "status='%s', create_time='%s', update_time='%s')>" \
               % (self.id, self.name, self.integral, self.expired_time, self.status,
                  self.create_time.strftime("%Y-%m-%d %H:%M:%S"), self.update_time.strftime("%Y-%m-%d %H:%M:%S"))


class PPortfolio(Base2):
    __tablename__ = 'portfolio'

    id = Column(Integer, primary_key=True)
    code = Column(String(20))
    name = Column(String(50))
    description = Column(JSON)
    create_time = Column(DATETIME)
    modified_time = Column(DATETIME)
    status = Column(Boolean)
    brief = Column(String(300))
    benchmark_id = Column(Integer)

    def __repr__(self):
        return "<PPortfolio(id='%s', code='%s', name='%s', description='%s', create_time='%s', modified_time='%s', " \
               "status='%s', brief='%s', benchmark_id='%s')>" \
               % (self.id, self.code, self.name, self.description, self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                  self.modified_time.strftime("%Y-%m-%d %H:%M:%S"), self.status, self.brief, self.benchmark_id)


def read_postgre_portfolio():
    engine = create_engine('postgresql+psycopg2://url:port/dataBase', echo=True, client_encoding='utf8')

    db_session = sessionmaker(bind=engine)
    session = db_session()
    pportfolios = []
    for s in session.query(PPortfolio):
        pportfolios.append(s)
    session.close()
    return pportfolios


def clear_mysql_portfolio():
    engine = create_engine('mysql+mysqlconnector://user:password@url:port/database?charset=utf8')
    db_session = sessionmaker(bind=engine)
    session = db_session()
    # 删user_portfolio外键
    session.execute(r'''ALTER TABLE quant_cube.user_portfolio DROP FOREIGN KEY user_portfolio_portfolio_fk;''')
    # 清空portfolio
    session.query(MPortfolio).delete()
    session.commit()


def append_to_mysql(args):
    engine = create_engine('mysql+mysqlconnector://user:password@url:port/database?charset=utf8')
    db_session = sessionmaker(bind=engine)
    session = db_session()

    # 写MySQL portfolio
    for port in args:
        session.add(port)

    session.commit()
    session.close()


def create_foreign_key():
    engine = create_engine('mysql+mysqlconnector://user:password@url:port/database?charset=utf8')
    db_session = sessionmaker(bind=engine)
    session = db_session()

    # 建MySQL user_portfolio --> portfolio 外键
    session.execute(r'''
        ALTER TABLE user_portfolio
        ADD CONSTRAINT user_portfolio_portfolio_FK
        FOREIGN KEY (portfolio_id) REFERENCES portfolio (id);
    ''')

    session.commit()
    session.close()


if __name__ == "__main__":

    # 查Postgre portfolio
    pportfolios = read_postgre_portfolio()

    port_list = []
    for pp in pportfolios:
        mp = MPortfolio(id=pp.id, name=pp.name, integral=20, expired_time=7, status=(1 if pp.status else -1),
                        create_time=pp.create_time, update_time=pp.modified_time)
        port_list.append(mp)

    # 删MySQL portfolio
    clear_mysql_portfolio()
    print('删数据成功')

    # 写数据到MySQL
    append_to_mysql(port_list)
    print('写数据成功')

    # 建外键
    create_foreign_key()

    print('-----------------------------------------Task Finished-----------------------------------------------------')
