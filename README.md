# McCoy
## A voice-based 3d model viewer for surgery.

This app is implemented using the following libraries:

Compile/download by hand:

* Pyglet - Pyglet is a simple, Pygame-like library for creating a window, capturing mouse movement, and rendering the OpenGL scene.
* Pexpect - In order to get the Julian output into Python, we use Pexpect and
  parse the shell output.
* VoxForge - 1MB speech model to recognize phonemes.

Install with APT:

* Julius/Julian - We use the Julian voice recognition engine to perform "small vocabulary" recognition on our own custom vocabulary and grammar.

Install with pip:
* PLY - We use Yacc and Lex to parse the text that comes into Python from Julian.

## Background

McCoy was born at Meetup's Battle of the Braces hackathon, Python vs Ruby round.

## Video

View the hackathon presentation on [YouTube](http://youtu.be/uC6h173sidA).

----------------------------------------
Copyright 2012 David Y. Kay
----------------------------------------
