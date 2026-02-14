# K-Arch
K-Arch is an arch based linux distro running the cachyOS kernel. It uses KDE plasma on wayland as default as well as custom configurations.
It uses the fully custom K-Arch-Installer & Updater

## Download
http://karch-linux.org:3000

## Showcase
<img width="1280" height="798" alt="image" src="https://github.com/user-attachments/assets/2ba8a597-44de-4eb9-bfde-20d13b19f0cf" />

<img width="1278" height="799" alt="image" src="https://github.com/user-attachments/assets/e56a11ef-090b-42e5-a6ca-c61daf2e747d" />

<img width="1277" height="797" alt="image" src="https://github.com/user-attachments/assets/46219ae3-1399-4d03-8ed5-d918cbf449da" />


## K-Arch-Installer
The K-Arch-Installer fully automates the installation and provides more options than most popular installers.

- detects your GPU and installs the proprietary drivers automatically
- offers templates to save time
- has a custom network manager
- **does not use** any calamares/anaconda base

## Build the ISO yourself
You can build the ISO from the source yourself by using mkarchiso.
The ISO file will end in **K-Arch/out/**

```
sudo pacman -S archiso git
git clone https://github.com/IttsMichael/K-Arch.git
cd K-Arch
sudo mkarchiso -v .
```
**That procces can take a while, especially on low end devices so you might want to download the ISO directly.**


## Licensing & Acknowledgment 

Project Code
All original code developed specifically for K-Arch—including the custom graphical installer and configuration scripts—is licensed under the [GPL-3.0] as specified in the LICENSE file.
Upstream & Third-Party Software
K-Arch is a derivative work that redistributes and integrates third-party open-source software. We extend our gratitude and credit to the following projects:
The Arch Linux Project: For the robust rolling-release base and package management tooling.
CachyOS: For the optimized Linux kernel and the high-performance package repositories utilized in this distribution.
KDE Community: For the Plasma desktop environment and the Qt-based application framework.
GNU Project & FSF: For the core utilities and essential free software components.
Licensing & Copyright
Ownership: Copyright of all third-party components remains with the original authors and contributors.
Compliance: All software is redistributed under its original license (e.g., GPL, LGPL, MIT, or BSD).
Source Code: In accordance with the GPL, source code for the kernel and all redistributed packages is available via the upstream Arch Linux and CachyOS mirrors.

All original code developed specifically for this project - including the custom graphical installer and related scripts - is licensed under the terms specified in the project's LICENSE file.


## Built With

This project is a custom ISO built using the following official tools:

* **Base:** [Arch Linux](https://archlinux.org/)
* **Build Tool:** [archiso](https://gitlab.archlinux.org/archlinux/archiso) - The official Arch Linux live image builder.

### Contact
michael.last1808@gmail.com
discord: #ittsmichael

