# db 연결 - mysql connector
import mysql.connector
import pygal


def payment_select1():
    # db 연결
    conn = mysql.connector.connect(host='192.168.0.170', user='scott', passwd='tiger', db='pythondb')
    cur1 = conn.cursor()

    sql1 = "SELECT c.month, sum(c.p_total) sum " \
           "FROM (SELECT Month(b.o_time) month , a.p_total p_total FROM payment as a JOIN orders as b ON a.o_no=b.o_no)c " \
           "GROUP BY c.MONTH"
    cur1.execute(sql1)

    sales = []
    rows1 = cur1.fetchall()
    for row in rows1:
        print(row[0], row[1])
        sales.append([str(row[0]), row[1]])

    return sales

    conn.commit()
    conn.close()
    

def payment_select2():
    # db 연결
    conn = mysql.connector.connect(host='192.168.0.170', user='scott', passwd='tiger', db='pythondb')
    cur2 = conn.cursor()

    sql2 = "SELECT * FROM payment"
    cur2.execute(sql2)

    method = []

    rows2 = cur2.fetchall()
    for row in rows2:
        print(row[0], row[1], row[2])
        method.append([row[0], row[1], row[2], str(row[3])])
    return method

    conn.commit()
    conn.close()


def p_chart():
    print('p_chart start')
    payment_chart = pygal.Bar(height=300, print_labels=True, print_values=True, pretty_print=True)

    sales = payment_select1()
    payment_chart.title = "월별 매출액"

    for i in sales:
        payment_chart.add(i[0], [{'value': i[1], 'label': '%s' % i[0]+'월'}])
        print(i[0], i[1])
    payment_chart.render_in_browser()


def p_pie():
    payment_donut = pygal.Pie(height=300, inner_radius=.3, print_values=True, print_labels=True, half_pie=True)

    method = payment_select2()
    payment_donut.title = '지불방식별 매출액'

    card = 0
    cash = 0
    for i in method:
        if i[3] == 'card':
            card += i[2]
        elif i[3] == 'cash':
            cash += i[2]

    payment_donut.add('card', [{'value': card, 'label': 'card'}])
    payment_donut.add('cash', [{'value': cash, 'label': 'cash'}])

    payment_donut.render_in_browser()
