import gi
import threading
import typer
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo
import imageio
import numpy as np
import time

DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720
DEFAULT_DEPTH = 8

INFO_DEPTH = {
    12: {'dtype': np.uint16, 'mask': 0xfff},
    10: {'dtype': np.uint16, 'mask': 0x3ff},
    8: {'dtype': np.uint8, 'mask': 0x3ff}
}
CAIRO_FORMAT = {
    32: cairo.FORMAT_ARGB32,
    10: cairo.FORMAT_RGB30,
    8: cairo.FORMAT_RGB24
}


class Viewer(object):

    def __init__(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, depth=DEFAULT_DEPTH):
        self._window = Gtk.Window(title="Viewer")
        self._painter = Gtk.DrawingArea()
        self._width = width
        self._height = height
        self._depth = depth
        self._image = np.zeros((height, width), dtype=np.uint32)
        self._mask = INFO_DEPTH[depth]['mask']
        self._dtype = INFO_DEPTH[depth]['dtype']
        self._initUI()

    def _initUI(self):
        """Init the Gui"""

        self._window.resize(self._width, self._height)
        self._window.add(self._painter)
        self._window.connect('window-state-event', self._window_state)

        cursor = Gdk.Cursor.new(Gdk.CursorType.BLANK_CURSOR)
        self._window.get_root_window().set_cursor(cursor)
        self._window.connect("destroy", self.destroy)

        self._painter.connect('draw', self._draw_on)
        self._window.show_all()
        self._draw()

    def _window_state(self, widget, event):
        self.is_fullscreen = bool(Gdk.WindowState.FULLSCREEN & event.new_window_state)

    @property
    def size(self):
        size = self._window.get_size()
        return size.width, size.height

    @size.setter
    def size(self, width, height):
        self._window.resize(width, height)
        self._draw()

    @property
    def fullscreen(self):
        return self.is_fullscreen

    @fullscreen.setter
    def fullscreen(self, fullscreen):
        if fullscreen:
            self._window.fullscreen()
        else:
            self._window.unfullscreen()

    def display_image(self, image):
        self._image = imageio.imread(image)
        self._draw()

    def _draw(self):
        self._painter.queue_draw()
        self._update()

    def _draw_on(self, widget, ctx):
        """ Draw the image using cairo"""
        h, w = self._image.shape[:2]
        img = np.zeros((h, w), dtype=np.uint32)
        img[:, :] = ((self._image[:, :, 0] & self._mask) << (2 * self._depth)) + \
                     ((self._image[:, :, 1] & self._mask) << self._depth) + \
                     (self._image[:, :, 2] & self._mask)

        surface = cairo.ImageSurface.create_for_data(img, CAIRO_FORMAT[self._depth], w, h)
        ctx.set_source_surface(surface, 0, 0)
        ctx.paint()

    def _update(self):
        """ manual main iteration """
        while Gtk.events_pending():
            Gtk.main_iteration()

    def destroy(self):
        try:
            cursor = Gdk.Cursor.new(Gdk.CursorType.ARROW)
            self._window.get_root_window().set_cursor(cursor)
            self._window.hide()
            Gtk.main_quit()
            self._update()
        except AttributeError:
            raise AttributeError("Already destroyed")

        self._painter = None
        self._window = None

    def display_video(self, video_path, fps=30):
        self.video_path = video_path
        self._fps = fps
        self._stop_video = False
        self._video_thread = threading.Thread(target=self._play_video)
        self._video_thread.start()

    def _play_video(self):
        video = imageio.get_reader(self.video_path, 'ffmpeg')
        for frame in video:
            if self._stop_video:
                break
            self._image = frame
            self._draw()
            time.sleep(1.0 / self._fps)
        video.close()

    def stop_video(self):
        self._stop_video = True
        if self._video_thread:
            self._video_thread.join()
        self._video_thread = None


def main(image_path: str = typer.Option(None, help="Path to the image file"), 
         video_path: str = typer.Option(None, help="Path to the video file")):

    v = Viewer(depth=10)
    if image_path:
        v.display_image(image_path)
    if video_path:
        v.display_video(video_path, fps=30)
    try:
        Gtk.main()
    except KeyboardInterrupt:
        if video_path:
            v.stop_video()
        v.destroy()


if __name__ == '__main__':
    typer.run(main)
