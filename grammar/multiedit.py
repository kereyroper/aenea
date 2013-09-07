# This file is a command-module for Dragonfly.
#
# (based on the multiedit module from dragonfly-modules project)
# (heavily modified, you probably want the original)
# (the original copyright notice is reproduced below)
#
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

import raul

try:
    import pkg_resources

    pkg_resources.require("dragonfly >= 0.6.5beta1.dev-r99")
except ImportError:
    pass

from dragonfly import Config, Section, Item, MappingRule, CompoundRule, Grammar, IntegerRef, Dictation, RuleRef, Alternative, Repetition, Literal, Sequence
from proxy_nicknames import *

vim_context = AppRegexContext(name=".*VIM.*")

#---------------------------------------------------------------------------
# Here we globally defined the release action which releases all
#  modifier-keys used within this grammar.  It is defined here
#  because this functionality is used in many different places.
#  Note that it is harmless to release ("...:up") a key multiple
#  times or when that key is not held down at all.

release = Key("Shift_L:up, Control_L:up")

#---------------------------------------------------------------------------
# Set up this module's configuration.

def Nested(command):
  return Text(command) + Key("Left:%i" % (len(command) / 2))

command_table = {
  # Spoken-form        normal command              VIM (can set to None if same as normal)

  #### Cursor manipulation
  "up [<n>]":(         Key("Up:%(n)d"),            None),
  "down [<n>]":(       Key("Down:%(n)d"),          None),
  "left [<n>]":(       Key("Left:%(n)d"),          None),
  "right [<n>]":(      Key("Right:%(n)d"),         None),
  "gope [<n>]":(       Key("Prior:%(n)d"),         None),
  "drop [<n>]":(       Key("Next:%(n)d"),          None),
  "port [<n>]":(       Key("c-Left:%(n)d"),        Key("Escape, [ %(n)dbi ]") ),
  "yope [<n>]":(       Key("c-Right:%(n)d"),       Key("Escape, [ %(n)dwwi ]") ),
  "care":(             Key("Home"),                None),
  "doll":(             Key("End"),                 None),
  "file top":(         Key("c-Home"),              Key("Escape, 1, s-g, i") ),
  "file toe":(         Key("c-End"),               Key("Escape, s-g, i") ),

  #### Various keys
  "ace [<n>]":(        Key("space:%(n)d"),         None),
  "tab [<n>]":(        Key("Tab:%(n)d"),           None),
  "slap [<n>]":(       Key("Return:%(n)d"),        None),
  "chuck [<n>]":(      Key("Delete:%(n)d"),        None),
  "scratch [<n>]":(    Key("BackSpace:%(n)d"),     None),
  "act":(              Key("Escape"),              None),

  #### Symbols
  "amp [<n>]":(        Key("ampersand:%(n)d"),     None),
  "star [<n>]":(       Key("asterisk:%(n)d"),      None),
  "at sign [<n>]":(    Key("at:%(n)d"),            None),
  "back ash [<n>]":(   Key("backslash:%(n)d"),     None),
  "backtick [<n>]":(   Key("grave:%(n)d"),         None),
  "bar [<n>]":(        Key("bar:%(n)d"),           None),
  "hat [<n>]":(        Key("asciicircum:%(n)d"),   None),
  "yeah [<n>]":(       Key("colon:%(n)d"),         None),
  "drip [<n>]":(       Key("comma:%(n)d"),         None),
  "dollar [<n>]":(     Key("dollar:%(n)d"),        None),
  "dot [<n>]":(        Key("period:%(n)d"),        None),
  "quote [<n>]":(      Key("quotedbl:%(n)d"),      None),
  "eek [<n>]":(        Key("equal:%(n)d"),         None),
  "bang [<n>]":(       Key("exclam:%(n)d"),        None),
  "pound [<n>]":(      Key("numbersign:%(n)d"),    None),
  "hyph [<n>]":(       Key("minus:%(n)d"),         None),
  "percent [<n>]":(    Key("percent:%(n)d"),       None),
  "cross [<n>]":(      Key("plus:%(n)d"),          None),
  "quest [<n>]":(      Key("question:%(n)d"),      None),
  "ash [<n>]":(        Key("slash:%(n)d"),         None),
  "smote [<n>]":(      Key("apostrophe:%(n)d"),    None),
  "tilde [<n>]":(      Key("asciitilde:%(n)d"),    None),
  "rail [<n>]":(       Key("underscore:%(n)d"),    None),
  "push [<n>]":(       Key("parenleft:%(n)d"),     None),
  "pop [<n>]":(        Key("parenright:%(n)d"),    None),

  #### Nested
  "circle":(           Nested("()"),               None),
  "square":(           Nested("[]"),               None),
  "box":(              Nested("[]"),               None),
  "diamond":(          Nested("<>"),               None),
  "hexy":(             Nested("{}"),               None),
  "nest quote":(       Nested("\"\""),             None),
  "nest smote":(       Nested("''"),               None),
    
  #### Legacy symbols (probably will remove these later)
  "oop [<n>]":(        Key("period:%(n)d"),        None),
  "dub quote [<n>]":( Key("quotedbl:%(n)d"),       None),
  "sing quote [<n>]":(  Key("apostrophe:%(n)d"),   None),

  # Spoken-form      normal command       VIM (can set to None if same as normal)

  #### Lines
  "wipe [<n>]":(     Key("Home, Shift_L:down, Down:%(n)d, Up, End, Delete, Shift_L:up, BackSpace"),
                                          Key("Escape, [ d%(n)ddi ]") ),
  "strip":(          Key("s-End, Delete"),
                                          Key("Escape, l, d, dollar, a") ),
  "striss":(         Key("s-Home, Delete"),
                                          Key("Escape, l, d, asciicircum, i") ),
  "nab [<n>]":(      Key("Home, Shift_L:down, Down:%(n)d, Up, End, Shift_L:up, c-j, End"),
                                          Key("Escape, [ y%(n)dyi ]") ),
  "trance [<n>]":(   Key("Home, Shift_L:down, Down:%(n)d, Up:2, End, Shift_L:up, c-j, End, Return, c-k"),
                                          Key("Escape, [ y%(n)dy%(n)djpi ]") ),
  "lineup [<n>]":(   Key("Home, Shift_L:down, End, Shift_L:up, c-q, Delete, Up:%(n)d, Home, Return, Up, c-k"),
                                          Key("Escape, [ dd%(n)dk ], Home, [ 1P ], i") ),
  "line down [<n>]":(Key("Home, Shift_L:down, End, Shift_L:up, c-q, Delete, Down:%(n)d, Home, Return, Up, c-k"),
                                          Key("Escape, [ dd%(n)dj ], Home, [ 1P ], i") ),

  #### Words
  "bump [<n>]":(     Key("Right:2, c-Left, cs-Right:%(n)d, Delete:2"),
                                          Key("Escape, [ lwbd%(n)dwi ]")),
  "whack [<n>]":(    Key("Left, c-Right, cs-Left:%(n)d, Delete:2"),
                                          Key("Escape, [ lw%(n)dbd%(n)dwi ]")),
  }

# Python specific
python_command_table = {
  # Spoken-form        normal command              VIM (can set to None if same as normal)
  "private":(          Nested("____"),             None),
  "dub dock string":(  Nested('""""""'),           None),
  "dock string":(      Nested("''''''"),           None),
  "square sing":(      Nested("['']"),             None),
  "box sing":(         Nested("['']"),             None),
  "square dub":(       Nested('[""]'),             None),
  "box dub":(          Nested('[""]'),             None),
  "int":(              Text("int"),                None),
  "float":(            Text("float"),              None),
  "stir":(             Text("str"),                None),
  "list":(             Text("list"),               None),
  "dictionary":(       Text("dict"),               None),
  "set":(              Text("set"),                None),
  "tuple":(            Text("tuple"),              None),
  "lazy range":(       Text("xrange"),             None),
  "range":(            Text("range"),              None),
  "is instance":(      Text("isinstance"),         None),
  "iter":(             Text("iter"),               None),
  "items":(            Text("items"),              None),
  "keys":(             Text("keys"),               None),
  "values":(           Text("values"),             None),
  "get atter":(        Text("getattr"),            None),
  "set atter":(        Text("setattr"),            None),
  "has atter":(        Text("hasattr"),            None),
  "print":(            Text("print"),              None),
  "if test":(          Text("if "),                None),
  "elif":(             Text("elif "),              None),
  "else":(             Text("else"),               None),
  "in it":(            Text("init"),               None),
  "repper":(           Text("repr"),               None),
  "deaf":(             Text("def "),               None),
  "log and":(          Text("and "),               None),
  "log or":(           Text("or "),                None),
  "log not":(          Text("not "),               None),
  "for loop":(         Text("for "),               None),
  "bit ore":(          Text("| "),                 None),
  "bit and":(          Text("& "),                 None),
  "bit ex or":(        Text("^ "),                 None),
  "times":(            Text("* "),                 None),
  "divided":(          Text("/ "),                 None),
  "plus":(             Text("+ "),                 None),
  "minus":(            Text("- "),                 None),
  "plus equal":(       Text("+= "),                None),
  "minus equal":(      Text("-= "),                None),
  "times equal":(      Text("*= "),                None),
  "divided equal":(    Text("/= "),                None),
  "mod equal":(        Text("%%= "),               None),
  "as name":(          Text("as "),                None),
  "in":(               Text("in "),                None),
  "while":(            Text("while "),             None),
  "class":(            Text("class "),             None),
  "with context":(     Text("with "),              None),
  "import":(           Text("import "),            None),
  "from":(             Text("from "),              None),
  "raise":(            Text("raise "),             None),
  "return":(           Text("return "),            None),
  "none":(             Text("None"),               None),
  "none":(             Text("True"),               None),
  "none":(             Text("False"),              None),
  "try":(              Text("try"),                None),
  "except":(           Text("except"),             None),
  "lambda":(           Text("lambda "),            None),
  "assert":(           Text("assert "),            None),
  "self":(             Text("self"),               None),
  "self dot":(         Text("self."),              None),
  "pass":(             Text("pass"),               None),
  "delete":(           Text("del "),               None),
  }

def format_snakeword(text):
  return text[0][0].upper() + text[0][1:] + ("_" if len(text) > 1 else "") + format_score(text[1:])

def format_score(text):
  return "_".join(text)

def format_camel(text):
  return text[0] + "".join([word[0].upper() + word[1:] for word in text[1:]])

def format_proper(text):
  return "".join(word.capitalize() for word in text)

def format_relpath(text):
  return "/".join(text)

def format_abspath(text):
  return "/" + format_relpath(text)

def format_scoperesolve(text):
  return "::".join(text)

def format_jumble(text):
  return "".join(text)

def format_dotword(text):
  return ".".join(text)

def format_dashword(text):
  return "-".join(text)

def format_natword(text):
  return " ".join(text)

class FormatRule(CompoundRule):
  spec = ("[upper | natural] ( proper | camel | rel-path | abs-path | score | "
          "scope-resolve | jumble | dotword | dashword | natword | snakeword) [<dictation>]")
  extras = [Dictation(name="dictation")]
  
  def value(self, node):
    words = node.words()

    uppercase = words[0] == "upper"
    lowercase = words[0] != "natural"

    if lowercase:
      words = [word.lower() for word in words]
    if uppercase:
      words = [word.upper() for word in words]

    words = [word.split("\\", 1)[0].replace("-", "") for word in words]
    if words[0].lower() in ("upper", "natural"):
      del words[0]

    function = globals()["format_%s" % words[0].lower()]
    formatted = function(words[1:])

    return Text(formatted)

# Set up vim default values.
for table in (command_table, python_command_table):
  for (key, (command, vim_command)) in table.iteritems():
    if vim_command is None:
      table[key] = (command, command)

#---------------------------------------------------------------------------
# Here we define the keystroke rule.

# This rule maps spoken-forms to actions.  Some of these 
#  include special elements like the number with name "n" 
#  or the dictation with name "text".  This rule is not 
#  exported, but is referenced by other elements later on.
#  It is derived from MappingRule, so that its "value" when 
#  processing a recognition will be the right side of the 
#  mapping: an action.
# Note that this rule does not execute these actions, it
#  simply returns them when it's value() method is called.
#  For example "up 4" will give the value Key("up:4").
# More information about Key() actions can be found here:
#  http://dragonfly.googlecode.com/svn/trunk/dragonfly/documentation/actionkey.html
class KeystrokeRule(MappingRule):
  exported = False

  extras = [
    IntegerRef("n", 1, 100),
    Dictation("text"),
    Dictation("text2"),
    ]
  defaults = {
    "n": 1,
    }

#---------------------------------------------------------------------------
# Here we create an element which is the sequence of keystrokes.

# First we create an element that references the keystroke rule.
#  Note: when processing a recognition, the *value* of this element
#  will be the value of the referenced rule: an action.

mapping = dict((key, value[0]) for (key, value) in command_table.iteritems())
command_table.update(python_command_table)
vim_mapping = dict((key, value[1]) for (key, value) in command_table.iteritems())

format_rule = RuleRef(name="format_rule", rule=FormatRule(name="i"))
alternatives = [
      RuleRef(rule=KeystrokeRule(mapping=mapping, name="c")),
      format_rule,
    ]

vim_alternatives = [
      RuleRef(rule=KeystrokeRule(mapping=vim_mapping, name="e")),
      format_rule,
    ]

single_action = Alternative(alternatives)
vim_single_action = Alternative(vim_alternatives)

# Can only be used as the last element
alphabet_mapping = dict((key, Text(value)) for (key, value) in raul.LETTERS.iteritems())
numbers_mapping = dict((key, Text(value)) for (key, value) in raul.DIGITS.iteritems())
alphanumeric_mapping = dict((key, Text(value)) for (key, value) in raul.ALPHANUMERIC.iteritems())

alphabet_rule = Sequence([Literal("letters"), Repetition(RuleRef(name="x", rule=MappingRule(name="t", mapping=alphabet_mapping)), min=1, max=20)])
numbers_rule = Sequence([Literal("digits"), Repetition(RuleRef(name="y", rule=MappingRule(name="u", mapping=numbers_mapping)), min=1, max=20)])
alphanumeric_rule = Sequence([Literal("alphanumeric"), Repetition(RuleRef(name="z", rule=MappingRule(name="v", mapping=alphanumeric_mapping)), min=1, max=20)])
finishes = [alphabet_rule, numbers_rule, alphanumeric_rule]

# Second we create a repetition of keystroke elements.
#  This element will match anywhere between 1 and 16 repetitions
#  of the keystroke elements.  Note that we give this element
#  the name "sequence" so that it can be used as an extra in
#  the rule definition below.
# Note: when processing a recognition, the *value* of this element
#  will be a sequence of the contained elements: a sequence of
#  actions.
sequence = Repetition(single_action, min=1, max=16, name="sequence")
vim_sequence = Repetition(vim_single_action, min=1, max=16, name="sequence")

extras = [
    sequence, # Sequence of actions defined above.
    IntegerRef("n", 1, 100), # Times to repeat the sequence.
    Alternative([Literal("hi")], name="finish"),
]

vim_extras = [
    vim_sequence, # Sequence of actions defined above.
    IntegerRef("n", 1, 100), # Times to repeat the sequence.
    Alternative([Literal("hi")], name="finish"),
]

#---------------------------------------------------------------------------
# Here we define the top-level rule which the user can say.

class LiteralRule(CompoundRule):
  spec = "literal <format_rule>"

  extras = [format_rule]

  def _process_recognition(self, node, extras):
    extras["format_rule"].execute()

# This is the rule that actually handles recognitions. 
#  When a recognition occurs, it's _process_recognition() 
#  method will be called.  It receives information about the 
#  recognition in the "extras" argument: the sequence of 
#  actions and the number of times to repeat them.
class RepeatRule(CompoundRule):
  # Here we define this rule's spoken-form and special elements.
  spec = "<sequence> [ ( literal <format_rule> )  | <finish> ] [repeat <n> times]"

  defaults = {
    "n": 1, # Default repeat count.
  }

  # This method gets called when this rule is recognized.
  # Arguments:
  #  - node -- root node of the recognition parse tree.
  #  - extras -- dict of the "extras" special elements:
  #   . extras["sequence"] gives the sequence of actions.
  #   . extras["n"] gives the repeat count.
  def _process_recognition(self, node, extras):
    sequence = extras["sequence"]
    count = extras["n"]
    for i in range(count):
      for action in sequence:
        action.execute()
        #release.execute()
      if "format_rule" in extras:
        extras["format_rule"].execute()
      if "finish" in extras:
        for action in extras["finish"][1]:
          action.execute()

#---------------------------------------------------------------------------
# Create and load this module's grammar.

grammar = Grammar("multi edit")
grammar.add_rule(RepeatRule(extras=vim_extras + [format_rule, Alternative(finishes, name="finish")], name="b", context=vim_context))
grammar.add_rule(RepeatRule(extras=extras + [format_rule, Alternative(finishes, name="finish")], name="a", context=(~vim_context)))
grammar.add_rule(LiteralRule())

grammar.load()

# Unload function which will be called at unload time.
def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None