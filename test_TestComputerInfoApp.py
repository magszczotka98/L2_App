import os
import psutil
import pytest
import io
from unittest.mock import patch, Mock
from PyQt5.Qt import QTest
from PyQt5.QtCore import Qt
from Lista_2_Msz import ComputerInfoApp
from unittest.mock import MagicMock
from unittest.mock import patch, Mock
from PyQt5.Qt import QTest
from PyQt5.QtCore import Qt
from Lista_2_Msz import ComputerInfoApp
from unittest.mock import patch
from unittest.mock import patch, MagicMock

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
        expected_output = "Moje Ipv4: 192.168.1.1\nCzy jest statyczne/dynamiczne:  Brak danych"
        qtbot.wait(500)  # Poczekaj chwilę na odświeżenie interfejsu
        assert expected_output in app.text_view.toPlainText()

def test_get_system_info(app, qtbot):
    with patch("platform.uname", return_value=("TestSystem", "TestRelease", "TestMachine", "TestVersion", "TestNode")), \
         patch("os.cpu_count", return_value=4), \
         patch("psutil.virtual_memory", return_value=MagicMock(total=8589934592)):  # Use MagicMock to set total attribute
        QTest.mouseClick(app.button2, Qt.LeftButton)
        expected_output = "Wersja systemu operacyjnego: TestSystem TestMachine\nTyp systemu: TestNode\nLiczba rdzeni: 4\nPamięć RAM: 8.00 GB"
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
    with patch("Lista_2_Msz.wmi.WMI") as mock_wmi:

        mock_bios = MagicMock()
        mock_bios.Manufacturer = "TestManufacturer"
        mock_bios.Version = "TestVersion"
        mock_bios.ReleaseDate = "TestReleaseDate"

        mock_wmi_instance = mock_wmi.return_value
        mock_wmi_instance.Win32_BIOS = MagicMock(return_value=[mock_bios])

        QTest.mouseClick(app.button4, Qt.LeftButton)

        actual_output = app.text_view.toPlainText()

        expected_output = f"BIOS Vendor: TestManufacturer\nBIOS Version: TestVersion\nBIOS Release Date: TestReleaseDate"
        assert actual_output == expected_output

def test_get_host_name(app, qtbot):
    with patch("socket.gethostname", return_value="TestHostname"):
        QTest.mouseClick(app.button5, Qt.LeftButton)
        expected_output = "Host Name: TestHostname"
        qtbot.wait(500)
        assert app.text_view.toPlainText() == expected_output
