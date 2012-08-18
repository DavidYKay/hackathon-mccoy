from camera import Camera

class ViewController:
  def __init__(self):
    self.camera = Camera()
    self.meshes = []
  
  def rotate_camera_to(self, x, y):
    self.camera.rotate_to(x, y)

  def rotate_camera_by(self, x, y):
    self.camera.rotate_by(x, y)
