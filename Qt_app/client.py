from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QTreeView, QMainWindow
from PyQt5.Qt import QStandardItemModel, QStandardItem
import sys
from PyQt5.QtSql import *
import socket


DB_name = r"C:\Users\rmo-1\Desktop\тестовое задание\Forsaving.db"
Form, Window = uic.loadUiType("qtdesigner.ui")   # Сюда вводить имя файла из Дизайнера
HOST = '127.0.0.1'
PORT = 65432


def connection():  # Подключение к БД через кнопку подключения
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(r"C:\Users\rmo-1\Desktop\тестовое задание\Forsaving.db")
    if not db.open():
        print("Connection Error")
        return False
    else:
        print("Connection OK")
        return db


app = QApplication([])
window = Window()
form = Form()  # Объект класса Form, который позволяет обращаться к различным элементам интерфейса
form.setupUi(window)
form.pushButton.clicked.connect(connection)


def get_file():
    BUFFER_SIZE = 4096  # Buffer size for sending
    global DB_name
    global HOST
    global PORT
    global form
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            form.ConnectionStatus.setText("    Connection Status:")
            form.ConnectionStatus.setText(form.ConnectionStatus.text() + "ON")
            with open(DB_name, 'wb') as f:
                while True:
                    file_data = s.recv(BUFFER_SIZE)
                    f.write(file_data)
                    if not file_data:
                        break
            print("Подключение выполнено успешно")
        except Exception:
            form.ConnectionStatus.setText("    Connection Status:")
            form.ConnectionStatus.setText(form.ConnectionStatus.text() + "OFF")
            print("Server Error")
        else:
            print('File saved successfully!')


form.begin.clicked.connect(get_file)


def info_block():
    #connection()
    global form
    table1 = QSqlTableModel()
    table1.setTable("Block")
    table1.select()
    form.tableView.setModel(table1)
    return None


def info_board():
    #connection()
    global form
    table2 = QSqlTableModel()
    table2.setTable("Board")
    table2.select()
    form.tableView.setModel(table2)
    return None


def info_port():
    #connection()
    global form
    table3 = QSqlTableModel()
    table3.setTable("Port")
    table3.select()
    form.tableView.setModel(table3)
    return None


form.BlockB.clicked.connect(info_block)
form.BoardB.clicked.connect(info_board)
form.PortB.clicked.connect(info_port)

window.show()
app.exec()
