import sys
import unittest

from antlr4 import *
from antlr.CoolLexer import CoolLexer
from antlr.CoolParser import CoolParser
from myexceptions import *
from jerarquias.jerarquiaPr import PreJerarquia
from jerarquias.jerarquia import Grarquia

def parseCase(caseName):
    parser = CoolParser(CommonTokenStream(CoolLexer(FileStream("input/semantic/%s.cool" % caseName))))
    return parser.program()

class CoolTests(unittest.TestCase):
    def setUp(self): 
        self.walker = ParseTreeWalker()

    def test1(self):
        tree = parseCase("assignnoconform")
        with self.assertRaises(DoesNotConform):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test2(self):
        tree = parseCase("attrbadinit")
        with self.assertRaises(UndeclaredIdentifier):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test3(self):
        tree = parseCase("attroverride")
        with self.assertRaises(NotSupported):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test4(self):
        tree = parseCase("badargs1")
        with self.assertRaises(DoesNotConform):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test5(self):
        tree = parseCase("badarith")
        with self.assertRaises(TypeCheckMismatch):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test6(self):
        tree = parseCase("baddispatch")
        with self.assertRaises(MethodNotFound):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test7(self):
        tree = parseCase("badequalitytest")
        with self.assertRaises(TypeCheckMismatch):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test8(self):
        tree = parseCase("badequalitytest2")
        with self.assertRaises(TypeCheckMismatch):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test9(self):
        tree = parseCase("badmethodcallsitself")
        with self.assertRaises(CallTypeCheckMismatch):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test10(self):
        tree = parseCase("badstaticdispatch")
        with self.assertRaises(MethodNotFound):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test11(self):
        tree = parseCase("badwhilebody")
        with self.assertRaises(MethodNotFound):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test12(self):
        tree = parseCase("badwhilecond")
        with self.assertRaises(TypeCheckMismatch):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test13(self):
        tree = parseCase("caseidenticalbranch")
        with self.assertRaises(InvalidCase):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test14(self):
        tree = parseCase("dupformals")
        with self.assertRaises(KeyError):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test15(self):
        tree = parseCase("letbadinit")
        with self.assertRaises(DoesNotConform):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test16(self):
        tree = parseCase("lubtest")
        with self.assertRaises(DoesNotConform):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test17(self):
        tree = parseCase("missingclass")
        with self.assertRaises(TypeNotFound):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test18(self):
        tree = parseCase("outofscope")
        with self.assertRaises(UndeclaredIdentifier):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test19(self):
        tree = parseCase("redefinedclass")
        with self.assertRaises(ClassRedefinition):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test20(self):
        tree = parseCase("returntypenoexist")
        with self.assertRaises(TypeNotFound):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test21(self):
        tree = parseCase("trickyatdispatch2")
        with self.assertRaises(MethodNotFound):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test22(self):
        tree = parseCase("selftypebadreturn")
        with self.assertRaises(TypeCheckMismatch):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test23(self):
        tree = parseCase("overridingmethod4")
        with self.assertRaises(InvalidMethodOverride):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

    def test24(self):
        tree = parseCase("signaturechange")
        with self.assertRaises(InvalidMethodOverride):
            self.walker.walk(PreJerarquia(), tree)
            self.walker.walk(Grarquia(), tree)

if __name__ == '__main__':
    unittest.main()