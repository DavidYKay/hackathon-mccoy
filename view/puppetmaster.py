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
    print "Command received: %s" % sentence
    #self.say_out_loud(words)
    self.view_controller.rotate_camera_by(45, 0)

  ########################################
  # Utility Methods
  ########################################
