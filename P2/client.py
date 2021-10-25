import sys
from antlr.CoolLexer import *
from antlr.CoolParser import *
from antlr.CoolListener import *
from typecheck import Typecheck
from antlr4 import *

class Printer(CoolListener):
   def exitEveryRule(self, ctx: ParserRuleContext):
       print("<{}>".format(ctx.getText()))

       return super().exitEveryRule(ctx) 

def main(file):
    parser = CoolParser(CommonTokenStream(CoolLexer(FileStream(file))))
    tree = parser.program()

    walker = ParseTreeWalker()
    typecheck = Typecheck()
    walker.walk(typecheck, tree)

if __name__ == '__main__':
    main("test.cool")
