# HDR-10bpp-Display-Test
To test HDR 4k display on linux 
### use imagej to view the image or gtk3viewer with RGB30 on
```
$ sudo systemctl stop lightdm || sudo systemctl stop gdm
$ sudo pkill Xorg
$ ./Xdepth.sh
```
