import sys
from PyQt6 import QtWidgets,QtGui
from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget,QLineEdit
from PyQt6.uic import loadUi
import sqlite3
import datetime

class Login(QMainWindow):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.createaccbutton.clicked.connect(self.gotocreate)
        self.loginbutton.clicked.connect(self.gotomenu)
        self.forgotbutton.clicked.connect(self.gotoforget)

    def gotocreate(self):
        createacc = CreateAcc()
        widget.addWidget(createacc)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotomenu(self):
        username = self.username.text()
        password = self.password.text()
        conn = sqlite3.connect('accounting.db')
        cursor = conn.cursor()
        sqlite_select_query = """SELECT * from users"""
        cursor.execute(sqlite_select_query)
        userlist = cursor.fetchall()
        c = 0
        for data in userlist:
            if data[3] == username and data[4] == password:
                print('login successful.')
                info = (data[3], data[4])
                sql = ''' INSERT INTO enteries(username, pass)
                                    VALUES(?,?) '''
                cur = conn.cursor()
                cur.execute(sql, info)
                conn.commit()
                menu = Menu()
                widget.addWidget(menu)
                widget.setCurrentIndex(widget.currentIndex() + 1)
                break
            else:
                c += 1
        if c == len(userlist):
            print('username or password incorrect, try again.')
            win = Login()
            widget.addWidget(win)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoforget(self):
        acc = Forgetpass()
        widget.addWidget(acc)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CreateAcc(QMainWindow):
    def __init__(self):
        super(CreateAcc,self).__init__()
        loadUi("createacc.ui",self)
        self.signupbutton.clicked.connect(self.signup)

    def signup(self):
        c = 0
        conn = sqlite3.connect('accounting.db')
        name = self.name.text()
        last_name = self.familyname.text()
        number = self.phone.text()
        username = self.username.text()
        password = self.password.text()
        passrepeat = self.passrepeat.text()
        city = self.city.text()
        email = self.email.text()
        birth = self.birth.text()
        color = self.favcol.text()
        if not name.isalpha():
            print("name should only contain english letters.try again: ")
            c += 1
        if not last_name.isalpha():
            print("last name should only contain english letters.try again: ")
            c += 1
        if not number.isnumeric():
            print("phone number should contain only numbers. try again: ")
            c += 1
        elif not number.startswith("09"):
            print("phone number should start with 09. try again: ")
            c += 1
        elif len(number) != 11:
            print("phone number should have 11 digits. try again: ")
            c += 1
        a = 0
        b = 0
        d = 0
        e = 0
        symbols = '!@#$%^&*()'
        for char in password:
            if char.isdigit():
                a += 1
            elif char.isupper():
                b += 1
            elif char.islower():
                d += 1
            elif char in symbols:
                e += 1
        if a < 1:
            print("password should have at least one number.")
            c += 1
        if b < 1:
            print("password should have at least one capital letter.")
            c += 1
        if d < 1:
            print("password should have at least one lowercase letter.")
            c += 1
        if e < 1:
            print("password should have at least one special character.")
            c += 1
        if len(password) < 6:
            print("password should be at least 6 characters.")
            c += 1
        if password != passrepeat:
            print("password and your input didn't match. try again:")
            c += 1
        s = 0
        if '@' not in email:
            s += 1
        elif not email.endswith('gmail.com') and not email.endswith('yahoo.com'):
            s += 1
        try:
            e1 = email.split("@")
            for i in e1[0]:
                if i in symbols:
                    s += 1
        except Exception:
            s += 1
        if s > 0:
            print("email is not the right format.try again.")
            c += 1
        l31 = [1, 3, 5, 7, 8, 10, 12]
        l30 = [4, 6, 9, 11]
        b1 = birth.split('/')
        if 2005 < int(b1[0]) < 1920:
            print("birth year should be at least 1920 and at most 2005. try again: ")
            c += 1
        elif int(b1[1]) in l31 and int(b1[2]) > 31:
            print("birth day is incorrect. try again: ")
            c += 1
        elif int(b1[1]) in l30 and int(b1[2]) > 30:
            print("birth day is incorrect. try again: ")
            c += 1
        elif int(b1[1]) == 2 and int(b1[2]) > 29:
            print("birth day is incorrect. try again: ")
            c += 1
        if c == 0:
            print("successful")
            win = Login()
            widget.addWidget(win)
            widget.setCurrentIndex(widget.currentIndex() + 1)
            user = (name, last_name, number, username, password, city, email, birth, color)
            sql = ''' INSERT INTO users(name,last_name,number,username,password,city,email,birth,color)
                              VALUES(?,?,?,?,?,?,?,?,?) '''
            cur = conn.cursor()
            cur.execute(sql, user)
            conn.commit()
        else:
            win = CreateAcc()
            widget.addWidget(win)
            widget.setCurrentIndex(widget.currentIndex() + 1)


class Menu(QMainWindow):
    def __init__(self):
        super(Menu,self).__init__()
        loadUi("menubar.ui",self)
        self.revenue.clicked.connect(self.getrevenue)
        self.expense.clicked.connect(self.getexpense)
        self.categories.clicked.connect(self.gotocategory)
        self.search.clicked.connect(self.gotosearch)
        self.debriefing.clicked.connect(self.gotodebrief)
        self.setting.clicked.connect(self.gotosetting)
        self.exitbutton.clicked.connect(self.exitprogram)

    def exitprogram(self):
        submit = Login()
        widget.addWidget(submit)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotosetting(self):
        submit = Setting()
        widget.addWidget(submit)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotodebrief(self):
        submit = Debriefing()
        widget.addWidget(submit)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def getexpense(self):
        submit = Expense()
        widget.addWidget(submit)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def getrevenue(self):
        submit = Revenue()
        widget.addWidget(submit)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotocategory(self):
        submit = Category()
        widget.addWidget(submit)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotosearch(self):
        submit = Search()
        widget.addWidget(submit)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Revenue(QMainWindow):
    def __init__(self):
        super(Revenue,self).__init__()
        loadUi("revenue.ui",self)
        self.submit.clicked.connect(self.revenue_record)
        self.back.clicked.connect(self.backtomenu)

    def backtomenu(self):
        submit = Menu()
        widget.addWidget(submit)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def revenue_record(self):
        c = 0
        amount = self.amount.text()
        date = self.date.text()
        source = self.source.text()
        typee = self.type.text()
        description = self.description.text()
        conn = sqlite3.connect('accounting.db')
        cur = conn.cursor()
        cur.execute("select * from categories")
        l = cur.fetchall()
        last = l[-1]
        username = last[0]
        if not amount.isnumeric() or int(amount) < 0:
            print("amount is not in the right form try again: ")
            c += 1
        l31 = [1, 3, 5, 7, 8, 10, 12]
        l30 = [4, 6, 9, 11]
        d1 = date.split('/')
        if int(d1[1]) in l31 and int(d1[2]) > 31:
            print("date is incorrect. try again: ")
            c += 1
        elif int(d1[1]) in l30 and int(d1[2]) > 30:
            print("date is incorrect. try again: ")
            c += 1
        elif int(d1[1]) == 2 and int(d1[2]) > 29:
            print("date is incorrect. try again: ")
            c += 1
        d2 = [*description]
        if len(d2) > 100:
            print('description should have at most 100 characters. try again')
            c += 1
        if c == 0:
            data = (username, amount, date, source, description, typee)
            sql = ''' INSERT INTO Revenue_record(username,amount,date,source,description,type)
                                VALUES(?,?,?,?,?,?) '''
            print("Revenue record finished successfully")
            cur = conn.cursor()
            cur.execute(sql, data)
            conn.commit()
            menu = Menu()
            widget.addWidget(menu)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            sub = Revenue()
            widget.addWidget(sub)
            widget.setCurrentIndex(widget.currentIndex() + 1)


class Expense(QMainWindow):
    def __init__(self):
        super(Expense,self).__init__()
        loadUi("expense.ui",self)
        self.confirm.clicked.connect(self.expense_record)
        self.back.clicked.connect(self.backtomenu)

    def backtomenu(self):
        submit = Menu()
        widget.addWidget(submit)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def expense_record(self):
        c = 0
        amount = self.amount.text()
        date = self.date.text()
        source = self.source.text()
        typee = self.type.text()
        description = self.description.text()
        conn = sqlite3.connect('accounting.db')
        cur = conn.cursor()
        cur.execute("select * from categories")
        l = cur.fetchall()
        last = l[-1]
        username = last[0]
        if not amount.isnumeric() or int(amount) < 0:
            print("amount is not in the right form try again: ")
            c += 1
        l31 = [1, 3, 5, 7, 8, 10, 12]
        l30 = [4, 6, 9, 11]
        d1 = date.split('/')
        if int(d1[1]) in l31 and int(d1[2]) > 31:
            print("date is incorrect. try again: ")
            c += 1
        elif int(d1[1]) in l30 and int(d1[2]) > 30:
            print("date is incorrect. try again: ")
            c += 1
        elif int(d1[1]) == 2 and int(d1[2]) > 29:
            print("date is incorrect. try again: ")
            c += 1
        d2 = [*description]
        if len(d2) > 100:
            print('description should have at most 100 characters. try again')
            c += 1
        if c == 0:
            data = (username, amount, date, source, description, typee)
            sql = ''' INSERT INTO Expense_record(username,amount,date,source,description,type)
                                VALUES(?,?,?,?,?,?) '''
            print("Expense record finished successfully")
            cur = conn.cursor()
            cur.execute(sql, data)
            conn.commit()
            menu = Menu()
            widget.addWidget(menu)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            sub = Expense()
            widget.addWidget(sub)
            widget.setCurrentIndex(widget.currentIndex() + 1)


class Forgetpass(QMainWindow):
    def __init__(self):
        super(Forgetpass,self).__init__()
        loadUi("forgetpass.ui",self)
        self.confirm.clicked.connect(self.login)

    def login(self):
        user = self.user.text()
        color = self.color.text()
        conn = sqlite3.connect('accounting.db')
        cursor = conn.cursor()
        sqlite_select_query = """SELECT * from users"""
        cursor.execute(sqlite_select_query)
        userlist = cursor.fetchall()
        for data in userlist:
            if data[3] == user or data[6] == user:
                if color == data[8]:
                    print('your password is', data[4])
                    log = Login()
                    widget.addWidget(log)
                    widget.setCurrentIndex(widget.currentIndex() + 1)
                    break


class Category(QMainWindow):
    def __init__(self):
        super(Category,self).__init__()
        loadUi("category1.ui",self)
        self.showcat.clicked.connect(self.gotoshow)
        self.addnew.clicked.connect(self.gotoadd)

    def gotoshow(self):
        cat = Showdb()
        widget.addWidget(cat)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotoadd(self):
        new = Addcat()
        widget.addWidget(new)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Showdb(QMainWindow):
    def __init__(self):
        super(Showdb,self).__init__()
        loadUi("showcat.ui",self)
        db = sqlite3.connect("accounting.db")
        cursor = db.cursor()
        command1 = '''SELECT * from categories'''
        res1 = cursor.execute(command1)
        reslist = res1.fetchall()
        command2 = '''SELECT * from enteries'''
        res2 = cursor.execute(command2)
        info = res2.fetchall()
        data = info[-1]
        name = data[0]
        categories = ''
        for i in reslist:
            if i[0] == name:
                categories = categories + i[1] + '\n'
        self.show.setText(categories)
        self.backbutton.clicked.connect(self.backtomenu)

    def backtomenu(self):
        menu = Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Addcat(QMainWindow):
    def __init__(self):
        super(Addcat, self).__init__()
        loadUi("addcat.ui", self)
        self.submitcat.clicked.connect(self.addcategory)

    def addcategory(self):
        conn = sqlite3.connect('accounting.db')
        cur = conn.cursor()
        cur.execute('SELECT * from categories')
        clist = cur.fetchall()
        cur.execute('SELECT * from enteries')
        info = cur.fetchall()
        data = info[-1]
        username = data[0]
        c = 0
        category_name = self.catname.text()
        item = (username, category_name)
        if len(category_name) > 15 or len(category_name) == 0:
            print("category name should have at most 15 characters and can't be empty.")
            c += 1
        a = 0
        for char in category_name:
            if char.isdigit():
                a += 1
            elif char.isalpha():
                a += 1
        if a != len(category_name):
            print("category name should only contain number or english alphabet.")
        if item in clist:
            print('category already exists.')
            c += 1
        if c == 0:
            sql = ''' INSERT INTO categories(username, category_name)
                                VALUES(?,?) '''
            cur = conn.cursor()
            cur.execute(sql, item)
            conn.commit()
            print("add successful")
            back = Menu()
            widget.addWidget(back)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            print("try again.")
            again = Addcat()
            widget.addWidget(again)
            widget.setCurrentIndex(widget.currentIndex() + 1)


class Search(QMainWindow):
    def __init__(self):
        super(Search, self).__init__()
        loadUi("search.ui", self)
        conn = sqlite3.connect('accounting.db')
        cursor = conn.cursor()
        sqlite_select_query1 = """SELECT * from Revenue_record"""
        cursor.execute(sqlite_select_query1)
        self.data1 = cursor.fetchall()
        sqlite_select_query2 = """SELECT * from Expense_record"""
        cursor.execute(sqlite_select_query2)
        self.data2 = cursor.fetchall()
        cursor.execute('SELECT * from enteries')
        info = cursor.fetchall()
        data = info[-1]
        self.username = data[0]
        self.withoutfilter.clicked.connect(self.searchwithoutfilter)
        self.withfilter.clicked.connect(self.searchwithfilter)
        self.backb.clicked.connect(self.backtomenu)

    def searchwithfilter(self):
        date = {"Revenue": [], "Expense": []}
        day = self.date.text()
        for i in self.data1:
            if i[0] == self.username and day in i[2]:
                date["Revenue"].append(i[1::])
        for i in self.data2:
            if i[0] == self.username and day in i[2]:
                date["Expense"].append(i[1::])
        number_range = self.range.text()
        if number_range != "-":
            number_range = number_range.split(" ")
            for i in date["Revenue"]:
                if not int(number_range[0]) < int(i[0]) < int(number_range[1]):
                    date["Revenue"].remove(i)
            for i in date["Expense"]:
                if not int(number_range[0]) < int(i[0]) < int(number_range[1]):
                    date["Expense"].remove(i)
        t1 = 'revenue:\n'
        for i in date["Revenue"]:
            t1 += str(i) + '\n'
        t2 = 'expense:\n'
        for i in date["Expense"]:
            t2 += str(i) + '\n'
        just = self.justone.text()
        if just == '1':
            self.result.setText(t1)
        elif just == '2':
            self.result.setText(t2)
        else:
            self.result.setText(t1+t2)

    def searchwithoutfilter(self):
        rev = "Revenue:\n"
        search = self.searchnofilter.text()
        for i in self.data1:
            if i[0] == self.username:
                for j in i[1::]:
                    if search in j:
                        rev += str(i[1::]) + '\n'
        exp = "expense:\n"
        for i in self.data2:
            if i[0] == self.username:
                for j in i[1::]:
                    if search in j:
                        exp += str(i[1::]) + '\n'
        result = rev + exp
        self.result.setText(result)

    def backtomenu(self):
        menu = Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Debriefing(QMainWindow):
    def __init__(self):
        super(Debriefing, self).__init__()
        loadUi("debriefing.ui", self)
        conn = sqlite3.connect('accounting.db')
        cursor = conn.cursor()
        sqlite_select_query1 = """SELECT * from Revenue_record"""
        cursor.execute(sqlite_select_query1)
        self.data1 = cursor.fetchall()
        sqlite_select_query2 = """SELECT * from Expense_record"""
        cursor.execute(sqlite_select_query2)
        self.data2 = cursor.fetchall()
        sqlite_select_query3 = """SELECT * from categories"""
        cursor.execute(sqlite_select_query3)
        self.data3 = cursor.fetchall()
        sqlite_select_query4 = """SELECT * from enteries"""
        cursor.execute(sqlite_select_query4)
        info = cursor.fetchall()
        data = info[-1]
        self.username = data[0]
        self.today.clicked.connect(self.todaydebrief)
        self.threedays.clicked.connect(self.threedaysdebrief)
        self.pastweek.clicked.connect(self.weekdebrief)
        self.specificdate.clicked.connect(self.specificdatedebrief)
        self.specificmonth.clicked.connect(self.specificmonthdebrief)
        self.specificmoney.clicked.connect(self.specificmoneydebrief)
        self.specificcat.clicked.connect(self.specificcatdebrief)
        self.specifictype.clicked.connect(self.specifictypedebrief)
        self.back.clicked.connect(self.getback)

    def getback(self):
        menu = Menu()
        widget.addWidget(menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def specifictypedebrief(self):
        revenue = 0
        total_revenue = 0
        expense = 0
        total_expense = 0
        n1 = 0
        n2 = 0
        typ = self.typ.text()
        for i in self.data1:
            if self.username == i[0]:
                total_revenue += int(i[1])
                n1 += 1
                if typ == i[5]:
                    revenue += int(i[1])
        for i in self.data2:
            if self.username == i[0]:
                total_expense += int(i[1])
                n2 += 1
                if typ == i[5]:
                    expense += int(i[1])
        t1 = "\ntotal revenue:" + str(revenue) + "\ntotal expense:" + str(expense)
        t2 = "\nratio to overall revenue" + str(
            round(revenue / total_revenue * 100, 2)) + "\nratio to overall expense" + str(
            round(expense / total_expense * 100, 2))
        t3 = "\nratio to other revenues" + str(
            round(revenue / (total_revenue / n1) * 100, 2)) + "\nratio to other revenues" + str(
            round(expense / (total_expense / n2) * 100, 2))
        t = t1 + t2 + t3
        self.debrief.setText(t)

    def specificcatdebrief(self):
        revenue = 0
        total_revenue = 0
        expense = 0
        total_expense = 0
        n1 = 0
        n2 = 0
        category = self.cat.text()
        for i in self.data1:
            if self.username == i[0]:
                total_revenue += int(i[1])
                n1 += 1
                if category == i[3]:
                    revenue += int(i[1])
        for i in self.data2:
            if self.username == i[0]:
                total_expense += int(i[1])
                n2 += 1
                if category == i[3]:
                    expense += int(i[1])
        t1 = "\ntotal revenue:" + str(revenue) + "\ntotal expense:" + str(expense)
        t2 = "\nratio to overall revenue" + str(
            round(revenue / total_revenue * 100, 2)) + "\nratio to overall expense" + str(
            round(expense / total_expense * 100, 2))
        t3 = "\nratio to other revenues" + str(
            round(revenue / (total_revenue / n1) * 100, 2)) + "\nratio to other revenues" + str(
            round(expense / (total_expense / n2) * 100, 2))
        t = t1 + t2 + t3
        self.debrief.setText(t)
    def specificmoneydebrief(self):
        revenue = 0
        total_revenue = 0
        expense = 0
        total_expense = 0
        n1 = 0
        n2 = 0
        a = self.frommoney.text()
        b = self.tomoney.text()
        for i in self.data1:
            if self.username == i[0]:
                total_revenue += int(i[1])
                n1 += 1
                if int(a) <= int(i[1]) <= int(b):
                    revenue += int(i[1])
        for i in self.data2:
            if self.username == i[0]:
                total_expense += int(i[1])
                n2 += 1
                if int(a) <= int(i[1]) <= int(b):
                    expense += int(i[1])
        t1 = "\ntotal revenue:" + str(revenue) + "\ntotal expense:" + str(expense)
        t2 = "\nratio to overall revenue" + str(
            round(revenue / total_revenue * 100, 2)) + "\nratio to overall expense" + str(
            round(expense / total_expense * 100, 2))
        t3 = "\nratio to other revenues" + str(
            round(revenue / (total_revenue / n1) * 100, 2)) + "\nratio to other revenues" + str(
            round(expense / (total_expense / n2) * 100, 2))
        t = t1 + t2 + t3
        self.debrief.setText(t)

    def specificmonthdebrief(self):
        month = self.month.text()
        revenue = 0
        total_revenue = 0
        expense = 0
        total_expense = 0
        n1 = 0
        n2 = 0
        for i in self.data1:
            if self.username == i[0]:
                total_revenue += int(i[1])
                n1 += 1
                if month in i[2]:
                    revenue += int(i[1])
        for i in self.data2:
            if self.username == i[0]:
                total_expense += int(i[1])
                n2 += 1
                if month in i[2]:
                    expense += int(i[1])
        t1 = "\ntotal revenue:" + str(revenue) + "\ntotal expense:" + str(expense)
        t2 = "\nratio to overall revenue" + str(
            round(revenue / total_revenue * 100, 2)) + "\nratio to overall expense" + str(
            round(expense / total_expense * 100, 2))
        t3 = "\nratio to other revenues" + str(
            round(revenue / (total_revenue / n1) * 100, 2)) + "\nratio to other revenues" + str(
            round(expense / (total_expense / n2) * 100, 2))
        t = t1 + t2 + t3
        self.debrief.setText(t)

    def specificdatedebrief(self):
        revenue = 0
        total_revenue = 0
        expense = 0
        total_expense = 0
        n1 = 0
        n2 = 0
        days = []
        c3 = self.fromdate.text()
        c4 = self.todate.text()
        c3 = datetime.datetime.strptime(c3, '%Y/%m/%d')
        c4 = datetime.datetime.strptime(c4, '%Y/%m/%d')
        n = c3 - c4
        for i in range(n.days + 1):
            n_days_ago = c3 - datetime.timedelta(days=i)
            days.append(n_days_ago.strftime(format='%Y/%m/%d'))
        for i in self.data1:
            if self.username == i[0]:
                total_revenue += int(i[1])
                n1 += 1
                if i[2] in days:
                    revenue += int(i[1])
        for i in self.data2:
            if self.username == i[0]:
                total_expense += int(i[1])
                n2 += 1
                if i[2] in days:
                    expense += int(i[1])
        t1 = "\ntotal revenue:" + str(revenue) + "\ntotal expense:" + str(expense)
        t2 = "\nratio to overall revenue" + str(
            round(revenue / total_revenue * 100, 2)) + "\nratio to overall expense" + str(
            round(expense / total_expense * 100, 2))
        t3 = "\nratio to other revenues" + str(
            round(revenue / (total_revenue / n1) * 100, 2)) + "\nratio to other revenues" + str(
            round(expense / (total_expense / n2) * 100, 2))
        t = t1 + t2 + t3
        self.debrief.setText(t)

    def weekdebrief(self):
        revenue = 0
        total_revenue = 0
        expense = 0
        total_expense = 0
        n1 = 0
        n2 = 0
        today = datetime.datetime.now()
        days = []
        for i in range(7):
            n_days_ago = today - datetime.timedelta(days=i)
            days.append(n_days_ago.strftime(format='%Y/%m/%d'))
        for i in self.data1:
            if self.username == i[0]:
                total_revenue += int(i[1])
                n1 += 1
                if i[2] in days:
                    revenue += int(i[1])
        for i in self.data2:
            if self.username == i[0]:
                total_expense += int(i[1])
                n2 += 1
                if i[2] in days:
                    expense += int(i[1])
        t1 = "\ntotal revenue:" + str(revenue) + "\ntotal expense:" + str(expense)
        t2 = "\nratio to overall revenue" + str(
            round(revenue / total_revenue * 100, 2)) + "\nratio to overall expense" + str(
            round(expense / total_expense * 100, 2))
        t3 = "\nratio to other revenues" + str(
            round(revenue / (total_revenue / n1) * 100, 2)) + "\nratio to other revenues" + str(
            round(expense / (total_expense / n2) * 100, 2))
        t = t1 + t2 + t3
        self.debrief.setText(t)

    def threedaysdebrief(self):
        revenue = 0
        total_revenue = 0
        expense = 0
        total_expense = 0
        n1 = 0
        n2 = 0
        today = datetime.datetime.now()
        days = []
        for i in range(3):
            n_days_ago = today - datetime.timedelta(days=i)
            days.append(n_days_ago.strftime(format='%Y/%m/%d'))
        for i in self.data1:
            if self.username == i[0]:
                total_revenue += int(i[1])
                n1 += 1
                if i[2] in days:
                    revenue += int(i[1])
        for i in self.data2:
            if self.username == i[0]:
                total_expense += int(i[1])
                n2 += 1
                if i[2] in days:
                    expense += int(i[1])
        t1 = "\ntotal revenue:" + str(revenue) + "\ntotal expense:" + str(expense)
        t2 = "\nratio to overall revenue" + str(
            round(revenue / total_revenue * 100, 2)) + "\nratio to overall expense" + str(
            round(expense / total_expense * 100, 2))
        t3 = "\nratio to other revenues" + str(
            round(revenue / (total_revenue / n1) * 100, 2)) + "\nratio to other revenues" + str(
            round(expense / (total_expense / n2) * 100, 2))
        t = t1 + t2 + t3
        self.debrief.setText(t)

    def todaydebrief(self):
        revenue = 0
        total_revenue = 0
        expense = 0
        total_expense = 0
        n1 = 0
        n2 = 0
        today = datetime.datetime.now()
        today = today.strftime(format='%Y/%m/%d')
        for i in self.data1:
            if self.username == i[0]:
                total_revenue += int(i[1])
                n1 += 1
                if i[2] == today:
                    revenue += int(i[1])
        for i in self.data2:
            if self.username == i[0]:
                total_expense += int(i[1])
                n2 += 1
                if i[2] == today:
                    expense += int(i[1])
        t1 = "\ntotal revenue:" + str(revenue) + "\ntotal expense:" + str(expense)
        t2 = "\nratio to overall revenue" + str(
            round(revenue / total_revenue * 100, 2)) + "\nratio to overall expense" + str(
            round(expense / total_expense * 100, 2))
        t3 = "\nratio to other revenues" + str(
            round(revenue / (total_revenue / n1) * 100, 2)) + "\nratio to other revenues" + str(
            round(expense / (total_expense / n2) * 100, 2))
        t = t1 + t2 + t3
        self.debrief.setText(t)


class Setting(QMainWindow):
    def __init__(self):
        conn = sqlite3.connect('accounting.db')
        cur = conn.cursor()
        cur.execute('SELECT * from enteries')
        info = cur.fetchall()
        data = info[-1]
        self.username = data[0]
        super(Setting, self).__init__()
        loadUi("setting.ui", self)
        self.changeemail.clicked.connect(self.changeemailinfo)
        self.changephone.clicked.connect(self.changephoneinfo)
        self.changepassword.clicked.connect(self.changepass)
        self.deleteaccount.clicked.connect(self.deleteacc)
        self.deletetransaction.clicked.connect(self.deletetrans)
        self.back.clicked.connect(self.getbackmenu)

    def getbackmenu(self):
        p = Menu()
        widget.addWidget(p)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def deletetrans(self):
        conn = sqlite3.connect('accounting.db')
        cur = conn.cursor()
        c2 = self.trans.text()
        if c2 == 'revenue' or c2 == 'both':
            sql = "DELETE FROM Revenue_record WHERE username = '%s'" % self.username
            cur.execute(sql)
            conn.commit()
            print("Revenue transactions deleted")
        if c2 == 'expense' or c2 == 'both':
            sql = "DELETE FROM Expense_record WHERE username = '%s'" % self.username
            cur.execute(sql)
            conn.commit()
            print("Expense transaction deleted")

    def deleteacc(self):
        conn = sqlite3.connect('accounting.db')
        cur = conn.cursor()
        sql = "DELETE FROM users WHERE username = '%s'" % self.username
        cur.execute(sql)
        conn.commit()
        sql = "DELETE FROM categories WHERE username = '%s'" % self.username
        cur.execute(sql)
        conn.commit()
        sql = "DELETE FROM Expense_record WHERE username = '%s'" % self.username
        cur.execute(sql)
        conn.commit()
        sql = "DELETE FROM Revenue_record WHERE username = '%s'" % self.username
        cur.execute(sql)
        conn.commit()
        print("user deleted, you logged out.")
        p = Login()
        widget.addWidget(p)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def changepass(self):
        conn = sqlite3.connect('accounting.db')
        cur = conn.cursor()
        password = self.newpass.text()
        c = 0
        a = 0
        b = 0
        d = 0
        e = 0
        symbols = '!@#$%^&*()'
        for char in password:
            if char.isdigit():
                a += 1
            elif char.isupper():
                b += 1
            elif char.islower():
                d += 1
            elif char in symbols:
                e += 1
        if a < 1:
            print("password should have at least one number.")
            c += 1
        if b < 1:
            print("password should have at least one capital letter.")
            c += 1
        if d < 1:
            print("password should have at least one lowercase letter.")
            c += 1
        if e < 1:
            print("password should have at least one special character.")
            c += 1
        if len(password) < 6:
            print("password should be at least 6 characters.")
            c += 1
        if c == 0:
            sql = "UPDATE users set password = '%s' where username = '%s'" % (password, self.username)
            cur.execute(sql)
            conn.commit()
            self.edit.setText("password changed successfully")
        else:
            p = Setting()
            widget.addWidget(p)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def changephoneinfo(self):
        conn = sqlite3.connect('accounting.db')
        cur = conn.cursor()
        phone = self.newphone.text()
        c = 0
        if not phone.isnumeric():
            phone = input("phone number should contain only numbers. try again: ")
            c += 1
        elif not phone.startswith("09"):
            phone = input("phone number should start with 09. try again: ")
            c += 1
        elif len(phone) != 11:
            phone = input("phone number should have 11 digits. try again: ")
            c += 1
        if c == 0:
            sql = "UPDATE users set number = '%s' where username = '%s'" % (phone, self.username)
            cur.execute(sql)
            conn.commit()
            self.edit.setText("phone number changed successfully")
        else:
            p = Setting()
            widget.addWidget(p)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def changeemailinfo(self):
        conn = sqlite3.connect('accounting.db')
        cur = conn.cursor()
        c = 0
        symbols = '!@#$%^&*()'
        email = self.newemail.text()
        s = 0
        if '@' not in email:
            s += 1
        elif not email.endswith('gmail.com') and not email.endswith('yahoo.com'):
            s += 1
        try:
            e1 = email.split("@")
            for i in e1[0]:
                if i in symbols:
                    s += 1
        except Exception:
            s += 1
        if s > 0:
            print("email is not the right format.try again.")
            c += 1
        if c == 0:
            sql = "UPDATE users set email = '%s' where username = '%s'" % (email, self.username)
            cur.execute(sql)
            conn.commit()
            self.edit.setText("email changed successfully")
        else:
            p = Setting()
            widget.addWidget(p)
            widget.setCurrentIndex(widget.currentIndex() + 1)



app = QApplication(sys.argv)
window = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(window)
widget.setFixedHeight(690)
widget.setFixedWidth(890)
widget.show()
app.exec()