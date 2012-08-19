from vectors import Vector3

class Camera:
  def __init__(self, position=Vector3(), rotation=Vector3()):
    self.rotation = rotation
    self.position = position
  
  def rotate_to(self, x, y):
    print "Rotating to: (%f, %f)" % (x, y)
    self.rotation.x = y
    self.rotation.y = x

  def rotate_by(self, x, y):
    print "Rotating by: (%f, %f)" % (x, y)
    self.rotation.x += y
    self.rotation.y += x
  
  def zoom_to(self, z):
    print "Zooming to: (%f)" % (z)
    self.position.z = z

  def zoom_by(self, z):
    print "Zooming by: (%f)" % (z)
    self.position.z += z
  
  def __repr__(self):
    return "Camera(%r, %r)" % (self.position, self.rotation,)
