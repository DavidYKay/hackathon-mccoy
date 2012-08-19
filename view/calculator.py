from __future__ import division
import unittest

def get_relative_zoom(current_zoom, divisor):
      delta = -1 * (current_zoom * divisor)
      return delta

class TestCalculator(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass

  def test_relative_zoom(self):
    input_output = {
        (-3, .5):  1.5,
        (-3, .25): .75,
    }
    for inputs, output in input_output.items():
      self.assertEqual(
          output,
          get_relative_zoom(inputs[0], inputs[1]))



if __name__ == '__main__':
  unittest.main()
