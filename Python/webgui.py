#!/usr/bin/env python
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import webkit
import gobject

gobject.threads_init()
win = gtk.Window()
bro = webkit.WebView()
bro.open("https://meet.jit.si/hello")
win.add(bro)
#win.fullscreen()
win.resize(gtk.gdk.screen_width(),480)
win.resize(gtk.gdk.screen_height(),320)
win.show_all()
gtk.main()