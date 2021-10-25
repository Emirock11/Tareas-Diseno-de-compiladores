from antlr.CoolListener import CoolListener
from antlr.CoolParser import CoolParser
from typing import KeysView
from unittest.main import main
import myexceptions
import structure as storage

class Lisstener(CoolListener):
    def __init__(self):
        self.currentClass = None
        self.baseClass = storage.SymbolTable()
        self.pending_inheritance = dict()

        # Reset st.classes so that it doesnt save other file klasses
        storage.allClasses = {}
        storage.ctxTypes = storage.SymbolTable()

        # Add classes to st
        self.setBaseClasses()

    def exitProgram(self, ctx: CoolParser.ProgramContext):
        try:
            storage.lookupClass('Main').lookupMethod('main')
        except KeyError as e:
            raise myexceptions.NoMainException
        
        # Fix inheritance now that the whole hierarchy is present
        for _name, _inherits in self.pending_inheritance.items():
            # Save previous attributes and methods
            _klass = storage.lookupClass(_name)
            _prev_attr = _klass.attributes
            _prev_methods = _klass.methods

            # Save same klass but now with inheritance,
            # check that the inherited klass exists.
            try:
                storage.Klass(_name, inherits=_inherits)
            except KeyError:
                raise myexceptions.TypeNotFound
            
            # Restore attributes and methods
            _new_klass = storage.lookupClass(_name)
            _new_klass.attributes = _prev_attr
            _new_klass.methods = _prev_methods



    def enterClass(self, ctx: CoolParser.KlassContext):
        _types = ctx.TYPE()
        _klassName = _types[0].getText()

        # Check if klass is redefining basic klasses
        if _klassName in self.baseClass:
            raise myexceptions.RedefineBasicClassException

        # Check if klass is being redifined
        try:
            _klass = storage.lookupClass(_klassName)
            if _klass:
                raise myexceptions.ClassRedefinition
        except KeyError:
            pass

        # Inheritance is dealt at exit given thatr validHierarchy in store is
        # preventing assigning inheritance without validating.
        # It is done on exit so that conformance listener has everything ready
        if len(_types) > 1:
            _inherit = _types[1].getText()

            # Check inheritance is not of these types.
            if _inherit in ['Bool', 'SELF_TYPE', 'String']:
                raise myexceptions.InvalidInheritsException
            
            # Save pending rearranging of inheritance after program exits.
            self.pending_inheritance[_klassName] = _inherit
            
        # Save klass
        _klass = storage.Klass(_klassName)
        self.currentClass = _klass
    
    def enterAtribute(self, ctx: CoolParser.AtributeContext):
        _id = ctx.ID().getText()
        _type = ctx.TYPE().getText()

        # Attribute name cannot be self
        if _id == 'self':
            raise myexceptions.SelfVariableException

        self.currentClass.addAttribute(_id, _type)

    def enterMethod(self, ctx: CoolParser.MethodContext):
        storage.ctxTypes[ctx] = ctx.TYPE().getText()

    def exitMethod(self, ctx: CoolParser.MethodContext):
        # Add method and its formals to the current klass
        name = ctx.ID().getText()
        _type = ctx.TYPE().getText()
        _formals = ctx.formal()
        _params = []
        for _formal in _formals:
            _params.append((_formal.ID().getText(), storage.ctxTypes[_formal]))
        self.currentClass.addMethod(name, storage.Method(_type, _params))
    
    def exitFormal(self, ctx: CoolParser.FormalContext):
        # Type rule: Pass TYPE()
        _type = ctx.TYPE().getText()
        storage.ctxTypes[ctx] = _type
    
    def setBaseClasses(self):
        storageClass = storage.Klass('SELF_TYPE')
        self.baseClass['SELF_TYPE'] = storageClass
        storageClass = storage.Klass('Int')
        self.baseClass['Int'] = storageClass
        storageClass = storage.Klass('Object')
        storageClass.addMethod('abort', storage.Method('Object'))
        storageClass.addMethod('type_name', storage.Method('Object'))
        storageClass.addMethod('copy', storage.Method('SELF_TYPE'))
        self.baseClass['String'] = storageClass
        storageClass = storage.Klass('Bool')
        self.baseClass['Bool'] = storageClass
        self.baseClass['Object'] = storageClass
        storageClass = storage.Klass('IO')
        storageClass.addMethod('out_string', storage.Method('SELF_TYPE', [('x', 'String')]))
        storageClass.addMethod('out_int', storage.Method('SELF_TYPE', [('x', 'Int')]))
        storageClass.addMethod('in_string', storage.Method('String'))
        storageClass.addMethod('in_int', storage.Method('Int'))
        self.baseClass['IO'] = storageClass
        storageClass = storage.Klass('String')
        storageClass.addMethod('length', storage.Method('Int'))
        storageClass.addMethod('concat', storage.Method('String', [('s', 'String')]))
        storageClass.addMethod('substr', storage.Method('String', [('i', 'Int'), ('l', 'Int')]))
        
        








