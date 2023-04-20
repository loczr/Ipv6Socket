import socket
from threading import Thread
import threading
import time
from datetime import datetime
from PyQt5.QtCore import QThread,pyqtSignal,QTimer,Qt,QSize
from PyQt5.QtWidgets import (QApplication,QTableWidget,QTableWidgetItem,QLineEdit,QListWidget,QListWidgetItem,
        QHBoxLayout, QLabel, QComboBox,QProgressBar,QPushButton,QSpacerItem,QSizePolicy,QTextBrowser,QTextEdit,
        QVBoxLayout, QWidget,QTabWidget)
from logger import logger
from ipv6_socket_client import ipv6_client

class SocketTools(QWidget):

    def __init__(self):
        super(SocketTools, self).__init__()

        mainlayout = QVBoxLayout()

        self.server_ip_info_layer()
        #self.client_ip_info_layer()
        #self.client_socket_info()
        self.server_socket_info()
        self.tab1_layout()
        self.tab2_layout()
        self.create_tabwidget()

        self.setLayout(mainlayout)
        self.setWindowTitle("QTtest")
        self.resize(800,300)
        mainlayout.addWidget(self.tabwidget)
        #self.tcp_listen_button.clicked.connect(self.tcp_listen_done)
        #self.tcp_listen_button.clicked.connect(self.tcp_btn_check)
        self.tcp_listen_button.pressed.connect(self.tcp_btn_check)
        self.udp_listen_button.pressed.connect(self.udp_btn_check)

        #self.tcp_connect_button.clicked.connect(self.tcp_connect_done)

        #self.udp_listen_button.clicked.connect(self.udp_listen_done)

        self.server_tcp_ipv6_line.setText("fe80::d869:5350:d234:24f3")
        self.server_tcp_port_line.setText("8989")
        self.client =""


        self.udp_socket_server = None
        self.tcp_socket_server = None


    def tab1_layout(self):
        self.tab1 = QWidget()
        self.tab1_layout = QVBoxLayout()
        self.tab1_layout.addLayout(self.server_all_layer)
        self.tab1_layout.addLayout(self.server_socket_list_layer)
        self.tab1.setLayout(self.tab1_layout)

    def tab2_layout(self):
        self.tab2 = ipv6_client()
#        self.tab2_layout = QVBoxLayout()
#        self.tab2_layout.addLayout(self.client_all_layer)
#        self.tab2_layout.addLayout(self.client_socket_list_layer)
#        self.tab2.setLayout(self.tab1_layout)

    def create_tabwidget(self):
        self.tabwidget = QTabWidget(self)
        self.tabwidget.setMinimumWidth(600)

        self.tabwidget.addTab(self.tab1,"server")
        self.tabwidget.addTab(self.tab2,"client")

        self.tab_layout=QHBoxLayout()
        self.tab_layout.addWidget(self.tabwidget)

    def server_ip_info_layer(self):
        self.server_tcp_ipv6_line = QLineEdit()
        self.server_tcp_port_line = QLineEdit()
        self.server_tcp_ipv6_lable = QLabel(text = "tcp_ipv6")
        self.server_tcp_port_label = QLabel(text = "tcp_port")
        self.server_udp_ipv6_line = QLineEdit()
        self.server_udp_port_line = QLineEdit()
        self.server_udp_ipv6_lable = QLabel(text = "udp_ipv6")
        self.server_udp_port_label = QLabel(text = "udp_port")

        self.tcp_listen_button = QPushButton()
        self.tcp_listen_button.setText("TCP_listen")
        self.udp_listen_button = QPushButton()
        self.udp_listen_button.setText("UDP_listen")


        #self.tcp_listen_button.setCheckable(True)
        # self.tcp_listen_button.setDefault(False)
        self.tcp_listen_button.toggle()
        self.udp_listen_button.toggle()


        self.link_status = QListWidget()
        self.link_status.itemPressed.connect(self.link_list_press)

        self.link_break_button = QPushButton()
        self.link_break_button.setText("Break_link")
        self.link_break_button.clicked.connect(self.tcp_client_close)

        self.tcp_ipv6_info_layer = QHBoxLayout()
        self.tcp_ipv6_info_layer.addWidget(self.server_tcp_ipv6_lable)
        self.tcp_ipv6_info_layer.addWidget(self.server_tcp_ipv6_line)
        self.tcp_ipv6_info_layer.addWidget(self.server_tcp_port_label)
        self.tcp_ipv6_info_layer.addWidget(self.server_tcp_port_line)
        self.tcp_ipv6_info_layer.addWidget(self.tcp_listen_button)

        self.udp_ipv6_info_layer = QHBoxLayout()
        self.udp_ipv6_info_layer.addWidget(self.server_udp_ipv6_lable)
        self.udp_ipv6_info_layer.addWidget(self.server_udp_ipv6_line)
        self.udp_ipv6_info_layer.addWidget(self.server_udp_port_label)
        self.udp_ipv6_info_layer.addWidget(self.server_udp_port_line)
        self.udp_ipv6_info_layer.addWidget(self.udp_listen_button)

        self.tcp_udp_ipv6_layer =QVBoxLayout()
        self.tcp_udp_ipv6_layer.addLayout(self.tcp_ipv6_info_layer)
        self.tcp_udp_ipv6_layer.addLayout(self.udp_ipv6_info_layer)

        self.link_layer = QHBoxLayout()
        self.link_layer.addWidget(self.link_status)
        self.link_layer.addWidget(self.link_break_button)

        self.server_all_layer = QHBoxLayout()
        self.server_all_layer.addLayout(self.tcp_udp_ipv6_layer)
        self.server_all_layer.addLayout(self.link_layer)


    def server_socket_info(self):

        self.server_socket_send_msg_text_line = QLineEdit()
        self.server_socket_send_button = QPushButton()
        self.server_socket_send_button.setText("send")
        self.server_socket_send_button.clicked.connect(self.server_socket_server_send)
        self.server_socket_listwidget = QListWidget()
        self.server_socket_listwidget.itemPressed.connect(self.server_socket_textbrowser_show)
        self.server_socket_link_data_textbrowser = QTextBrowser()

        self.server_socket_send_layer = QHBoxLayout()
        self.server_socket_send_layer.addWidget(self.server_socket_send_msg_text_line)
        self.server_socket_send_layer.addWidget(self.server_socket_send_button)


        self.server_socket_list_layer = QVBoxLayout()
        self.server_socket_list_layer.addLayout(self.server_socket_send_layer)
        self.server_socket_list_layer.addWidget(self.server_socket_listwidget)
        self.server_socket_list_layer.addWidget(self.server_socket_link_data_textbrowser)

    def server_socket_server_send(self):
        try:
            socket_type = self.link_status.currentItem().socket_type
            address = self.link_status.currentItem().address
            port = self.link_status.currentItem().port
            client = self.link_status.currentItem().client
            msg = self.server_socket_send_msg_text_line.text()

            if socket_type == "TCP":
                self.tcp_socket_server.send_msg(client,msg)
            elif socket_type =="UDP":
                self.udp_socket_server.send_msg(address,port,msg)

        except Exception as e:
            logger.debug(e)

    def server_socket_textbrowser_show(self):
        self.server_socket_link_data_textbrowser.setText("")
        data = self.server_socket_listwidget.currentItem().data
        self.server_socket_link_data_textbrowser.setText(data)

    def socket_list_add(self,address,data):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        item = QListWidgetItem(timestamp+" "+address+":"+data)
        item.data = data
        self.server_socket_listwidget.addItem(item)

    def link_list_add(self,type,address,port,client):
        item = QListWidgetItem("%s-[%s]:%s" % (type,address, port))
        item.socket_type = type
        item.client = client
        item.address = address
        item.port = port
        self.link_status.addItem(item)

    def link_list_press(self,item):
        print(type(item))
        logger.debug(item.socket_type)
        logger.debug(item.address)
        logger.debug(item.port)
        logger.debug(item.client)

    def tcp_listen_done(self):
        tcp_ipv6 = self.server_tcp_ipv6_line.text()
        tcp_port = int(self.server_tcp_port_line.text())
        try:
            self.tcp_socket_server =Tcp_Server(tcp_ipv6,tcp_port)
            self.tcp_socket_server.tcp_get_msg_sin.connect(self.socket_list_add)
            self.tcp_socket_server.tcp_client_sin.connect(self.link_list_add)
            self.tcp_socket_server.start()
            logger.debug(tcp_ipv6)
            logger.debug(tcp_port)
            logger.debug("start_tcp_socket")
        except Exception as e:
            logger.debug(e)

        #self.socket_server.get_conn()
        self.server_tcp_ipv6_line.setEnabled(False)
        self.server_tcp_port_line.setEnabled(False)
        self.tcp_listen_button.setEnabled(False)

    def udp_listen_done(self):
        udp_ipv6 = self.server_udp_ipv6_line.text()
        udp_port = int(self.server_udp_port_line.text())
        try:
            self.udp_socket_server =Udp_Server(udp_ipv6,udp_port)
            self.udp_socket_server.tcp_get_msg_sin.connect(self.socket_list_add)
            self.udp_socket_server.udp_client_sin.connect(self.link_list_add)
            self.udp_socket_server.start()
            logger.debug(udp_ipv6)
            logger.debug(udp_port)
            logger.debug("start_udp_socket")
        except Exception as e:
            logger.debug(e)

        #self.socket_server.get_conn()
        self.server_udp_ipv6_line.setEnabled(False)
        self.server_udp_port_line.setEnabled(False)
        self.udp_listen_button.setEnabled(False)

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

    def tcp_btn_check(self):
        self.tcp_listen_button.setCheckable(True)
        if not self.tcp_listen_button.isChecked():
            tcp_ipv6 = self.server_tcp_ipv6_line.text()
            tcp_port = int(self.server_tcp_port_line.text())
            try:
                self.tcp_socket_server = Tcp_Server(tcp_ipv6, tcp_port)
                self.tcp_socket_server.tcp_get_msg_sin.connect(self.socket_list_add)
                self.tcp_socket_server.tcp_client_sin.connect(self.link_list_add)
                self.tcp_socket_server.start()
                logger.debug(tcp_ipv6)
                logger.debug(tcp_port)
                logger.debug("start_tcp_socket")
            except Exception as e:
                logger.debug(e)

            self.server_tcp_ipv6_line.setEnabled(False)
            self.server_tcp_port_line.setEnabled(False)

        else:
            try:
                self.tcp_socket_server.server_close_done()
                self.tcp_socket_server.wait()
                self.tcp_socket_server=None
                logger.debug("close_tcp_socket")
                self.server_tcp_ipv6_line.setEnabled(True)
                self.server_tcp_port_line.setEnabled(True)
            except BaseException as e:
                logger.debug(e)

    def udp_btn_check(self):
        self.udp_listen_button.setCheckable(True)
        if not self.udp_listen_button.isChecked():
            udp_ipv6 = self.server_udp_ipv6_line.text()
            udp_port = int(self.server_udp_port_line.text())
            try:
                self.udp_socket_server = Udp_Server(udp_ipv6, udp_port)
                self.udp_socket_server.tcp_get_msg_sin.connect(self.socket_list_add)
                self.udp_socket_server.udp_client_sin.connect(self.link_list_add)
                self.udp_socket_server.start()
                logger.debug(udp_ipv6)
                logger.debug(udp_port)
                logger.debug("start_udp_socket")
            except Exception as e:
                logger.debug(e)

            # self.socket_server.get_conn()
            self.server_udp_ipv6_line.setEnabled(False)
            self.server_udp_port_line.setEnabled(False)
            #self.udp_listen_button.setEnabled(False)
        else:
            try:
                self.udp_socket_server.exit()
                logger.debug("close_tcp_socket")
                self.server_udp_ipv6_line.setEnabled(True)
                self.server_udp_port_line.setEnabled(True)
            except BaseException as e:
                logger.debug(e)


class Tcp_Server(QThread):

    tcp_listen_sin = pyqtSignal(object)
    tcp_close_socket_sin = pyqtSignal(object)
    tcp_get_msg_sin = pyqtSignal(object,object)
    tcp_client_sin = pyqtSignal(object,object,object,object)

    def __init__(self,ipv6,port):
        super(Tcp_Server,self).__init__()
        self.ipv6 = ipv6
        self.port = port
        self.addrinfo = socket.getaddrinfo(self.ipv6, int(self.port))[0]

        self.clients=[]
        self.clients_name_ip={}

    # def exit(self, returnCode: int = ...) -> None:
    #     self.server.close()

    def server_close_done(self):
        for client in self.clients:
            try:
                self.client_close(client)
            except BaseException as e:
                logger.debug(e)
        #self.exit()
        logger.debug("tcp_server_client_close")




    def get_conn(self):
        while True:
            client,address=self.server.accept()
            print("TCP " + address[0] + "：" + str(address[1]))
            # data="与服务器链接成功，请输入昵称才可以聊天"
            # # server与client通信，send() decode
            # client.send(data.encode())
            # 链接用户添加到服务器的用户列表
            self.tcp_client_sin.emit("TCP",address[0],address[1],client)
            self.clients.append(client)
            Thread(target=self.get_msg,args=(client,self.clients,self.clients_name_ip,address)).start()
            #self.get_msg(client,self.clients,self.clients_name_ip,address)

    def get_msg(self,client,clients,clients_name_ip,address):
        while client:

        #while True:
            data = client.recv(65535).decode()
            logger.debug(data)

            if data:
                addr = "TCP " + address[0] + "：" + str(address[1])
                self.tcp_get_msg_sin.emit(addr,data)
            elif data ==b'':
                print("client close")
            else:
                logger.debug(client)
                logger.debug(data)
                #break

        logger.debug(client)
        logger.debug("close error")


    def send_msg(self, client, msg):
        client.send(msg.encode())

    def client_close(self,client):
        client.close()

    def run(self):
        try:
            self.server=socket.socket(socket.AF_INET6, socket.SOCK_STREAM, 0)
            self.server.bind(self.addrinfo[-1])
            self.server.listen(5)
            self.get_conn()
        except Exception as e:
            logger.debug(e)

class Udp_Server(QThread):

    tcp_listen_sin = pyqtSignal(object)
    tcp_close_socket_sin = pyqtSignal(object)
    tcp_get_msg_sin = pyqtSignal(object,object)
    udp_client_sin = pyqtSignal(object,object,object,object)

    def __init__(self,ipv6,port):
        super(Udp_Server,self).__init__()
        self.ipv6 = ipv6
        self.port = port
        self.addrinfo = socket.getaddrinfo(self.ipv6, int(self.port))[0]

        self.clients=[]
        self.clients_name_ip={}

    def exit(self, returnCode: int = ...) -> None:
        self.udp_server.close()

    # 监听客户端链接
    def get_conn(self):
        while True:
            client,address=self.server.accept()
            print("TCP " + address[0] + "：" + str(address[1]))
            data="与服务器链接成功，请输入昵称才可以聊天"
            # server与client通信，send() decode
            client.send(data.encode())
            # 链接用户添加到服务器的用户列表
            self.tcp_client_sin.emit("%s:%s"%(address[0],address[1]),client)
            self.clients.append(client)
            Thread(target=self.get_msg,args=(client,self.clients,self.clients_name_ip,address)).start()

    def get_msg(self):
        while self.udp_server:
            data,address = self.udp_server.recvfrom(65535)
            data =data.decode()
            logger.debug(data)
            if data:
                self.udp_client_sin.emit("UDP", address[0], address[1],None)
                addr = "UDP " + address[0] + "：" + str(address[1])
                self.tcp_get_msg_sin.emit(addr,data)
                #logger.debug(data)

                # length = len(threading.enumerate())
                # print('当前运行的线程数为：%d' % length)
                # if length <= 1:
                #     break
            else:
                break

        logger.debug(address)
        logger.debug("close error")

    def send_msg(self, address,port, msg):
        msg = msg.encode()
        if self.udp_server:
            self.udp_server.sendto(msg,(address,port))

        #接受消息


    def client_close(self,client):
        client.close()
        #     匿名类，线程处理,发送是一个线程，接受是一个线程

    def run(self):

        try:
            self.udp_server = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM,0)
            self.udp_server.bind(self.addrinfo[-1])
            logger.debug(self.addrinfo[-1])
            logger.debug("udp_server start")
            Thread(target=self.get_msg).start()

        except Exception as e:
            logger.debug(e)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    screenshot = SocketTools()
    screenshot.show()
    sys.exit(app.exec_())




