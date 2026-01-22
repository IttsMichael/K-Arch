#!/usr/bin/env python

import sys
import os
import subprocess
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
base_dir = os.path.dirname(os.path.abspath(__file__))

page = 0


disks = []
for line in subprocess.check_output(["lsblk", "-dn", "-o", "NAME,TYPE"], text = True).splitlines():
    name, typ = line.split()
    if typ == "disk":
        disks.append("/dev/" + name)

def saved():
    disk = window.comboBox.currentText()
    with open("./disk.sh", "w") as f:
        f.write("TARGET_DISK=" + disk + "\n")

def next_clicked():
    print("next was clicked")
    global page
    page += 1
    if page == 1:
        page1()
    

def page1():
    window.stackedWidget.setCurrentIndex(1)
    window.comboBox.addItems(disks)
    window.savedisks.clicked.connect(saved)


app = QApplication(sys.argv)

file = QFile(os.path.join(base_dir, "installer.ui"))
file.open(QFile.ReadOnly)


loader = QUiLoader()
window = loader.load(file)
file.close()

next_btn = window.findChild(QPushButton, "nextButton")
next_btn.clicked.connect(next_clicked)

window.show()
window.stackedWidget.setCurrentIndex(0)
sys.exit(app.exec())


    

