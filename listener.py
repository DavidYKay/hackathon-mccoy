#!/usr/bin/env python

import pexpect
import re

#CMSCORE_THRESHOLD = 0.999
CMSCORE_THRESHOLD = 0.995
SCORE_THRESHOLD   = -13000

def process_sentence(sentence):
  print "Processing sentence: %s" % sentence

def process_julius(out_text):
  match_res = re.match(r'(.*)sentence1(\.*)', out_text, re.S)
  if match_res:
    get_confidence(out_text)
  else:
    pass

def get_confidence(out_text):
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
        process_sentence(sentence1)
    else:
        pass

command = 'padsp julius -input mic -C voice/julian.jconf'
#command = 'julius -input mic -C julian.jconf'
child = pexpect.spawn (command)

while True:
  try:
    child.expect('please speak')
    process_julius(child.before)
  except KeyboardInterrupt:
    child.close(force=True)
    break
