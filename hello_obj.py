#!/usr/bin/env python

__docformat__ = 'restructuredtext'
__version__ = '$Id: hello_world.py 2090 2008-05-29 12:49:25Z Alex.Holkner $'

import pyglet

window = pyglet.window.Window()
label = pyglet.text.Label('Hello, world', 
                          font_name='Times New Roman', 
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

@window.event
def on_draw():
    window.clear()
    label.draw()

pyglet.app.run()
