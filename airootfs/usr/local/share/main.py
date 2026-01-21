#!/usr/bin/env python

import sys
import os
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
base_dir = os.path.dirname(os.path.abspath(__file__))
ui_path = os.path.join(base_dir, "installer.ui")

page = 0

def next_clicked():
    print("next was clicked")
    global page
    page += 1
    if page == 1:
        page1()
    
    

def page1():
    window.head.setText("Partitioning")
    with open(os.path.join(base_dir, "text", "page1.html"), "r", encoding="utf-8") as f:
        window.info.setText(f.read())

app = QApplication(sys.argv)

file = QFile(ui_path)
file.open(QFile.ReadOnly)

loader = QUiLoader()
window = loader.load(file)
file.close()

next_btn = window.findChild(QPushButton, "nextButton")
next_btn.clicked.connect(next_clicked)

window.show()
sys.exit(app.exec())


    

