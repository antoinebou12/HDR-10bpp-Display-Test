# HDR-10bpp-Display-Test
## For X11 
To test HDR 4k display on linux 


### use 
- imagej 
- gtk3viewer in projet with RGB30 on
```
$ sudo systemctl stop lightdm || sudo systemctl stop gdm
$ sudo pkill Xorg
$ ./Xdepth.sh
```
