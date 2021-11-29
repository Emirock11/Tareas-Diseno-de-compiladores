from typing import KeysView
from unittest.main import main
from antlr.CoolListener import CoolListener
from antlr.CoolParser import CoolParser
import myexceptions
import structure as struct
import time

class PreJerarquia(CoolListener):

    def __init__(self):
        # Se establecen los parametros iniciales
        self.claseActual = None
        # Obtener las clases base
        self.clasesBase = struct.SymbolTable()
        
        # Diccionario vacío
        self.herencia = dict()
        # La variable de todas las clases del archivo struct como vacío
        struct.allClasses = {}
        # Todos los tipos del contexto se guardan en ctxTypes
        struct.ctxTypes = struct.SymbolTable()
        # Se establecen las clases base
        self.setClasesBase()

    def ingresarClass(self, ctx: CoolParser.KlassContext):
        #print("ingresarClass()")
        #time.sleep(1)
        # Se obtienen todos los tipos que están dentro de la variable context
        types = ctx.TYPE()
        # Se obtiene el nombre de la clase que está dentro de la pocision 0 de types
        className = types[0].getText()
        # Si el nombre de la clase se establece como el nombre de una clase base...
        if className in self.clasesBase:
            # Se levanta un exception mostrando el error de que se tiene que redefinir el nombre de la clase
            raise myexceptions.RedefineBasicClassException
        try:
            # Se observa si hay una clase con el nombre del className regresando una lista desde el archivo de estructura...
            klass = struct.lookupClass(className)
            # Si la lista tiene un elemento / Si ya hay una clase con el mismo nombre dentro de la estructura...
            if klass:
                # Se levanta un exception mostrando que se deben redefinir el nombre de la clase
                raise myexceptions.ClassRedefinition
        except KeyError:
            pass
        
        if len(types) > 1:
            # Se guarda la herencia que se entuentra dentro de la lista de tipos...
            inherit = types[1].getText()
            # Si la herencia tiene como texto que es de tipo Bool, String o SELF_TYPE...
            if inherit in ['Bool', 'SELF_TYPE', 'String']:
                # Se regresa la excepcion que el tipo de la herencia es inválido...
                raise myexceptions.InvalidInheritsException
            # Se agrega la herencia en la posicion del nombre de la clase
            self.herencia[className] = inherit
        # Se guarda la estructura de la klase actual en la variable Klass
        klass = struct.Klass(className)
        # Se establece la clase actual dentro de la variable de claseActual global
        self.claseActual = klass
    
    def ingresarMethod(self, ctx: CoolParser.MethodContext):
        #print("ingresarMethod()")
        #time.sleep(1)
        # Al ingresar al metodo se agrega el tipo de ctx en una lista dentro del archivo de la estreuctura del código
        struct.ctxTypes[ctx] = ctx.TYPE().getText()

    def salirMethod(self, ctx: CoolParser.MethodContext):
        #print("salirMethod()")
        #time.sleep(1)
        # Se guarda el ID de la variable context
        ID = ctx.ID().getText()
        # Se guarda el tipo de la variable context
        type = ctx.TYPE().getText()
        # Se guarda la lista de los formals que se encuentran dentro del método
        formals = ctx.formal()
        # Se crea una lista de los parametros que se puede encontrar dentro del metodo
        listaPar = []
        for formal in formals:
            # Se agrega dentro de la lista del parseo el id del formal junto con su tipo de estructura, si es una lista (l) o un int (i)
            listaPar.append((formal.ID().getText(), struct.ctxTypes[formal]))
        # Se agrega el metodo dentro de la variable global de la clase actual con su id y
        # guardando el tipo del metodo junto con la lista de los parametros que tiene dentro el metodo
        self.claseActual.addMethod(ID, struct.Method(type, listaPar))
        # Se establece el tipo el nombre del metodo con su id (head, tail, init, main, print_list, cons, isNil)
        ctx.namemethod = ID
        # Y su tipo del metodo dentro de la variable de context (Int, List, Bool, Object)
        ctx.typemethod = type

    def ingresarAtribute(self, ctx: CoolParser.AtributeContext):
        #print("ingresarAtribute()")
        #time.sleep(1)
        # Se guarda el ID de la variable context
        ID = ctx.ID().getText()
        # Se guarda el tipo de la variable context
        type = ctx.TYPE().getText()
        # Si ID es self...
        if ID == 'self':
            # Se muestra la excepcion de que no puede ser una variable self
            raise myexceptions.SelfVariableException
        # Se agrega el atributo ingresando su ID y su tipo...
        self.claseActual.addAttribute(ID, type)

    def salirPrograma(self, ctx: CoolParser.ProgramContext):
        #print("salirPrograma()")
        #time.sleep(1)
        # Se realiza un try y un except para ver dentro de la clase si hay un metodo de tipo main
        try:
            struct.lookupClass('Main').lookupMethod('main')
        except KeyError as e:
            # Si no es asi, entonces se muestra la excepcion de que no hay un main dentro del archivo
            raise myexceptions.NoMainException
        # Dentro de toda la lista de herencia creado al estar ingresando en el programa...
        for name, inherits in self.herencia.items():
            # En la variable Klass se guarda la estructura segun el nombre del item de la herencia
            klass = struct.lookupClass(name)
            # Se cuardan los atributos y metodos de la clase
            antAtri = klass.attributes
            antMetho = klass.methods

            try:
                # Se busca el nombre y la herencia por cada tipo de variable de toda la clase...
                struct.Klass(name, inherits=inherits)
            except KeyError:
                # Si no se encuentra, se muestra una excepcion de que no se encontro el tipo o el nombre de la variable
                raise myexceptions.TypeNotFound
            # Se establece una nueva clase con el nombre de los items de la herencia
            newKlass = struct.lookupClass(name)
            # Los atributos anteriores se agregan a la nueva clase
            newKlass.attributes = antAtri
            # Y los metodos anteriores
            newKlass.methods = antMetho
    
    def salirFormal(self, ctx: CoolParser.FormalContext):
        #print("salirFormal()")
        #time.sleep(1)
        # Se guarda el type de la variable context
        type = ctx.TYPE().getText()
        # Se guarda el type dentro de la estructura del archivo 
        # en la lista de los context types segun la variable context con la que se este trabajando
        struct.ctxTypes[ctx] = type
        # Se setea el tipo de nombre de context con el type
        ctx.typename = type
    
    
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