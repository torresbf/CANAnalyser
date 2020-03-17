
from can_analyzer_ui import Ui_MainWindow
from serial_port import PortaSerial
from can_message import CanMessage
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QMessageBox
import numpy as np
import pyqtgraph as pg
from time import sleep, time
import serial


class Analyzer():

    def __init__(self, ui, port):
        self.ui = ui
        self.portaSerial = port

    # Inicializa o programa
    def start_program(self):
        # abre e configura a porta serial utilizando os valores definidos
        try:
            # Pega baud rate e porta dainterface
            baudrate = ui.comboBox_Baudrate.currentText()
            portName = ui.comboBox_SerialPorts.currentText()
            self.portaSerial.config_port(baudrate=2000000, portName=portName, timeout=1)
            #print(porta.is_open)
            self.portaSerial.open_port()
            sleep(2)

            # Inicia programa principal
            self.program()

        except serial.serialutil.SerialException:
            dlg = QMessageBox(None)
            dlg.setWindowTitle("Error!")
            dlg.setIcon(QMessageBox.Warning)
            dlg.setText(
                "<center>Failed to receive data!<center> \n\n <center>Check Serial Ports and Telemetry System.<center>")
            dlg.exec_()

    # Atualiza portas seriais disponiveis
    def update_ports(self):
        self.ui.comboBox_SerialPorts.clear()
        self.ui.comboBox_SerialPorts.addItems(self.portaSerial.list_ports())

    def displayErrorMessage(self, text):
        dlg = QMessageBox(None)
        dlg.setWindowTitle("Error!")
        dlg.setIcon(QMessageBox.Warning)
        dlg.setText(
         "<center>" + text + "<center>")
        dlg.exec_()

    # Programa principal, roda continuamente
    def program(self):
        try:
            if self.portaSerial.readAvailable:
                # Le conjunto de dados da porta serial
                read_buffer, command = self.portaSerial.read_buffer(['T', 't'], 40)
                msg = CanMessage(read_buffer, command)
                msg.print_msg()
                #print(read_buffer[0:8])
        finally:
            # Chama de novo funcao prgram() depois de update_time segundos
            QtCore.QTimer.singleShot(update_time, self.program)


# Roda janela
app = QtWidgets.QApplication(sys.argv)
app.setStyle("fusion")
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

porta = PortaSerial()
canAnalyzer = Analyzer(ui, porta)


# Conecta sinal do botao com a funcao respectiva
ui.comboBox_SerialPorts.addItems(porta.list_ports())  # mostra as portas seriais disponíveis
ui.pushButton_UpdatePorts.clicked.connect(canAnalyzer.update_ports)  # botão para atualizar as portas seriis disponíveis
ui.pushButton_StartProgram.clicked.connect(canAnalyzer.start_program)  # botão para iniciar o programa

# Pega update time da interface
update_time = ui.doubleSpinBox_UpdateTime.value() * 1000

# Mostra a janela e fecha o programa quando ela é fechada (?)
MainWindow.show()
sys.exit(app.exec_())
