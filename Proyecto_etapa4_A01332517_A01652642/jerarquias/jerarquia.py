from antlr.CoolListener import CoolListener
from antlr.CoolParser import CoolParser
import myexceptions
import structure as struct
import time

class Grarquia(CoolListener):

    def __init__(self):
        self.idsTypes = None

    def ingresarClass(self, ctx: CoolParser.KlassContext):
        #print("ingresarClase()")
        ##time.sleep(1)
        className = ctx.TYPE()[0].getText()
        ctx.nameklass = className
        _klass = struct.lookupClass(className)
        ctx.nameinherits = _klass.inherits

        self.idsTypes = struct.SymbolTableWithScopes(_klass)
        self.idsTypes.openScope()
        self.idsTypes['self'] = 'self'
    
    def salirClass(self, ctx: CoolParser.KlassContext):
        #print("salirClase()")
        #time.sleep(1)
        self.idsTypes.closeScope()

    def ingresarAtribute(self, ctx: CoolParser.AtributeContext):
        #print("IngresarAtributo")
        #time.sleep(1)
        ID = ctx.ID().getText()
        _type = ctx.TYPE().getText()

        expr = ctx.expr()
        if expr:
            if hasattr(expr.getChild(0), 'ID'):
                exprID = expr.getChild(0).ID().getText()
                try:
                    self.idsTypes[exprID]
                except KeyError as e:
                    raise myexceptions.UndeclaredIdentifier
    
        try:
            _klass = self.idsTypes.klass
            _inherited = struct.lookupClass(_klass.inherits)
            _found = _inherited.lookupAttribute(ID)
            if _found != _type:
                raise myexceptions.NotSupported
        except KeyError:
            pass

        self.idsTypes[ID] = _type
        self.idsTypes.openScope()
    
    def salirAtribute(self, ctx: CoolParser.AtributeContext):
        #print("salirAtribute")
        #time.sleep(1)
        self.idsTypes.closeScope()

    def ingresarMethod(self, ctx: CoolParser.MethodContext):
        #print("ingresarMethod")
        #time.sleep(1)
        metodo = ctx.ID().getText()
        _inherits = self.idsTypes.klass.inherits
        if _inherits:
            _inheritedklass = struct.lookupClass(_inherits)
            try:
                _inheritedMethod = _inheritedklass.lookupMethod(metodo)
                if _inheritedMethod.type != ctx.TYPE().getText():
                    raise myexceptions.InvalidMethodOverride
                _inheritedFormals = _inheritedMethod.params
                _formals = ctx.formal()
                if len(_inheritedFormals) != len(_formals):
                    raise myexceptions.InvalidMethodOverride
                for i, v in enumerate(_inheritedFormals.values()):
                    _new_type = _formals[i].TYPE().getText()
                    if _new_type != v:
                        raise myexceptions.InvalidMethodOverride
            except KeyError:
                pass
        
        self.idsTypes.openScope()
        _formals = ctx.formal()
        for _formal in _formals:
            self.idsTypes[_formal.ID().getText()] = _formal.TYPE().getText()
    
    def salirMethod(self, ctx: CoolParser.MethodContext):
        #print("salirMethod")
        #time.sleep(1)
        expr = ctx.expr() 
        _type = ctx.TYPE().getText()

        if _type == 'SELF_TYPE':
            _type = self.idsTypes.klass.name
            exprType = struct.ctxTypes[expr]
            if exprType != 'self' and exprType != 'SELF_TYPE':
                raise myexceptions.TypeCheckMismatch
        else:
            try:
                exprType = struct.ctxTypes[expr]
                if exprType == 'self':
                    exprType = self.idsTypes.klass.name

                exprKlass = struct.lookupClass(exprType)
                _typeKlass = struct.lookupClass(_type)
            except KeyError:
                raise myexceptions.TypeNotFound

            if not _typeKlass.conforms(exprKlass):
                raise myexceptions.DoesNotConform
        
        self.idsTypes.closeScope()

    def ingresarFormal(self, ctx: CoolParser.FormalContext):
        #print("ingresarFormal")
        #time.sleep(1)
        ID = ctx.ID().getText()
        _type = ctx.TYPE().getText()
        if ID == 'self':
            raise myexceptions.SelfVariableException
        
        if _type == 'SELF_TYPE':
            raise myexceptions.SelftypeInvalidUseException
        
    
    def salirBase(self, ctx: CoolParser.BaseContext):
        #print("salirBase")
        #time.sleep(1)
        _type = struct.ctxTypes[ctx.getChild(0)]
        struct.ctxTypes[ctx] = _type
        ctx.typename = _type

    def ingresarIf(self, ctx: CoolParser.IfContext):
        #print("ingresarIf")
        #time.sleep(1)
        self.idsTypes.openScope()
        self.idsTypes.openScope()
    
    def salirIf(self, ctx: CoolParser.IfContext):
        #print("salirIf")
        #time.sleep(1)
        _trueType = struct.ctxTypes[ctx.expr()[1]]
        _falseType = struct.ctxTypes[ctx.expr()[2]]

        _trueKlass = struct.lookupClass(_trueType)
        _falseKlass = struct.lookupClass(_falseType)
        _union = _trueKlass.union(_falseKlass)

        struct.ctxTypes[ctx] = _union
        ctx.typename = _union
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()
    
    def ingresarWhile(self, ctx: CoolParser.WhileContext):
        #print("ingresarWhile")
        #time.sleep(1)
        self.idsTypes.openScope()
        self.idsTypes.openScope()
    
    def salirWhile(self, ctx: CoolParser.WhileContext):
        #print("salirWhile")
        #time.sleep(1)
        if struct.ctxTypes[ctx.expr()[0]] != 'Bool':
            raise myexceptions.TypeCheckMismatch
        
        struct.ctxTypes[ctx] = 'Object'
        ctx.typename = 'Object'
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()
    
    def ingresarLet(self, ctx: CoolParser.LetContext):
        #print("ingresarLet")
        #time.sleep(1)
        di = ctx.ID()
        types = ctx.TYPE()
        for i in range(len(di)-1, -1, -1):
            if di[i].getText() == 'self':
                raise myexceptions.SelfVariableException

            self.idsTypes.openScope()
            self.idsTypes[di[i].getText()] = types[i].getText()
    
    def salirLet(self, ctx: CoolParser.LetContext):
        #print("salirLet")
        #time.sleep(1)
        types = ctx.TYPE()
        expr = ctx.expr()

        for i, _type in enumerate(types):
            if i < (len(expr) - 1):
                _assign = struct.lookupClass(struct.ctxTypes[expr[i]])
                _to = struct.lookupClass(_type.getText())
                if not _to.conforms(_assign):
                    raise myexceptions.DoesNotConform

        _last = expr[len(expr) - 1]
        _lastType = struct.ctxTypes[_last]
        struct.ctxTypes[ctx] = _lastType
        ctx.typename = _lastType
        for _i in ctx.ID():
            self.idsTypes.closeScope()

    def ingresarCase(self, ctx: CoolParser.CaseContext):
        #print("ingresarCase")
        #time.sleep(1)
        di = ctx.ID()
        types = ctx.TYPE()

        _saved = set()
        for i, ID in reversed(list(enumerate(di))):
            _type = types[i].getText()

            if _type in _saved:
                raise myexceptions.InvalidCase

            _saved.add(_type)
            self.idsTypes.openScope()
            self.idsTypes[ID.getText()] = types[i].getText()
        
        _firstName = types[0].getText()
        _saved.discard(_firstName)
        _first  = struct.lookupClass(_firstName)
        _union = struct.union_mult(_first, _saved)
        struct.ctxTypes[ctx] = _union
        ctx.typename = _union
        self.idsTypes.openScope()
    
    def salirCase(self, ctx: CoolParser.CaseContext):
        #print("salirCase")
        #time.sleep(1)
        self.idsTypes.closeScope()
    
    def ingresarNew(self, ctx: CoolParser.NewContext):
        #print("ingresarNew")
        #time.sleep(1)
        self.idsTypes.openScope()
    
    def salirNew(self, ctx: CoolParser.NewContext):
        #print("salirNew")
        #time.sleep(1)
        _type = ctx.TYPE().getText()
        struct.ctxTypes[ctx] = _type
        ctx.typename = _type
        self.idsTypes.closeScope()
    
    def ingresarBlock(self, ctx: CoolParser.BlockContext):
        #print("ingresarBlock")
        #time.sleep(1)
        expr = ctx.expr()
        for _ex in expr:
            self.idsTypes.openScope()

    def salirBlock(self, ctx: CoolParser.BlockContext):
        #print("salirBlock")
        #time.sleep(1)
        expr = ctx.expr()
        _last = struct.ctxTypes[expr[len(expr) - 1]]
        struct.ctxTypes[ctx] = _last
        ctx.typename = _last
        for _ex in expr:
            self.idsTypes.closeScope()
    
    def ingresarCall(self, ctx: CoolParser.CallContext):
        #print("ingresarCall")
        #time.sleep(1)
        expr = ctx.expr()
        for _ex in expr:
            self.idsTypes.openScope()
        
    def salirCall(self, ctx: CoolParser.CallContext):
        #print("salirCall")
        #time.sleep(1)
        ID = ctx.ID().getText()
        expr = ctx.expr()

        className = None
        _starter = ctx.getChild(1).getText()
        _starterexpr = -1 
        if _starter == '.':
            _starterexpr = 1

            if type(expr[0]) is CoolParser.NewContext:
                className = expr[0].TYPE().getText()

            if type(expr[0]) is CoolParser.BaseContext:
                className = struct.ctxTypes[expr[0]]
            
            if type(expr[0]) is CoolParser.LetContext:
                _let = expr[0]
                _caller = _let.getChild(_let.getChildCount() - 1)
                className = struct.ctxTypes[_caller]

            if className == None:
                className = struct.ctxTypes[expr[0]]
            
        elif _starter == '(':
            _starterexpr = 0
            className = self.idsTypes.klass.name

        _klass = struct.lookupClass(className)
            
        _method = None
        try:
            _method = _klass.lookupMethod(ID)
        except KeyError:
            raise myexceptions.MethodNotFound
        
        _method = _klass.lookupMethod(ID)
        for i, _expected_type in enumerate(_method.params.values()):
            _inserted_type = struct.ctxTypes[expr[_starterexpr + i]]

            if _inserted_type == 'self' or _inserted_type == 'SELF_TYPE':
                _inserted_type = self.idsTypes.klass.name

            if (_inserted_type == _method.type 
                and type(expr[_starterexpr + i]) is CoolParser.CallContext
                and _expected_type != _inserted_type):
                raise myexceptions.CallTypeCheckMismatch

            if not struct.lookupClass(_expected_type).conforms(struct.lookupClass(_inserted_type)):
                raise myexceptions.DoesNotConform
        
        _calltype = _method.type
        if _method.type == 'SELF_TYPE':
            _calltype = _klass.name

        struct.ctxTypes[ctx] = _calltype
        ctx.typename = _calltype
        for _ex in expr:
            self.idsTypes.closeScope()
        
    def ingresarAt(self, ctx: CoolParser.AtContext):
        #print("ingresarAt")
        #time.sleep(1)
        expr = ctx.expr()
        for _ex in expr:
            self.idsTypes.openScope()

    def salirAt(self, ctx: CoolParser.AtContext):
        #print("salirAt")
        #time.sleep(1)
        ID = ctx.ID().getText()
        expr = ctx.expr()
        _type = ctx.TYPE().getText()

        izquierdaType = struct.ctxTypes[expr[0]]
        if izquierdaType == 'self':
            izquierdaType = self.idsTypes.klass.name

        izquierda = struct.lookupClass(izquierdaType)
        derecha = struct.lookupClass(_type)

        if not derecha.conforms(izquierda):
            raise myexceptions.MethodNotFound
        
        _methodType = derecha.lookupMethod(ID).type
        struct.ctxTypes[ctx] = _methodType
        ctx.typename = _methodType
        for _ex in expr:
            self.idsTypes.closeScope()
    
    def ingresarN(self, ctx: CoolParser.NegContext):
        #print("ingresarN")
        #time.sleep(1)
        self.idsTypes.openScope()

    def salirN(self, ctx: CoolParser.NegContext):
        #print("salirN")
        #time.sleep(1)
        expr = ctx.expr()
        if struct.ctxTypes[ctx.expr()] == 'Int':
            struct.ctxTypes[ctx] = 'Int'
        
        self.idsTypes.closeScope()
    
    def ingresarVoid(self, ctx: CoolParser.IsvoidContext):
        #print("ingresarVoid")
        #time.sleep(1)
        self.idsTypes.openScope()
    
    def salirVoid(self, ctx: CoolParser.IsvoidContext):
        #print("salirVoid")
        #time.sleep(1)
        struct.ctxTypes[ctx] = 'Bool'
        self.idsTypes.closeScope()
    
    def ingresarMult(self, ctx: CoolParser.MultContext):
        #print("ingresarMult")
        #time.sleep(1)
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def salirMult(self, ctx: CoolParser.MultContext):
        #print("salirMult")
        #time.sleep(1)
        izquierda = ctx.getChild(0)
        derecha = ctx.getChild(2)
        if (struct.ctxTypes[izquierda] != 'Int' or struct.ctxTypes[derecha] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            struct.ctxTypes[ctx] = 'Int'
            ctx.typename = 'Int'
        
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def ingresarDiv(self, ctx: CoolParser.DivContext):
        #print("ingresarDiv")
        #time.sleep(1)
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def salirDiv(self, ctx: CoolParser.DivContext):
        #print("salirDiv")
        #time.sleep(1)
        izquierda = ctx.getChild(0)
        derecha = ctx.getChild(2)
        if (struct.ctxTypes[izquierda] != 'Int' or struct.ctxTypes[derecha] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            struct.ctxTypes[ctx] = 'Int'
            ctx.typename = 'Int'

        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def ingresarSuma(self, ctx: CoolParser.AddContext):
        #print("ingresarSuma")
        #time.sleep(1)
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def salirSuma(self, ctx: CoolParser.AddContext):
        #print("salirSuma")
        #time.sleep(1)
        izquierda = ctx.getChild(0)
        derecha = ctx.getChild(2)
        if (struct.ctxTypes[izquierda] != 'Int' or struct.ctxTypes[derecha] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            struct.ctxTypes[ctx] = 'Int'
            ctx.typename = 'Int'
        
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def ingresarResta(self, ctx: CoolParser.SubContext):
        #print("ingresarResta")
        #time.sleep(1)
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def salirResta(self, ctx: CoolParser.SubContext):
        #print("salirResta")
        #time.sleep(1)
        izquierda = ctx.getChild(0)
        derecha = ctx.getChild(2)
        if (struct.ctxTypes[izquierda] != 'Int' or struct.ctxTypes[derecha] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            struct.ctxTypes[ctx] = 'Int'
            ctx.typename = 'Int'

        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def IngresarLt(self, ctx: CoolParser.LtContext):
        #print("IngresarLt")
        #time.sleep(1)
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def salirLt(self, ctx: CoolParser.LtContext):
        #print("salirLt")
        #time.sleep(1)
        izquierda = ctx.getChild(0)
        derecha = ctx.getChild(2)
        if (struct.ctxTypes[izquierda] != 'Int' or struct.ctxTypes[derecha] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            struct.ctxTypes[ctx] = 'Bool'
            ctx.typename = 'Int'
        
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def ingresarLe(self, ctx: CoolParser.LeContext):
        #print("ingresarLe")
        #time.sleep(1)
        self.idsTypes.openScope()
        self.idsTypes.openScope()
        
    def salirLe(self, ctx: CoolParser.LeContext):
        #print("salirLe")
        #time.sleep(1)
        izquierda = ctx.getChild(0)
        derecha = ctx.getChild(2)
        if (struct.ctxTypes[izquierda] != 'Int' or struct.ctxTypes[derecha] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            struct.ctxTypes[ctx] = 'Bool'
            ctx.typename = 'Int'
        
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def ingresarEq(self, ctx: CoolParser.EqContext):
        #print("ingresarEq")
        #time.sleep(1)
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def salirEq(self, ctx: CoolParser.EqContext):
        #print("salirEq")
        #time.sleep(1)
        expr = ctx.expr()
        izquierda = struct.ctxTypes[expr[0]]
        derecha = struct.ctxTypes[expr[1]]
        ignorar = ['Int', 'String', 'Bool']
        if izquierda in ignorar or derecha in ignorar:
            if izquierda != derecha:
                raise myexceptions.TypeCheckMismatch

        struct.ctxTypes[ctx] = 'Bool'
        ctx.typename = 'Int'

        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def ingresarNot(self, ctx: CoolParser.NotContext):
        #print("ingresarNot")
        #time.sleep(1)
        self.idsTypes.openScope()

    def salirNot(self, ctx: CoolParser.NotContext):
        #print("salirNot")
        #time.sleep(1)
        if struct.ctxTypes[ctx.expr()] == 'Bool':
            struct.ctxTypes[ctx] = 'Bool'
            ctx.typename = 'Bool'
        
        self.idsTypes.closeScope()

    def ingresarAssign(self, ctx: CoolParser.AssignContext):
        #print("ingresarAssign")
        #time.sleep(1)
        if ctx.ID().getText() == 'self':
            raise myexceptions.SelfAssignmentException
        
        self.idsTypes.openScope()
    

    def salirAssign(self, ctx: CoolParser.AssignContext):
        #print("salirAssign")
        #time.sleep(1)
        IDType = self.idsTypes[ctx.ID().getText()]
        exprType = struct.ctxTypes[ctx.expr()]
        IDClass = struct.lookupClass(IDType)
        exprKlass = struct.lookupClass(exprType)
        
        if not IDClass.conforms(exprKlass):
            raise myexceptions.DoesNotConform

        struct.ctxTypes[ctx] = exprType
        ctx.typename = exprType
        self.idsTypes.closeScope()

    def salirParens(self, ctx: CoolParser.ParensContext):
        #print("salirParens")
        #time.sleep(1)
        _type = struct.ctxTypes[ctx.expr()]
        struct.ctxTypes[ctx] = _type
        ctx.typename = _type

    def salirObject(self, ctx: CoolParser.ObjectContext):
        #print("salirObject")
        #time.sleep(1)
        ID = ctx.ID().getText()

        try:
            _type = self.idsTypes[ID]
            struct.ctxTypes[ctx] = _type
            ctx.typename = _type
        except KeyError:
            raise myexceptions.UndeclaredIdentifier
    
    def salirInt(self, ctx: CoolParser.IntegerContext):
        #print("salirInt")
        #time.sleep(1)
        struct.ctxTypes[ctx] = 'Int'
        ctx.truevalue = ctx.INTEGER().getText()
        ctx.typename = 'Int'
    
    def salirString(self, ctx: CoolParser.StringContext):
        #print("salirString")
        #time.sleep(1)
        struct.ctxTypes[ctx] = 'String'
        ctx.typename = 'String'
    
    def salirBool(self, ctx: CoolParser.BoolContext):
        #print("salirBool")
        ##time.sleep(1)
        struct.ctxTypes[ctx] = 'Bool'
        ctx.typename = 'Bool'