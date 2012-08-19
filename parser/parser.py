#!/usr/bin/env python
# Uses David Beazley's PLY parser.
# Implements two functions: count the total number of atoms in the equation and
#   count the number of times each element occurs in the equation.

from ply import lex
from ply import yacc

import collections
import unittest

########################################
# Util
########################################

PORTIONS_TO_NUM = {
    'FULL' : 1.0,
    'HALF' : 0.5,
    'HALFWAY' : 0.5,
    'QUARTER' : 0.25,
    'SLIGHTLY' : 0.05,
    'SLIGHT' : 0.05,
}

# Tokens up to 90
DIGITS_TO_ENGLISH = {
    '0' : '',
    '1' : 'ONE',
    '2' : 'TWO',
    '3' : 'THREE',
    '4' : 'FOUR',
    '5' : 'FIVE',
    '6' : 'SIX',
    '7' : 'SEVEN',
    '8' : 'EIGHT',
    '9' : 'NINE',
    '10' : 'TEN',
    '11' : 'ELEVEN',
    '12' : 'TWELVE',
    '13' : 'THIRTEEN',
    '14' : 'FOURTEEN',
    '15' : 'FIFTEEN',
    '16' : 'SIXTEEN',
    '17' : 'SEVENTEEN',
    '18' : 'EIGHTEEN',
    '19' : 'NINETEEN',
    '20' : 'TWENTY',
    '30' : 'THIRTY',
    '40' : 'FORTY',
    '50' : 'FIFTY',
    '60' : 'SIXTY',
    '70' : 'SEVENTY',
    '80' : 'EIGHTY',
    '90' : 'NINETY',
    '100' : 'HUNDRED',
}

ENGLISH_TO_DIGITS = dict([[v,k] for k,v in DIGITS_TO_ENGLISH.items()])

def english_to_digit(english):
  return int(ENGLISH_TO_DIGITS[english])

########################################
# Begin Lex
########################################

tokens = (
    "BODYPART",

    "BODYPART_COMMAND",
    "QUANTITY_COMMAND",
    "BASIC_COMMAND",

    "DECIMAL",
    "DIGIT",
    "FLAVOR",
    "NAME",
    "PORTION",
    "TRIPLEDIGIT",
    "UNIT",
    "STARTUP",
)

t_PORTION = (r"FULL|HALFWAY|HALF|QUARTER|SLIGHTLY|SLIGHT")

t_NAME = (r"MCCOY")

t_STARTUP = (r"BEGIN")

t_BODYPART = (r"ARM|LEG|HEAD|BODY|ALL")

t_BODYPART_COMMAND = (r"VIEW")
t_QUANTITY_COMMAND = (r"UP|DOWN|LEFT|RIGHT|NEARER|CLOSER|FURTHER")
t_BASIC_COMMAND    = (r"RUN|RESET|BORED")

t_FLAVOR = (r"LET'S")

t_UNIT = (r"DEGREE|FEET|FOOT|INCH")


t_DIGIT = (r"OH|ZERO|ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE")
t_DECIMAL = (r"THIRTY|FORTY|SIXTY|EIGHTY|NINETY")
t_TRIPLEDIGIT = (r"HUNDRED")

def t_newline(t):
  r'\n+'
  t.lexer.lineno += len(t.value)

t_ignore = (" \t")

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))


########################################
# Begin Yacc
########################################

class Quantity(object):
  def __init__(self, amount):
    if amount in PORTIONS_TO_NUM:
      self.amount = PORTIONS_TO_NUM[amount]
      self.portion = True
    else:
      self.amount = amount
      self.portion = False

  def __repr__(self):
    return "Qty(%r, %r)" % (self.amount, self.portion)

class Command(object):
  def __init__(self, symbol, subtype=None, quantity=0, unit=None):
    self.symbol   = symbol
    self.subtype  = subtype
    self.quantity = quantity
    self.unit = unit

  def __repr__(self):
    return "Command(%r, %r, %r, %r)" % (self.symbol, self.subtype,
                                                  self.quantity,
                                                  self.unit)

# When parsing starts, try to make a "chemical_equation" because it's
# the name on left-hand side of the first p_* function definition.
# The first rule is empty because I let the empty string be valid

def p_command_portion_reverse(p):
  'command : PORTION QUANTITY_COMMAND'
  p[0] = Command(p[1], quantity=Quantity(p[2]))

def p_startup(p):
  'command : FLAVOR STARTUP'
  #p[0] = p[2]
  p[0] = Command('BEGIN')

def p_command_basic(p):
  'command : BASIC_COMMAND'
  p[0] = Command(p[1])

#def p_mccoy_command(p):
#  'command : NAME command'
#  p[0] = p[2]

def p_command_bodypart(p):
  'command : BODYPART_COMMAND BODYPART'
  p[0] = Command(p[1], subtype=p[2])

def p_number_digit(p):
  'number : DIGIT'
  p[0] = english_to_digit(p[1]) 

def p_number_decimal(p):
  'number : DECIMAL'
  p[0] = english_to_digit(p[1]) 

def p_number_tripledigit(p):
  'number : TRIPLEDIGIT'
  p[0] = english_to_digit(p[1]) 

def p_number_decimal_digit(p):
  'number : DECIMAL DIGIT'
  p[0] = english_to_digit(p[1]) + english_to_digit(p[2]) 

def p_number_triple_decimal_digit(p):
  'number : TRIPLEDIGIT DECIMAL DIGIT'
  #p[0] = p[1] + p[2] + p[3]
  p[0] = english_to_digit(p[1]) + english_to_digit(p[2]) + english_to_digit(p[3])

def p_quantity_portion(p):
  'quantity : PORTION'
  p[0] = Quantity(p[1])

def p_quantity_number(p):
  'quantity : number'
  p[0] = Quantity(p[1])

def p_command_portion(p):
  'command : QUANTITY_COMMAND PORTION'
  p[0] = Command(p[1], quantity=Quantity(p[2]))


def p_command_quantity_unit(p):
  'command : QUANTITY_COMMAND quantity UNIT'
  p[0] = Command(p[1], quantity=p[2], unit=p[3])


def p_error(p):
    raise TypeError("unknown text at %r" % (p.value,))

  
class McCoyParser:
  def __init__(self):
    self.lexer = lex.lex()
    self.parser = yacc.yacc()

######

class TestPly(unittest.TestCase):
  def setUp(self):
    print "--------------"
    print "Begin New Test"
    print "--------------"
    self.parser = McCoyParser()
    self.data = '''
    MCCOY
    LET'S BEGIN
    HUNDRED FORTY FIVE
    MCCOY RIGHT HUNDRED FORTY FIVE DEGREE
    MCCOY LEFT THIRTY TWO DEGREE
    MCCOY HALFWAY CLOSER
    MCCOY HALFWAY FURTHER
    MCCOY HALFWAY NEARER
    MCCOY VIEW BODY
    MCCOY VIEW LEG
    MCCOY VIEW ARM
    MCCOY VIEW HEAD
    MCCOY VIEW ALL
    SLIGHTLY CLOSER
    SLIGHTLY FURTHER
    '''
  def tearDown(self):
    pass

  def test_tokenize(self):
    self.parser.lexer.input(self.data)
    while True:
      tok = self.parser.lexer.token()
      if not tok: break      # No more input
      print tok

class TestParser(unittest.TestCase):
  def setUp(self):
    print "--------------"
    print "Begin New Test"
    print "--------------"
    self.parser = McCoyParser()
    self.data = '''
    LET'S BEGIN
    VIEW BODY
    VIEW LEG
    VIEW ARM
    VIEW HEAD
    VIEW ALL
    RIGHT FIVE DEGREE
    RIGHT FORTY DEGREE
    RIGHT HUNDRED DEGREE
    RIGHT FORTY FIVE DEGREE
    RIGHT HUNDRED FORTY FIVE DEGREE
    RIGHT HALFWAY
    RIGHT QUARTER
    SLIGHTLY CLOSER
    SLIGHTLY FURTHER
    BORED
    '''
    '''
    '''
    #MCCOY RIGHT HUNDRED FORTY FIVE DEGREE
  def tearDown(self):
    pass

  def test_parse(self):
    lines = self.data.strip().split('\n')
    for line in lines:
      result = self.parser.parser.parse(line)
      print result

# Give the lexer some input

if __name__ == '__main__':
  unittest.main()
