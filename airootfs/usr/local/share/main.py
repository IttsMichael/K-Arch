#!/usr/bin/env python
#a
import subprocess
from uuid import RESERVED_MICROSOFT
import subprocess
import sys
import os
import json
import threading
from style import apply_style
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QMovie

base_dir = os.path.dirname(os.path.abspath(__file__))
spinner_path = os.path.join(base_dir, "images", "spinner.gif")
drivers = " "
page = 0
wifi_status = "Disconnected"
disks = []
layouts = []
subprocess.run(["systemctl", "start", "NetworkManager"], check=True)
connected = False
gpu_command = ""
user = "root"
password = "root"
sudo = True
installing = False
dev = False
gaming = False
template = False
useryn = False



datadisk = subprocess.check_output(
    ["lsblk", "-dn", "-o", "NAME,MODEL,SIZE,TYPE", "-J"],
    text=True
)

timezones = subprocess.check_output(
    ["timedatectl", "list-timezones"],
    text=True).splitlines()

for device in json.loads(datadisk)["blockdevices"]:
    if device ["type"] == "disk":
        model = device["model"] or "Unknown device"
        model = model.replace("_", " ").strip()
        size = device["size"]
        name = device["name"]

        displaydisk = f"{model} ({size}) - /dev/{name}"
        pathdisk = f"/dev/{name}"

        disks.append((displaydisk, pathdisk))


def install():
    global installing
    installing = True
    window.installStatus.setText("Installing packages...")
    global drivers
    global template
    global gaming
    global dev
    add = ""
    if template == True:
        if dev == True:
            add = "git wget curl docker docker-compose neovim tmux vim python npm go rustup ripgrep fzf htop zsh"

    print("Starting base installation...")
    base_cmd = ["pacstrap", "-K", "/mnt", "base", "linux-cachyos", "linux-firmware", "linux-cachyos-headers", "base-devel",
    "networkmanager", "vim", "plasma-desktop", "sddm", "firefox", "konsole", "dolphin", "fastfetch", "imagemagick", "karch-updater"]
    full_command = base_cmd + drivers.split() + add.split()
    
    try:
        installation = subprocess.run(full_command, capture_output=False, check=True)

        if gaming == True:
            print("Enabling multilib...")    
            sed_script = r'/^# *\[multilib\]/,/^# *Include/ s/^# *//'

            sed_cmd = [
                "sed", "-i", 
                sed_script, 
                "/mnt/etc/pacman.conf"
            ]

            try:
                subprocess.run(sed_cmd, check=True)
                print("Multilib enabled successfully.")
                print("Installing gaming packages...")
                subprocess.run(["pacstrap", "-K", "/mnt", "steam", "wine",  "giflib",
                "lutris", "discord", "openrgb", "gamemode"])
            except subprocess.CalledProcessError:
                print("Error: Could not modify pacman.conf. Check if /mnt is mounted.")

        
        print("Generating fstab...")
        window.installStatus.setText("Generating fstab...")
        with open("/mnt/etc/fstab", "w") as fstab_file:
            subprocess.run(["genfstab", "-U", "/mnt"], stdout=fstab_file, check=True)
            
        window.installStatus.setText("Copying installer scripts...")
        print("Copying installer scripts...")
        bash_dir = os.path.join(base_dir, "bash")
        subprocess.run(["bash", os.path.join(bash_dir, "copyscripts")], check=True)
        
        window.installStatus.setText("Post install configuration...")
        print("Running post-install configuration...")
        make_user()
        save_time()
        
        window.installStatus.setText("Installing bootloader...")
        print("Installing bootloader...")
        subprocess.run(["arch-chroot", "/mnt", "/usr/local/bin/installgrub"], check=True)

        window.installStatus.setText("Enabling display manager...")
        print("enabling display manager")
        subprocess.run(["arch-chroot", "/mnt", "systemctl", "enable", "sddm"], check=True)

        window.installStatus.setText("Enabling network manager...")
        print("enabling network manager")
        subprocess.run(["arch-chroot", "/mnt", "systemctl", "enable", "NetworkManager"], check=True)
        
        print("Installation finished successfully!")
        next_clicked()
        window.installButton.setEnabled(True)

        
        
    except subprocess.CalledProcessError as e:
        print(f"Installation Failed: {e}")

def make_user():
    global user
    global useryn
    global password
    root_pass = "root"
    if useryn == True:
        window.installStatus.setText("Creating user " + user)
        print(f"Creating user {user}...")
        subprocess.run(["arch-chroot", "/mnt", "useradd", "-m", "-G", "wheel", user], check=True)
    
    auth_string = f"{user}:{password}\nroot:{root_pass}\n"
    subprocess.run(
        ["arch-chroot", "/mnt", "chpasswd"],
        input=auth_string.encode(), 
        check=True)
    
    # Enable sudo for wheel group
    subprocess.run(["arch-chroot", "/mnt", "sed", "-i", "s/^# %wheel ALL=(ALL:ALL) ALL/%wheel ALL=(ALL:ALL) ALL/", "/etc/sudoers"], check=True)


def toggle_swap(enabled: bool):
    window.spinSwap.setEnabled(enabled)

def check_uefi():
    try:
        if os.path.exists("/sys/firmware/efi/"):
            print("UEFI detected")
            next_clicked()
        else:
            print("Legacy BIOS detected")
            window.stackedWidget.setCurrentIndex(12)
    except Exception as e:
        print(f"Error checking BIOS mode: {e}")
        return None


def savedisk():
    
    window.installButton.setEnabled(False)
    next_clicked()
    window.installStatus.setText("Partitioning...")
    
    def run_partition():
        
        idxdisks = window.comboDisk.currentIndex()
        pathdisk = disks[idxdisks][1]
        root_size = window.spinRoot.value()
        swap_enabled = window.swapCheck.isChecked()
        swap_size = window.spinSwap.value() if swap_enabled else 0
        swapyn = "y" if swap_enabled else "n"
        root_enabled = window.rootCheck.isChecked()
        rootyn = "y" if root_enabled else "n"
        vars_path = os.path.join(base_dir, "disk.sh")

        try:
            with open(vars_path, "w", encoding="utf-8") as f:
                f.write(f'TARGET_DISK="{pathdisk}"\n')
                f.write(f'rootsize="{root_size}"\n')
                f.write(f'swapyn="{swapyn}"\n')
                f.write(f'rootyn="{rootyn}"\n')
                f.write(f'swapsize="{swap_size}"\n')
                f.write("export TARGET_DISK rootsize swapyn swapsize rootyn\n")
                
            bash_dir = os.path.join(base_dir, "bash")
            partition_script = os.path.join(bash_dir, "partitionscript")
            
            env = os.environ.copy()
            env["VARS_FILE"] = vars_path
            env["BASH_SCRIPTS_DIR"] = bash_dir
            
            partition_result = subprocess.run(["bash", partition_script], env=env, capture_output=False, check=False)
        
            if partition_result.returncode == 0:
                install()
            else:
                print("Partitioning failed!")
                window.installStatus.setText("Installation failed")
                window.installButton.setEnabled(True)
        
        except subprocess.CalledProcessError as e:
            print(f"{e}")
            
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
    global installing
    layout_code = window.comboLayout.currentData()
    idxtime = window.comboZone.currentText()
    
    def run_commands():
        try:
            if layout_code in ("us", "de", "fr", "uk", "es", "it"):
                subprocess.run(["localectl", "set-keymap", layout_code], check=True)
            
            subprocess.run(["timedatectl", "set-timezone", idxtime], check=True)

            if installing == True:
                if os.path.exists("/mnt/etc"):
                    
                    zone_path = f"/usr/share/zoneinfo/{idxtime}"
                    if os.path.exists(zone_path):
                        subprocess.run(["ln", "-sf", zone_path, "/mnt/etc/localtime"], check=True)
                        subprocess.run(["arch-chroot", "/mnt", "hwclock", "--systohc"], check=True)
                    
                    
                    if layout_code:
                        with open("/mnt/etc/vconsole.conf", "w") as f:
                            f.write(f"KEYMAP={layout_code}\n")

                        # X11 layout config
                        x11_conf_dir = "/mnt/etc/X11/xorg.conf.d"
                        os.makedirs(x11_conf_dir, exist_ok=True)
                        with open(os.path.join(x11_conf_dir, "00-keyboard.conf"), "w") as f:
                            f.write('Section "InputClass"\n')
                            f.write('        Identifier "system-keyboard"\n')
                            f.write('        MatchIsKeyboard "on"\n')
                            f.write(f'        Option "XkbLayout" "{layout_code}"\n')
                            f.write('EndSection\n')

            print("Time and layout updated.")
        except subprocess.CalledProcessError as e:
            print(f"Error setting time/layout: {e}")

    threading.Thread(target=run_commands, daemon=True).start()

def next_clicked(plus=0):
    if isinstance(plus, bool):
        plus = 0
    print("next was clicked")
    global page
    page += 1 + plus
    print(page)
    window.stackedWidget.setCurrentIndex(page)
    page_turn()

def back(checked=False):
    print("back was clicked")
    global page
    page -= 1
    print(page)
    window.stackedWidget.setCurrentIndex(page)
    page_turn()

def page_turn():
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
    elif page == 5:
        print("page5")
        page5()
    elif page == 6:
        print("page6")
    elif page == 7:
        print("page7")
    elif page == 8:
        print("page8")
        page8()
    

def on_save_clicked():
    save_time()
    next_clicked(0)

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
        next_clicked(1)
    else:
        next_clicked(0)

def install_drivers():
    global gpu_command
    global drivers
    drivers = gpu_command
    next_clicked()


def save_user():
    global useryn
    useryn = True
    global user
    global password
    usertest = window.userLine.text().strip()
    passwordtest = window.passLine.text().strip()
    passconfirm = window.pass2Line.text().strip()

    if not usertest:
        window.empty.setText("User can't be empty")
    else:
        if passwordtest == passconfirm and passwordtest != "":
            user = usertest
            password = passwordtest
            print(user)
            print(password)
            next_clicked()
        else:
            window.passMis.setText("Password empty or doesn't match")

def skip_user():
    global useryn
    next_clicked()
    useryn = False

def reboot():
    subprocess.run(["reboot"], shell=True, check=True)

def toggle_dev(enabled = bool):
    global dev
    dev = enabled

def toggle_gaming(enabled = bool):
    global gaming
    gaming = enabled

def save_template():
    global template
    template = True
    next_clicked()

def toggle_root(enabled = bool):
    window.spinRoot.setEnabled(not enabled)

def page1():
    layout_format()

def page2():
    pass


def page3():
    global wifi_status
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
    global gpu_command

    gpu_vendor = subprocess.check_output("lspci | grep -E 'VGA|3D'", shell=True, text=True)
    print(gpu_vendor)
    
    if "NVIDIA" in gpu_vendor:
        gpu_vendor = "An NVIDIA GPU"
        gpu_command = "nvidia-dkms nvidia-utils lib32-nvidia-utils egl-wayland"
        window.labelGpu.setText(gpu_vendor + " was detected")
    elif "AMD" in gpu_vendor:
        gpu_vendor = "AMD Radeon"
        gpu_command = "mesa lib32-mesa vulkan-radeon lib32-vulkan-radeon libva-mesa-driver"
        window.labelGpu.setText(gpu_vendor + " was detected")
    elif "Intel" in gpu_vendor:
        gpu_vendor = "Intel Graphics"
        gpu_command = "mesa vulkan-intel"
        window.labelGpu.setText(gpu_vendor + " was detected")
    else:
        gpu_vendor = "Unknown"
        gpu_command = "mesa"
        window.labelGpu.setText("No specific GPU detected.")

    print(gpu_command)

def page8():
    global user
    disk_overview = window.comboDisk.currentText()
    root_size = window.spinRoot.value()
    print(disk_overview)
    print(root_size)
    window.ovDisk.setText("Selected Disk: " + disk_overview)
    window.ovRoot.setText("Root Size: " + str(root_size) + " MiB")
    window.ovUser.setText("Useraccount:  " + user)

# type and file

app = QApplication(sys.argv)
file = QFile(os.path.join(base_dir, "installer.ui"))
file.open(QFile.ReadOnly)

# loading, reading window and applying style

loader = QUiLoader()
window = loader.load(file)
file.close()

apply_style(window) # from style..py

# previous and back

window.previous.clicked.connect(back)
window.previous1.clicked.connect(back)
window.previous2.clicked.connect(back)
window.previous3.clicked.connect(back)
window.previous4.clicked.connect(back)
window.previous5.clicked.connect(back)
window.previous6.clicked.connect(back)
window.previous7.clicked.connect(back)

# save and next

window.nextButton.clicked.connect(check_uefi)
window.saveUser.clicked.connect(save_user)
window.yesgpu.clicked.connect(install_drivers)
window.next4.clicked.connect(next_clicked)
window.installButton.clicked.connect(savedisk)
window.saveTemplate.clicked.connect(save_template)
window.nextInternet.clicked.connect(next_internet)
window.savetime.clicked.connect(on_save_clicked)
window.savedisks.clicked.connect(next_clicked)
window.rebootButton.clicked.connect(reboot)
window.rebootBtn.clicked.connect(reboot)

# toggles and checkmarks

window.ethernetCheck.toggled.connect(toggle_ethernet)
window.rootCheck.toggled.connect(toggle_root)
window.swapCheck.toggled.connect(toggle_swap)
window.checkDev.toggled.connect(toggle_dev)
window.checkGaming.toggled.connect(toggle_gaming)

# rest

window.connect_button.clicked.connect(connect_wifi)
window.refreshn.clicked.connect(page3)
toggle_swap(window.swapCheck.isChecked())

window.nogpu.clicked.connect(next_clicked)
window.skipLogin.clicked.connect(skip_user)
window.skipTemplate.clicked.connect(next_clicked)

# combo and spin boxes

window.comboZone.addItems(timezones)
window.comboDisk.addItems(d[0] for d in disks)
window.wifiList.itemSelectionChanged.connect(log_item)

# loading gif

movie = QMovie(spinner_path) 
window.gif_label.setMovie(movie)
window.gif_label.setScaledContents(True)
movie.start()

# open window, reset variables

window.show()
window.stackedWidget.setCurrentIndex(0)
page_turn() # ensure first page is initialized
sys.exit(app.exec())


    

