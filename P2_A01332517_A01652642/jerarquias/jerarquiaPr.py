from typing import KeysView
from unittest.main import main
from antlr.CoolListener import CoolListener
from antlr.CoolParser import CoolParser
import myexceptions
import structure as struct

class PreJerarquia(CoolListener):

    def __init__(self):
        self.currentKlass = None
        self.baseKlasses = struct.SymbolTable()
        self.pending_inheritance = dict()

        struct.allClasses = {}
        struct.ctxTypes = struct.SymbolTable()

        self.setBaseClasses()

    def enterMethod(self, ctx: CoolParser.MethodContext):
        struct.ctxTypes[ctx] = ctx.TYPE().getText()

    def exitMethod(self, ctx: CoolParser.MethodContext):
        name = ctx.ID().getText()
        _type = ctx.TYPE().getText()
        _formals = ctx.formal()
        _params = []
        for _formal in _formals:
            _params.append((_formal.ID().getText(), struct.ctxTypes[_formal]))
        self.currentKlass.addMethod(name, struct.Method(_type, _params))
        ctx.namemethod = name
        ctx.typemethod = _type

    def enterKlass(self, ctx: CoolParser.KlassContext):
        _types = ctx.TYPE()
        className = _types[0].getText()

        if className in self.baseKlasses:
            raise myexceptions.RedefineBasicClassException

        try:
            _klass = struct.lookupClass(className)
            if _klass:
                raise myexceptions.ClassRedefinition
        except KeyError:
            pass

        if len(_types) > 1:
            _inherit = _types[1].getText()

            if _inherit in ['Bool', 'SELF_TYPE', 'String']:
                raise myexceptions.InvalidInheritsException
            
            self.pending_inheritance[className] = _inherit
            
        _klass = struct.Klass(className)
        self.currentKlass = _klass
    
    def enterAtribute(self, ctx: CoolParser.AtributeContext):
        _id = ctx.ID().getText()
        _type = ctx.TYPE().getText()

        if _id == 'self':
            raise myexceptions.SelfVariableException

        self.currentKlass.addAttribute(_id, _type)

    def exitProgram(self, ctx: CoolParser.ProgramContext):
        try:
            struct.lookupClass('Main').lookupMethod('main')
        except KeyError as e:
            raise myexceptions.NoMainException
        
        for _name, _inherits in self.pending_inheritance.items():
            _klass = struct.lookupClass(_name)
            _prev_attr = _klass.attributes
            _prev_methods = _klass.methods

            try:
                struct.Klass(_name, inherits=_inherits)
            except KeyError:
                raise myexceptions.TypeNotFound
            
            _new_klass = struct.lookupClass(_name)
            _new_klass.attributes = _prev_attr
            _new_klass.methods = _prev_methods



    

    
    
    def exitFormal(self, ctx: CoolParser.FormalContext):
        _type = ctx.TYPE().getText()
        struct.ctxTypes[ctx] = _type
        ctx.typename = _type
    
    def setBaseClasses(self):
        k = struct.Klass('Object')
        k.addMethod('abort', struct.Method('Object'))
        k.addMethod('type_name', struct.Method('Object'))
        k.addMethod('copy', struct.Method('SELF_TYPE'))
        self.baseKlasses['Object'] = k
        k = struct.Klass('IO')
        k.addMethod('out_string', struct.Method('SELF_TYPE', [('x', 'String')]))
        k.addMethod('out_int', struct.Method('SELF_TYPE', [('x', 'Int')]))
        k.addMethod('in_string', struct.Method('String'))
        k.addMethod('in_int', struct.Method('Int'))
        self.baseKlasses['IO'] = k
        k = struct.Klass('Int')
        self.baseKlasses['Int'] = k
        k = struct.Klass('String')
        k.addMethod('length', struct.Method('Int'))
        k.addMethod('concat', struct.Method('String', [('s', 'String')]))
        k.addMethod('substr', struct.Method('String', [('i', 'Int'), ('l', 'Int')]))
        self.baseKlasses['String'] = k
        k = struct.Klass('Bool')
        self.baseKlasses['Bool'] = k
        k = struct.Klass('SELF_TYPE')
        self.baseKlasses['SELF_TYPE'] = k