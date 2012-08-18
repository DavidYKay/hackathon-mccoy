#!/usr/bin/env python

import pexpect
import re

PERFECT = 0.999
HIGH    = 0.995
MEDIUM  = 0.900
LOW     = 0.800
CMSCORE_THRESHOLD = LOW
SCORE_THRESHOLD   = -13000

COMMAND = 'padsp julius -input mic -C voice/julian.jconf'

class SpeechListener:
  def __init__(self, sentence_callback):
    self.sentence_callback = sentence_callback

  def process_julius(self, out_text):
    match_res = re.match(r'(.*)sentence1(\.*)', out_text, re.S)
    if match_res:
      self.get_confidence(out_text)
    else:
      pass

  def get_confidence(self, out_text):
      linearray = out_text.split("\n")
      for line in linearray:
          if line.find('sentence1') != -1:
              sentence1 = line
          elif line.find('cmscore1') != -1:
              cmscore1 = line
          elif line.find('score1') != -1:
              score1 = line
      cmscore_array = cmscore1.split()
      #process sentence
      err_flag = False
      for score in cmscore_array:
          try:
              ns = float(score)
          except ValueError:
              continue
          if (ns < CMSCORE_THRESHOLD):
              err_flag = True
              print "confidence error:", ns, ":", sentence1
      score1_val = float(score1.split()[1])
      if score1_val < SCORE_THRESHOLD:
          err_flag = True
          print "score1 error:", score1_val, sentence1
      if (not err_flag):
          print sentence1
          print score1
          #process sentence
          #process_sentence(sentence1)
          self.sentence_callback(sentence1)
      else:
          pass

  def loop(self):
    child = pexpect.spawn(COMMAND)

    while True:
      try:
        child.expect('please speak')
        self.process_julius(child.before)
      except KeyboardInterrupt:
        child.close(force=True)
        break


def print_sentence(sentence):
  print "Printing sentence: %s" % sentence

if __name__ == "__main__":
  listener = SpeechListener(print_sentence)
  listener.loop()
