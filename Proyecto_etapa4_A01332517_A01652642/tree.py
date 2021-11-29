from antlr.CoolListener import CoolListener
from antlr.CoolParser import CoolParser
from jerarquias.jerarquiaPr import PreJerarquia
from jerarquias.jerarquia import Grarquia
from myexceptions import *

# Excluded
ex = {'Base'}

# Special no incluyen tipo al final
es = {'Program', 'Klass', 'Method'}

# True names
tt = {'Program': 'AProgram', 'Klass': 'AClassDecl', 'Method': 'AMethodFeature', 'Block':'AListExpr', 'Add':'APlusExpr', 'Sub':'AMinusExpr','Mult':'AMultExpr', 'Div':'ADivExpr','Integer':'AIntExpr', 'Bool':'ABoolExpr', 'Call':'ACallExpr', 'Object':'AObjectExpr', 'Formal':'AFormal'}


class TreePrinter(CoolListener):
    def __init__(self, types={}):
        self.depth = 0
        self.types = types

    def checkContext(self, type):
        if type in CoolParser.ProgramContext:
            return True
        return False

    def enterEveryRule(self, ctx):
        self.depth = self.depth + 1
        s = ''
        nTabs = 0
        #print("ctxName: "+str(type(ctx).__name__[:-7]))
        for i in range(self.depth-1):
            s += " "
            # Se tienen que dividir si son de tipo Program, Klass, un Metodo o un Entero
        typ3 = str(type(ctx).__name__[:-7])
        #print("Entrando: "+typ3)
        if typ3 not in ex:
            #print("typ3 not in ex")
            _extra = ''
            if typ3 not in es:
                #print("typ3 not in es")
                _extra = ":" + typ3
            
            if type(ctx) is CoolParser.ProgramContext:
                print("%s - %s" % (s, type(ctx).__name__[:-7]))
                #self.output += "{}>- {}\n".format(s, typ3)
            else:
                print("| %s - %s: " % (s, type(ctx).__name__[:-7]))
                #self.output += "{}`- {}{}\n".format(s, typ3, _extra)
            if type(ctx) is CoolParser.KlassContext:
                print("\t\\%s - %s" % (s, type(ctx).__name__[:-7]))
                PreJerarquia().ingresarClass(ctx)
                #self.output += "{}   |- {}\n".format(s, ctx.nameklass)
                #self.output += "{}   |- {}\n".format(s, ctx.nameinherits)
            if type(ctx) is CoolParser.MethodContext:
                print("\t\t\\%s - %s\n" % (s, type(ctx).__name__[:-7]))
                #self.output += "{}   |- {}\n".format(s, ctx.namemethod)
                #self.output += "{}   |- {}\n".format(s, ctx.typemethod)
            if type(ctx) is CoolParser.IntegerContext:
                print("\t\t\t\\%s - %s\n" % (s, type(ctx).__name__[:-7]))
                #self.output += "{}|   `- {}\n".format(s, ctx.truevalue) 
        '''
        if str(type(ctx).__name__[:-7]) == "Program":
            print("%s - %s\n" % (s, type(ctx).__name__[:-7]))
            nTabs+=1
        elif str(type(ctx).__name__[:-7]) == "Klass":
            print("\t\\%s - %s\n" % (s, type(ctx).__name__[:-7]))
            nTabs+=1
        elif str(type(ctx).__name__[:-7]) == "Method":
            print("\t\t|%s - %s\n" % (s, type(ctx).__name__[:-7]))
            nTabs+=1
        '''

        '''
        try:
            print ("%s%s:%s" % (s, type(ctx).__name__[:-7], self.types[ctx]))
        except:
            print ("%s%s" % (s, type(ctx).__name__[:-7]))
        '''

    def exitEveryRule(self, ctx):
        self.depth = self.depth - 1

    def getOutput(self):
        print(self.output)
        return self.output