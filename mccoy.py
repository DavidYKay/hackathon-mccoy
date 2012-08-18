#!/usr/bin/env python

'''Displays a rotating torus using OpenGL.

This example demonstrates:

 * Using a 3D projection on a window by overriding the default on_resize
   handler
 * Enabling multisampling if available
 * Drawing a simple 3D primitive using vertex and index arrays
 * Using a display list
 * Fixed-pipeline lighting

'''

import threading
from math import pi, sin, cos

from pyglet.gl import *
from pyglet.window import mouse
import pyglet

import kytten

from listener import SpeechListener

from view import obj
from view.obj import Mesh, OBJ, loadOBJ
from view.vectors import Vector3
from view.shapes import Torus

try:
    # Try and create a window with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4,
                    depth_size=16, double_buffer=True,)
    window = pyglet.window.Window(resizable=True, config=config)
except pyglet.window.NoSuchConfigException:
    # Fall back to no multisampling for old hardware
    window = pyglet.window.Window(resizable=True)

@window.event
def on_resize(width, height):
    # Override the default on_resize handler to create a 3D projection
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60., width / float(height), .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED

camera_rotation = Vector3()

def update(dt):
  pass
    #global rx, ry, rz
    #rx += dt * 1
    #ry += dt * 80
    #rz += dt * 30
    #rx %= 360
    #ry %= 360
    #rz %= 360
pyglet.clock.schedule(update)

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    #glTranslatef(0, 0, -4)
    glTranslatef(0, 0, -3)
    glRotatef(camera_rotation.z, 0, 0, 1)
    glRotatef(camera_rotation.y, 0, 1, 0)
    glRotatef(camera_rotation.x, 1, 0, 0)
    for mesh in meshes:
      mesh.draw()
    #torus.draw()
    
    # draw the UI
    batch.draw()

def setup():
    # One-time GL setup
    glClearColor(1, 1, 1, 1)
    glColor3f(1, 0, 0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    # Uncomment this line for a wireframe view
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    # Simple light setup.  On Windows GL_LIGHT0 is enabled by default,
    # but this is not the case on Linux or Mac, so remember to always
    # include it.
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    # Define a simple function to create ctypes arrays of floats:
    def vec(*args):
        return (GLfloat * len(args))(*args)

    glLightfv(GL_LIGHT0 , GL_POSITION , vec(.5 , .5 , 1  , 0))
    glLightfv(GL_LIGHT0 , GL_SPECULAR , vec(.5 , .5 , 1  , 1))
    glLightfv(GL_LIGHT0 , GL_DIFFUSE  , vec(1  , 1  , 1  , 1))

    glLightfv(GL_LIGHT1 , GL_POSITION , vec(1  , 0  , .5 , 0))
    glLightfv(GL_LIGHT1 , GL_DIFFUSE  , vec(.5 , .5 , .5 , 1))
    glLightfv(GL_LIGHT1 , GL_SPECULAR , vec(1  , 1  , 1  , 1))
    
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, vec(0.5, 0, 0.3, 1))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec(1, 1, 1, 1))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50)

def rotate_model_to(x, y):
  global camera_rotation
  #rx = x
  #ry = y
  camera_rotation.x = y
  camera_rotation.y = x
  #rz = y

def rotate_model_by(x, y):
  global camera_rotation
  camera_rotation.x += y
  camera_rotation.y += x

class McCoyMouseHandler:
  def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
    print "Mouse was dragged!"
    rotate_model_to(x, y)
    #if buttons & mouse.LEFT:
    #    pass

def print_sentence(sentence):
  print "Printing sentence: %s" % sentence

def handle_speech(sentence):
  rotate_model_by(30, 0)

class SpeechListenerThread(threading.Thread):
 def run (self):
  listener = SpeechListener(handle_speech)
  listener.loop()


def main():
  SpeechListenerThread().start()

  setup()
  torus = Torus(1, 0.3, 50, 30)

  box = OBJ('models/box.obj')
  man = OBJ('models/man-colored.obj')

  global meshes 
  meshes = []
  meshes.append(torus)
  meshes.append(man)

  global batch
  batch = pyglet.graphics.Batch()

  window.push_handlers(McCoyMouseHandler())
  pyglet.app.run()

#dialog = kytten.Dialog(
#    kytten.TitleFrame("Kytten Demo",
#                      kytten.VerticalLayout([
#                          kytten.Label("Select dialog to show"),
#                          kytten.Menu(options=["Document", "Form", "Scrollable"],
#                                      on_select=on_select),
#                          ]),
#                      ),
#    window=window, batch=batch, group=fg_group,
#    anchor=kytten.ANCHOR_TOP_LEFT,
#    theme=theme)

if __name__ == "__main__":
  main()
