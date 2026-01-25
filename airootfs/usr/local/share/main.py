#!/usr/bin/env python

import sys
import os
import json
import subprocess
import threading
from style import apply_style
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt

base_dir = os.path.dirname(os.path.abspath(__file__))

page = 0
wifi_status = "Disconnected"
disks = []
layouts = []
subprocess.run(["systemctl", "start", "NetworkManager"], check=True)
connected = False

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
    
    def run_partition():
        next_clicked()
        
        idxdisks = window.comboDisk.currentIndex()
        pathdisk = disks[idxdisks][1]
        root_size = window.spinRoot.value()
        swap_enabled = window.swapCheck.isChecked()
        swap_size = window.spinSwap.value() if swap_enabled else 0
        swapyn = "y" if swap_enabled else "n"
        vars_path = os.path.join(base_dir, "disk.sh")

        try:
            with open(vars_path, "w", encoding="utf-8") as f:
                f.write(f'TARGET_DISK="{pathdisk}"\n')
                f.write(f'rootsize="{root_size}"\n')
                f.write(f'swapyn="{swapyn}"\n')
                f.write(f'swapsize="{swap_size}"\n')
                f.write("export TARGET_DISK rootsize swapyn swapsize\n")
            # subprocess.run(["bash", "/usr/local/share/bash/partitionscript"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error setting time/layout: {e}")
            
    threading.Thread(target=run_partition, daemon=True).start()
    
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
    
    def run_commands():
        try:
            if layout_code in ("us", "de", "fr", "uk", "es", "it"):
                subprocess.run(["localectl", "set-keymap", layout_code], check=True)
            
            subprocess.run(["timedatectl", "set-timezone", idxtime], check=True)
            print("Time and layout updated.")
        except subprocess.CalledProcessError as e:
            print(f"Error setting time/layout: {e}")

    threading.Thread(target=run_commands, daemon=True).start()

def next_clicked():
    print("next was clicked")
    global page
    page += 1
    print(page)
    if page == 1:
        print("page1")
        page1()
    elif page == 2:
        print("page2")
        page2()
    elif page == 3:
        print("page3")
        page3()
    elif page == 4:
        print("page4")
        window.stackedWidget.setCurrentIndex(4)
    elif page == 5:
        print("page5")
        page5()

def on_save_clicked():
    save_time()
    next_clicked()

def disconnect_wifi():
    subprocess.run(
        ["nmcli", "device", "disconnect", "wlan0"],
        check=True
    )
    page3()

def connect_wifi():
    
    item = window.wifiList.currentItem()
    if not item:
        return

    data = item.data(Qt.UserRole)
    ssid = data["ssid"]
    secure = data["secure"]
    password = window.passwordWifi.text().strip()

    if secure and not password:
        window.labelStatusWifi.setText("Password required")
        return

    window.labelStatusWifi.setText("Connecting...")
    window.connect_button.setEnabled(False)

    def run_connection():
        try:

            if secure:
                subprocess.run([
                    "nmcli", "connection", "add",
                    "type", "wifi", "ifname", "*",
                    "con-name", ssid, "ssid", ssid,
                    "wifi-sec.key-mgmt", "wpa-psk",
                    "wifi-sec.psk", password
                ], check=True)

                subprocess.run(["nmcli", "connection", "up", ssid], check=True)
            else:
                subprocess.run(["nmcli", "device", "wifi", "connect", ssid], check=True)
            
            print(f"Successfully connected to {ssid}")
            window.labelStatusWifi.setText("Connected")
            window.connect_button.setEnabled(True)
            page3()
            global connected
            connected = True
            print(connected)
            
        except subprocess.CalledProcessError:
            QTimer.singleShot(0, lambda: window.labelStatusWifi.setText("Connection Failed"))

    threading.Thread(target=run_connection, daemon=True).start()

def log_item():
    item = window.wifiList.currentItem()
    if item:
        print(f"User clicked: {item.text()}")
        window.passwordWifi.setEnabled(True)


def toggle_ethernet(enabled = bool):
    window.passwordWifi.setEnabled(not enabled)
    window.refreshn.setEnabled(not enabled)
    window.wifiList.setEnabled(not enabled)
    window.connect_button.setEnabled(not enabled)
    
    if enabled == True:
        command = 'nmcli device | grep "ethernet" | awk \'{print $1}\' | head -n 1'

        devicelan = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True
        )

        devicelan = devicelan.stdout.strip()
        print(f"Device found: {devicelan}")

        subprocess.run(["nmcli", "device", "connect", devicelan], check=True)

        global connected
        connected = True
        print(connected)


def next_internet():
    global connected
    if connected == True:
        page == 5
        window.stackedWidget.setCurrentIndex(5)
    else:
        next_clicked()

def back_wifi():
    global page
    page = 3
    window.stackedWidget.setCurrentIndex(3)
        


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


def page3():
    global wifi_status
    window.stackedWidget.setCurrentIndex(3)
    window.wifiList.clear()
    status = subprocess.check_output(
    ["nmcli", "-t", "-f", "STATE", "general"],
    text=True
)    
    window.labelStatusWifi.setText(status.capitalize())
    wifi_status = window.labelStatusWifi.setText(status.capitalize())
    wifilist = subprocess.check_output(
    ["nmcli", "-t", "-f", "IN-USE,SSID,SECURITY,SIGNAL", "device", "wifi", "list"],
    text=True
)
    for line in wifilist.splitlines():
        in_use, ssid, security, signal = line.split(":", 3)        
        lock = "🔒" if security != "--" else "🔓"
        text = f"{ssid}  {lock}  {signal}%"

        if in_use == "*":
            connected_icon = " ✅"
        else:
            connected_icon = ""

        item = QListWidgetItem(text)
        item.setData(Qt.UserRole, {
            "ssid": ssid,
            "secure": security != "--"
        })

        item.setText(text + connected_icon)
        window.wifiList.addItem(item)

def page5():
    window.stackedWidget.setCurrentIndex(4)





app = QApplication(sys.argv)
file = QFile(os.path.join(base_dir, "installer.ui"))
file.open(QFile.ReadOnly)


loader = QUiLoader()
window = loader.load(file)
file.close()

apply_style(window)
window.wifiList.itemSelectionChanged.connect(log_item)

window.next4.clicked.connect(next_clicked)
window.cancelInternet.clicked.connect(back_wifi)
window.nextInternet.clicked.connect(next_internet)
window.connect_button.clicked.connect(connect_wifi)
window.refreshn.clicked.connect(page3)
window.swapCheck.toggled.connect(toggle_swap)
window.ethernetCheck.toggled.connect(toggle_ethernet)
toggle_swap(window.swapCheck.isChecked())
next_btn = window.findChild(QPushButton, "nextButton")
next_btn.clicked.connect(next_clicked)

window.show()
window.stackedWidget.setCurrentIndex(0)
sys.exit(app.exec())


    

