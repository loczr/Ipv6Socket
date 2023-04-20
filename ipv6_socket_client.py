import socket
from threading import Thread
import threading

from datetime import datetime
from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5.QtWidgets import (QApplication,QLineEdit,QListWidget,QListWidgetItem,QPushButton,
        QHBoxLayout, QLabel, QTextBrowser,
        QVBoxLayout, QWidget,QTabWidget)
from logger import logger


class ipv6_client(QWidget):

    def __init__(self):
        super(ipv6_client, self).__init__()
        self.tcp_flag = 0
        self.udp_flag = 0

        mainlayout = QVBoxLayout()

        self.client_ip_info_layer()
        self.client_socket_info()

        self.tab2_layout()
        # self.create_tabwidget()

        self.setLayout(mainlayout)
        # self.setWindowTitle("QTtest")
        # self.resize(800,300)
        # mainlayout.addWidget(self.tabwidget)
        mainlayout.addWidget(self.tab2)

        # self.tcp_connect_button.clicked.connect(self.tcp_connect_done)

        self.client =None
        self.tcp_socket_client =None
        self.udp_client1 = None



    def tab2_layout(self):
        self.tab2 = QWidget()
        self.tab2_layout = QVBoxLayout()
        self.tab2_layout.addLayout(self.client_all_layer)
        self.tab2_layout.addLayout(self.client_socket_list_layer)
        self.tab2.setLayout(self.tab2_layout)

    # def create_tabwidget(self):
    #     self.tabwidget = QTabWidget(self)
    #     self.tabwidget.setMinimumWidth(600)
    #
    #     self.tabwidget.addTab(self.tab2,"client")
    #
    #     self.tab_layout=QHBoxLayout()
    #     self.tab_layout.addWidget(self.tabwidget)

    def client_ip_info_layer(self):
        self.client_tcp_ipv6_line = QLineEdit()
        self.client_tcp_port_line = QLineEdit()


        self.client_tcp_ipv6_line.setText("fe80::d869:5350:d234:24f3")
        self.client_tcp_port_line.setText("8989")
        self.client_tcp_ipv6_lable = QLabel(text="ipv6")
        self.client_tcp_port_label = QLabel(text="port")


        self.tcp_connect_button = QPushButton()
        self.tcp_connect_button.setText("TCP_connect")
        self.tcp_connect_button.toggle()

        self.udp_connect_button = QPushButton()
        self.udp_connect_button.setText("UDP_connect")
        self.udp_connect_button.toggle()


        self.tcp_connect_button.pressed.connect(self.tcp_click_button_method)
        self.udp_connect_button.pressed.connect(self.udp_click_button_method)

        self.client_link_status = QListWidget()
        self.client_link_status.itemPressed.connect(self.link_list_press)

        self.client_ipv6_info_layer = QHBoxLayout()
        self.client_ipv6_info_layer.addWidget(self.client_tcp_ipv6_lable)
        self.client_ipv6_info_layer.addWidget(self.client_tcp_ipv6_line)
        self.client_ipv6_info_layer.addWidget(self.client_tcp_port_label)
        self.client_ipv6_info_layer.addWidget(self.client_tcp_port_line)
        self.client_ipv6_info_layer.addWidget(self.tcp_connect_button)
        self.client_ipv6_info_layer.addWidget(self.udp_connect_button)


        self.client_ipv6_layer =QVBoxLayout()
        self.client_ipv6_layer.addLayout(self.client_ipv6_info_layer)
        # self.tcp_udp_client_ipv6_layer.addLayout(self.udp_conenct_ipv6_info_layer)

        self.client_all_layer = QHBoxLayout()
        self.client_all_layer.addLayout(self.client_ipv6_layer)


    def client_socket_info(self):

        self.client_send_msg_text_line = QLineEdit()
        self.client_socket_send_button = QPushButton()
        self.client_socket_send_button.setText("send")
        self.client_socket_send_button.clicked.connect(self.client_send)
        self.client_socket_listwidget = QListWidget()
        self.client_socket_listwidget.itemPressed.connect(self.client_socket_textbrowser_show)
        self.client_socket_link_data_textbrowser = QTextBrowser()

        self.client_socket_send_layer = QHBoxLayout()
        self.client_socket_send_layer.addWidget(self.client_send_msg_text_line)
        self.client_socket_send_layer.addWidget(self.client_socket_send_button)


        self.client_socket_list_layer = QVBoxLayout()
        self.client_socket_list_layer.addLayout(self.client_socket_send_layer)
        self.client_socket_list_layer.addWidget(self.client_socket_listwidget)
        self.client_socket_list_layer.addWidget(self.client_socket_link_data_textbrowser)

    def socket_list_add(self,address,data):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        item = QListWidgetItem(timestamp+" "+address+":"+data)
        item.data = data
        self.server_socket_listwidget.addItem(item)

    # def link_list_add(self,address,client):
    #     item = QListWidgetItem(address)
    #     item.client = client
    #     self.link_status.addItem(item)

    def link_list_press(self,item):
        print(type(item))
        logger.debug(item.client)

    def tcp_listen_close(self):
        self.server_tcp_ipv6_line.setEnabled(True)
        self.server_tcp_port_line.setEnabled(True)
        self.server_tcp_listen_button.setEnabled(True)

    def tcp_client_close(self,client):
        if client:
            for i in self.link_status.item():
                if client == i.client:
                    row = self.link_status.row(i)
                    if row:
                        self.link_status.takeItem(row)
        else:
            row = self.link_status.currentRow()
            client = self.link_status.currentItem().client
            logger.debug(client)
            try:
                self.tcp_socket_server.client_close(client)
                self.link_status.takeItem(row)
            except Exception as e:
                logger.debug(e)

    def tcp_connect_done(self):
        tcp_ipv6 = self.client_tcp_ipv6_line.text()
        tcp_port = int(self.client_tcp_port_line.text())
        try:

            self.tcp_socket_client =Tcp_Client(tcp_ipv6,tcp_port)
            self.tcp_socket_client.tcp_client_get_msg_sin.connect(self.client_list_add)
            self.tcp_socket_client.start()
            logger.debug(tcp_ipv6)
            logger.debug(tcp_port)
            logger.debug("start_tcp_client_connect")
            self.client_list_add("Tcp_server connect success")

        except Exception as e:
            logger.debug(e)

    def udp_connect_done(self):
        tcp_ipv6 = self.client_tcp_ipv6_line.text()
        tcp_port = int(self.client_tcp_port_line.text())

        try:
            self.udp_client1 = Udp_Client(tcp_ipv6,tcp_port)
            self.udp_client1.udp_client_get_msg_sin.connect(self.client_list_add)
            self.udp_client1.start()
            logger.debug(tcp_ipv6)
            logger.debug(tcp_port)
            logger.debug("start_udp_client_connect")

        except Exception as e:
            logger.debug(e)

    def tcp_close_done(self):
        try:

            self.tcp_socket_client.exit()
            self.tcp_socket_client.quit()
            #print(self.tcp_socket_client.isAlive())
            print(self.tcp_socket_client)
            self.tcp_socket_client = None

            logger.debug("close_tcp_client_connect")
        except BaseException as e:
            logger.debug(e)

    def udp_close_done(self):
        try:
            self.udp_client1.exit()
            logger.debug("close_udp_client_connect")
        except BaseException as e:
            logger.debug(e)

    def tcp_click_button_method(self):
        self.tcp_connect_button.setCheckable(True)

        if self.tcp_connect_button.isChecked() == False:
            if self.udp_connect_button.isChecked():
                print(self.tcp_connect_button.isChecked())
                print(self.udp_connect_button.isChecked())
                logger.debug("TCP "+self.tcp_connect_button.isChecked())
                logger.debug("UDP "+self.udp_connect_button.isChecked())
                logger.debug("udp_close_client")
                self.udp_close_done()
                self.udp_connect_button.setChecked(False)

            self.tcp_connect_done()
            logger.debug("tcp_client_connect")
        elif self.tcp_connect_button.isChecked():
            logger.debug("tcp_close_connect")
            self.tcp_close_done()

    def udp_click_button_method(self):
        self.udp_connect_button.setCheckable(True)

        if self.udp_connect_button.isChecked() == False:
            if self.tcp_connect_button.isChecked():
                print(self.tcp_connect_button.isChecked())
                print(self.udp_connect_button.isChecked())
                logger.debug("TCP "+self.tcp_connect_button.isChecked())
                logger.debug("UDP "+self.udp_connect_button.isChecked())
                self.tcp_close_done()
                logger.debug("tcp_close_client")
                self.tcp_connect_button.setChecked(False)

            self.udp_connect_done()
            logger.debug("udp_client_connect")
        elif self.udp_connect_button.isChecked():
            self.udp_close_done()
            logger.debug("udp_close_connect")

    def client_list_add(self,data):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        item = QListWidgetItem(timestamp+":"+data)
        item.data = data
        self.client_socket_listwidget.addItem(item)

    def client_send(self):
        try:
            msg = self.client_send_msg_text_line.text()
            if self.tcp_socket_client:

                self.tcp_socket_client.client_send_msg(msg)
            elif self.udp_client1:
                self.udp_client1.send_msg(msg)
            else:
                pass

        except Exception as e:
            logger.debug(e)

    def client_socket_textbrowser_show(self):
        self.client_socket_link_data_textbrowser.setText("")
        data = self.client_socket_listwidget.currentItem().data
        self.client_socket_link_data_textbrowser.setText(data)


class Tcp_Client(QThread):

    tcp_connect_sin = pyqtSignal(object)
    tcp_close_socket_sin = pyqtSignal(object)
    tcp_client_get_msg_sin = pyqtSignal(object)
    tcp_client_sin = pyqtSignal(object,object)

    def __init__(self,ipv6,port):
        super(Tcp_Client,self).__init__()
        self.ipv6 = ipv6
        self.port = port
        self.addrinfo = socket.getaddrinfo(self.ipv6, int(self.port))[0]

        self.clients=[]
        self.clients_name_ip={}


    def get_msg(self,client,clitens,clients_name_ip,address):
        while True:
            try:
                data = client.recv(35565).decode()
                if data:
                    addr = "TCP " + address[0] + "：" + str(address[1])
                    self.tcp_get_msg_sin.emit(addr,data)
                    logger.debug(data)

                    length = len(threading.enumerate())
                    print('当前运行的线程数为：%d' % length)
                    if length <= 1:
                        break

            except Exception as e:
                logger.debug(client)
                logger.debug("close error")
                break

        #         发送消息

    def send_msg(self,client,msg):
        client.send(msg.encode())


    def recv_msg(self):
        while True:
            try:
                data = self.client.recv(35565).decode()
                print(data)
                data = data + "\n"
                self.content.append(data)
            except BaseException as e:
                logger.debug(e)


    def client_close(self,client):
        client.close()

        #     匿名类，线程处理,发送是一个线程，接受是一个线程

    def client_send_msg(self,data):
            self.client.send(data.encode())  # 把命令发送给对端

    def client_recv_msg(self):
        while self.client:
        #while True:
            data = self.client.recv(65535).decode()
            logger.debug(data)
            self.tcp_client_get_msg_sin.emit(data)

    def run(self):
        try:
            self.client= socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
            self.client.connect(self.addrinfo[-1])
            Thread(target=self.client_recv_msg).start()

        except Exception as e:
            logger.debug(e)

class Udp_Client(QThread):
    tcp_connect_sin = pyqtSignal(object)
    tcp_close_socket_sin = pyqtSignal(object)
    udp_client_get_msg_sin = pyqtSignal(object)
    tcp_client_sin = pyqtSignal(object,object)

    def __init__(self,ipv6,port):
        super(Udp_Client,self).__init__()
        self.ipv6 = ipv6
        self.port = port
        self.addrinfo = socket.getaddrinfo(self.ipv6, int(self.port))[0]

        self.clients=[]
        self.clients_name_ip={}
        self.send_flag = False

    def send_msg(self,msg):
        msg = msg.encode()
        self.udp_client.sendto(msg,self.addrinfo[-1])
        self.send_flag =True

    def udp_recv_msg(self):
        while True:
            while self.send_flag:
                data,address = self.udp_client.recvfrom(65535)
                data = data.decode()
                logger.debug(data)
                if data:
                    addr = "UDP " + address[0] + "：" + str(address[1])
                    self.udp_client_get_msg_sin.emit(data)
                    # logger.debug(data)

                    # length = len(threading.enumerate())
                    # print('当前运行的线程数为：%d' % length)
                    # if length <= 1:
                    #     break

    def run(self) :
        self.udp_client = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)

        Thread(target=self.udp_recv_msg).start()


# if __name__ == '__main__':
#     import sys
#     app = QApplication(sys.argv)
#     screenshot = ipv6_client()
#     screenshot.show()
#     sys.exit(app.exec_())




