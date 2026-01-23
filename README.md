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

K-Arch ships with a bespoke graphical installer written from scratch.

The installer was designed and implemented entirely in-house:

Custom installation flow and UI

Manual control over disk detection, partitioning, and mounting

Explicit package selection and system setup logic

• Direct use of standard Arch tools (pacman, pacstrap, etc.) without relying on existing installer frameworks

This approach keeps the installer flexible, understandable, and fully under the project's control

## Current Status

Early development

# The installer is NOT complete or suitable for a full installation 

Expect:

Rapid changes

Incomplete features

Occasional breakage

This project is actively evolving and not yet recommended for production systems.

## Licensing & Acknowledgment 

K-Arch is composed of original code as well as software developed by the wider open-source community.

Project Code

All original code developed specifically for this project - including the custom graphical installer and related scripts - is licensed under the terms specified in the project's LICENSE file.

This project's configuration files are licensed under GPL. 
Individual packages included in the ISO are subject to their own respective licenses from the Arch Linux repositories.

Third-Party Software

K-Arch redistributes and makes use of third-party open-source software, including but not limited to:

The Linux kernel (via the CachyOS kernel)

Arch Linux packages and tooling

KDE Plasma desktop environment

Qt framework

GNU core utilities and other free software

ChatGPT fragen

All third-party components are distributed under their respective licenses.

Ownership and copyright re. uin with their original

authors

## Built With

This project is a custom ISO built using the following official tools:

* **Base:** [Arch Linux](https://archlinux.org/)
* **Build Tool:** [archiso](https://gitlab.archlinux.org/archlinux/archiso) - The official Arch Linux live image builder.

