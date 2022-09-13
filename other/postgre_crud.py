import psycopg2
import sys


class Portfolio(object):
    def __init__(self, param):
        self.id, self.code = param

    def __str__(self):
        return 'Portfolio{%d, %s}' % (self.id, self.code);


def get_portfolio_infos(**kwargs):
    conn = None

    try:
        conn = psycopg2.connect(database="imatrix-cube", host="dev.quantcube.com.cn", port="5432", user="imatrix",
                                password="D74GM8hHTU28y2QU")
        cur = conn.cursor()
        cur.execute("select id, code from portfolio")  # 加载所有组合数据构造字典，无论状态
        all = cur.fetchall()
        all = [Portfolio(x) for x in all]
        cur.close()
        conn.close()

        print(all)

        return all
    except psycopg2.DatabaseError as e:
        print('Error %s' % e)
        sys.exit(1)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    get_portfolio_infos()
