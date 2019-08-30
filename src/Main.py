import csv
import datetime
from src import SaveMenu
import tkinter
from tkinter import *
from PIL import ImageTk
from PIL import Image
import matplotlib.pylab as plt
from src import ChartView

root = Tk()
root.geometry("1280x800+10+10")

flag = False


def hidden_button():
    global flag
    flag = True

img = Image.open('./img/logo1.PNG')
tkimage = ImageTk.PhotoImage(img)
logo = Label(root, image=tkimage, borderwidth=0).place(x=20, y=5)
#Label(root, text=u"통계자료").place(x=20, y=5) ********************* SIZE 조절
Button(root, text=u"월별매출", bg='lightblue', command=lambda: ChartView.p_chart(), height='5', width='15').place(x=530, y=45)
Button(root, text=u"지불방식", bg='lightblue', command=lambda: ChartView.p_pie(), height='5', width='15').place(x=660, y=45)

# 피자, 사이드디시, 음료, 피클&소스 서브메뉴를 db에 가져와서 넣는다.


category = ['C0102','C0201','C0202','C0203']

sel_List=[]
for j,k in enumerate(category):
    menu_list = SaveMenu.select_menu('pythondb', k)

    sel = {1: (u"선택하지 않음", 0)}
    for i, m in enumerate(menu_list):
        mp = int(m[1].split('/')[0])
        sel[i+2] = (m[0],mp)
    sel_List.append(sel)

    # 서브메뉴
sel_menu = {u"피자": sel_List[0], u"사이드디시": sel_List[1], u"음료": sel_List[2], u"피클&소스": sel_List[3]}

    # 선택하지 않았을 때 0값
final_selected = {1: (u"선택하지 않음", 0), 2: (u"선택하지 않음", 0), 3: (u"선택하지 않음", 0), 4: (u"선택하지 않음", 0)}

    # 주메뉴
menu_name = {1: u"피자", 2: u"사이드디시", 3: u"음료", 4: u"피클&소스"}


class menu:

    def __init__(self, number):
        self.number = number
        self.this_menu_name = menu_name.get(number)
        self.var = IntVar()
        self.var.set(1)

    # 선택
    def selected(self):
        temp = sel_menu.get(self.this_menu_name).get(self.var.get())[0]
        menu_1.destroy()
        Label(root, text=u"선택된 메뉴 :                           ", background="seashell3").place(x=1000, y=170 + 170 * (
                    self.number - 1))
        Label(root, text=u"선택된 메뉴 : " + temp, background="seashell3").place(x=1000, y=170 + 170 * (self.number - 1))
        global final_selected
        final_selected[self.number] = sel_menu.get(self.this_menu_name).get(self.var.get())  # 최종선택

    # 서브 메뉴
    def pop_menu(self):
        global menu_1
        menu_1 = Toplevel(root)
        menu_1.title(self.this_menu_name)
        y = 170 * self.number + 25

        cnt = len(sel_List[self.number-1])*25
        menu_1.geometry("250x%d+110+%d" % (cnt, y))
        for i in sel_menu.get(self.this_menu_name):
            Radiobutton(menu_1, text=sel_menu.get(self.this_menu_name).get(i)[0:2], variable=self.var, value=i,
                        indicatoron=0, relief=RAISED, command=self.selected).pack(fill=X)


# 매출 관리, db에서 가져온 판매일자 x축, 매출 y축
def sales_management():
    plt.title("sales_management")
    plt.plot([10, 20, 30, 40], [1, 4, 9, 16])
    plt.show()


# 주메뉴
def make_menu(number):
    global this_menu
    this_menu = menu(number)
    this_menu.pop_menu()  # 서브메뉴 호출


# 주문
def order():
    global v
    global flag
    ordering = Toplevel(root)
    cost = 0
    receipt = []

    for i in final_selected:
        menu_name1 = final_selected[i][0]
        menu_price1 = final_selected[i][1]
        menu_sel = [menu_name1, menu_price1]
        receipt.append(menu_sel)
        cost += final_selected[i][1]
        print(menu_name1, menu_price1)
    receipt.append(cost)
    now = datetime.datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H-%M-%S')
    print(type(nowDatetime))  # 2015-04-19 12:11:32
    f = open('./receipt/{0}.csv'.format(nowDatetime), 'wt', encoding='utf-8', newline='')
    wr = csv.writer(f)
    wr.writerow(receipt)
    print(receipt)
    f.close()
    for i in menu_name:
        Label(ordering, text=menu_name.get(i) + ':').grid(row=i, column=1)
        Label(ordering, text=final_selected.get(i)[0]).grid(row=i, column=3)
        Label(ordering, text=final_selected.get(i)[1]).grid(row=i, column=5)

    Label(ordering, text=u"계산하실 금액은 " + str(cost) + u"원 입니다.").grid(row=7, column=3)
    Button(ordering, text=u"결제", font='Ariel 9 bold', command=lambda: pop_sales(cost)).grid(row=7, column=5)

# 결제
def pop_sales(cost):
    sales = Toplevel()
    sales.title("결제")
    sales.geometry("150x150+1000+20")
    Label(sales, text="결제되었습니다.").place(x=10, y=10)


# 메인 화면을 띄운다.
mymenu = menu(root)

# 4가지 주메뉴 버튼을 생성 후 make_menu() 호출
Button(root, text=u"피자", command=lambda: make_menu(1), height='5', width='15').place(x=10, y=170)
Button(root, text=u"사이드디시", command=lambda: make_menu(2), height='5', width='15').place(x=10, y=340)
Button(root, text=u"음료", command=lambda: make_menu(3), height='5', width='15').place(x=10, y=510)
Button(root, text=u"피클&소스", command=lambda: make_menu(4), height='5', width='15').place(x=10, y=680)

Button(root, text=u"주문하기", bg='lightgreen', font='Ariel 9 bold', command=order, height='5', width='15').place(x=800, y=45)

# 주메뉴 이미지 붙이기
images = [(1, "./img/pizza.png"), (2, "./img/side_dish.png"), (3, "./img/beverage.png"), (4, "./img/pickle&sauce.png")]
for i, image in images:
    img = Image.open(image)
    this_image = ImageTk.PhotoImage(img)
    mylabel = Label(image=this_image)
    mylabel.image = this_image
    mylabel.place(x=150, y=140 + (i - 1) * 170)

v = StringVar()

root.config(width=600, height=800, background="white")

root.title(u"Welcome to Dominsok's")
root.mainloop()