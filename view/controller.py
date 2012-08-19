from camera import Camera
from vectors import Vector3

DEFAULT_CAMERA_POSITION = Vector3(0,0,-3)
DEFAULT_CAMERA_ROTATION = Vector3(0,0,0)

class ViewController:
  def __init__(self):
    self.camera = Camera(position=Vector3(0,0,-3))
    self.meshes = []
  
  def reset_camera(self):
    self.camera.position.x = DEFAULT_CAMERA_POSITION.x
    self.camera.position.y = DEFAULT_CAMERA_POSITION.y
    self.camera.position.z = DEFAULT_CAMERA_POSITION.z
    
    self.camera.rotation.x = DEFAULT_CAMERA_ROTATION.x
    self.camera.rotation.y = DEFAULT_CAMERA_ROTATION.y
    self.camera.rotation.z = DEFAULT_CAMERA_ROTATION.z
  
  def rotate_camera_to(self, x, y):
    self.camera.rotate_to(x, y)

  def rotate_camera_by(self, x, y):
    self.camera.rotate_by(x, y)
  
  def zoom_camera_by(self, z):
    self.camera.zoom_by(z)
  
  def zoom_camera_to(self, z):
    self.camera.zoom_to(z)
