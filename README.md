## K-Arch

K-Arch is an independent, Arch-based Linux distribution focused on performance, modern defaults, and a clean user experience.

## Key-Features 

• Fully custom graphical installer

• Designed in Qt

• Installer logic written entirely in Bash and Python

• No third-party installer frameworks

• CachyOS kernel by default for improved responsiveness and performance

• KDE Plasma (Wayland) as the default desktop

environment

• Arch-based rolling release model

• Minimal, transparent system configuration

## Custom Installer

https://github.com/IttsMichael/K-Arch-Installer

K-Arch ships with a bespoke graphical installer written from scratch.

The installer was designed and implemented entirely in-house:

Custom installation flow and UI

Manual control over disk detection, partitioning, and mounting

Explicit package selection and system setup logic

• Direct use of standard Arch tools (pacman, pacstrap, etc.) without relying on existing installer frameworks

This approach keeps the installer flexible, understandable, and fully under the project's control

## Current Status

Early development

### The installer is NOT complete or suitable for a full installation 

Expect:

Rapid changes

Incomplete features

Occasional breakage

This project is actively evolving and not yet recommended for production systems.

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

