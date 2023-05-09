# HDR-10bpp-Display-Test

This is a simple test to verify the HDR 4K display on Linux using a color depth of 10 bits per channel. The test requires an HDR 4K display and a Linux environment with the X server installed.

## Getting Started

### Prerequisites

To run the test, you will need the following software installed on your system:

- X server
- Python 3
- GTK 3
- ImageJ (for displaying images with a 10-bit color depth)
- ImageIO (for reading image files)

You can install these packages on Ubuntu or Debian-based systems by running the following command:

```
sudo apt-get install xserver-xorg python3 python3-gi python3-gi-cairo gir1.2-gtk-3.0 imagej
```

### Installing

To install ImageIO, you can use pip:

```
pip3 install imageio
```

### Running the test

To run the test, follow these steps:

1. Clone the repository:

```
git clone https://github.com/yourusername/HDR-10bpp-Display-Test.git
```

2. Navigate to the project directory:

```
cd HDR-10bpp-Display-Test
```

3. Stop the display manager and X server:

```
sudo systemctl stop lightdm || sudo systemctl stop gdm
sudo pkill Xorg
```

4. Start the X server with a color depth of 30:

```
startx -- -depth 30
```

5. If the X server was started successfully, the output of the following command should indicate a depth of 30:

```
xwininfo -root | grep Depth
```

6. Launch the viewer application:

```
python3 Viewer.py
```

7. The viewer window will open. To display an image, run the following command:

```
imagej --no-splash /path/to/image
```

8. The image should be displayed in the viewer window. Verify that the image is displayed correctly and that the colors are accurate.

## Troubleshooting

If the X server does not start with a color depth of 30, try starting it with a color depth of 24:

```
startx -- -depth 24
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

This test is based on the work of [Hans-Christoph Steiner](https://github.com/eighthave/HDR-10bpp-Display-Test). Thanks to Hans-Christoph Steiner for the original code and inspiration for this test.
