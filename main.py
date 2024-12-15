import sys
import requests
from PyQt5 import QtWidgets
from my1 import *
from movie import *
from staff import *
#lineEdit это Username в login
#lineEdit_3 это Password в login
#lineEdit_4 это Username в register
#lineEdit_5 это Password в register

seats = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'a9', 'a10', 'a11', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8']
admins = ['emil']
me = []

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.login_register_window = QtWidgets.QMainWindow()
        self.login_register_ui = Ui_login_register()
        self.login_register_ui.setupUi(self.login_register_window)
        self.login_register_window.setMaximumSize(609, 432)
        self.login_register_window.show()

        self.login_register_ui.pushButton.clicked.connect(self.switch_to_tab_login)
        self.login_register_ui.pushButton_2.clicked.connect(self.switch_to_tab_register)

        self.login_register_ui.pushButton_5.clicked.connect(self.login)
        self.login_register_ui.pushButton_6.clicked.connect(self.register)

        self.mouse_moved = False
        self.setMouseTracking(True)
        self.login_register_window.setMouseTracking(True)


        self.movie = None
        self.film = None
        self.dict = {i : False for i in seats}
        self.seatsClient = []

    def reset(self):
        self.login_register_ui.tabWidget.setCurrentIndex(0)
        self.__init__()

    def switch_to_tab_login(self):
        self.login_register_ui.tabWidget.setCurrentIndex(1)

    def switch_to_tab_register(self):
        self.login_register_ui.tabWidget.setCurrentIndex(2)

    def filter_list(self):
        search_text = self.mainwindow_ui.lineEdit.text().lower()

        for i in range(self.mainwindow_ui.listWidget.count()):
            item = self.mainwindow_ui.listWidget.item(i)
            if search_text in item.text().lower():  
                item.setHidden(False)  
            else:
                item.setHidden(True) 

    def login(self):
        url = 'https://Aa12321231.pythonanywhere.com/login'
        username = self.login_register_ui.lineEdit.text()
        password = self.login_register_ui.lineEdit_3.text()
        if 1 > len(username) or 1 > len(password):
            return QtWidgets.QMessageBox.warning(self.login_register_window, "Error", "Please type login/register.")
        response = requests.get(url, {'username':username, 'password':password})
        if response.status_code == 200:
            me.append(username)
            self.login_register_window.close()
            if username in admins:
                self.open_staffwindow()
            self.open_mainwindow()
        else:
            QtWidgets.QMessageBox.warning(self.login_register_window, "Error", "Wrong username/password.")

    def register(self):
        url = 'https://Aa12321231.pythonanywhere.com/register'
        username = self.login_register_ui.lineEdit_4.text()
        password = self.login_register_ui.lineEdit_5.text()
        if 1 > len(username) or 1 > len(password):
            return QtWidgets.QMessageBox.warning(self.login_register_window, "Error", "Please type login/register.")
        if not self.login_register_ui.radioButton.isChecked():
            QtWidgets.QMessageBox.warning(self.login_register_window, "Error", "Please confirm you are not a robot.")
            return
        response = requests.get(url, {'username':username, 'password':password})
        if response.text == 'Success':
            me.append(username)
            self.login_register_window.close()
            self.open_mainwindow()
        else:
            QtWidgets.QMessageBox.warning(self.login_register_window, "Error", "Login is already exist, try another one")

    def mouseMoveEvent(self, event):
        if not self.mouse_moved:
            self.mouse_moved = True
            self.login_register_ui.radioButton.setEnabled(True)

    def open_staffwindow(self):
        self.staffwindow = QtWidgets.QMainWindow()
        self.staffwindow_ui = Ui_StaffWindow()
        self.staffwindow_ui.setupUi(self.staffwindow)
        self.staffwindow.show()

        self.staffwindow_ui.pushButton_3.clicked.connect(self.open_1)
        self.staffwindow_ui.pushButton_7.clicked.connect(self.open_2)
        self.staffwindow_ui.pushButton_9.clicked.connect(self.addMovie)
        for i, (key, value) in enumerate(self.getProfit().items()):
            self.staffwindow_ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(key))
            self.staffwindow_ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(value)))

    

        
    def addMovie(self):
        url = 'https://Aa12321231.pythonanywhere.com/add_movie'
        title = self.staffwindow_ui.lineEdit.text()
        time1 = self.staffwindow_ui.lineEdit_6.text()
        time2 = self.staffwindow_ui.lineEdit_7.text()
        time3 = self.staffwindow_ui.lineEdit_8.text()
        time4 = self.staffwindow_ui.lineEdit_9.text()
        price = self.staffwindow_ui.lineEdit_5.text()
        response1 = requests.get(url, params = {'title':title, 'time':time1, 'price':price})
        response2 = requests.get(url, params = {'title':title, 'time':time2, 'price':price})
        response3 = requests.get(url, params = {'title':title, 'time':time3, 'price':price})
        response4 = requests.get(url, params = {'title':title, 'time':time4, 'price':price})
        if response1.status_code == 200 and response2.status_code == 200 and response3.status_code == 200 and response4.status_code == 200:
            QtWidgets.QMessageBox.information(self.mainwindow, 'Done', 'Success')
        else:
            QtWidgets.QMessageBox.warning(self.mainwindow, 'Error', 'Unknown Error')

    def getProfit(self):
        url = 'https://Aa12321231.pythonanywhere.com/getProfit'
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            return response

    def open_1(self):
        self.staffwindow_ui.tabWidget.setCurrentIndex(1)

    def open_2(self):
        self.staffwindow_ui.tabWidget.setCurrentIndex(2)

    def open_mainwindow(self):
        self.mainwindow = QtWidgets.QMainWindow()
        self.mainwindow_ui = Ui_MainWindow()
        self.mainwindow_ui.setupUi(self.mainwindow)
        self.mainwindow.show()

        self.mainwindow_ui.listWidget.itemDoubleClicked.connect(self.switch_to_tab_schedule)
        self.mainwindow_ui.pushButton.clicked.connect(self.switch_to_tab_buy_seats)
        self.mainwindow_ui.pushButton_2.clicked.connect(self.switch_to_tab_buy_seats)
        self.mainwindow_ui.pushButton_3.clicked.connect(self.switch_to_tab_buy_seats)
        self.mainwindow_ui.pushButton_4.clicked.connect(self.switch_to_tab_buy_seats)
        # self.mainwindow_ui.pushButton_5.clicked.connect(self.switch_to_tab_movies)
        # self.mainwindow_ui.pushButton_6.clicked.connect(self.switch_to_tab_schedule1)
        self.mainwindow_ui.pushButton_7.clicked.connect(self.switch_to_tab_final)
        self.mainwindow_ui.pushButton_8.clicked.connect(self.buySeats)
        self.mainwindow_ui.pushButton_9.clicked.connect(self.removeSeats)
        self.mainwindow_ui.lineEdit.textChanged.connect(self.filter_list)

        for i in self.checkMovies():
            _translate = QtCore.QCoreApplication.translate
            item = QtWidgets.QListWidgetItem()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("logo.qrc.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            item.setIcon(icon)
            font = QtGui.QFont()
            font.setPointSize(20)
            item.setFont(font)
            item.setText(_translate("MainWindow", i))
            self.mainwindow_ui.listWidget.addItem(item)

    def switch_to_tab_movies(self):
        self.mainwindow_ui.tabWidget.setCurrentIndex(0)

    def switch_to_tab_schedule(self, item):
        self.mainwindow_ui.tabWidget.setCurrentIndex(1)
        self.movie = item
        arr = self.checkSchedule()
        self.mainwindow_ui.pushButton.setText(arr[0])
        self.mainwindow_ui.pushButton_2.setText(arr[1])
        self.mainwindow_ui.pushButton_3.setText(arr[2])
        self.mainwindow_ui.pushButton_4.setText(arr[3])
        

    def switch_to_tab_buy_seats(self):
        self.mainwindow_ui.tabWidget.setCurrentIndex(2)
        self.time = self.sender()
        print(self.time.text())
        for i,k in self.checkSeats().items():
            if k and k == me[0]:
                button = getattr(self.mainwindow_ui, i, None)
                button.setStyleSheet("QPushButton { background-color: darkred; border-radius: 15px; padding: 10px 20px; border: none; font-size: 16px;}")
                self.dict[i] = True
            elif k and k != me[0]:
                button = getattr(self.mainwindow_ui, i, None)
                button.setStyleSheet("QPushButton { background-color: black; border-radius: 15px; padding: 10px 20px; border: none; font-size: 16px;}")
                button.setEnabled(False)

        for i in seats:
            button = getattr(self.mainwindow_ui, i, None)
            button.clicked.connect(self.createfun(i))

    def switch_to_tab_final(self):
        price = self.getPrice()
        self.mainwindow_ui.tabWidget.setCurrentIndex(3)
        self.mainwindow_ui.lineEdit_3.setText(self.movie.text())
        self.mainwindow_ui.lineEdit_4.setText(' '.join([i for i in self.seatsClient]))
        self.mainwindow_ui.lineEdit_5.setText(str(price))
        self.mainwindow_ui.lineEdit_6.setText(str(int(price)*len(self.seatsClient)))

    def getPrice(self):
        url = 'https://Aa12321231.pythonanywhere.com/getPrice'
        title = self.movie.text()
        response = requests.get(url, params= {'title':title})
        if response.status_code == 200:
            response = response.json()
            print(response)
            return response

    def checkSchedule(self):
        url = 'https://Aa12321231.pythonanywhere.com/get_schedule'
        response = requests.get(url, params= {'title':self.movie.text()})
        if response.status_code == 200:
            response = response.json()
            return response

    def checkMovies(self):
        url = 'https://Aa12321231.pythonanywhere.com/get_onlymovies'
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            return response

    def checkSeats(self):
        url = 'https://Aa12321231.pythonanywhere.com/get_seatsInDict'
        movie = self.movie.text()
        time = self.time.text()
        response = requests.get(url, params={'title':movie, 'time':time})
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        #     for i,k in response_data.items():
        #         if k:
        #             button = getattr(self.mainwindow_ui, i, None)
        #             button.setStyleSheet("QPushButton { background-color: darkred; border-radius: 15px; padding: 10px 20px; border: none; font-size: 16px;}")
        #             self.dict[i] = True
    
        # for i in seats:
        #     button = getattr(self.mainwindow_ui, i, None)
        #     button.clicked.connect(self.createfun(i))

    def createfun(self, v):
        def button():
            but = getattr(self.mainwindow_ui, v, None)
            if not self.dict[v]:
                but.setStyleSheet("QPushButton { background-color: darkred; border-radius: 15px; padding: 10px 20px; border: none; font-size: 16px;}")
                self.dict[v] = True
                self.seatsClient.append(v)
            else:
                but.setStyleSheet("QPushButton { background-color: white; border-radius: 15px; padding: 10px 20px; border: none; font-size: 16px;}")
                self.dict[v] = False
                try:
                    self.seatsClient.remove(v)
                except:
                    pass
        return button

    def buySeats(self):
        url = 'https://aa12321231.pythonanywhere.com/bookSeats'
        seats = ','.join(self.seatsClient)
        response = requests.get(url, params= {'title':self.movie.text(), 'time':self.time.text(), 'client':me[0], 'seats':seats}) 
        if response.text == 'Done':
            print('12')
            QtWidgets.QMessageBox.information(self.mainwindow, 'Success', 'Your seats have been reserved')
            self.seatsClient.clear()
            self.mainwindow_ui.lineEdit_3.clear()
            self.mainwindow_ui.lineEdit_4.clear()
            self.mainwindow_ui.lineEdit_5.clear()
            self.mainwindow_ui.lineEdit_6.clear()
            self.open_mainwindow()
        else:
            print(response)
            QtWidgets.QMessageBox.warning(self.mainwindow, 'Error', 'Unknown Error')

    def removeSeats(self):
        url = 'https://aa12321231.pythonanywhere.com/removeSeats'
        seats = ','.join(self.seatsClient)
        response = requests.get(url, params= {'title':self.movie.text(), 'time':self.time.text(), 'client':me[0], 'seats':seats})
        if response.text == 'Done':
            print('12')
            QtWidgets.QMessageBox.information(self.mainwindow, 'Success', 'Your seats have been reserved')
            self.seatsClient.clear()
            self.mainwindow_ui.lineEdit_3.clear()
            self.mainwindow_ui.lineEdit_4.clear()
            self.mainwindow_ui.lineEdit_5.clear()
            self.mainwindow_ui.lineEdit_6.clear()
            self.open_mainwindow()
        else:
            print(response)
            QtWidgets.QMessageBox.warning(self.mainwindow, 'Error', 'Unknown Error')





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainApp()
    sys.exit(app.exec_())