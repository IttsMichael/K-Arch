#!/usr/bin/env bash
# shellcheck disable=SC2034

AIROOTFS_BUILD_HOOKS=(root/custom_hooks/*.sh)


iso_name="k-arch"
iso_label="KARCH_$(date --date="@${SOURCE_DATE_EPOCH:-$(date +%s)}" +%Y%m)"
iso_publisher="K-Arch Linux <https://github.com/IttsMichael/K-Arch>"
iso_application="K-Arch Linux Live/Rescue DVD"
iso_version="$(date --date="@${SOURCE_DATE_EPOCH:-$(date +%s)}" +%Y.%m.%d)"
install_dir="k-arch"
buildmodes=('iso')
bootmodes=('bios.syslinux'
           'uefi.systemd-boot')
pacman_conf="pacman.conf"
airootfs_image_type="squashfs"
airootfs_image_tool_options=('-comp' 'xz' '-Xbcj' 'x86' '-b' '1M' '-Xdict-size' '1M')
bootstrap_tarball_compression=('zstd' '-c' '-T0' '--auto-threads=logical' '--long' '-19')
file_permissions=(
  ["/etc/shadow"]="0:0:400"
  ["/root"]="0:0:750"
  ["/root/.automated_script.sh"]="0:0:755"
  ["/root/.gnupg"]="0:0:700"
  ["/usr/local/bin/choose-mirror"]="0:0:755"
  ["/usr/local/bin/Installation_guide"]="0:0:755"
  ["/usr/local/bin/livecd-sound"]="0:0:755"
  ["/usr/bin/installgrub"]="0:0:755"
  ["/usr/bin/copyscripts"]="0:0:755"
  ["/usr/bin/partitionscript"]="0:0:755"
  ["/usr/bin/formatscript"]="0:0:755"
  ["/usr/bin/mountingscript"]="0:0:755"
  ["/usr/local/share/main.py"]="0:0:755"
)
