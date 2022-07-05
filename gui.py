from ast import Pass
from cgi import test
import os
import sys
import base64

from tkinter import E, scrolledtext
from winreg import SetValue
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget, QScrollArea, QDockWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize
from PIL import Image
from pathlib import Path

from util.generate_image import generateImage
from nn.chat import chat

pixmap = "" 
        
class Ui_MainWindow(object):                                                     
    def setupUi(self, MainWindow, firstSetup):
        # Create main window
        MainWindow.setObjectName("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Create chat label
        self.lblChat = QtWidgets.QTextEdit(self.centralwidget)
        self.lblChat.setAutoFillBackground(False)
        self.lblChat.setObjectName("lblChat")
        self.lblChat.setAlignment(Qt.AlignBottom)
        # self.lblChat.setWordWrap(True)
        self.lblChat.setGeometry(QtCore.QRect(20, 70, 750, 410))
        self.lblChat.setReadOnly(True)
        self.lblChat.setFontPointSize(12)
        self.lblChat.setAlignment(QtCore.Qt.AlignBottom)
        
        # Create input button
        self.btnSend = QtWidgets.QPushButton(self.centralwidget)
        self.btnSend.setObjectName("btnSend")
        
        # Create input text box
        self.tbInput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.tbInput.setObjectName("tbInput")
        
        
        # Create agent image
        self.lblImage = QtWidgets.QLabel(self.centralwidget)
        self.lblImage.setObjectName("lblImage")
        self.lblImage.setGeometry(QtCore.QRect(20, 10, 55, 55))
        
        # Create agent name label
        self.lblName = QtWidgets.QLabel(self.centralwidget)
        self.lblName.setObjectName("lblName")
        self.lblName.setGeometry(QtCore.QRect(90, 10, 241, 61)) 
        self.lblName.setText("Place holder")      
                
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow, firstSetup)
        
    def retranslateUi(self, MainWindow, firstSetup):           
        _translate = QtCore.QCoreApplication.translate      
        MainWindow.setWindowTitle(_translate("MainWindow", "Generic Inc. Chat"))
        self.btnSend.setText(_translate("MainWindow", "SEND"))
        self.tbInput.setPlaceholderText(_translate("MainWindow", "Please enter your message."))
        self.lblImage.setText(_translate("MainWindow", "Placeholder"))
        
        generator_returns = generateImage()
        image = Image.open(generator_returns[0])
        new_image = image.resize((55, 55))
        new_image.save(generator_returns[0])  
        pixmap = QPixmap(generator_returns[0])
        self.lblImage.setPixmap(pixmap)
        os.remove(generator_returns[0])  
        self.lblImage.setGeometry(QtCore.QRect(20, 10, 55, 55))
        self.lblName.setGeometry(QtCore.QRect(90, 10, 241, 61))
        self.btnSend.setGeometry(QtCore.QRect(662, 500, 111, 41))
        self.tbInput.setGeometry(QtCore.QRect(20, 500, 621, 41))
        
        self.lblName.setText(generator_returns[0][:-4])
        
        self.lblChat.setText(str(generator_returns[1] + ": Hello. My name is " + str(generator_returns[1]) + "." + \
            " How can I help you today?"))
        
        app.setStyleSheet("QLabel{font-size: 12pt;}")
        
        # connect button to function on_click
        self.btnSend.clicked.connect(lambda: self.on_click())
        

    def on_click(self):
        censor = False
        chat_input = str(self.tbInput.toPlainText())
        
        holder = str(self.lblChat.toHtml()).count('<p ')
        
        data = open("blacklist.txt", "r").read()
        blacklist_dc = str(base64.b64decode(data))
        blacklist = blacklist_dc.split(r"\n")
        
        for word in chat_input.split():
            if word.lower() in blacklist:
                chat_input = chat_input.replace(word, "*" * len(word))
                censor = True
         
        if censor == True:       
            self.lblChat.setText(str(self.lblChat.toHtml()) + "<p align='right'>" + "You: " + chat_input + "</p>")
            
            font = QtGui.QFont()
            font.setPointSize(12)
            self.lblChat.setFont(font)
            self.lblChat.setText(str(self.lblChat.toHtml()) + "<p align='left'>" + str(self.lblName.text()) + ": Please mind your langauge" + \
                "</p>")
            self.tbInput.setPlainText("")
        else:
            self.lblChat.setText(str(self.lblChat.toHtml()) + "<p align='right'>" + "You: " + chat_input + "</p>")
            font = QtGui.QFont()
            font.setPointSize(12)
            self.lblChat.setFont(font)
            
            chat_returns = chat(chat_input)
            
            if chat_returns[0] == "goodbye":
                self.lblChat.setText(str(self.lblChat.toHtml()) + "<p align='left'>" + str(self.lblName.text()) + ": " + chat_returns[1] + "</p>")
                self.tbInput.setPlainText("")
                self.tbInput.setReadOnly(True)
                self.tbInput.setPlaceholderText("Please exit the program")
            elif chat_returns[0] == "name":
                self.lblChat.setText(str(self.lblChat.toHtml()d) + "<p align='left'>" + str(self.lblName.text()) + ": " + chat_returns[1].format(str(self.lblName.text())) + "</p>")
                self.tbInput.setPlainText("")
            else:
                self.lblChat.setText(str(self.lblChat.toHtml()) + "<p align='left'>" + str(self.lblName.text()) + ": " + chat_returns[1] + "</p>")
                self.tbInput.setPlainText("")
            
            font = QtGui.QFont()
            font.setPointSize(12)
            self.lblChat.setFont(font)

class Window(QtWidgets.QMainWindow):
    def  __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)
        self.setWindowTitle("TEST")
        self.setFixedSize(800, 601)
        ui = Ui_MainWindow()
        ui.setupUi(self, True)

if __name__ == "__main__":
    import sys
    os.chdir(Path(__file__).parent)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Window()
    MainWindow.show()
    sys.exit(app.exec_())