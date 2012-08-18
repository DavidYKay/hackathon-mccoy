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

from math import pi, sin, cos

from pyglet.gl import *
import pyglet

import obj
from obj import Mesh, OBJ, loadOBJ
from shapes import Torus

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

def update(dt):
    global rx, ry, rz
    #rx += dt * 1
    ry += dt * 80
    #rz += dt * 30
    rx %= 360
    ry %= 360
    rz %= 360
pyglet.clock.schedule(update)

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    #glTranslatef(0, 0, -4)
    glTranslatef(0, 0, -3)
    glRotatef(rz, 0, 0, 1)
    glRotatef(ry, 0, 1, 0)
    glRotatef(rx, 1, 0, 0)
    for mesh in meshes:
      mesh.draw()
    #torus.draw()

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

meshes = []

setup()
torus = Torus(1, 0.3, 50, 30)

box = OBJ('models/box.obj')
#man = OBJ('models/man.obj')
#man = OBJ('models/man-centered.obj')
#man = OBJ('models/man-centered-2.obj')
#man = OBJ('models/man-smooth.obj')
#man = OBJ('models/man-red.obj')
#man.load_material_library('man-centered-2.mtl')
#man = OBJ('models/man-normals.obj')
man = OBJ('models/man-colored.obj')

#man = obj.Man('models/man-red.obj')
#man = obj.Man('models/box.obj')

meshes.append(torus)
#meshes.append(box)
meshes.append(man)

rx = ry = rz = 0

pyglet.app.run()
