import subprocess

from parser.parser import McCoyParser

class PuppetMaster:
  ########################################
  # Initialization
  ########################################

  def __init__(self, view_controller):
    self.view_controller = view_controller
    self.parser = McCoyParser()
    self.command_methods = {
      'VIEW':     self.handle_view,
      'LEFT':     self.handle_rotate,
      'RIGHT':    self.handle_rotate,
      'UP':       self.handle_rotate,
      'DOWN':     self.handle_rotate,
      'CLOSER':   self.handle_zoom,
      'FURTHER':  self.handle_zoom,
      'SLIGHTLY': self.handle_slightly,
    }
  
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
    print "Sentence received: %s" % sentence
    #self.say_out_loud(words)
    command = self.parser.parser.parse(sentence)
    self.execute_command(command)
  
  def execute_command(self, command):
    print "executing command: %s" % command
    method = self.command_methods[command.symbol]
    #apply(method, command)
    method(command)

  ########################################
  # Utility Methods
  ########################################
  def handle_rotate(self, command):
    x = y = 0
    if command.symbol == 'LEFT':
      x = command.quantity.amount
    elif command.symbol == 'RIGHT':
      x = command.quantity.amount * -1
    elif command.symbol == 'UP':
      y = command.quantity.amount 
    elif command.symbol == 'DOWN':
      y = command.quantity.amount * -1

    # Handle portions
    if command.quantity.portion == True:
      x *= 360
      y *= 360
    else:
      pass
    self.view_controller.rotate_camera_by(x, y)
 
  def handle_zoom(self, command):
    pass
  
  def handle_slightly(self, command):
    pass
  
  def handle_view(self, command):
    pass
