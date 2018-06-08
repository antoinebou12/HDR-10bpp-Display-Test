#!/bin/bash
if [! -d /etc/X11/xorg.conf.d]; then
    mkdir /etc/X11/xorg.conf.d
    mkdir /etc/X11/xorg.conf.d/30
    mkdir /etc/X11/xorg.conf.d/24


cat > /etc/X11/xorg.conf.d/30/xorg.conf <<EOF
Section "Screen"
    Identifier "Screen0"
    Device     "Card0"
    Monitor    "Monitor0"
    DefaultDepth 30
    SubSection "Display"
        Viewport 0 0
        Depth 30
    EndSubSection
EndSection

EOF

cat > /etc/X11/xorg.conf.d/24/xorg.conf <<EOF
Section "Screen"
    Identifier "Screen0"
    Device     "Card0"
    Monitor    "Monitor0"
    DefaultDepth 30
    SubSection "Display"
        Viewport 0 0
        Depth 30
    EndSubSection
EndSection

EOF

xinit -- usr/bin/X -config xorg.conf.d/$1/xorg.conf

