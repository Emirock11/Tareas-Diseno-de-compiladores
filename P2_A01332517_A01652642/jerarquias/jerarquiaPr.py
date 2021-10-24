from typing import KeysView
from unittest.main import main
from antlr.CoolListener import CoolListener
from antlr.CoolParser import CoolParser
import myexceptions
import structure as struct

class PreJerarquia(CoolListener):

    def __init__(self):
        self.claseActual = None
        self.clasesBase = struct.SymbolTable()
        self.herencia = dict()

        struct.allClasses = {}
        struct.ctxTypes = struct.SymbolTable()

        self.setClasesBase()

    def ingresarClass(self, ctx: CoolParser.KlassContext):
        _types = ctx.TYPE()
        className = _types[0].getText()

        if className in self.clasesBase:
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
            
            self.herencia[className] = _inherit
            
        _klass = struct.Klass(className)
        self.claseActual = _klass
    
    def ingresarMethod(self, ctx: CoolParser.MethodContext):
        struct.ctxTypes[ctx] = ctx.TYPE().getText()

    def salirMethod(self, ctx: CoolParser.MethodContext):
        ID = ctx.ID().getText()
        type = ctx.TYPE().getText()
        formals = ctx.formal()
        listaPar = []
        for formal in formals:
            listaPar.append((formal.ID().getText(), struct.ctxTypes[formal]))
        self.claseActual.addMethod(ID, struct.Method(type, listaPar))
        ctx.namemethod = ID
        ctx.typemethod = type

    def ingresarAtribute(self, ctx: CoolParser.AtributeContext):
        _id = ctx.ID().getText()
        _type = ctx.TYPE().getText()

        if _id == 'self':
            raise myexceptions.SelfVariableException

        self.claseActual.addAttribute(_id, _type)

    def salirPrograma(self, ctx: CoolParser.ProgramContext):
        try:
            struct.lookupClass('Main').lookupMethod('main')
        except KeyError as e:
            raise myexceptions.NoMainException
        
        for _name, _inherits in self.herencia.items():
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
    
    def salirFormal(self, ctx: CoolParser.FormalContext):
        _type = ctx.TYPE().getText()
        struct.ctxTypes[ctx] = _type
        ctx.typename = _type
    
    def setClasesBase(self):
        k = struct.Klass('Object')
        k.addMethod('abort', struct.Method('Object'))
        k.addMethod('type_name', struct.Method('Object'))
        k.addMethod('copy', struct.Method('SELF_TYPE'))
        self.clasesBase['Object'] = k
        k = struct.Klass('IO')
        k.addMethod('out_string', struct.Method('SELF_TYPE', [('x', 'String')]))
        k.addMethod('out_int', struct.Method('SELF_TYPE', [('x', 'Int')]))
        k.addMethod('in_string', struct.Method('String'))
        k.addMethod('in_int', struct.Method('Int'))
        self.clasesBase['IO'] = k
        k = struct.Klass('Int')
        self.clasesBase['Int'] = k
        k = struct.Klass('String')
        k.addMethod('length', struct.Method('Int'))
        k.addMethod('concat', struct.Method('String', [('s', 'String')]))
        k.addMethod('substr', struct.Method('String', [('i', 'Int'), ('l', 'Int')]))
        self.clasesBase['String'] = k
        k = struct.Klass('Bool')
        self.clasesBase['Bool'] = k
        k = struct.Klass('SELF_TYPE')
        self.clasesBase['SELF_TYPE'] = k