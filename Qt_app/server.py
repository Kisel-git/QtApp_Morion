import xml.etree.ElementTree as Et
import sqlite3
import os
from lxml import etree
import time
import schedule
import socket


trees = []
sent_file_name = r"C:\Users\rmo-1\Desktop\тестовое задание\test-task.db"  # Name of the file to be sent
HOST = '127.0.0.1'
PORT = 65432


# Получаем путь до каждого из файлов формата xml
def findfiles():
    directory = r"C:\Users\rmo-1\Desktop\тестовое задание v2\directory_xml"
    files = os.listdir(directory)
    for i in range(len(files)):
        files[i] = os.path.join(directory, files[i])
    return files


# Функция для обновления базы данных по данным из файлов
def updatetables():

    # Функция для нахождения родителя в дереве xml
    def find_parent(rot, child):
        for parent in rot.iter():
            for elems in parent:
                if elems == child:
                    return parent

    connection = sqlite3.connect(r"C:\Users\rmo-1\Desktop\тестовое задание\test-task.db")
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys=OFF")
    cursor.execute("DELETE FROM Port")
    cursor.execute("DELETE FROM Board")
    cursor.execute("DELETE FROM Block")
    cursor.execute("PRAGMA foreign_keys=ON")
    connection.commit()
    tags = ["block", "board", "port"]
    files_xml = findfiles()
    for file in files_xml:
        tree = Et.parse(file)
        tree_lxml = etree.parse(file)
        global trees
        trees.append(etree.tostring(tree_lxml))
        root = tree.getroot()
        for elem in tags:
            for components in root.iter(elem):
                if components.tag == "block":
                    cursor.execute("INSERT INTO Block VALUES(?,?,?,?,?,?,?,?)", tuple(components.attrib.values()))
                elif components.tag == "board":
                    BlockID = find_parent(root, components).attrib["id"]
                    coloms = ["id", "Num", "Name", "PortCount", "IntLinks", "Algoritms"]  # переписать как функцию
                    if len(components.attrib) < 6:
                        for el in coloms:
                            if el not in components.attrib.keys():
                                components.attrib[el] = "None"
                    components.attrib["BlockID"] = BlockID
                    cursor.execute("INSERT INTO Board VALUES(?,?,?,?,?,?,?)", tuple(components.attrib.values()))
                elif components.tag == "port":
                    BoardID = find_parent(root, components).attrib["id"]
                    coloms = ["id", "Num", "Media", "Signal"]
                    if len(components.attrib) < 4:
                        for el in coloms:
                            if el not in components.attrib.keys():
                                components.attrib[el] = "None"
                    components.attrib["BoardID"] = BoardID
                    cursor.execute("INSERT INTO Port VALUES(?,?,?,?,?)", tuple(components.attrib.values()))
    connection.commit()
    connection.close()
    return None


# функция которая отслеживает изменение в xml файлах, и в случае их обнаружение обновляет данные в БД
def checking_updates():
    trees_of_comparison = []
    files_xml = findfiles()
    for file in files_xml:
        tre = etree.parse(file)
        trees_of_comparison.append(etree.tostring(tre))
    global trees
    if trees_of_comparison == trees:
        print("Pass")
        pass
    else:
        trees = []
        updatetables()
        print("функция выполнилась")
    return None


def sent_file(file_name, host, port):
    BUFFER_SIZE = 4096  # Buffer size for receiving

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f'Waiting for connection at {host}:{port}')
        conn, addr = s.accept()
        with conn:
            print(f'Connected by {addr}') ###
            ###
            with open(file_name, 'rb') as f:
                while True:
                    data = f.read(BUFFER_SIZE)
                    if not data:
                        break
                    conn.sendall(data)
            print('File send successfully!')


schedule.every(1).minutes.do(checking_updates, sent_file(sent_file_name, HOST, PORT))
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)