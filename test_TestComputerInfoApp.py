import os

import psutil
import pytest
from unittest.mock import patch, Mock
import io

from PyQt5.Qt import QTest
from PyQt5.QtCore import Qt
from Lista_2_Msz import ComputerInfoApp

@pytest.fixture
def app(qtbot):
    app = ComputerInfoApp()
    app.show()
    qtbot.addWidget(app)  # Użyj qtbot do zarządzania widgetem
    yield app
    app.close()

def test_get_network_info(app, qtbot):
    with patch("socket.gethostname", return_value="testhostname"), \
         patch("socket.gethostbyname", return_value="192.168.1.1"), \
         patch("psutil.net_if_stats", return_value={"Wi-Fi": {}}):
        QTest.mouseClick(app.button1, Qt.LeftButton)
        expected_output = "Moje Ipv4: 192.168.1.1\nCzy jest statyczne/dynamiczne:  Brak danych\nWi-Fi/Ethernet: Ethernet"
        qtbot.wait(500)  # Poczekaj chwilę na odświeżenie interfejsu
        assert app.text_view.toPlainText() == expected_output

def test_get_system_info(app, qtbot):
    with patch("platform.uname", return_value=("TestSystem", "TestRelease", "TestMachine", "TestVersion", "TestNode")), \
         patch("os.cpu_count", return_value=4), \
         patch("psutil.virtual_memory", return_value=psutil.virtual_memory(total=8589934592)):
        QTest.mouseClick(app.button2, Qt.LeftButton)
        expected_output = "Wersja systemu operacyjnego: TestSystem TestRelease\nTyp systemu: TestMachine\nLiczba rdzeni: 4\nPamięć RAM: 8.00 GB"
        qtbot.wait(500)
        assert app.text_view.toPlainText() == expected_output

def test_get_proxy_info(app, qtbot):
    with patch("urllib.request.ProxyHandler"), \
         patch("urllib.request.build_opener") as mock_build_opener, \
         patch("urllib.request.OpenerDirector") as mock_opener:
        mock_opener.open.return_value = io.BytesIO(b"Test response")

        QTest.mouseClick(app.button3, Qt.LeftButton)
        expected_output = "Czy jest uruchomione Proxy: Proxy is enabled"
        qtbot.wait(500)
        assert app.text_view.toPlainText() == expected_output

def test_get_bios_version(app, qtbot):
    with patch("wmi.WMI") as mock_wmi:
        mock_bios = mock_wmi.return_value.Win32_BIOS.return_value
        mock_bios.Manufacturer = "TestManufacturer"
        mock_bios.Version = "TestVersion"
        mock_bios.ReleaseDate = "TestReleaseDate"

        QTest.mouseClick(app.button4, Qt.LeftButton)
        expected_output = "BIOS Vendor: TestManufacturer\nBIOS Version: TestVersion\nBIOS Release Date: TestReleaseDate"
        qtbot.wait(500)
        assert app.text_view.toPlainText() == expected_output

def test_get_host_name(app, qtbot):
    with patch("socket.gethostname", return_value="TestHostname"):
        QTest.mouseClick(app.button5, Qt.LeftButton)
        expected_output = "Host Name: TestHostname"
        qtbot.wait(500)
        assert app.text_view.toPlainText() == expected_output
