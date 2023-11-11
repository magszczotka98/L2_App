import pytest
from PyQt5.QtCore import Qt  # Dodaj ten import
from PyQt5.QtTest import QTest
from Lista_2_Msz import ComputerInfoApp

@pytest.fixture
def app(qtbot):
    app = ComputerInfoApp()
    qtbot.addWidget(app)
    return app

def test_get_network_info(app, qtbot):
    # Kliknij przycisk "Komputer"
    QTest.mouseClick(app.button1, Qt.LeftButton)
    
    # Sprawdź treść text_view
    assert "Moje Ipv4" in app.text_view.toPlainText()
    assert "Wi-Fi/Ethernet" in app.text_view.toPlainText()

def test_get_system_info(app, qtbot):
    # Kliknij przycisk "System"
    QTest.mouseClick(app.button2, Qt.LeftButton)
    
    # Sprawdź treść text_view
    assert "Wersja systemu operacyjnego" in app.text_view.toPlainText()
    assert "Liczba rdzeni" in app.text_view.toPlainText()

def test_get_proxy_info(app, qtbot):
    # Kliknij przycisk "Proxy"
    QTest.mouseClick(app.button3, Qt.LeftButton)
    
    # Sprawdź treść text_view
    assert "Czy jest uruchomione Proxy:" in app.text_view.toPlainText()
    assert "Proxy is enabled" in app.text_view.toPlainText() or "Proxy is disabled" in app.text_view.toPlainText()

def test_get_bios_version(app, qtbot):
    # Kliknij przycisk "BIOS"
    QTest.mouseClick(app.button4, Qt.LeftButton)
    
    # Sprawdź treść text_view
    assert "BIOS Vendor:" in app.text_view.toPlainText()
    assert "BIOS Version:" in app.text_view.toPlainText()
    assert "BIOS Release Date:" in app.text_view.toPlainText()

def test_get_host_name(app, qtbot):
    # Kliknij przycisk "Host Name"
    QTest.mouseClick(app.button5, Qt.LeftButton)
    
    # Sprawdź treść text_view
    assert "Host Name:" in app.text_view.toPlainText()
