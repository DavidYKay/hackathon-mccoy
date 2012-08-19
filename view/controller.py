from camera import Camera
from vectors import Vector3

class ViewController:
  def __init__(self):
    self.camera = Camera(position=Vector3(0,0,-3))
    self.meshes = []
  
  def rotate_camera_to(self, x, y):
    self.camera.rotate_to(x, y)

  def rotate_camera_by(self, x, y):
    self.camera.rotate_by(x, y)
  
  def zoom_camera_by(self, z):
    self.camera.zoom_by(z)
  
  def zoom_camera_to(self, z):
    self.camera.zoom_to(z)
