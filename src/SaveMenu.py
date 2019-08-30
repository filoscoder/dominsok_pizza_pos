#-*- coding:utf-8 -*-
import MySQLdb

def insertdata(db,data):
    print(data.m_name, data.m_price, data.c_id, data.m_quantity, data.m_img, data.m_desc)
    conn = MySQLdb.connect(host='192.168.0.170',user='scott',passwd='tiger',db=db, charset="utf8")
    #conn.set_character_set("utf-8")
    cur = conn.cursor()
    sql = "INSERT INTO menu(m_name,m_price,c_id,m_quantity,m_img,m_desc) VALUES(%s,%s,%s,%s,%s,%s)"
    m =(data.m_name, data.m_price, data.c_id, data.m_quantity, data.m_img, data.m_desc)
    cur.execute(sql,m)
    conn.commit()
    conn.close()

#print(type(menu))
#insertdata('pythondb',["아",1,"c0201",2,"아","아"])

def select_menu(db,c_id):
    conn = MySQLdb.connect(host='192.168.0.170', user='scott', passwd='tiger', db=db, charset="utf8")
    cur = conn.cursor()
    sql = "SELECT m_name,m_price FROM menu WHERE c_id='{}' ".format(c_id)
    cur.execute(sql)
    a = cur.fetchall()
    print(a)
    for row in a :
        print(row)
    conn.commit()
    conn.close()
    return a
#select_menu('pythondb')