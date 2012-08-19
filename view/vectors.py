class Vector3:
  def __init__(self, x=0, y=0, z=0):
    self.x = x
    self.y = y
    self.z = z
  
  def __repr__(self):
    return "(%r, %r, %r)" % (
        self.x,
        self.y,
        self.z)
