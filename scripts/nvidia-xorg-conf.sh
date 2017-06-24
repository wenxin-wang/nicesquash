#!/bin/bash

if [ $# -ne 1 ]; then
    echo "usage: $0 /etc/X11/xorg.conf"
    exit 1
fi

F=$1

if [ -e $F ]; then
    mv $F $F.bak
fi

ngpu=$(nvidia-smi -L | wc -l)

if [ $ngpu -le 0 ]; then
    echo "No nvidia card found"
    exit 1
fi

cat >$F <<EOF
Section "ServerLayout"
    Identifier     "Layout0"
    Screen      0  "Screen0"
EOF
for i in $(seq 1 $((ngpu-1))); do
    cat >>$F <<EOF
    Screen      $i  "Screen$i" RightOf "Screen$((i-1))"
EOF
done
cat >>$F <<EOF
EndSection

Section "Files"
EndSection
EOF

xconfig_field() {
    nvidia-xconfig --query-gpu-info | grep $1 | cut -d ':' -f 2- | cut -d ' ' -f 2-
}

IFS=$'\n' read -d '' -r -a names <<< $(xconfig_field Name)
IFS=$'\n' read -d '' -r -a buses <<< $(xconfig_field PCI)

for i in $(seq 0 $((ngpu-1))); do
    cat >>$F <<EOF

Section "Device"
    Identifier     "Device$i"
    Driver         "nvidia"
    VendorName     "NVIDIA Corporation"
    BoardName      "${names[i]}"
    BusID          "${buses[i]}"
    Option         "Coolbits" "7"
    Option         "AllowEmptyInitialConfiguration"
EndSection
EOF
done

for i in $(seq 0 $((ngpu-1))); do
    cat >>$F <<EOF

Section "Screen"
    Identifier     "Screen$i"
    Device         "Device$i"
EndSection
EOF
done
