from vectors import Vector3

class Camera:
  def __init__(self):
    self.rotation = Vector3()
    self.position = Vector3()
  
  def rotate_to(self, x, y):
    print "Rotating to: (%f, %f)" % (x, y)
    self.rotation.x = y
    self.rotation.y = x

  def rotate_by(self, x, y):
    print "Rotating by: (%f, %f)" % (x, y)
    self.rotation.x += y
    self.rotation.y += x
