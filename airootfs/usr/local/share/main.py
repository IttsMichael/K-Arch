#!/usr/bin/env python

import sys
import os
import json
import subprocess
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
base_dir = os.path.dirname(os.path.abspath(__file__))

page = 0

disks = []

datadisk = subprocess.check_output(
    ["lsblk", "-dn", "-o", "NAME,MODEL,SIZE,TYPE", "-J"],
    text=True
)

for dev in json.loads(datadisk)["blockdevices"]:
    if dev ["type"] == "disk":
        model = dev["model"] or "Unknown device"
        model = model.replace("_", " ").strip()
        size = dev["size"]
        name = dev["name"]

        displaydisk = f"{model} ({size}) - /dev/{name}"
        pathdisk = f"/dev/{name}"

        disks.append((displaydisk, pathdisk))

def toggle_swap(enabled: bool):
    window.spinSwap.setEnabled(enabled)


def saved():
    idxdisks = window.comboBox.currentIndex()
    pathdisk = disks[idxdisks][1]
    root_size = window.spinRoot.value()
    swap_enabled = window.swapCheck.isChecked()
    swap_size = window.spinSwap.value() if swap_enabled else 0
    swapyn = "y" if swap_enabled else "n"
    vars_path = os.path.join(base_dir, "disk.sh")
    with open(vars_path, "w", encoding="utf-8") as f:
        f.write(f'TARGET_DISK="{pathdisk}"\n')
        f.write(f'rootsize="{root_size}"\n')
        f.write(f'swapyn="{swapyn}"\n')
        f.write(f'swapsize="{swap_size}"\n')
        f.write("export TARGET_DISK rootsize swapyn swapsize\n")
    subprocess.run(["bash", "/usr/local/share/bash/partitionscript"], check=True)

def next_clicked():
    print("next was clicked")
    global page
    page += 1
    if page == 1:
        page1()
    

def page1():
    window.stackedWidget.setCurrentIndex(1)
    window.comboBox.addItems(d[0] for d in disks)
    window.savedisks.clicked.connect(saved)


app = QApplication(sys.argv)
file = QFile(os.path.join(base_dir, "installer.ui"))
file.open(QFile.ReadOnly)


loader = QUiLoader()
window = loader.load(file)
file.close()

window.swapCheck.toggled.connect(toggle_swap)
toggle_swap(window.swapCheck.isChecked())
next_btn = window.findChild(QPushButton, "nextButton")
next_btn.clicked.connect(next_clicked)

window.show()
window.stackedWidget.setCurrentIndex(0)
sys.exit(app.exec())


    

