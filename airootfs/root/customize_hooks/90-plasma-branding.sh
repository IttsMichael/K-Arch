#!/usr/bin/env bash

mkdir -p /etc/skel/.config

echo "[KDE]" > /etc/skel/.config/kdeglobals
echo "lookAndFeelPackage=com.yourdistro.desktop" >> /etc/skel/.config/kdeglobals

chown -R root:root /etc/skel/.config
chmod -R 755 /etc/skel/.config