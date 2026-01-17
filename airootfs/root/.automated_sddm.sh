#!/bin/bash
# Archiso hook script to set up automatic GUI login (SDDM + Plasma Wayland)

# 1. Set graphical.target as the default systemd target (runlevel):
ln -sf /usr/lib/systemd/system/graphical.target /etc/systemd/system/default.target

# 2. Enable SDDM to start at boot (graphical.target):
systemctl enable sddm.service

# 3. Create SDDM autologin config for root user on Plasma Wayland:
mkdir -p /etc/sddm.conf.d
cat > /etc/sddm.conf.d/autologin.conf <<'EOF'
[Autologin]
User=root
Session=plasmawayland.desktop
EOF

# 4. (Optional) You can adjust SDDM settings if needed (e.g., MinimumUid=0) 
#    to include root in the greeter list. Not required for autologin.

# 5. Switch to graphical.target now to launch SDDM immediately:
systemctl isolate graphical.target
