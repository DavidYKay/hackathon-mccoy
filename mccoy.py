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

from listener import SpeechListener

from view import obj
from view.obj import Mesh, OBJ, loadOBJ
from view.puppetmaster import PuppetMaster
#from view.camera import Camera
from view.controller import ViewController
from view.vectors import Vector3
from view.shapes import Torus

IDLE_ROTATE_SPEED = 1

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

view_controller = ViewController()
#view_controller.camera.rotation = Vector3()

bored = False
def update(dt):
  if bored:
    view_controller.rotate_camera_by(IDLE_ROTATE_SPEED, 0)
  else:
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
    glTranslatef(view_controller.camera.position.x,
                 view_controller.camera.position.y,
                 view_controller.camera.position.z)
    #glTranslatef(0, 0, -4)
    #glTranslatef(0, 0, -3)
    glRotatef(view_controller.camera.rotation.z, 0, 0, 1)
    glRotatef(view_controller.camera.rotation.y, 0, 1, 0)
    glRotatef(view_controller.camera.rotation.x, 1, 0, 0)
    for mesh in view_controller.meshes:
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

class McCoyMouseHandler:
  def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
    #view_controller.rotate_camera_by(dx, dy)
    view_controller.rotate_camera_to(x, y)

def handle_speech(sentence):
  view_controller.rotate_camera_by(30, 0)

puppet_master = PuppetMaster(view_controller)

class SpeechListenerThread(threading.Thread):
 def run (self):
  listener = SpeechListener(puppet_master.handle_speech)
  listener.loop()

def main():
  SpeechListenerThread().start()

  setup()
  torus = Torus(1, 0.3, 50, 30)

  box = OBJ('models/box.obj')
  man = OBJ('models/man-colored.obj')

  view_controller.meshes.append(torus)
  view_controller.meshes.append(man)

  global batch
  batch = pyglet.graphics.Batch()

  window.push_handlers(McCoyMouseHandler())
  pyglet.app.run()

if __name__ == "__main__":
  main()
