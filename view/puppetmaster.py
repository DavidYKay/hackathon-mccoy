class PuppetMaster:
  
  ########################################
  # Initialization
  ########################################

  def __init__(self, view_controller):
    self.view_controller = view_controller
  
  ########################################
  # Public Methods
  ########################################

  def handle_speech(self, sentence):
    self.rotate_model_by(45, 0)

  ########################################
  # Utility Methods
  ########################################

  def rotate_model_to(self, x, y):
    global view_controller
    self.view_controller.camera.rotation.x = y
    self.view_controller.camera.rotation.y = x

  def rotate_model_by(self, x, y):
    global view_controller
    self.view_controller.camera.rotation.x += y
    self.view_controller.camera.rotation.y += x
