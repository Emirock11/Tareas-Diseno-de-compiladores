from antlr.CoolListener import CoolListener
from antlr.CoolParser import CoolParser
import myexceptions
import structure as struct
import time

class Grarquia(CoolListener):

    def __init__(self):
        # Se inicializa los tipos de id como una variable vacia
        self.idsTypes = None

    def ingresarClass(self, ctx: CoolParser.KlassContext):
        #print("ingresarClase()")
        ##time.sleep(1)
        # Se guarda el nombre de la clase al momento de ingresar a la clase
        className = ctx.TYPE()[0].getText()
        # En la variable ctx se guarda el nombre de la variable (Para el arbol)
        ctx.nameklass = className
        # Se guarda la estructura de la clase dentro de la variable klass
        klass = struct.lookupClass(className)
        # Se guarda el nombre de la herencia en context
        ctx.nameinherits = klass.inherits
        # Se guarda la tabla de simbolos que se utilizan en la clase dentro de la
        # variable global llamada idsTypes
        self.idsTypes = struct.SymbolTableWithScopes(klass)
        # Se realiza un openscope a la tabla de los simbolos para recorrer la clase
        self.idsTypes.openScope()
        # el idTypes de tipo self se guarda el string de self
        self.idsTypes['self'] = 'self'
    
    def salirClass(self, ctx: CoolParser.KlassContext):
        #print("salirClase()")
        #time.sleep(1)
        # Se realiza un close scope a la clase, significando que se ha terminado de analizar
        self.idsTypes.closeScope()

    def ingresarAtribute(self, ctx: CoolParser.AtributeContext):
        #print("IngresarAtributo")
        #time.sleep(1)
        # Se obtiene el tipo del atributo dentro de la variable id
        ID = ctx.ID().getText()
        # Se guarda el string del tipo del contexto
        _type = ctx.TYPE().getText()
        # Se guarda la expresion del contexto
        expr = ctx.expr()
        if expr:
            # Si hay alguna expresion se checa si el hijo tiene un id regresando un booleano 
            if hasattr(expr.getChild(0), 'ID'):
                # Se guarda el id del hijo
                exprID = expr.getChild(0).ID().getText()
                try:
                    # Se busca si el identificador esta dentro de la lista de los tipos del archivo
                    self.idsTypes[exprID]
                except KeyError as e:
                    # Si no esta el identificador, se muestra una excepcion de identificacor sin declarar
                    raise myexceptions.UndeclaredIdentifier
    
        try:
            # Se obtiene toda la lista de los tipos de id se la clase
            klass = self.idsTypes.klass
            # Se guarda la herencia de la clase en la variable inherited
            inherited = struct.lookupClass(klass.inherits)
            # Se busca el atributo ID dentro de la lista de la herencia
            found = inherited.lookupAttribute(ID)
            # Si no se encuentra el ID se muestra una excepcion de que no es valido
            if found != _type:
                raise myexceptions.NotSupported
        except KeyError:
            pass
        # Se guarda el tipo del atributo segun el id de la lista de los tipos de id
        self.idsTypes[ID] = _type
        # Se realiza un openscope para adentrarse dentro de los tipos de id de la clase
        self.idsTypes.openScope()
    
    def salirAtribute(self, ctx: CoolParser.AtributeContext):
        #print("salirAtribute")
        #time.sleep(1)
        # Se realiza un close scope al atributo, significando que se ha terminado de analizar
        self.idsTypes.closeScope()

    def ingresarMethod(self, ctx: CoolParser.MethodContext):
        #print("ingresarMethod")
        #time.sleep(1)
        # Se obtiene el tipo del metodo dentro de la variable id
        metodo = ctx.ID().getText()
        # Se guardan todas las herencias de la clase en inherits
        inherits = self.idsTypes.klass.inherits
        # Si hay alguna herencia
        if inherits:
            # Se realiza un lookup a la herencia de la clase
            inheritedklass = struct.lookupClass(inherits)
            try:
                # Se obtiene los metodos heredados de la clase
                inheritedMethod = inheritedklass.lookupMethod(metodo)
                # Si el tipo del metodo heredado es distinto al nombre del tipo de context
                if inheritedMethod.type != ctx.TYPE().getText():
                    # Se muestra un exception de que el metodo no se puede sobreescribir
                    raise myexceptions.InvalidMethodOverride
                # Formals heredados de llos parametros del metodo heredado
                inheritedFormals = inheritedMethod.params
                # Se guardan los formals del metodo acual en la variabla formals
                formals = ctx.formal()
                # Se compara la cantidad de formals heredados con la del metodo actual
                if len(inheritedFormals) != len(formals):
                    # Si es distinta la cantidad, el metodo no puede sobreescribirse
                    raise myexceptions.InvalidMethodOverride
                for i, v in enumerate(inheritedFormals.values()):
                    # Se obtiene el tipo de los formals y se establece como un nuevo tipo
                    _new_type = formals[i].TYPE().getText()
                    # Si el nuevo tipo es distinto a el valor de los formals heredados
                    if _new_type != v:
                        # Se realiza la exception de que el metodo no se puede sobreescribir
                        raise myexceptions.InvalidMethodOverride
            except KeyError:
                pass
        # Se realiza un openscope para adentrarse dentro de los tipos de id del metodo
        self.idsTypes.openScope()
        # Se guardan los formals de la variable context en formals
        formals = ctx.formal()
        for formal in formals:
            # Para cada formal en formals, se establece dentro de la 
            # lista de los tipos de toda la clase el tipo de formal segun su ID
            self.idsTypes[formal.ID().getText()] = formal.TYPE().getText()
    
    def salirMethod(self, ctx: CoolParser.MethodContext):
        #print("salirMethod")
        #time.sleep(1)
        # Se obtiene la expresion del metodo y se guarda en la variable de expr 
        expr = ctx.expr()
        # Se obtiene el tipo del metodo
        _type = ctx.TYPE().getText()
        # Si es de tipo self_type
        if _type == 'SELF_TYPE':
            # El tipo de la clase se guarda en type
            _type = self.idsTypes.klass.name
            # Se obtiene el tipo de expresion
            exprType = struct.ctxTypes[expr]
            # Si el tipo es distinto al tipo self y SELF_TYPE
            if exprType != 'self' and exprType != 'SELF_TYPE':
                # Se muestra el exception de que el tipo es diferente
                raise myexceptions.TypeCheckMismatch
        else:
            # Si no es de tipo self type
            try:
                # Se obtiene el tipo de expresion
                exprType = struct.ctxTypes[expr]
                # Si es de tipo self
                if exprType == 'self':
                    # Se establece el tipo de la expresion con el nombre de la clase
                    exprType = self.idsTypes.klass.name
                # Se busca la expresion de la clase 
                exprKlass = struct.lookupClass(exprType)
                # Se busca el tipo de la clase
                _typeKlass = struct.lookupClass(_type)
            except KeyError:
                # si no se logra entontrar el tipo, se muestra la exception de que el tipo no se encontro
                raise myexceptions.TypeNotFound
            # Si el tipo de la clase no es parte de la expresion de la clase
            if not _typeKlass.conforms(exprKlass):
                # Se muestra que el tipo no es parte de la expresion
                raise myexceptions.DoesNotConform
        # Se realiza un close scope al metodo, significando que se ha terminado de analizar
        self.idsTypes.closeScope()

    def ingresarFormal(self, ctx: CoolParser.FormalContext):
        #print("ingresarFormal")
        #time.sleep(1)
        # Se obtiene el ID del formal dentro de la variable id
        ID = ctx.ID().getText()
        # Se obtiene el tipo del formal dentro de la variable type
        _type = ctx.TYPE().getText()
        # Si el ID es self
        if ID == 'self':
            # Se muestra la exception de que la variable es self
            raise myexceptions.SelfVariableException
        # Si el tipo es SELF_TYPE
        if _type == 'SELF_TYPE':
            # Se muestra la exception de que la variable es SELF_TYPE
            raise myexceptions.SelftypeInvalidUseException
        
    
    def salirBase(self, ctx: CoolParser.BaseContext):
        #print("salirBase")
        #time.sleep(1)
        # Se obtiene el tipo del contexto dentro de la variable type
        _type = struct.ctxTypes[ctx.getChild(0)]
        # Se establece el tipo de expresion de la base
        struct.ctxTypes[ctx] = _type
        # Se establece el nombre del tipo de expresion de la base
        ctx.typename = _type

    def ingresarIf(self, ctx: CoolParser.IfContext):
        #print("ingresarIf")
        #time.sleep(1)
        # Se infresa al iff con dos scopes
        self.idsTypes.openScope()
        self.idsTypes.openScope()
    
    def salirIf(self, ctx: CoolParser.IfContext):
        #print("salirIf")
        #time.sleep(1)
        # Se obtienen los tipos de expresion truetype y falsetype
        tT = struct.ctxTypes[ctx.expr()[1]]
        fT = struct.ctxTypes[ctx.expr()[2]]
        # Se obtienen los tipos de expresion trueklass y falseklass
        tK = struct.lookupClass(tT)
        fK = struct.lookupClass(fT)
        # Se tealiza una union entre ambos
        union = tK.union(fK)
        # Se guarda la union en la lista de los contextTypes
        struct.ctxTypes[ctx] = union
        # Se guarda el nombre del context como la union
        ctx.typename = union
        # Dos scope para salir
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()
    
    def ingresarWhile(self, ctx: CoolParser.WhileContext):
        #print("ingresarWhile")
        #time.sleep(1)
        # Dos scope para ingresar
        self.idsTypes.openScope()
        self.idsTypes.openScope()
    
    def salirWhile(self, ctx: CoolParser.WhileContext):
        #print("salirWhile")
        #time.sleep(1)
        # Si los tipos de estructura son distintos a booleano
        if struct.ctxTypes[ctx.expr()[0]] != 'Bool':
            # Se regresa un exception de tipo missmatch
            raise myexceptions.TypeCheckMismatch
        # Se establece el tipo del contexto como Object
        struct.ctxTypes[ctx] = 'Object'
        # Se guarda el nombre del context como Object
        ctx.typename = 'Object'
        # Dos scope para salir
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()
    
    def ingresarLet(self, ctx: CoolParser.LetContext):
        #print("ingresarLet")
        #time.sleep(1)
        # Se obtiene el ID del contexto
        di = ctx.ID()
        # Se obtiene los tipos del contexto
        types = ctx.TYPE()
        # Se realiza un for para adentrarnos dentro del id
        for i in range(len(di)-1, -1, -1):
            # Si alguno de los textos del ID del contexto es de tipo self
            if di[i].getText() == 'self':
                # Se muestra la exception de la declaracionde variable
                raise myexceptions.SelfVariableException
            # Se realiza un openscope del tipo
            self.idsTypes.openScope()
            # Se establece el tipo del ID en el que se esta en el momento
            self.idsTypes[di[i].getText()] = types[i].getText()
    
    def salirLet(self, ctx: CoolParser.LetContext):
        #print("salirLet")
        #time.sleep(1)
        # Se obtiene los tipos del contexto
        types = ctx.TYPE()
        # Se obtiene la expresion del contexto
        expr = ctx.expr()

        for i, _type in enumerate(types):
            # si i es menot a la longitud de la expresion
            if i < (len(expr) - 1):
                # Se guarda la asignacion que se busca dentro de la estructura de la clase seun la expresion
                assign = struct.lookupClass(struct.ctxTypes[expr[i]])
                # Se guarda el tipo a asignar
                _to = struct.lookupClass(_type.getText())
                # Si el tipo no es parte de la asignacion
                if not _to.conforms(assign):
                    # Se muestra la exception que no es conforme
                    raise myexceptions.DoesNotConform
        # Se obtiene la ultima expresion
        _last = expr[len(expr) - 1]
        # Se obtiene el tipo de la ultima expresion
        _lastType = struct.ctxTypes[_last]
        # Se agrega el tipo de la ultima expresion del contexto
        struct.ctxTypes[ctx] = _lastType
        # Se cambia el nombre del tipo del ultimo tipo
        ctx.typename = _lastType
        for _i in ctx.ID():
            # Se realiza un close scope por cada id
            self.idsTypes.closeScope()

    def ingresarCase(self, ctx: CoolParser.CaseContext):
        #print("ingresarCase")
        #time.sleep(1)
        # Se obtiene el id del contexto
        di = ctx.ID()
        # Se obtiene los tipos del contexto
        types = ctx.TYPE()
        # Se crea la variable de guardado
        guardado = set()

        for i, ID in reversed(list(enumerate(di))):
            # Se obtiene el tipo de toda la lista de tipos
            _type = types[i].getText()
            # Si el tipo esta guardado ya
            if _type in guardado:
                # Se muestra el exception de que el case es invalido
                raise myexceptions.InvalidCase
            # se agrega el tipo
            guardado.add(_type)
            # Se raliza un openscope
            self.idsTypes.openScope()
            # Se establece el tipo de cada ID 
            self.idsTypes[ID.getText()] = types[i].getText()
        # Se obtiene el primer dato del tipo
        firstName = types[0].getText()
        # Se quita el primer nombre
        guardado.discard(firstName)
        # Se busca dentro de la estructura de la clase el firstname
        first  = struct.lookupClass(firstName)
        # se realiza una union entre el primero y lo guardado
        union = struct.union_mult(first, guardado)
        # El tipo del contexto es la union
        struct.ctxTypes[ctx] = union
        # Se establece el nombre del cointext con la union
        ctx.typename = union
        # Entrar con un openScope
        self.idsTypes.openScope()
    
    def salirCase(self, ctx: CoolParser.CaseContext):
        #print("salirCase")
        #time.sleep(1)
        # Salir con un closescope
        self.idsTypes.closeScope()
    
    def ingresarNew(self, ctx: CoolParser.NewContext):
        #print("ingresarNew")
        #time.sleep(1)
        # Entrar con un openScope
        self.idsTypes.openScope()
    
    def salirNew(self, ctx: CoolParser.NewContext):
        #print("salirNew")
        #time.sleep(1)
        # Se obtiene el tipo del New
        _type = ctx.TYPE().getText()
        # Se establece el tipo del New
        struct.ctxTypes[ctx] = _type
        # Se establece el nombre del tipo del New
        ctx.typename = _type
        # Salir con un closescope
        self.idsTypes.closeScope()
    
    def ingresarBlock(self, ctx: CoolParser.BlockContext):
        #print("ingresarBlock")
        #time.sleep(1)
        # Se obtienen todas las expresiones del context
        expr = ctx.expr()
        for _ex in expr:
            # Entrar a las expresiones con un openScope
            self.idsTypes.openScope()

    def salirBlock(self, ctx: CoolParser.BlockContext):
        #print("salirBlock")
        #time.sleep(1)
        # Se obtienen todas las expresiones del context
        expr = ctx.expr()
        _last = struct.ctxTypes[expr[len(expr) - 1]]
        struct.ctxTypes[ctx] = _last
        ctx.typename = _last
        for _ex in expr:
            # Salir de las expresiones con un closeScope
            self.idsTypes.closeScope()
    
    def ingresarCall(self, ctx: CoolParser.CallContext):
        #print("ingresarCall")
        #time.sleep(1)
        # Se obtienen todas las expresiones del context
        expr = ctx.expr()
        for _ex in expr:
            # Entrar a las expresiones con un openScope
            self.idsTypes.openScope()
        
    def salirCall(self, ctx: CoolParser.CallContext):
        #print("salirCall")
        #time.sleep(1)
        ID = ctx.ID().getText()
        expr = ctx.expr()
        # Se establece el nombre de la clase como none
        className = None
        # Se obtiene el segundo hijo de context
        starter = ctx.getChild(1).getText()
        # La espresion inicial se establece como -1
        starterexpr = -1 
        # Si el hijo 1 es un punto
        if starter == '.':
            # se establece la expresion inicial como 1
            starterexpr = 1
            # Si el tipo de la expresion es de un contexto new
            if type(expr[0]) is CoolParser.NewContext:
                # El nombre de la clase es el tipo de la expresion 0
                className = expr[0].TYPE().getText()
            # Si el tipo de la expresion es de un contexto base
            if type(expr[0]) is CoolParser.BaseContext:
                # El nombre de la clase es el tipo de la expresion 0 que esta dentro de la estructura de la clase
                className = struct.ctxTypes[expr[0]]
            # Si el tipo de la expresion es de un contexto let
            if type(expr[0]) is CoolParser.LetContext:
                let = expr[0]
                _caller = let.getChild(let.getChildCount() - 1)
                className = struct.ctxTypes[_caller]
            # Si el tipo de la expresion es de un contexto none
            if className == None:
                # El nombre de la clase es el tipo de la expresion 0 que esta dentro de la estructura de la clase
                className = struct.ctxTypes[expr[0]]
        # Si el hijo 1 es un parentesis
        elif starter == '(':
            # Al espresion inicial es 0
            starterexpr = 0
            # El nombre de la clase es el del tipo de la Klass
            className = self.idsTypes.klass.name
        # Se obtiene la estructura de la clase
        klass = struct.lookupClass(className)
        # Se establece el metodo como ninguno
        method = None
        try:
            # Se busda dentro de la estructura de la clase el id del context
            method = klass.lookupMethod(ID)
        except KeyError:
            # Si no se encuentra, se muestra el exeption de que el metodo no se encontro
            raise myexceptions.MethodNotFound
        
        # Se busda dentro de la estructura de la clase el id del context
        method = klass.lookupMethod(ID)
        # Se enumeran todos los valores de los parametros
        for i, expectType in enumerate(method.params.values()):
            # Se obtiene el tipo a ingresar segun la expresion inicial mas el index del for
            insertType = struct.ctxTypes[expr[starterexpr + i]]
            # Si el tipo a insertar es self, o SELF_TYPE
            if insertType == 'self' or insertType == 'SELF_TYPE':
                # El tipo a insertar se establece como el nombre de la clase
                insertType = self.idsTypes.klass.name
            # Si es del tipo method y el tipo de expresion es un call y el tipo expectado es el diferente al que se quiere insertar
            if (insertType == method.type and type(expr[starterexpr + i]) is CoolParser.CallContext and expectType != insertType):
                # Se muestra el exception de mismatch
                raise myexceptions.CallTypeCheckMismatch
            # Si el tipo esperado no es parte de la estructura de la clase
            if not struct.lookupClass(expectType).conforms(struct.lookupClass(insertType)):
                # Se muestra la exception de que no es parte de la clase
                raise myexceptions.DoesNotConform
        # El tipo de llamado se setea como el tipo del metodo
        calltype = method.type
        # Si el metodo es de tipo SELF_TYPE
        if method.type == 'SELF_TYPE':
            # El tipo de llamado es el nombre de la clase
            calltype = klass.name
        # el tipo del contexto se setea segun el tipo del llamado
        struct.ctxTypes[ctx] = calltype
        # Se setea el nombre del tipo con el tipo de call
        ctx.typename = calltype
        for _ex in expr:
            # Salir de las expresiones con un closeScope
            self.idsTypes.closeScope()
        
    def ingresarAt(self, ctx: CoolParser.AtContext):
        #print("ingresarAt")
        #time.sleep(1)
        # Se guarda la expresion del contexto
        expr = ctx.expr()
        for _ex in expr:
            # Entrar a las expresiones con un openScope
            self.idsTypes.openScope()

    def salirAt(self, ctx: CoolParser.AtContext):
        #print("salirAt")
        #time.sleep(1)
        # Se obtiene el ID del at dentro de la variable id
        ID = ctx.ID().getText()
        # Se guarda la expresion del contexto
        expr = ctx.expr()
        # Se guarda el string del tipo del contexto
        _type = ctx.TYPE().getText()
        # Se obiene el tipo de la izquierda
        izquierdaType = struct.ctxTypes[expr[0]]
        # Si es self
        if izquierdaType == 'self':
            # izquierdaType cambia a ser el nombre de la clase
            izquierdaType = self.idsTypes.klass.name
        # Se obtiene el tipo de la izquierda buscando dentro de la estructura de la clase
        izquierda = struct.lookupClass(izquierdaType)
        # Se obtiene el tipo del string en la clase
        derecha = struct.lookupClass(_type)
        # Si el dato de la izquierda no es parte de la derecha
        if not derecha.conforms(izquierda):
            # Se muestra la exception de que elmetodo no se encontro
            raise myexceptions.MethodNotFound
        # Se guarda el tipo del metodo
        methodType = derecha.lookupMethod(ID).type
        # Se establece el tipo del context con el tipo del metodo
        struct.ctxTypes[ctx] = methodType
        # Se establece el nombre del tipo con el tipo del metodo del contexto
        ctx.typename = methodType
        for _ex in expr:
            # Salir de las expresiones con un closeScope
            self.idsTypes.closeScope()
    
    def ingresarN(self, ctx: CoolParser.NegContext):
        #print("ingresarN")
        #time.sleep(1)
        # Entrar Neg con un openScope
        self.idsTypes.openScope()

    def salirN(self, ctx: CoolParser.NegContext):
        #print("salirN")
        #time.sleep(1)
        expr = ctx.expr()
        # Si el tipo de expresion es de tipo int
        if struct.ctxTypes[ctx.expr()] == 'Int':
            # Se establece el tipo del contexto como INT
            struct.ctxTypes[ctx] = 'Int'
        # Salir Neg con un closeScope
        self.idsTypes.closeScope()
    
    def ingresarVoid(self, ctx: CoolParser.IsvoidContext):
        #print("ingresarVoid")
        #time.sleep(1)
        # Entrar void con un openScope
        self.idsTypes.openScope()
    
    def salirVoid(self, ctx: CoolParser.IsvoidContext):
        #print("salirVoid")
        #time.sleep(1)
        # Se establece el tipo de contexto como booleano
        struct.ctxTypes[ctx] = 'Bool'
        # Salir void con un closescope
        self.idsTypes.closeScope()
    
    def ingresarMult(self, ctx: CoolParser.MultContext):
        #print("ingresarMult")
        #time.sleep(1)
        # Ingresar multiplicacion con dos openscope
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def salirMult(self, ctx: CoolParser.MultContext):
        #print("salirMult")
        #time.sleep(1)
        # Se obtiene el dato de la izquierda
        izquierda = ctx.getChild(0)
        # Se obtiene el dato de la derecha
        derecha = ctx.getChild(2)
        # Si la estructura de la izquierda es distinto a un int o lo mismo en la derecha
        if (struct.ctxTypes[izquierda] != 'Int' or struct.ctxTypes[derecha] != 'Int'):
            # Se regresa un excepption de tipos que no son match
            raise myexceptions.TypeCheckMismatch
        else:  
            # Se establece el tipo del contexto como INT
            struct.ctxTypes[ctx] = 'Int'
            # El nombre del tipo como INT
            ctx.typename = 'Int'
        # Salir multiplicacion con dos openscope
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def ingresarDiv(self, ctx: CoolParser.DivContext):
        #print("ingresarDiv")
        #time.sleep(1)
        # Ingresar division con dos openscope
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def salirDiv(self, ctx: CoolParser.DivContext):
        #print("salirDiv")
        #time.sleep(1)
        # Se obtiene el dato de la izquierda
        izquierda = ctx.getChild(0)
        # Se obtiene el dato de la derecha
        derecha = ctx.getChild(2)
        # Si la estructura de la izquierda es distinto a un int o lo mismo en la derecha
        if (struct.ctxTypes[izquierda] != 'Int' or struct.ctxTypes[derecha] != 'Int'):
            # Se regresa un excepption de tipos que no son match
            raise myexceptions.TypeCheckMismatch
        else:  
            # Se establece el tipo del contexto como INT
            struct.ctxTypes[ctx] = 'Int'
            # El nombre del tipo como INT
            ctx.typename = 'Int'
        # Salir division con dos openscope
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def ingresarSuma(self, ctx: CoolParser.AddContext):
        #print("ingresarSuma")
        #time.sleep(1)
        # Ingresar suma con dos openscope
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def salirSuma(self, ctx: CoolParser.AddContext):
        #print("salirSuma")
        #time.sleep(1)
        # Se obtiene el dato de la izquierda
        izquierda = ctx.getChild(0)
        # Se obtiene el dato de la derecha
        derecha = ctx.getChild(2)
        # Si la estructura de la izquierda es distinto a un int o lo mismo en la derecha
        if (struct.ctxTypes[izquierda] != 'Int' or struct.ctxTypes[derecha] != 'Int'):
            # Se regresa un excepption de tipos que no son match
            raise myexceptions.TypeCheckMismatch
        else:  
            # Se establece el tipo del contexto como INT
            struct.ctxTypes[ctx] = 'Int'
            # El nombre del tipo como INT
            ctx.typename = 'Int'
        # Salir suma con dos openscope
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def ingresarResta(self, ctx: CoolParser.SubContext):
        #print("ingresarResta")
        #time.sleep(1)
        # Ingresar resta con dos openscope
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def salirResta(self, ctx: CoolParser.SubContext):
        #print("salirResta")
        #time.sleep(1)
        # Se obtiene el dato de la izquierda
        izquierda = ctx.getChild(0)
        # Se obtiene el dato de la derecha
        derecha = ctx.getChild(2)
        # Si la estructura de la izquierda es distinto a un int o lo mismo en la derecha
        if (struct.ctxTypes[izquierda] != 'Int' or struct.ctxTypes[derecha] != 'Int'):
            # Se regresa un excepption de tipos que no son match
            raise myexceptions.TypeCheckMismatch
        else:  
            # Se establece el tipo del contexto como INT
            struct.ctxTypes[ctx] = 'Int'
            # El nombre del tipo como INT
            ctx.typename = 'Int'
        # Salir resta con dos closescope
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def IngresarLt(self, ctx: CoolParser.LtContext):
        # Menor que
        #print("IngresarLt")
        #time.sleep(1)
        # Se ingresa a menor que con dos openscope
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def salirLt(self, ctx: CoolParser.LtContext):
        # Menor que
        #print("salirLt")
        #time.sleep(1)
        # Se obtiene el dato de la izquierda
        izquierda = ctx.getChild(0)
        # Se obtiene el dato de la derecha
        derecha = ctx.getChild(2)
         # Si la estructura de la izquierda es distinto a un int o lo mismo en la derecha
        if (struct.ctxTypes[izquierda] != 'Int' or struct.ctxTypes[derecha] != 'Int'):
             # Se regresa un excepption de tipos que no son match
            raise myexceptions.TypeCheckMismatch
        else:  
            # Se establece el tipo del contexto como booleano
            struct.ctxTypes[ctx] = 'Bool'
            # El nombre del tipo como INT
            ctx.typename = 'Int'
        # Se ingresa a menor que con dos openscope
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def ingresarLe(self, ctx: CoolParser.LeContext):
        # Menor o igual
        #print("ingresarLe")
        #time.sleep(1)
        # Se ingresa a menor o igual con dos openscope
        self.idsTypes.openScope()
        self.idsTypes.openScope()
        
    def salirLe(self, ctx: CoolParser.LeContext):
        # Menor o igual
        #print("salirLe")
        #time.sleep(1)
        # Se obtiene el dato de la izquierda
        izquierda = ctx.getChild(0)
        # Se obtiene el dato de la derecha
        derecha = ctx.getChild(2)
        # Si la estructura de la izquierda es distinto a un int o lo mismo en la derecha
        if (struct.ctxTypes[izquierda] != 'Int' or struct.ctxTypes[derecha] != 'Int'):
            # Se regresa un excepption de tipos que no son match
            raise myexceptions.TypeCheckMismatch
        else:  
            # Se establece el tipo del contexto como booleano
            struct.ctxTypes[ctx] = 'Bool'
            # El nombre del tipo como INT
            ctx.typename = 'Int'
        # Se sale a menor o igual con dos openscope
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def ingresarEq(self, ctx: CoolParser.EqContext):
        #print("ingresarEq")
        #time.sleep(1)
        # Se entra al equals con dos openscope
        self.idsTypes.openScope()
        self.idsTypes.openScope()

    def salirEq(self, ctx: CoolParser.EqContext):
        #print("salirEq")
        #time.sleep(1)
        # Se obtiene la expresion del contexto
        expr = ctx.expr()
        # Se obtienen los tipoe de valor de la izquierda
        izquierda = struct.ctxTypes[expr[0]]
        # Se obtienen los tipoe de valor de la derecha
        derecha = struct.ctxTypes[expr[1]]
        # Se establecen los parametros que se van a ignorar
        ignorar = ['Int', 'String', 'Bool']
        # Si alguno de la izquierda o derecha se encuentra dento de la lista a ignorar se entra
        if izquierda in ignorar or derecha in ignorar:
            # Si la izquierda es distinta a la derecha (Si son dos tipos distintos)
            if izquierda != derecha:
                # Se muestra la exception que soin distintos tipos
                raise myexceptions.TypeCheckMismatch

        struct.ctxTypes[ctx] = 'Bool'
        ctx.typename = 'Int'
        # Se sale del equals con dos closescope
        self.idsTypes.closeScope()
        self.idsTypes.closeScope()

    def ingresarNot(self, ctx: CoolParser.NotContext):
        #print("ingresarNot")
        #time.sleep(1)
        # Se ingresa al not con el openscope
        self.idsTypes.openScope()

    def salirNot(self, ctx: CoolParser.NotContext):
        #print("salirNot")
        #time.sleep(1)
        # Si la expresion del contexto de not es de tipo bool
        if struct.ctxTypes[ctx.expr()] == 'Bool':
            # El tipo del contexto se establece como bool
            struct.ctxTypes[ctx] = 'Bool'
            # Al igual que su nombre del tipo
            ctx.typename = 'Bool'
        # Se sale del not con un close scope
        self.idsTypes.closeScope()

    def ingresarAssign(self, ctx: CoolParser.AssignContext):
        #print("ingresarAssign")
        #time.sleep(1)
        # Si el id del contexto es de tipo self
        if ctx.ID().getText() == 'self':
            # Se muestra la exceltion de que no debe ser de tipo self
            raise myexceptions.SelfAssignmentException
        # Se realiza un openscope para adentrarnos mas dentro de la asignacion
        self.idsTypes.openScope()
    

    def salirAssign(self, ctx: CoolParser.AssignContext):
        #print("salirAssign")
        #time.sleep(1)
        # Se establece el id de la asignacion
        IDType = self.idsTypes[ctx.ID().getText()]
        # Se establece el tipo de la expresion del contesto
        exprType = struct.ctxTypes[ctx.expr()]
        # Se busca el ID de la clase con el ID del tipo
        IDClass = struct.lookupClass(IDType)
        # Se busca la expresion de la clase con el tipo de la expresion
        exprKlass = struct.lookupClass(exprType)
        # Si el ID se la clase no es parte de la expresion de la clase
        if not IDClass.conforms(exprKlass):
            # Se muestra la excepsion de que no es parte de la expresion
            raise myexceptions.DoesNotConform
        # Se establece el tipo de expresion de la asignacion
        struct.ctxTypes[ctx] = exprType
        # Se cambia el nombre del tipo de la expresion
        ctx.typename = exprType
        # Se realiza un close scope que significa que se sale de la asignacion
        self.idsTypes.closeScope()

    def salirInt(self, ctx: CoolParser.IntegerContext):
        #print("salirInt")
        #time.sleep(1)
        # Se establece el tipo de estructura y del nombre del context como Int
        struct.ctxTypes[ctx] = 'Int'
        ctx.truevalue = ctx.INTEGER().getText()
        # Determinar literales Int
        struct.valuesInt.append(int(ctx.INTEGER().getText()))
        ctx.typename = 'Int'
    
    def salirString(self, ctx: CoolParser.StringContext):
        #print("salirString")
        #time.sleep(1)
        # Se establece el tipo de estructura y del nombre del context como String
        struct.ctxTypes[ctx] = 'String'
        ctx.typename = 'String'
        ctx.truevalue = ctx.STRING().getText()[1:-1]
        # Determinar literales string
        struct.valuesString.append(ctx.STRING().getText()[1:-1])
    
    def salirBool(self, ctx: CoolParser.BoolContext):
        #print("salirBool")
        ##time.sleep(1)
        # Se establece el tipo de estructura y del nombre del context como booleano
        struct.ctxTypes[ctx] = 'Bool'
        ctx.typename = 'Bool'
        ctx.truevalue = ctx.getText()
        
    def salirParens(self, ctx: CoolParser.ParensContext):
        #print("salirParens")
        #time.sleep(1)
        # Se guarda el tipo de estructura de la expresion en type
        _type = struct.ctxTypes[ctx.expr()]
        # Se establece el tipo de context dentro de la lista de los tipos
        struct.ctxTypes[ctx] = _type
        # Se establece el nombre del tipo
        ctx.typename = _type

    def salirObject(self, ctx: CoolParser.ObjectContext):
        #print("salirObject")
        #time.sleep(1)
        # Se obtiene el id del objeto dentro de la variable id
        ID = ctx.ID().getText()
        try:
            # Se obtiene el tipo del metodo dentro de la variable type segun su id
            _type = self.idsTypes[ID]
            # Se establece el tipo del objeto dentro de la lista de tipos con la variable type
            struct.ctxTypes[ctx] = _type
            # Se establece el nombre del context del objeto
            ctx.typename = _type
        except KeyError:
            # Si no se puede obtener el tipo segun su id, se muestra la excepcion de identificador sin declarar
            raise myexceptions.UndeclaredIdentifier
    
    