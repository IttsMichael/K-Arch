#!/usr/bin/env python

import sys
import os
import json
import subprocess
from style import apply_style
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
base_dir = os.path.dirname(os.path.abspath(__file__))

page = 0

disks = []
layouts = []

datadisk = subprocess.check_output(
    ["lsblk", "-dn", "-o", "NAME,MODEL,SIZE,TYPE", "-J"],
    text=True
)

timezones = subprocess.check_output(
    ["timedatectl", "list-timezones"],
    text=True).splitlines()

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

#test

def savedisk():
    idxdisks = window.comboDisk.currentIndex()
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
    # subprocess.run(["bash", "/usr/local/share/bash/partitionscript"], check=True)

def layout_format():
    window.comboLayout.clear()

    with open("/usr/share/X11/xkb/rules/base.lst", encoding="utf-8") as f:
        in_layouts = False
        for line in f:
            line = line.strip()
            if line.startswith("! layout"):
                in_layouts = True
                continue
            if line.startswith("!") and in_layouts:
                break
            if in_layouts and line:
                parts = line.split(None, 1)
                if len(parts) == 2:
                    code, name = parts
                    layouts.append((name, code))
                    window.comboLayout.addItem(f"{name} — {code}", code)


def save_time():
    layout_code = window.comboLayout.currentData()
    idxtime = window.comboZone.currentText()
    print(layout_code)
    subprocess.run(["localectl", "set-x11-keymap", layout_code], check=True)

    if layout_code in ("us", "de", "fr", "uk", "es", "it"):
        subprocess.run(["localectl", "set-keymap", layout_code], check=True)

    subprocess.run(["timedatectl", "set-timezone", idxtime], check=True)

def next_clicked():
    print("next was clicked")
    global page
    page += 1
    if page == 1:
        print("page1")
        page1()
    elif page == 2:
        print("page2")
        page2()

def on_save_clicked():
    save_time()
    next_clicked()

def page1():
    layout_format()
    window.savetime.clicked.connect(on_save_clicked)
    window.stackedWidget.setCurrentIndex(1)
    window.comboZone.addItems(timezones)
    window.savetime.clicked.connect(save_time)

def page2():
    window.stackedWidget.setCurrentIndex(2)
    window.comboDisk.addItems(d[0] for d in disks)
    window.savedisks.clicked.connect(savedisk)


app = QApplication(sys.argv)
file = QFile(os.path.join(base_dir, "installer.ui"))
file.open(QFile.ReadOnly)


loader = QUiLoader()
window = loader.load(file)
file.close()

apply_style(window)

window.swapCheck.toggled.connect(toggle_swap)
toggle_swap(window.swapCheck.isChecked())
next_btn = window.findChild(QPushButton, "nextButton")
next_btn.clicked.connect(next_clicked)

window.show()
window.stackedWidget.setCurrentIndex(0)
sys.exit(app.exec())


    

