from antlr.CoolListener import CoolListener
from antlr.CoolParser import CoolParser
import myexceptions
import structure as struct

class Grarquia(CoolListener):

    def __init__(self):
        self.idsTypes = None

    def enterKlass(self, ctx: CoolParser.KlassContext):
        className = ctx.TYPE()[0].getText()
        ctx.nameklass = className
        _klass = struct.lookupClass(className)
        ctx.nameinherits = _klass.inherits

        self.idsTypes = struct.SymbolTableWithScopes(_klass)
        self.idsTypes.openScope()
        self.idsTypes['self'] = 'self'
    
    def exitKlass(self, ctx: CoolParser.KlassContext):
        self.idsTypes.closeScope()
    
    def enterMethod(self, ctx: CoolParser.MethodContext):
        _methodName = ctx.ID().getText()

        _inherits = self.idsTypes.klass.inherits
        if _inherits:
            _inheritedklass = struct.lookupClass(_inherits)
            try:
                _inheritedMethod = _inheritedklass.lookupMethod(_methodName)
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
    
    def exitMethod(self, ctx: CoolParser.MethodContext):
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
    
    def enterAtribute(self, ctx: CoolParser.AtributeContext):
        _id = ctx.ID().getText()
        _type = ctx.TYPE().getText()

        expr = ctx.expr()
        if expr:
            if hasattr(expr.getChild(0), 'ID'):
                expr_id = expr.getChild(0).ID().getText()
                try:
                    self.idsTypes[expr_id]
                except KeyError as e:
                    raise myexceptions.UndeclaredIdentifier
    
        try:
            _klass = self.idsTypes.klass
            _inherited = struct.lookupClass(_klass.inherits)
            _found = _inherited.lookupAttribute(_id)
            if _found != _type:
                raise myexceptions.NotSupported
        except KeyError:
            pass

        self.idsTypes[_id] = _type
        self.idsTypes.openScope()
    
    def exitAtribute(self, ctx: CoolParser.AtributeContext):
        self.idsTypes.closeScope()

    def enterFormal(self, ctx: CoolParser.FormalContext):
        _id = ctx.ID().getText()
        _type = ctx.TYPE().getText()
        if _id == 'self':
            raise myexceptions.SelfVariableException
        
        if _type == 'SELF_TYPE':
            raise myexceptions.SelftypeInvalidUseException
        
    
    def exitBase(self, ctx: CoolParser.BaseContext):
        _type = struct.ctxTypes[ctx.getChild(0)]
        struct.ctxTypes[ctx] = _type
        ctx.typename = _type

    def enterIf(self, ctx: CoolParser.IfContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()
    
    def exitIf(self, ctx: CoolParser.IfContext):
        _trueType = struct.ctxTypes[ctx.expr()[1]]
        _falseType = struct.ctxTypes[ctx.expr()[2]]

        _trueKlass = struct.lookupClass(_trueType)
        _falseKlass = struct.lookupClass(_falseType)
        _union = _trueKlass.union(_falseKlass)

        struct.ctxTypes[ctx] = _union
        ctx.typename = _union
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()
    
    def enterWhile(self, ctx: CoolParser.WhileContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()
    
    def exitWhile(self, ctx: CoolParser.WhileContext):
        if struct.ctxTypes[ctx.expr()[0]] != 'Bool':
            raise myexceptions.TypeCheckMismatch
        
        struct.ctxTypes[ctx] = 'Object'
        ctx.typename = 'Object'
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()
    
    def enterLet(self, ctx: CoolParser.LetContext):
        di = ctx.ID()
        types = ctx.TYPE()
        for i in range(len(di)-1, -1, -1):
            if di[i].getText() == 'self':
                raise myexceptions.SelfVariableException

            self.idsTypes.openScope()
            self.idsTypes[di[i].getText()] = types[i].getText()
    
    def exitLet(self, ctx: CoolParser.LetContext):
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

    def enterCase(self, ctx: CoolParser.CaseContext):
        di = ctx.ID()
        types = ctx.TYPE()

        _saved = set()
        for i, _id in reversed(list(enumerate(di))):
            _type = types[i].getText()

            if _type in _saved:
                raise myexceptions.InvalidCase

            _saved.add(_type)
            self.idsTypes.openScope()
            self.idsTypes[_id.getText()] = types[i].getText()
        
        _firstName = types[0].getText()
        _saved.discard(_firstName)
        _first  = struct.lookupClass(_firstName)
        _union = struct.union_mult(_first, _saved)
        struct.ctxTypes[ctx] = _union
        ctx.typename = _union
        self.idsTypes.openScope()
    
    def exitCase(self, ctx: CoolParser.CaseContext):
        self.idsTypes.closeScope()
    
    def enterNew(self, ctx: CoolParser.NewContext):
        self.idsTypes.openScope()
    
    def exitNew(self, ctx: CoolParser.NewContext):
        _type = ctx.TYPE().getText()
        struct.ctxTypes[ctx] = _type
        ctx.typename = _type
        self.idsTypes.closeScope()
    
    def enterBlock(self, ctx: CoolParser.BlockContext):
        expr = ctx.expr()
        for _ex in expr:
            self.idsTypes.openScope()

    def exitBlock(self, ctx: CoolParser.BlockContext):
        expr = ctx.expr()
        _last = struct.ctxTypes[expr[len(expr) - 1]]
        struct.ctxTypes[ctx] = _last
        ctx.typename = _last
        for _ex in expr:
            self.idsTypes.closeScope()
    
    def enterCall(self, ctx: CoolParser.CallContext):
        expr = ctx.expr()
        for _ex in expr:
            self.idsTypes.openScope()
        
    def exitCall(self, ctx: CoolParser.CallContext):
        _id = ctx.ID().getText()
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
            _method = _klass.lookupMethod(_id)
        except KeyError:
            raise myexceptions.MethodNotFound
        
        _method = _klass.lookupMethod(_id)
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
        
    def enterAt(self, ctx: CoolParser.AtContext):
        expr = ctx.expr()
        for _ex in expr:
            self.idsTypes.openScope()

    def exitAt(self, ctx: CoolParser.AtContext):
        _id = ctx.ID().getText()
        expr = ctx.expr()
        _type = ctx.TYPE().getText()

        _leftType = struct.ctxTypes[expr[0]]
        if _leftType == 'self':
            _leftType = self.idsTypes.klass.name

        _left = struct.lookupClass(_leftType)
        _right = struct.lookupClass(_type)

        if not _right.conforms(_left):
            raise myexceptions.MethodNotFound
        
        _methodType = _right.lookupMethod(_id).type
        struct.ctxTypes[ctx] = _methodType
        ctx.typename = _methodType
        for _ex in expr:
            self.idsTypes.closeScope()
    
    def entrarN(self, ctx: CoolParser.NegContext):
        self.idsTypes.openScope()

    def salirN(self, ctx: CoolParser.NegContext):
        expr = ctx.expr()
        if struct.ctxTypes[ctx.expr()] == 'Int':
            struct.ctxTypes[ctx] = 'Int'
        
        self.idsTypes.closeScope()
    
    def enterIsvoid(self, ctx: CoolParser.IsvoidContext):
        self.idsTypes.openScope()
    
    def exitIsvoid(self, ctx: CoolParser.IsvoidContext):
        struct.ctxTypes[ctx] = 'Bool'
        self.idsTypes.closeScope()
    
    def enterMult(self, ctx: CoolParser.MultContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def exitMult(self, ctx: CoolParser.MultContext):
        _left = ctx.getChild(0)
        _right = ctx.getChild(2)
        if (struct.ctxTypes[_left] != 'Int' or struct.ctxTypes[_right] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            struct.ctxTypes[ctx] = 'Int'
            ctx.typename = 'Int'
        
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterDiv(self, ctx: CoolParser.DivContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def exitDiv(self, ctx: CoolParser.DivContext):
        _left = ctx.getChild(0)
        _right = ctx.getChild(2)
        if (struct.ctxTypes[_left] != 'Int' or struct.ctxTypes[_right] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            struct.ctxTypes[ctx] = 'Int'
            ctx.typename = 'Int'

        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterAdd(self, ctx: CoolParser.AddContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def exitAdd(self, ctx: CoolParser.AddContext):
        _left = ctx.getChild(0)
        _right = ctx.getChild(2)
        if (struct.ctxTypes[_left] != 'Int' or struct.ctxTypes[_right] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            struct.ctxTypes[ctx] = 'Int'
            ctx.typename = 'Int'
        
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterSub(self, ctx: CoolParser.SubContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def exitSub(self, ctx: CoolParser.SubContext):
        _left = ctx.getChild(0)
        _right = ctx.getChild(2)
        if (struct.ctxTypes[_left] != 'Int' or struct.ctxTypes[_right] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            struct.ctxTypes[ctx] = 'Int'
            ctx.typename = 'Int'

        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterLt(self, ctx: CoolParser.LtContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def exitLt(self, ctx: CoolParser.LtContext):
        _left = ctx.getChild(0)
        _right = ctx.getChild(2)
        if (struct.ctxTypes[_left] != 'Int' or struct.ctxTypes[_right] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            struct.ctxTypes[ctx] = 'Bool'
            ctx.typename = 'Int'
        
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterLe(self, ctx: CoolParser.LeContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()
        
    def exitLe(self, ctx: CoolParser.LeContext):
        _left = ctx.getChild(0)
        _right = ctx.getChild(2)
        if (struct.ctxTypes[_left] != 'Int' or struct.ctxTypes[_right] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            struct.ctxTypes[ctx] = 'Bool'
            ctx.typename = 'Int'
        
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterEq(self, ctx: CoolParser.EqContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def exitEq(self, ctx: CoolParser.EqContext):
        expr = ctx.expr()
        _left = struct.ctxTypes[expr[0]]
        _right = struct.ctxTypes[expr[1]]
        _except = ['Int', 'String', 'Bool']
        if _left in _except or _right in _except:
            if _left != _right:
                raise myexceptions.TypeCheckMismatch

        struct.ctxTypes[ctx] = 'Bool'
        ctx.typename = 'Int'

        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterNot(self, ctx: CoolParser.NotContext):
        self.idsTypes.openScope()

    def exitNot(self, ctx: CoolParser.NotContext):
        if struct.ctxTypes[ctx.expr()] == 'Bool':
            struct.ctxTypes[ctx] = 'Bool'
            ctx.typename = 'Bool'
        
        self.idsTypes.closeScope()

    def enterAssign(self, ctx: CoolParser.AssignContext):
        if ctx.ID().getText() == 'self':
            raise myexceptions.SelfAssignmentException
        
        self.idsTypes.openScope()
    

    def exitAssign(self, ctx: CoolParser.AssignContext):
        _id = ctx.ID().getText()
        expr = ctx.expr()
        _idType = self.idsTypes[ctx.ID().getText()]
        exprType = struct.ctxTypes[ctx.expr()]
        _idKlass = struct.lookupClass(_idType)
        exprKlass = struct.lookupClass(exprType)
        
        if not _idKlass.conforms(exprKlass):
            raise myexceptions.DoesNotConform

        struct.ctxTypes[ctx] = exprType
        ctx.typename = exprType
        self.idsTypes.closeScope()

    def exitParens(self, ctx: CoolParser.ParensContext):
        _type = struct.ctxTypes[ctx.expr()]
        struct.ctxTypes[ctx] = _type
        ctx.typename = _type

    def exitObject(self, ctx: CoolParser.ObjectContext):
        _id = ctx.ID().getText()

        try:
            _type = self.idsTypes[_id]
            struct.ctxTypes[ctx] = _type
            ctx.typename = _type
        except KeyError:
            raise myexceptions.UndeclaredIdentifier
    
    def exitInteger(self, ctx: CoolParser.IntegerContext):
        struct.ctxTypes[ctx] = 'Int'
        ctx.truevalue = ctx.INTEGER().getText()
        ctx.typename = 'Int'
    
    def exitString(self, ctx: CoolParser.StringContext):
        struct.ctxTypes[ctx] = 'String'
        ctx.typename = 'String'
    
    def exitBool(self, ctx: CoolParser.BoolContext):
        struct.ctxTypes[ctx] = 'Bool'
        ctx.typename = 'Bool'