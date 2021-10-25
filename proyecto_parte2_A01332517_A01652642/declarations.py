from antlr.CoolListener import CoolListener
from antlr.CoolParser import CoolParser
import myexceptions
import structure as storage

class Declarations(CoolListener):

    def __init__(self):
        self.idsTypes = None

    def enterClass(self, ctx: CoolParser.ProgramContext):
        _klassName = ctx.TYPE()[0].getText()
        _klass = storage.lookupClass(_klassName)

        
        self.idsTypes = storage.SymbolTableWithScopes(_klass)
        self.idsTypes.openScope()
        self.idsTypes['self'] = 'self'
    
    def exitClass(self, ctx: CoolParser.ProgramContext):
        self.idsTypes.closeScope()
    
    def enterMethod(self, ctx: CoolParser.MethodContext):
        _methodName = ctx.ID().getText()
        
        _inherits = self.idsTypes.klass.inherits
        if _inherits:
            _inheritedklass = storage.lookupClass(_inherits)

            try:
                _inheritedMethod = _inheritedklass.lookupMethod(_methodName)
                
                if _inheritedMethod.type != ctx.TYPE().getText():
                    raise myexceptions.InvalidMethodOverride


                _inheritedFormals = _inheritedMethod.params
                _formals = ctx.formal()
                if len(_inheritedFormals) != len(_formals):
                    raise myexceptions.InvalidMethodOverride

                # Every new formal should be the same
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
        _expr = ctx.expr() 
        _type = ctx.TYPE().getText()

        
        if _type == 'SELF_TYPE':
            _type = self.idsTypes.klass.name
            _exprType = storage.ctxTypes[_expr]
            if _exprType != 'self' and _exprType != 'SELF_TYPE':
                raise myexceptions.TypeCheckMismatch
        else:
            try:
                _exprType = storage.ctxTypes[_expr]
                if _exprType == 'self':
                    _exprType = self.idsTypes.klass.name

                _exprKlass = storage.lookupClass(_exprType)
                _typeKlass = storage.lookupClass(_type)
            except KeyError:
                raise myexceptions.TypeNotFound

            if not _typeKlass.conforms(_exprKlass):
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
            _inherited = storage.lookupClass(_klass.inherits)
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
        _type = storage.ctxTypes[ctx.getChild(0)]
        storage.ctxTypes[ctx] = _type

    def enterIf(self, ctx: CoolParser.IfContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()
        self.idsTypes.openScope()
    
    def exitIf(self, ctx: CoolParser.IfContext):
        _trueType = storage.ctxTypes[ctx.expr()[1]]
        _falseType = storage.ctxTypes[ctx.expr()[2]]

        _trueKlass = storage.lookupClass(_trueType)
        _falseKlass = storage.lookupClass(_falseType)
        _union = _trueKlass.union(_falseKlass)

        storage.ctxTypes[ctx] = _union
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()
    
    def enterWhile(self, ctx: CoolParser.WhileContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()
    
    def exitWhile(self, ctx: CoolParser.WhileContext):
        if storage.ctxTypes[ctx.expr()[0]] != 'Bool':
            raise myexceptions.TypeCheckMismatch
        
        storage.ctxTypes[ctx] = 'Object'
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()
    
    def enterLet(self, ctx: CoolParser.LetContext):
        _ids = ctx.ID()
        _types = ctx.TYPE()
        for i in range(len(_ids)-1, -1, -1):
            if _ids[i].getText() == 'self':
                raise myexceptions.SelfVariableException

            self.idsTypes.openScope()
            self.idsTypes[_ids[i].getText()] = _types[i].getText()
    
    def exitLet(self, ctx: CoolParser.LetContext):
        _types = ctx.TYPE()
        _expr = ctx.expr()

        for i, _type in enumerate(_types):
            if i < (len(_expr) - 1):
                _assign = storage.lookupClass(storage.ctxTypes[_expr[i]])
                _to = storage.lookupClass(_type.getText())
                if not _to.conforms(_assign):
                    raise myexceptions.DoesNotConform

        _last = _expr[len(_expr) - 1]
        _lastType = storage.ctxTypes[_last]
        storage.ctxTypes[ctx] = _lastType
        for _i in ctx.ID():
            self.idsTypes.closeScope()

    def enterCase(self, ctx: CoolParser.CaseContext):
        _ids = ctx.ID()
        _types = ctx.TYPE()

        _saved = set()
        for i, _id in reversed(list(enumerate(_ids))):
            _type = _types[i].getText()

            if _type in _saved:
                raise myexceptions.InvalidCase

            _saved.add(_type)
            self.idsTypes.openScope()
            self.idsTypes[_id.getText()] = _types[i].getText()
        
        _firstName = _types[0].getText()
        _saved.discard(_firstName)
        _first  = storage.lookupClass(_firstName)
        _union = storage.union_mult(_first, _saved)
        storage.ctxTypes[ctx] = _union
        self.idsTypes.openScope()
    
    def exitCase(self, ctx: CoolParser.CaseContext):
        self.idsTypes.closeScope()
    
    def enterNew(self, ctx: CoolParser.NewContext):
        self.idsTypes.openScope()
    
    def exitNew(self, ctx: CoolParser.NewContext):
        _type = ctx.TYPE().getText()
        storage.ctxTypes[ctx] = _type
        self.idsTypes.closeScope()
    
    def enterBlock(self, ctx: CoolParser.BlockContext):
        _expr = ctx.expr()
        for _ex in _expr:
            self.idsTypes.openScope()

    def exitBlock(self, ctx: CoolParser.BlockContext):
        _expr = ctx.expr()
        _last = storage.ctxTypes[_expr[len(_expr) - 1]]
        storage.ctxTypes[ctx] = _last
        for _ex in _expr:
            self.idsTypes.closeScope()
    
    def enterCall(self, ctx: CoolParser.CallContext):
        _expr = ctx.expr()
        for _ex in _expr:
            self.idsTypes.openScope()
        
    def exitCall(self, ctx: CoolParser.CallContext):
        _id = ctx.ID().getText()
        _expr = ctx.expr()

        _klassName = None
        _starter = ctx.getChild(1).getText()
        _starter_expr = -1 
        if _starter == '.':
            _starter_expr = 1

            if type(_expr[0]) is CoolParser.NewContext:
                _klassName = _expr[0].TYPE().getText()

            if type(_expr[0]) is CoolParser.BaseContext:
                _klassName = storage.ctxTypes[_expr[0]]
            
            if type(_expr[0]) is CoolParser.LetContext:
                _let = _expr[0]
                _caller = _let.getChild(_let.getChildCount() - 1) 
                _klassName = storage.ctxTypes[_caller]

            if _klassName == None:
                _klassName = storage.ctxTypes[_expr[0]]
            
        elif _starter == '(':
            _starter_expr = 0
            _klassName = self.idsTypes.klass.name

        _klass = storage.lookupClass(_klassName)
            
        _method = None
        try:
            _method = _klass.lookupMethod(_id)
        except KeyError:
            raise myexceptions.MethodNotFound
        
        _method = _klass.lookupMethod(_id)
        for i, _expected_type in enumerate(_method.params.values()):
            _inserted_type = storage.ctxTypes[_expr[_starter_expr + i]]

            if _inserted_type == 'self' or _inserted_type == 'SELF_TYPE':
                _inserted_type = self.idsTypes.klass.name

            
            if (_inserted_type == _method.type 
                and type(_expr[_starter_expr + i]) is CoolParser.CallContext
                and _expected_type != _inserted_type):
                raise myexceptions.CallTypeCheckMismatch

            if not storage.lookupClass(_expected_type).conforms(storage.lookupClass(_inserted_type)):
                raise myexceptions.DoesNotConform
        
        _calltype = _method.type
        if _method.type == 'SELF_TYPE':
            _calltype = _klass.name

        storage.ctxTypes[ctx] = _calltype
        for _ex in _expr:
            self.idsTypes.closeScope()
        
    def enterAt(self, ctx: CoolParser.AtContext):
        _expr = ctx.expr()
        for _ex in _expr:
            self.idsTypes.openScope()

    def exitAt(self, ctx: CoolParser.AtContext):
        _id = ctx.ID().getText()
        _expr = ctx.expr()
        _type = ctx.TYPE().getText()

        _leftType = storage.ctxTypes[_expr[0]]
        if _leftType == 'self':
            _leftType = self.idsTypes.klass.name

        _left = storage.lookupClass(_leftType)
        _right = storage.lookupClass(_type)

        if not _right.conforms(_left):
            raise myexceptions.MethodNotFound
        
        _methodType = _right.lookupMethod(_id).type
        storage.ctxTypes[ctx] = _methodType
        for _ex in _expr:
            self.idsTypes.closeScope()
    
    def enterNeg(self, ctx: CoolParser.NegContext):
        self.idsTypes.openScope()

    def exitNeg(self, ctx: CoolParser.NegContext):
        _expr = ctx.expr()
        if storage.ctxTypes[ctx.expr()] == 'Int':
            storage.ctxTypes[ctx] = 'Int'
        
        self.idsTypes.closeScope()
    
    def enterIsvoid(self, ctx: CoolParser.IsvoidContext):
        self.idsTypes.openScope()
    
    def exitIsvoid(self, ctx: CoolParser.IsvoidContext):
        storage.ctxTypes[ctx] = 'Bool'
        self.idsTypes.closeScope()
    
    def enterMult(self, ctx: CoolParser.MultContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def exitMult(self, ctx: CoolParser.MultContext):
        _left = ctx.getChild(0)
        _right = ctx.getChild(2)
        if (storage.ctxTypes[_left] != 'Int' or storage.ctxTypes[_right] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            storage.ctxTypes[ctx] = 'Int'
        
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterDiv(self, ctx: CoolParser.DivContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def exitDiv(self, ctx: CoolParser.DivContext):
        _left = ctx.getChild(0)
        _right = ctx.getChild(2)
        if (storage.ctxTypes[_left] != 'Int' or storage.ctxTypes[_right] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            storage.ctxTypes[ctx] = 'Int'

        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterAdd(self, ctx: CoolParser.AddContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def exitAdd(self, ctx: CoolParser.AddContext):
        _left = ctx.getChild(0)
        _right = ctx.getChild(2)
        if (storage.ctxTypes[_left] != 'Int' or storage.ctxTypes[_right] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            storage.ctxTypes[ctx] = 'Int'
        
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterSub(self, ctx: CoolParser.SubContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def exitSub(self, ctx: CoolParser.SubContext):
        _left = ctx.getChild(0)
        _right = ctx.getChild(2)
        if (storage.ctxTypes[_left] != 'Int' or storage.ctxTypes[_right] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            storage.ctxTypes[ctx] = 'Int'

        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterLt(self, ctx: CoolParser.LtContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def exitLt(self, ctx: CoolParser.LtContext):
        _left = ctx.getChild(0)
        _right = ctx.getChild(2)
        if (storage.ctxTypes[_left] != 'Int' or storage.ctxTypes[_right] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            storage.ctxTypes[ctx] = 'Bool'
        
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterLe(self, ctx: CoolParser.LeContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()
        
    def exitLe(self, ctx: CoolParser.LeContext):
        _left = ctx.getChild(0)
        _right = ctx.getChild(2)
        if (storage.ctxTypes[_left] != 'Int' or storage.ctxTypes[_right] != 'Int'):
            raise myexceptions.TypeCheckMismatch
        else:  
            storage.ctxTypes[ctx] = 'Bool'
        
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterEq(self, ctx: CoolParser.EqContext):
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def exitEq(self, ctx: CoolParser.EqContext):
        _expr = ctx.expr()
        _left = storage.ctxTypes[_expr[0]]
        _right = storage.ctxTypes[_expr[1]]
        _except = ['Int', 'String', 'Bool']
        if _left in _except or _right in _except:
            if _left != _right:
                raise myexceptions.TypeCheckMismatch

        storage.ctxTypes[ctx] = 'Bool'

        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def enterNot(self, ctx: CoolParser.NotContext):
        self.idsTypes.openScope()

    def exitNot(self, ctx: CoolParser.NotContext):
        if storage.ctxTypes[ctx.expr()] == 'Bool':
            storage.ctxTypes[ctx] = 'Bool'
        
        self.idsTypes.closeScope()

    def enterAssign(self, ctx: CoolParser.AssignContext):
        if ctx.ID().getText() == 'self':
            raise myexceptions.SelfAssignmentException
        
        self.idsTypes.openScope()
    

    def exitAssign(self, ctx: CoolParser.AssignContext):
        _id = ctx.ID().getText()
        _expr = ctx.expr()
        _idType = self.idsTypes[ctx.ID().getText()]
        _exprType = storage.ctxTypes[ctx.expr()]
        _idKlass = storage.lookupClass(_idType)
        _exprKlass = storage.lookupClass(_exprType)
        
        if not _idKlass.conforms(_exprKlass):
            raise myexceptions.DoesNotConform

        storage.ctxTypes[ctx] = _exprType
        self.idsTypes.closeScope()

    def exitParens(self, ctx: CoolParser.ParensContext):
        _type = storage.ctxTypes[ctx.expr()]
        storage.ctxTypes[ctx] = _type

    def exitObject(self, ctx: CoolParser.ObjectContext):
        _id = ctx.ID().getText()

        try:
            _type = self.idsTypes[_id]
            storage.ctxTypes[ctx] = _type
        except KeyError:
            raise myexceptions.UndeclaredIdentifier
    
    def exitInteger(self, ctx: CoolParser.IntegerContext):
        storage.ctxTypes[ctx] = 'Int'
    
    def exitString(self, ctx: CoolParser.StringContext):
        storage.ctxTypes[ctx] = 'String'
    
    def exitBool(self, ctx: CoolParser.BoolContext):
        storage.ctxTypes[ctx] = 'Bool'