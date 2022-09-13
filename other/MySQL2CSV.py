#!/usr/bin/python
# -*- coding: UTF-8 -*-
# This is a script that writes data from MySQL to csv

import csv
import mysql.connector


def main():
    # 连接数据库
    conn = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123456',
        db='test',
    )
    cur = conn.cursor()
    print('已连接MySQL数据库')

    # 以写的方式打开 csv 文件并将内容写入到w
    f = open("//home//cx4gxf//Documents//data.csv", 'w')
    write_file = csv.writer(f)

    # 从 student 表里面读出数据，写入到 csv 文件里
    cur.execute("select * from student")
    while True:
        row = cur.fetchone()  # 获取下一个查询结果集为一个对象
        if not row:
            break
        write_file.writerow(row)  # csv模块方法一行一行写入
    f.close()
    print('已写入数据到CSV文件')

    # 关闭连接
    if cur:
        cur.close()
    if conn:
        conn.close()


if __name__ == '__main__':
    main()
