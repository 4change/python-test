#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# This is a script that writes data from CSV to MySQL

import csv
import mysql.connector


def main():
    # 连接数据库
    conn = conn = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123456',
        db='test',
    )
    cur = conn.cursor()

    # 创建数据表
    cur.execute("DROP TABLE IF EXISTS `student`")
    conn.commit()
    create_db = """create table student(
                        id int ,
                        name varchar(10),
                        sex varchar(10),
                        age int
                    )
                   ENGINE=InnoDB DEFAULT CHARSET=utf8"""
    cur.execute(create_db)  # 执行创建表语句
    conn.commit()
    print('创建student表完成')

    # 把 CSV 读到数组里
    f = open("//home//cx4gxf//Documents//data.csv", 'r')
    student = []
    for row in csv.reader(f):
        student.append(row)

    print(student)
    f.close()
    print('读入CSV数据完成')

    # 还可以替换成为with
    # student = []
    # with open("/var/python_code/input_CSV_file.csv", 'r') as f:
    #     for row in csv.reader(f):
    #         student.append(row)

    # 执行 insert
    insert_db = "insert into student(id, name, sex, age) values(%s, %s, %s, %s)"
    cur.executemany(insert_db, student)  # 批量高效插入
    conn.commit()
    print('写入数据库完成')

    # 关闭连接
    if cur:
        cur.close()
    if conn:
        conn.close()


if __name__ == '__main__':
    main()
