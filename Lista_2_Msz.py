import sys
import ctypes
import socket
import platform
import urllib.request  # Dodano '.request' do 'urllib'
import psutil
import os
import PyQt5.QtWidgets as QtWidgets
import wmi


class ComputerInfoApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Informacje o Komputerze")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #AFE3E9;")  # Tło w kolorze jasno-turkusowym

        self.text_view = QtWidgets.QTextEdit(self)
        self.text_view.setGeometry(10, 10, 380, 200)

        self.button1 = QtWidgets.QPushButton("Komputer", self)
        self.button1.setGeometry(10, 220, 70, 30)
        self.button1.setStyleSheet("background-color: red; color: white;")  # Kolor Czerwony

        self.button2 = QtWidgets.QPushButton("System", self)
        self.button2.setGeometry(90, 220, 70, 30)
        self.button2.setStyleSheet("background-color: yellow;")  # Kolor Zółty

        self.button3 = QtWidgets.QPushButton("Proxy", self)
        self.button3.setGeometry(170, 220, 70, 30)
        self.button3.setStyleSheet("background-color: green; color: white;")  # Kolor Zielony

        self.button4 = QtWidgets.QPushButton("BIOS", self)
        self.button4.setGeometry(250, 220, 70, 30)
        self.button4.setStyleSheet("background-color: blue; color: white;")  # Kolor Niebieski

        self.button5 = QtWidgets.QPushButton("Host Name", self)
        self.button5.setGeometry(330, 220, 70, 30)
        self.button5.setStyleSheet("background-color: purple; color: white;")  # Kolor Fioletowy

        self.button1.clicked.connect(self.get_network_info)
        self.button2.clicked.connect(self.get_system_info)
        self.button3.clicked.connect(self.get_proxy_info)
        self.button4.clicked.connect(self.get_bios_version)
        self.button5.clicked.connect(self.get_host_name)

    def get_network_info(self):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        is_wifi = "Wi-Fi" in psutil.net_if_stats()
        connection_type = "Wi-Fi" if is_wifi else "Ethernet"

        message = f"Moje Ipv4: {ip_address}\nCzy jest statyczne/dynamiczne:  Brak danych\nWi-Fi/Ethernet: {connection_type}"
        self.text_view.setPlainText(message)

    def get_system_info(self):
        system_info = platform.uname()
        cpu_cores = os.cpu_count()
        ram_info = psutil.virtual_memory()

        message = f"Wersja systemu operacyjnego: {system_info.system} {system_info.release}\nTyp systemu: {system_info.machine}\nLiczba rdzeni: {cpu_cores}\nPamięć RAM: {ram_info.total / (1024 ** 3):.2f} GB"
        self.text_view.setPlainText(message)

    def get_proxy_info(self):
        proxy_handler = urllib.request.ProxyHandler()
        opener = urllib.request.build_opener(proxy_handler)

        try:
            opener.open("http://www.google.com", timeout=5)
            is_proxy_enabled = True
        except Exception:
            is_proxy_enabled = False

        if is_proxy_enabled:
            proxy_status = "Proxy is enabled"
        else:
            proxy_status = "Proxy is disabled"

        message = f"Czy jest uruchomione Proxy: {proxy_status}"
        self.text_view.setPlainText(message)

    def get_bios_version(self):
        c = wmi.WMI()
        bios = c.Win32_BIOS()[0]
        result = f"BIOS Vendor: {bios.Manufacturer}\nBIOS Version: {bios.Version}\nBIOS Release Date: {bios.ReleaseDate}"
        self.text_view.setPlainText(result)

    def get_host_name(self):
        hostname = socket.gethostname()
        message = f"Host Name: {hostname}"
        self.text_view.setPlainText(message)


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ComputerInfoApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
