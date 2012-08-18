import subprocess
class PuppetMaster:

  
  ########################################
  # Initialization
  ########################################

  def __init__(self, view_controller):
    self.view_controller = view_controller
  
  ########################################
  # Public Methods
  ########################################
  def trim_tags(self, sentence):
    sentence = sentence.replace('sentence1:', '')
    sentence = sentence.replace('<s>', '')
    sentence = sentence.replace('</s>', '')
    sentence = sentence.strip()
    return sentence
  
  def say_out_loud(self, words):
    args = ['/usr/bin/espeak', '-v', 'en', words]
    subprocess.Popen(args)

  def handle_speech(self, sentence):
    sentence = self.trim_tags(sentence)
    words = "Command received: %s" % sentence
    print words
    #self.say_out_loud(words)
    self.rotate_model_by(45, 0)

  ########################################
  # Utility Methods
  ########################################

  def rotate_model_to(self, x, y):
    self.view_controller.camera.rotation.x = y
    self.view_controller.camera.rotation.y = x

  def rotate_model_by(self, x, y):
    self.view_controller.camera.rotation.x += y
    self.view_controller.camera.rotation.y += x
