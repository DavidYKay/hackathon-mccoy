from vectors import Vector3
from copy import deepcopy

class Camera:
  def __init__(self, position=Vector3(), rotation=Vector3()):
    self.rotation = deepcopy(rotation)
    self.position = deepcopy(position)
    self.target_rotation = deepcopy(rotation)
    self.target_position = deepcopy(position)
  
  def rotate_to(self, x, y):
    print "Rotating to: (%f, %f)" % (x, y)
    self.target_rotation.x = y
    self.target_rotation.y = x

  def rotate_by(self, x, y):
    print "Rotating by: (%f, %f)" % (x, y)
    self.target_rotation.x += y
    self.target_rotation.y += x
  
  def zoom_to(self, z):
    print "Zooming to: (%f)" % (z)
    self.target_position.z = z

  def zoom_by(self, z):
    print "Zooming by: (%f)" % (z)
    self.target_position.z += z
  
  def find_step_distance(self, current, target):
    return (target - current) * .01
  
  def step_to_target(self):
    print "Stepping! Current Pos: %s, Target: %s" % (self.position,
                                                     self.target_position)
    if self.rotation.x != self.target_rotation.x:
      self.rotation.x += self.find_step_distance(self.rotation.x, self.target_rotation.x)
    if self.rotation.y != self.target_rotation.y:
      self.rotation.y += self.find_step_distance(self.rotation.y, self.target_rotation.y)
    if self.rotation.z != self.target_rotation.z:
      self.rotation.z += self.find_step_distance(self.rotation.z, self.target_rotation.z)
    
    if self.position.x != self.target_position.x:
      self.position.x += self.find_step_distance(self.position.x, self.target_position.x)
    if self.position.y != self.target_position.y:
      self.position.y += self.find_step_distance(self.position.y, self.target_position.y)
    if self.position.z != self.target_position.z:
      self.position.z += self.find_step_distance(self.position.z, self.target_position.z)
  
  def __repr__(self):
    return "Camera(%r, %r)" % (self.position, self.rotation,)
