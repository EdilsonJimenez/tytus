# ======================================================================
#                          IMPORTES Y PLY
# ======================================================================
#importamos la libreria PLY para hacer nuestro analizador lexico.
import ply.lex as lex
#importamos la libreria para llamar al parcer de PLY
import ply.yacc as yacc
#importamos mas librerias que seran utilizadas en el analizador.
#Estas librerias son compatibles con la licencia ya que son librerias propias de python
import re
import codecs
import os
import sys
# ======================================================================
#                          ENTORNO Y PRINCIPAL
# ======================================================================
from execution.symbol.environment import Environment
from TypeChecker.Database_Types import *
from execution.symbol.typ import *
from execution.main import Main

# ======================================================================
#                          INSTRUCCIONES DDL
# ======================================================================
from execution.querie.use import Use
from execution.querie.create import Create
from execution.querie.show_database import Show_Database
from execution.querie.drop_database import Drop_Database
from execution.querie.alter_database import Alter_Database
from execution.querie.add_column import Add_Column
from execution.querie.add_constraint import Add_Constraint
from execution.querie.alter_column import Alter_Column
from execution.querie.alter_table import Alter_Table
from execution.querie.case import Case
from execution.querie.create_t import Create_Table
from execution.querie.create_type import Create_Type
from execution.querie.drop_column import Drop_Column
from execution.querie.drop_constraint import Drop_Constraint
from execution.querie.drop_database import Drop_Database
from execution.querie.drop_t import Drop_Table

from execution.symbol.column import Column

# ======================================================================
#                          INSTRUCCIONES DML
# ======================================================================
from execution.querie.insert import Insert
from execution.querie.update import Update
from execution.querie.select_ import Select
from execution.querie.delete import Delete

# ======================================================================
#                             EXPRESIONES
# ======================================================================
from execution.expression.arithmetic import Arithmetic
from execution.expression.greatest import Greatest
from execution.expression.id import Id
from execution.expression.least import Least
from execution.expression.literal import Literal
from execution.expression.neg import Neg
from execution.expression.logic import Logic
from execution.expression.predicates import Predicates
from execution.expression.relational import Relational
from execution.expression.stringop import Stringop

# ======================================================================
#                        FUNCIONES MATEMATICAS
# ======================================================================
from execution.function.mathematical.abs import Abs
from execution.function.mathematical.cbrt import Cbrt
from execution.function.mathematical.ceil import Ceil
from execution.function.mathematical.ceiling import Ceiling
from execution.function.mathematical.degrees import Degrees
from execution.function.mathematical.div import Div
from execution.function.mathematical.exp import Exp
from execution.function.mathematical.factorial import Factorial
from execution.function.mathematical.floor import Floor
from execution.function.mathematical.gcd import Gcd
from execution.function.mathematical.ln import Ln
from execution.function.mathematical.log import Log
from execution.function.mathematical.pi import Pi
from execution.function.mathematical.power import Power
from execution.function.mathematical.radians import Radians
from execution.function.mathematical.random import Randomic
from execution.function.mathematical.round import Round
from execution.function.mathematical.sign import Sign
from execution.function.mathematical.sqrt import Sqrt
from execution.function.mathematical.trunc import Trunc

# ======================================================================
#                       FUNCIONES TRIGONOMETRICAS
# ======================================================================
from execution.function.trigonometric.acos import Acos
from execution.function.trigonometric.acosd import Acosd
from execution.function.trigonometric.acosh import Acosh
from execution.function.trigonometric.asin import Asin
from execution.function.trigonometric.asind import Asind
from execution.function.trigonometric.asinh import Asinh
from execution.function.trigonometric.atan import Atan
from execution.function.trigonometric.atan2 import Atan2
from execution.function.trigonometric.atan2d import Atan2d
from execution.function.trigonometric.atand import Atand
from execution.function.trigonometric.atanh import Atanh
from execution.function.trigonometric.cos import Cos
from execution.function.trigonometric.cosd import Cosd
from execution.function.trigonometric.cosh import Cosh
from execution.function.trigonometric.cot import Cot
from execution.function.trigonometric.cotd import Cotd
from execution.function.trigonometric.sin import Sin
from execution.function.trigonometric.sind import Sind
from execution.function.trigonometric.sinh import Sinh
from execution.function.trigonometric.tan import Tan
from execution.function.trigonometric.tand import Tand
from execution.function.trigonometric.tanh import Tanh

# ======================================================================
#                       FUNCIONES DE AGREGADO
# ======================================================================
from execution.function.agreggates.avg import Avg
from execution.function.agreggates.count import Count
from execution.function.agreggates.max import Max
from execution.function.agreggates.min import Min
from execution.function.agreggates.sum import Sum

# ======================================================================
#                       FUNCIONES BINARIAS
# ======================================================================
from execution.function.binary.get_byte import Get_Byte
from execution.function.binary.length import Length
from execution.function.binary.md5 import Md5
from execution.function.binary.set_byte import Set_Byte
from execution.function.binary.sha256 import Sha256
from execution.function.binary.substr import Substr
from execution.function.binary.substring import Substring
from execution.function.binary.trim import Trim

# creamos la lista de tokens de nuestro lenguaje.
reservadas = ['SMALLINT','INTEGER','BIGINT','DECIMAL','NUMERIC','REAL','DOBLE','PRECISION','MONEY',
              'VARYING','VARCHAR','CHARACTER','CHAR','TEXT',
              'TIMESTAMP','DATE','TIME','INTERVAL',
              'YEAR','MONTH','DAY','HOUR','MINUTE','SECOND',
              'BOOLEAN',
              'CREATE','TYPE','AS','ENUM','USE',
              'BETWEEN','LIKE','ILIKE','SIMILAR','ON','INTO','TO',
              'IS','ISNULL','NOTNULL',
              'NOT','AND','OR',
              'REPLACE','DATABASE','DATABASES','IF','EXISTS','OWNER','MODE','SELECT','EXIST',
              'ALTER','DROP','RENAME','SHOW','ADD','COLUMN','DELETE','FROM',
              'INSERT','VALUES','UPDATE','SET','GROUP','BY','HAVING','ORDER',
              'RETURNING','USING','DISTINCT',
              'TABLE','CONSTRAINT','NULL','CHECK','UNIQUE',
              'PRIMARY','KEY','REFERENCES','FOREIGN',
              'FALSE','TRUE','UNKNOWN','SYMMETRIC','SUBSTRING',
              'ALL','SOME','ANY','INNER','JOIN','LEFT','RIGTH','FULL','OUTER','NATURAL',
              'ASC','DESC','FIRST','LAST','NULLS',
              'CASE','WHEN','THEN','ELSE','END','LIMIT',
              'UNION','INTERSECT','EXCEPT','OFFSET','GREATEST','LEAST','WHERE','DEFAULT','CASCADE','NO','ACTION',
              'COUNT','SUM','AVG','MAX','MIN',
              'ABS','CBRT','CEIL','CEILING','DEGREES','DIV','EXP','FACTORIAL','FLOOR','GCD','IN','LN','LOG','MOD','PI','POWER','ROUND',
              'ACOS','ACOSD','ASIN','ASIND','ATAN','ATAND','ATAN2','ATAN2D','COS','COSD','COT','COTD','SIN','SIND','TAN','TAND',
              'SINH','COSH','TANH','ASINH','ACOSH','ATANH',
              'DATE_PART','NOW','EXTRACT','CURRENT_TIME','CURRENT_DATE',
              'LENGTH','TRIM','GET_BYTE','MOD5','SET_BYTE','SHA256','SUBSTR','CONVERT','ENCODE','DECODE','DOUBLE','INHERITS'
              ]

tokens = reservadas + ['PUNTO','PUNTO_COMA','CADENASIMPLE','COMA','SIGNO_IGUAL','PARABRE','PARCIERRE','SIGNO_MAS','SIGNO_MENOS',
                       'SIGNO_DIVISION','SIGNO_POR','NUMERO','NUM_DECIMAL','CADENA','ID','LLAVEABRE','LLAVECIERRE','CORCHETEABRE',
                       'CORCHETECIERRE','DOBLE_DOSPUNTOS','SIGNO_POTENCIA','SIGNO_MODULO','MAYORQUE','MENORQUE',
                       'MAYORIGUALQUE','MENORIGUALQUE',
                       'SIGNO_PIPE','SIGNO_DOBLE_PIPE','SIGNO_AND','SIGNO_VIRGULILLA','SIGNO_NUMERAL','SIGNO_DOBLE_MENORQUE','SIGNO_DOBLE_MAYORQUE',
                       'FECHA_HORA','F_HORA','COMILLA','SIGNO_MENORQUE_MAYORQUE','SIGNO_NOT'
                       ]


# lista para definir las expresiones regulares que conforman los tokens.
t_ignore = '\t\r '

t_SIGNO_DOBLE_PIPE = r'\|\|'
t_SIGNO_PIPE = r'\|'
t_SIGNO_AND = r'\&'
t_SIGNO_VIRGULILLA = r'\~'
t_SIGNO_NUMERAL = r'\#'
t_SIGNO_DOBLE_MENORQUE = r'\<\<'
t_SIGNO_DOBLE_MAYORQUE = r'\>\>'
t_SIGNO_MENORQUE_MAYORQUE = r'\<\>'
t_SIGNO_NOT = r'\!\='

t_PUNTO= r'\.'
t_PUNTO_COMA = r'\;'
t_COMA = r'\,'
t_SIGNO_IGUAL = r'\='
t_PARABRE = r'\('
t_PARCIERRE = r'\)'
t_SIGNO_MAS = r'\+'
t_SIGNO_MENOS = r'\-'
t_SIGNO_DIVISION = r'\/'
t_SIGNO_POR= r'\*'
t_LLAVEABRE = r'\{'
t_LLAVECIERRE = r'\}'
t_CORCHETEABRE = r'\['
t_CORCHETECIERRE = r'\]'
t_DOBLE_DOSPUNTOS= r'\:\:'
t_SIGNO_POTENCIA = r'\^'
t_SIGNO_MODULO = r'\%'
t_MAYORIGUALQUE = r'\>\='
t_MENORIGUALQUE = r'\<\='
t_MAYORQUE = r'\>'
t_MENORQUE = r'\<'
t_COMILLA = r'\''


# expresion regular para los id´s
def t_ID (t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        if t.value.upper() in reservadas:
            t.value = t.value.upper()
            t.type = t.value    
        return t

def t_CADENASIMPLE(t):
    r'\'.*?\''
    t.value = str(t.value)
    t.value = t.value[1:-1]
    return t

# expresion regular para comentario de linea
def t_COMMENT(t):
    r'--.*'
    t.lexer.lineno += 1

# expresion regular para comentario de linea
def t_COMMENT_MULT(t):
    r'/\*(.|\n)?\*/'
    t.lexer.lineno += t.value.count('\n')

def t_NUM_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t
    
# expresion regular para reconocer numeros
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# expresion regular para reconocer formato hora
def t_F_HORA(t):
    r'\'\s*(\d+\s+(hours|HOURS))?(\s*\d+\s+(minutes|MINUTES))?(\s*\d+\s+(seconds|SECONDS))?\s*\''
    t.value = t.value[1:-1]
    return t

# expresion regular para reconocer fecha_hora
def t_FECHA_HORA(t):
    r'\'\d+-\d+-\d+ \d+:\d+:\d+\''
    t.value = t.value[1:-1]
    from datetime import datetime
    try:
        t.value = datetime.strptime(t.value,'%Y-%m-%d %H:%M:%S')
    except ValueError:
        t.value = datetime(2000,1,1)
    return t
    
# expresion regular para reconocer cadenas
def t_CADENA(t):
    r'\".*?\"'
    t.value = str(t.value)
    t.value = t.value[1:-1]
    return t

# expresion regular para saltos de linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
# expresion regular para reconocer errores
def t_error(t):
    print ("caracter desconocido '%s'" % t.value[0])
    t.lexer.skip(1)

# fin de las expresiones regulares para reconocer nuestro lenguaje.


# funcion para realizar el analisis lexico de nuestra entrada
def analizarLex(texto):    
    analizador = lex.lex()
    analizador.input(texto)# el parametro cadena, es la cadena de texto que va a analizar.

    #ciclo para la lectura caracter por caracter de la cadena de entrada.
    textoreturn = ""
    while True:
        tok = analizador.token()
        if not tok : break
        #print(tok)
        textoreturn += str(tok) + "\n"
    return textoreturn 


 ######### inicia el analizador Sintactico ##########

 # Asociación de operadores y precedencia

 #FALTAN ALGUNOS SIGNOS/PALABRAS RESERVADAS EN LA PRECEDENCIA
precedence = (
    ('left','OR'),
    ('left','AND'),
    ('left','MAYORIGUALQUE','MENORIGUALQUE','MAYORQUE','MENORQUE'),
    ('left','SIGNO_MAS','SIGNO_MENOS'),
    ('left','SIGNO_POR','SIGNO_DIVISION'),
    ('left','SIGNO_POTENCIA','SIGNO_MODULO'),    
    ('right','UMENOS')
    )          


# Definición de la gramática
def p_inicio(t):
    '''inicio : instrucciones '''
    envGlobal = Environment(None)
    iniciarEjecucion = Main(t[1])
    iniciarEjecucion.execute(envGlobal)

def p_instrucciones_lista(t):
    '''instrucciones : instrucciones instruccion 
                     | instruccion '''
    if len(t) == 3:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_instrucciones_evaluar(t):
    '''instruccion : ins_use
                   | ins_show
                   | ins_alter
                   | ins_drop
                   | ins_create
                   | ins_insert
                   | ins_select
                   | ins_update
                   | ins_delete
                   | exp'''
    t[0] = t[1]

def p_instruccion_use(t):
    '''ins_use : USE ID PUNTO_COMA'''
    t[0] = Use(t[2], t.slice[1].lexpos,t.slice[1].lineno)

def p_instruccion_show(t):
    '''ins_show : SHOW DATABASES PUNTO_COMA'''
    t[0] = Show_Database(t.slice[1].lexpos,t.slice[1].lineno)

def p_instruccion_create(t):
    '''ins_create : CREATE tipo_create'''
    t[0] = t[2]  

def p_tipo_create(t):
    '''tipo_create : ins_replace DATABASE if_exists ID create_opciones PUNTO_COMA
                   | TABLE ID PARABRE definicion_columna PARCIERRE ins_inherits PUNTO_COMA
                   | TYPE ID AS ENUM PARABRE list_vls PARCIERRE PUNTO_COMA'''
    if t[1] == 'TYPE':
        print('TYPE')
    elif t[1] == 'TABLE':
        arreglo = []
        for item in t[4]:
            for i in item:
                arreglo.append(i)

        t[0] = Create_Table(t[2], arreglo, t.slice[1].lexpos,t.slice[1].lineno)
    else:
        pass

def p_definicion_columna(t):
    '''definicion_columna : definicion_columna COMA columna 
                          | columna ''' # no se *** si va la coma o no
    if len(t) == 4:
        t[1].append(t[3])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_columna(t):
    '''columna : ID tipo_dato definicion_valor_defecto ins_constraint
                | primary_key 
                | foreign_key 
                | unique'''
    if len(t) == 1:
        t[0] = t[1]
    else:
        columna = []
        columna.append( Column(t[1], t[2]['type'], t[3], t[2]['length']))

        for item in t[4]:
            if 'name' not in item:
                if item['type'] == 'primary':
                    item['name'] = 'pk_' + t[1]
                if item['type'] == 'not null':
                    item['name'] = 'nn_' + t[1]
                if item['type'] == 'unique':
                    item['name'] = 'uq_' + t[1]
                if item['type'] == 'foreign':
                    item['name'] = 'fk_' + t[1]
                if item['type'] == 'check':
                    item['name'] = 'ch_' + t[1]
            if item['type'] != 'check':
                item['value'] = t[1]
            columna.append(item)
        t[0] = columna


def p_ins_inherits(t):
    '''ins_inherits : INHERITS PARABRE ID PARCIERRE
                |  ''' #EPSILON

def p_unique(t):
    ''' unique : UNIQUE PARABRE nombre_columnas PARCIERRE  '''
    if isinstance(t[3],list):
        ids = []
        for item in t[3]:
            ids.append({'type': 'unique', 'name': 'uq_'+item, 'value': item})
        t[0] = ids
    else:
        t[0] = [{'type': 'unique', 'name': 'uq_'+t[3], 'value': t[3]}]

def p_primary_key(t):
    '''primary_key : PRIMARY KEY PARABRE nombre_columnas PARCIERRE ins_references'''
    if isinstance(t[4],list):
        ids = []
        for item in t[4]:
            ids.append({'type': 'primary', 'name': 'pk_'+item, 'value': item})
        t[0] = ids
    else:
        t[0] = [{'type': 'primary', 'name': 'pk_'+t[4], 'value': t[4]}]
 
def p_foreign_key(t):
    '''foreign_key : FOREIGN KEY PARABRE nombre_columnas PARCIERRE REFERENCES ID PARABRE nombre_columnas PARCIERRE ins_references'''
    
    if isinstance(t[4],list):
        ids = []
        posicion = t[4]
        reference = t[9]
        for i in range(len(posicion)):
            ids.append({'type': 'foreign', 'name':'fk_'+posicion[i], 'value': posicion[i], 'references': reference[i]})
        t[0] = ids
    else:
        t[0] = [{'type': 'foreign', 'name':'fk_'+t[4], 'value': t[4], 'references': t[9]}]

def p_nombre_columnas(t):
    '''nombre_columnas : nombre_columnas COMA ID 
                          | ID '''
    if len(t) == 4:
        t[1].append(t[3])
    else:
        t[0] = [t[1]]

def p_tipo_dato(t):
    '''tipo_dato : SMALLINT          
                 | BIGINT
                 | NUMERIC
                 | DECIMAL
                 | INTEGER
                 | REAL
                 | DOUBLE PRECISION
                 | CHAR PARABRE NUMERO PARCIERRE
                 | VARCHAR PARABRE NUMERO PARCIERRE
                 | CHARACTER PARABRE NUMERO PARCIERRE
                 | TEXT
                 | TIMESTAMP arg_precision
                 | TIME arg_precision
                 | DATE
                 | INTERVAL arg_tipo arg_precision
                 | BOOLEAN
                 | MONEY'''
    if t.slice[1] == 'SMALLINT':
        t[0] = {'type':DBType.smallint, 'length': -1, 'default':0 }
    elif t.slice[1] == 'BIGINT':
        t[0] = {'type':DBType.bigint, 'length': -1, 'default':0 }
    elif t.slice[1] == 'NUMERIC':
        t[0] = {'type':DBType.numeric, 'length': -1, 'default':0 }
    elif t.slice[1] == 'DECIMAL':
        t[0] = {'type':DBType.decimal, 'length': -1, 'default':0.0 }
    elif t.slice[1] == 'INTEGER':
        t[0] = {'type':DBType.integer, 'length': -1, 'default':0 }
    elif t.slice[1] == 'REAL':
        t[0] = {'type':DBType.real, 'length': -1, 'default':0.0 }
    elif t.slice[1] == 'DOUBLE':
        t[0] = {'type':DBType.double_precision, 'length': -1, 'default':0.0 }
    elif t.slice[1] == 'TEXT':
        t[0] = {'type':DBType.text, 'length': -1, 'default':"" }
    elif t.slice[1] == 'DATE':
        t[0] = {'type':DBType.date, 'length': -1, 'default':"2000-01-01" }
    elif t.slice[1] == 'BOOLEAN':
        t[0] = {'type':DBType.boolean, 'length': -1, 'default':False }
    elif t.slice[1] == 'MONEY':
        t[0] = {'type':DBType.money, 'length': -1, 'default':0.0 }
    
    elif t.slice[1] == 'TIMESTAMP':
        t[0] = {'type':DBType.timestamp_wtz, 'length': t[2], 'default':"2000-01-01" }
    elif t.slice[1] == 'TIME':
        t[0] = {'type':DBType.time_wtz, 'length': t[2], 'default':"00:00:01" }
    elif t.slice[1] == 'INTERVAL':
        t[0] = {'type':DBType.interval, 'length': -1, 'default':"1 HOUR 1 MINUTE 1 SECOND" }

    elif t.slice[1] == 'CHAR':
        t[0] = {'type':DBType.char, 'length':t[3], 'default':"" }
    elif t.slice[1] == 'VARCHAR':
        t[0] = {'type':DBType.varchar, 'length':t[3], 'default':"" }
    elif t.slice[1] == 'CHARACTER':
        t[0] = {'type':DBType.character, 'length':t[3], 'default':"" }

def p_arg_precision(t):
    '''arg_precision : PARABRE NUMERO PARCIERRE 
                     | ''' #epsilon
    if len(t) == 4:
        t[0] = t[2]
    else:
        t[0] = None

def p_arg_tipo(t):
    '''arg_tipo : MONTH
                | YEAR
                | HOUR
                | MINUTE
                | SECOND            
                | '''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = None

def p_definicion_valor_defecto(t):
    '''definicion_valor_defecto : DEFAULT tipo_default 
                                | ''' #epsilon
    if len(t) == 3:
        t[0] = t[2]
    else:
        t[0] = None

def p_ins_constraint(t):
    '''ins_constraint : ins_constraint constraint restriccion_columna 
                        | restriccion_columna
                        |''' #epsilon
    if len(t) == 4:
        if t[2] != None:
            diccionario = t[3]
            diccionario['name'] = t[2]
            t[1].append(diccionario)
        else:
            t[1].append(t[3])
    elif len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = []

def p_constraint(t):
    '''constraint :  CONSTRAINT ID 
                    |  '''
    if len(t) == 3:
        t[0] = t[2]
    else:
        t[0] = None

def p_restriccion_columna(t):
    '''restriccion_columna : NOT NULL 
                           | SET NOT NULL 
                           | PRIMARY KEY 
                           | UNIQUE 
                           | NULL 
                           | NOT NULL PRIMARY KEY 
                           | CHECK PARABRE exp PARCIERRE 
                           | 
                           ''' #cambio del condicion columna
    if len(t) > 1:
        if t.slice[1].type == 'NOT' and t.slice[1].type == 'NULL':
            t[0] = {'type' : 'not null' }
        elif t.slice[1].type == 'SET' and t.slice[2].type == 'NOT' and t.slice[3].type == 'NULL':
            pass
        elif t.slice[1].type == 'PRIMARY' and t.slice[1].type == 'KEY':
            t[0] = {'type':'primary'}
        elif t.slice[1].type == 'UNIQUE' :
            t[0] = {'type':'unique'}
        elif t.slice[1].type == 'NULL' :
            t[0] = {'type' : 'null' }
        elif t.slice[1].type == 'NOT' and t.slice[2].type == 'NULL' and t.slice[3].type == 'PRIMARY' and t.slice[3].type == 'KEY':
            t[0] = {'type':'primary'}
        elif t.slice[1].type == 'CHECK' :
            {'type':'check', 'value': t[3]}




def p_references(t):
    '''ins_references : ON DELETE accion ins_references
                      | ON UPDATE accion ins_references
                      | '''

def p_accion(t):
    '''accion : CASCADE
              | SET NULL
              | SET DEFAULT
              | NO ACTION'''

def p_tipo_default(t): #ESTE NO SE SI SON RESERVADAS O LOS VALORES
    '''tipo_default : NUMERIC
                    | DECIMAL
                    | CADENA
                    | TRUE
                    | FALSE
                    | DATE
                    | TIME
                    | NULL'''
    t[0] = t[1]
 
def p_ins_replace(t): 
    '''ins_replace : OR REPLACE
               | '''#EPSILON
    if len(t) ==3:
        t[0] = True
    else: 
        t[0] = False

def p_if_exists(t): 
    '''if_exists :  IF NOT EXISTS
                |  IF EXISTS
                | ''' # EPSILON

def p_create_opciones(t): 
    '''create_opciones : OWNER SIGNO_IGUAL user_name create_opciones
                       | MODE SIGNO_IGUAL NUMERO create_opciones
                       | '''
    #if len(t) == 5:
    #    if t[1] == 'MODE':
    #        t[0] = t[3]
    #    else:
    #        t[0] = 0
    #else: 
    #    t[0] = 0

def p_user_name(t):
    '''user_name : ID
                  | CADENA 
                  | CADENASIMPLE'''
    #t[0] = t[1]

def p_alter(t): 
    '''ins_alter : ALTER tipo_alter ''' 
    #t[0] = t[2]

def p_tipo_alter(t): 
    '''tipo_alter : DATABASE ID alter_database PUNTO_COMA
                  | TABLE ID alteracion_tabla PUNTO_COMA''' # NO SE SI VAN LOS PUNTO Y COMA
    #if t[1] == 'DATABASE':
    #    if t[3] == None:
    #        t[0] = Alter_Database(t[2],t[2], 0, 0)
    #    else: 
    #        t[0] = Alter_Database(t[2],t[3], 0, 0)
    #else: 
    #    print('TABLE')

def p_alteracion_tabla(t): 
    '''alteracion_tabla : alteracion_tabla COMA alterar_tabla
                        | alterar_tabla'''

def p_alterar_tabla(t): 
    #alter column viene como una lista
    '''alterar_tabla : ADD COLUMN ID tipo_dato
                     | ADD CONSTRAINT ins_constraint
                     | ALTER COLUMN ID TYPE tipo_dato
                     | ALTER COLUMN ID SET NOT NULL
                     | DROP COLUMN ID
                     | DROP CONSTRAINT ID'''

def p_alter_database(t): 
    '''alter_database : RENAME TO ID
                      | OWNER TO ID'''
    #if t[1] == 'RENAME':
    #    t[0] = t[3]
    #else:
    #    t[0] = None

def p_drop(t): 
    '''ins_drop : DROP tipo_drop'''
    #t[0] = t[2]

def p_tipo_drop(t): 
    '''tipo_drop : DATABASE if_exists ID PUNTO_COMA
                 | TABLE ID PUNTO_COMA'''
    #if len(t) == 5:
    #    t[0] = Drop_Database(t[3], 0, 0)

def p_ins_insert(t):
    '''ins_insert : INSERT INTO ID VALUES PARABRE list_vls PARCIERRE PUNTO_COMA 
                  | INSERT INTO ID PARABRE list_id PARCIERRE VALUES PARABRE list_vls PARCIERRE PUNTO_COMA'''
    print('INSERT INTO ID VALUES ( *values* )')

def p_list_id(t):
    '''list_id : list_id COMA ID
               | ID'''

def p_list_vls(t):
    '''list_vls : list_vls COMA val_value
                | val_value '''

def p_val_value(t):
    '''val_value : CADENA
                |   CADENASIMPLE
                |   NUMERO
                |   NUM_DECIMAL
                |   FECHA_HORA
                |   TRUE
                |   FALSE 
                |   NULL
                |   F_HORA'''
    if t.slice[1].type == 'CADENA':
        ob = Literal(t[1],Type.STRING,t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'CADENASIMPLE':
        ob = Literal(t[1],Type.STRING,t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'NUMERO':
        ob = Literal(t[1],Type.INT,t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'NUM_DECIMAL':
        ob = Literal(t[1],Type.DECIMAL,t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'FECHA_HORA':
        ob = Literal(t[1],Type.DATE,t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'F_HORA':
        ob = Literal(t[1],Type.DATE,t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'TRUE':
        ob = Literal(True,Type.BOOLEAN,t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'FALSE':
        ob = Literal(False,Type.BOOLEAN,t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'NULL':
        ob = Literal(t[1],Type.NULL,t.slice[1].lexpos,t.slice[1].lineno)
    t[0] = ob

def p_ins_select(t):
    '''ins_select : ins_select UNION option_all ins_select PUNTO_COMA
                    |    ins_select INTERSECT option_all ins_select PUNTO_COMA
                    |    ins_select EXCEPT option_all ins_select PUNTO_COMA
                    |    SELECT arg_distict colum_list FROM table_list arg_where arg_group_by arg_order_by arg_limit arg_offset PUNTO_COMA
                    |    SELECT functions as_id'''

def p_option_all(t):
    '''option_all   :   ALL
                    |    '''

def p_arg_distict(t):
    '''arg_distict :    DISTINCT
                    |    '''

def p_colum_list(t):
    '''colum_list   :   s_list
                    |   SIGNO_POR '''

def p_s_list(t):
    '''s_list   :   s_list COMA columns as_id
                |   columns as_id'''

def p_columns(t):
    '''columns   : ID dot_table
                    |   aggregates '''

def p_dot_table(t):
    '''dot_table    :   PUNTO ID
                    |    '''
    if len(t) == 2:
        t[0] = t[2]
    else:
        t[0] = None

def p_as_id(t): #  REVISRA CADENA Y AS CADENA
    '''as_id    :   AS ID
                    |   AS CADENA
                    |   CADENA
                    |   '''


def p_aggregates(t):
    '''aggregates   :   COUNT PARABRE param PARCIERRE
                    |   SUM PARABRE param PARCIERRE
                    |   AVG PARABRE param PARCIERRE
                    |   MAX PARABRE param PARCIERRE
                    |   MIN PARABRE param PARCIERRE ''' 
    if t.slice[1] == 'COUNT':
        t[0] = Count(t[3])
    if t.slice[1] == 'SUM':
        t[0] = Sum(t[3]) 
    if t.slice[1] == 'AVG':
        t[0] = Avg(t[3])
    if t.slice[1] == 'MAX':
        t[0] = Max(t[3])
    if t.slice[1] == 'MIN':
        t[0] = Min(t[3])

def p_functions(t):
    '''functions    :   math
                    |   trig
                    |   string_func
                    |   time_func
                     '''
    t[0] = t[1]
                    # CORREGIR GRAMATICA <STRING_FUNC>

def p_math(t):
    '''math :   ABS PARABRE op_numero PARCIERRE
                |   CBRT PARABRE op_numero PARCIERRE
                |   CEIL PARABRE op_numero PARCIERRE
                |   CEILING PARABRE op_numero PARCIERRE
                |   DEGREES PARABRE op_numero PARCIERRE
                |   DIV PARABRE op_numero COMA op_numero PARCIERRE
                |   EXP PARABRE op_numero PARCIERRE
                |   FACTORIAL PARABRE op_numero PARCIERRE
                |   FLOOR PARABRE op_numero PARCIERRE
                |   GCD PARABRE op_numero COMA op_numero PARCIERRE
                |   LN PARABRE op_numero PARCIERRE
                |   LOG PARABRE op_numero PARCIERRE
                |   MOD PARABRE op_numero COMA op_numero PARCIERRE
                |   PI PARABRE  PARCIERRE
                |   POWER PARABRE op_numero COMA op_numero PARCIERRE 
                |   ROUND PARABRE op_numero arg_num PARCIERRE '''
    if t.slice[1].type == 'PI':
        t[0] = Pi(t.slice[3].lexpos,t.slice[3].lineno)
    else:
        if t.slice[1].type == 'ABS':
            t[0] = Abs(t[3],t.slice[1].lexpos,t.slice[1].lineno)
        elif t.slice[1].type == 'CBRT':
            t[0] = Cbrt(t[3],t.slice[1].lexpos,t.slice[1].lineno)
        elif t.slice[1].type == 'CEIL':
            t[0] = Ceil(t[3],t.slice[1].lexpos,t.slice[1].lineno)
        elif t.slice[1].type == 'CEILING':
            t[0] = Ceiling(t[3],t.slice[1].lexpos,t.slice[1].lineno)
        elif t.slice[1].type == 'DEGREES':
            t[0] = Degrees(t[3],t.slice[1].lexpos,t.slice[1].lineno)
        elif t.slice[1].type == 'DIV':
            t[0] = Div(t[3],t[5],t.slice[1].lexpos,t.slice[1].lineno)
        elif t.slice[1].type == 'EXP':
            t[0] = Exp(t[3],t.slice[1].lexpos,t.slice[1].lineno)
        elif t.slice[1].type == 'FACTORIAL':
            t[0] = Factorial(t[3],t.slice[1].lexpos,t.slice[1].lineno)
        elif t.slice[1].type == 'FLOOR':
            t[0] = Floor(t[3],t.slice[1].lexpos,t.slice[1].lineno)
        elif t.slice[1].type == 'GCD':
            t[0] = Gcd(t[3],t[5],t.slice[1].lexpos,t.slice[1].lineno)
        elif t.slice[1].type == 'LN':
            t[0] = Ln(t[3],t.slice[1].lexpos,t.slice[1].lineno)
        elif t.slice[1].type == 'LOG':
            t[0] = Log(t[3],t.slice[1].lexpos,t.slice[1].lineno)
        elif t.slice[1].type == 'MOD':
            #FASE 2
            print("MOD - FASE 2")
        elif t.slice[1].type == 'POWER':
            t[0] = Power(t[3],t[5],t.slice[1].lexpos,t.slice[1].lineno)
        elif t.slice[1].type == 'ROUND':
            t[0] = Round(t[3],t[5],t.slice[1].lexpos,t.slice[1].lineno)

def p_arg_num(t):
    ''' arg_num : COMA NUMERO 
                |'''
    if len(t) == 3:
        t[0] = Literal(t[2],Type.INT,t.slice[2].lexpos,t.slice[2].lineno)
    t[0] = Literal(0,Type.INT,t.slice[2].lexpos,t.slice[2].lineno)

def p_op_numero(t):
    '''  op_numero : NUMERO 
                | DECIMAL
                | SIGNO_MENOS NUMERO %prec UMENOS
                | SIGNO_MENOS DECIMAL %prec UMENOS'''
    if t.slice[1].type == 'NUMERO':
        t[0] = Literal(t[1],Type.INT,t.slice[1].lexpos,t.slice[1].lineno)
    else:
        t[0] = Literal(t[1],Type.DECIMAL,t.slice[1].lexpos,t.slice[1].lineno)

    if t.slice[1].type == 'SIGNO_MENOS':
        if  t.slice[2].type == 'NUMERO':
            t[0] =  Neg(t[2],Type.INT,t.slice[2].lexpos,t.slice[2].lineno)
        else:
            t[0] =  Neg(t[2],Type.DECIMAL,t.slice[2].lexpos,t.slice[2].lineno)


def p_trig(t):
    '''trig :   ACOS PARABRE op_numero PARCIERRE
                |   ACOSD PARABRE op_numero PARCIERRE
                |   ASIN PARABRE op_numero PARCIERRE
                |   ASIND PARABRE op_numero PARCIERRE
                |   ATAN PARABRE op_numero PARCIERRE
                |   ATAND PARABRE op_numero PARCIERRE
                |   ATAN2 PARABRE op_numero COMA op_numero PARCIERRE
                |   ATAN2D PARABRE NUMERO COMA op_numero PARCIERRE
                |   COS PARABRE op_numero PARCIERRE
                |   COSD PARABRE op_numero PARCIERRE
                |   COT PARABRE op_numero PARCIERRE
                |   COTD PARABRE op_numero PARCIERRE
                |   SIN PARABRE op_numero PARCIERRE
                |   SIND PARABRE op_numero PARCIERRE
                |   TAN PARABRE op_numero PARCIERRE
                |   TAND PARABRE op_numero PARCIERRE
                |   SINH PARABRE op_numero PARCIERRE
                |   COSH PARABRE op_numero PARCIERRE
                |   TANH PARABRE op_numero PARCIERRE
                |   ASINH PARABRE op_numero PARCIERRE
                |   ACOSH PARABRE op_numero PARCIERRE
                |   ATANH PARABRE op_numero PARCIERRE  '''
    if t.slice[1].type == 'ACOS':
        t[0] = Acos(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'ACOSD':
        t[0] = Acosd(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'ASIN':
        t[0] = Asin(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'ASIND':
        t[0] = Asind(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'ATAN':
        t[0] = Atan(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'ATAND':
        t[0] = Atand(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'ATAN2':
        t[0] = Atan2(t[3],t[5],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'ATAN2D':
        t[0] = Atan2d(t[3],t[5],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'COS':
        t[0] = Cos(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'COSD':
        t[0] = Cosd(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'COT':
        t[0] = Cot(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'COTD':
        t[0] = Cotd(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'SIN':
        t[0] = Sin(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'SIND':
        t[0] = Sind(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'TAN':
        t[0] = Tan(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'TAND':
        t[0] = Tand(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'SINH':
        t[0] = Sinh(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'COSH':
        t[0] = Cosh(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'TANH':
        t[0] = Tanh(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'ASINH':
        t[0] = Asinh(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'ACOSH':
        t[0] = Acosh(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'ATANH':
        t[0] = Atanh(t[3],t.slice[1].lexpos,t.slice[1].lineno)

def p_string_func(t):   # CORREGIR GRAMÁTICA
    '''string_func  :   LENGTH PARABRE s_param PARCIERRE
                    |   SUBSTRING PARABRE s_param COMA NUMERO COMA NUMERO PARCIERRE
                    |   TRIM PARABRE s_param PARCIERRE
                    |   GET_BYTE PARABRE s_param COMA NUMERO PARCIERRE
                    |   MOD5 PARABRE s_param PARCIERRE
                    |   SET_BYTE PARABRE s_param COMA NUMERO COMA s_param PARCIERRE
                    |   SHA256 PARABRE s_param PARCIERRE
                    |   SUBSTR PARABRE s_param COMA NUMERO COMA NUMERO PARCIERRE
                    |   CONVERT PARABRE tipo_dato COMA ID dot_table PARCIERRE
                    |   ENCODE PARABRE s_param COMA s_param PARCIERRE
                    |   DECODE PARABRE s_param COMA s_param PARCIERRE '''
    if t.slice[1].type == 'LENGTH':
        t[0] = Length(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'SUBSTRING':
        op1 = Literal(t[5],Type.INT,t.slice[1].lexpos,t.slice[1].lineno)
        op2 = Literal(t[7],Type.INT,t.slice[1].lexpos,t.slice[1].lineno)
        t[0] = Substring(t[3],op1,op2,t.slice[1].lexpos,t.slice[1].lineno)
    if t.slice[1].type == 'TRIM':
        t[0] = Trim(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    if t.slice[1].type == 'GET_BYTE':
        op1 = Literal(t[5],Type.INT,t.slice[1].lexpos,t.slice[1].lineno)
        t[0] = Get_Byte(t[3],op1,t.slice[1].lexpos,t.slice[1].lineno)
    if t.slice[1].type == 'MOD5':
        t[0] = Trim(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    if t.slice[1].type == 'SET_BYTE':
        op1 = Literal(t[5],Type.INT,t.slice[1].lexpos,t.slice[1].lineno)
        t[0] = Set_Byte(t[3],op1,t[7],t.slice[1].lexpos,t.slice[1].lineno)
    if t.slice[1].type == 'SHA256':
        t[0] = Sha256(t[3],t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'SUBSTRING':
        op1 = Literal(t[5],Type.INT,t.slice[1].lexpos,t.slice[1].lineno)
        op2 = Literal(t[7],Type.INT,t.slice[1].lexpos,t.slice[1].lineno)
        t[0] = Substr(t[3],op1,op2,t.slice[1].lexpos,t.slice[1].lineno)

def p_s_param(t):
    '''s_param  :   s_param string_op s_param
                |   CADENA 
                |   NUMERO'''
    if t.slice[1].type == 'CADENA':
        t[0] = Literal(t[1],Type.STRING,t.slice[1].lexpos,t.slice[1].lineno)
    elif t.slice[1].type == 'NUMERO':
        t[0] = Literal(t[1],Type.INT,t.slice[1].lexpos,t.slice[1].lineno)
    else:
        t[0] = Stringop(t[1],t[3],t[2],t.slice[2].lexpos,t.slice[2].lineno)

def p_string_op(t):
    '''string_op    :   SIGNO_PIPE
                    |   SIGNO_DOBLE_PIPE
                    |   SIGNO_AND
                    |   SIGNO_VIRGULILLA
                    |   SIGNO_NUMERAL
                    |   SIGNO_DOBLE_MENORQUE
                    |   SIGNO_DOBLE_MAYORQUE'''
    t[0] = t[1]


def p_time_func(t):
    '''time_func    :   DATE_PART PARABRE COMILLA h_m_s COMILLA COMA INTERVAL F_HORA PARCIERRE 
                    |   NOW PARABRE PARCIERRE
                    |   EXTRACT PARABRE reserv_time  FROM TIMESTAMP  PARCIERRE
                    |   CURRENT_TIME
                    |   CURRENT_DATE'''

def p_reserv_time(t):
    '''reserv_time  :   h_m_s 
                    |   YEAR
                    |   MONTH
                    |   DAY'''

def p_h_m_s(t):
    '''h_m_s    :   HOUR
                    |   MINUTE
                    |   SECOND '''

def p_param(t):
    '''param    :   ID dot_table
                |   SIGNO_POR '''
    if t.slice[1].type == 'ID':
        if t[1] != None:
            t[0] = t[1] + '.' + t[1]
        else:
            t[0] = t[1]
    else: 
        t[0] = t[1]


def p_table_list(t):
    '''table_list   :   table_list COMA ID as_id
                    |   ID as_id'''

def p_arg_where(t):
    '''arg_where    :   WHERE exp
                    |    '''

def p_exp(t):
    '''exp  : exp SIGNO_MAS exp
            | exp SIGNO_MENOS exp 
            | exp SIGNO_POR exp 
            | exp SIGNO_DIVISION exp 
            | exp SIGNO_MODULO exp 
            | exp SIGNO_POTENCIA exp 
            | exp OR exp 
            | exp AND exp 
            | exp MENORQUE exp 
            | exp MAYORQUE exp 
            | exp MAYORIGUALQUE exp 
            | exp MENORIGUALQUE exp 
            | exp SIGNO_IGUAL exp
            | exp SIGNO_MENORQUE_MAYORQUE exp
            | exp SIGNO_NOT exp 
            | arg_pattern
            | sub_consulta
            | NOT exp
            | data
            | predicates
            | aggregates
            | functions
            | arg_case
            | arg_greatest
            | arg_least 
            | val_value'''
    
    t[0] = t[1]
    if 'Error' in t[0].execute(""):
        print(t[0])
    else:
        print(t[0].execute(""))
# values -> list_vls
    
    try:
        if t.slice[1].type == 'NOT' :
            t[0] = Logic(t[2],None,t[1], t.slice[1].lexpos,t.slice[1].lineno)

        elif t.slice[2].type == 'SIGNO_MAS' or t.slice[2].type == 'SIGNO_MENOS' or t.slice[2].type == 'SIGNO_POR' or t.slice[2].type == 'SIGNO_MODULO' or t.slice[2].type == 'SIGNO_POTENCIA':
            t[0] = Arithmetic(t[1],t[3],t[2], t.slice[2].lexpos,t.slice[2].lineno)        
        
        elif t.slice[2].type == 'MENORQUE' or t.slice[2].type == 'MAYORQUE' or t.slice[2].type == 'MAYORIGUALQUE' or t.slice[2].type == 'MENORIGUALQUE' or t.slice[2].type == 'SIGNO_IGUAL' or t.slice[2].type == 'SIGNO_MENORQUE_MAYORQUE':
            t[0] = Relational(t[1],t[3],t[2], t.slice[2].lexpos,t.slice[2].lineno)
            
        elif t.slice[2].type == 'OR' or t.slice[2].type == 'AND' :
            t[0] = Logic(t[1],t[3],t[2], t.slice[2].lexpos,t.slice[2].lineno)
            
    except IndexError:
        t[0] = t[1]


def p_arg_greatest(t):
    '''arg_greatest  : GREATEST PARABRE exp_list PARCIERRE''' 

def p_arg_least(t):
    '''arg_least  : LEAST PARABRE exp_list PARCIERRE''' 

def p_exp_list(t):
    '''exp_list  : exp_list COMA exp
                 | exp'''

def p_case(t):
    '''arg_case  : CASE arg_when arg_else END''' 

def p_arg_when(t):
    '''arg_when  : arg_when WHEN exp THEN exp
                 | WHEN exp THEN exp''' 
def p_arg_else(t):
    '''arg_else :  ELSE exp
                 | ''' # epsilon

def p_predicates(t):
    '''predicates  : data BETWEEN list_vls AND list_vls
                   | data NOT BETWEEN list_vls AND list_vls
                   | data BETWEEN SYMMETRIC list_vls AND list_vls 
                   | data NOT BETWEEN SYMMETRIC list_vls AND list_vls
                   | data IS DISTINCT FROM list_vls
                   | data IS NOT DISTINCT FROM list_vls
                   | data IS NULL 
                   | data ISNULL
                   | data NOTNULL
                   | data IS TRUE
                   | data IS NOT TRUE
                   | data IS FALSE
                   | data IS NOT FALSE
                   | data IS UNKNOWN
                   | data IS NOT UNKNOWN'''

    if t.slice[2].type == 'ISNULL':
        t[0] = Predicates(t[1],None,None, 'ISNULL', t.slice[2].lexpos,t.slice[2].lineno)
    elif t.slice[2].type == 'NOTNULL':
        t[0] = Predicates(t[1],None,None, 'NOTNULL', t.slice[2].lexpos,t.slice[2].lineno)
    
    elif t.slice[2].type == 'IS'and t.slice[3].type == 'NULL':
        t[0] = Predicates(t[1],None,None, 'IS NULL', t.slice[2].lexpos,t.slice[2].lineno)
    elif t.slice[2].type == 'IS'and t.slice[3].type == 'TRUE' :
        t[0] = Predicates(t[1],None,None, 'IS TRUE', t.slice[2].lexpos,t.slice[2].lineno)
    elif t.slice[2].type == 'IS'and t.slice[3].type == 'FALSE' :
        t[0] = Predicates(t[1],None,None, 'IS FALSE', t.slice[2].lexpos,t.slice[2].lineno)
    elif t.slice[2].type == 'IS'and t.slice[3].type == 'UNKNOWN' :
        t[0] = Predicates(t[1],None,None, 'IS UNKNOWN', t.slice[2].lexpos,t.slice[2].lineno)
    elif t.slice[2].type == 'IS' and t.slice[3].type == 'NOT' and t.slice[4].type == 'NULL':
        t[0] = Predicates(t[1],None,None, 'IS NOT TRUE', t.slice[2].lexpos,t.slice[2].lineno)
    elif t.slice[2].type == 'IS' and t.slice[3].type == 'NOT' and t.slice[4].type == 'FALSE':
        t[0] = Predicates(t[1],None,None, 'IS NOT FALSE', t.slice[2].lexpos,t.slice[2].lineno)
    elif t.slice[2].type == 'IS' and t.slice[3].type == 'NOT' and t.slice[4].type == 'FALSE':
        t[0] = Predicates(t[1],None,None, 'IS NOT UNKNOWN', t.slice[2].lexpos,t.slice[2].lineno)

    elif t.slice[2].type == 'IS' and t.slice[3].type == 'DISTINCT' :
        t[0] = Predicates(t[1],t[5],None, 'IS DISTINCT', t.slice[2].lexpos,t.slice[2].lineno)
    elif t.slice[2].type == 'BETWEEN':
        t[0] = Predicates(t[1],t[3],t[5], 'BETWEEN', t.slice[2].lexpos,t.slice[2].lineno)
    elif t.slice[2].type == 'IS' and t.slice[3].type == 'NOT' and t.slice[4].type == 'DISTINCT' :
        t[0] = Predicates(t[1],t[6],None, 'IS NOT DISTINCT', t.slice[2].lexpos,t.slice[2].lineno)
    elif t.slice[2].type == 'NOT' and t.slice[3].type == 'BETWEEN' :
        t[0] = Predicates(t[1],t[4],t[6], 'NOT BETWEEN', t.slice[2].lexpos,t.slice[2].lineno)
    elif t.slice[2].type == 'BETWEEN' and t.slice[3].type == 'SYMMETRIC':
        t[0] = Predicates(t[1],t[4],t[6], 'BETWEEN SYMMETRIC', t.slice[2].lexpos,t.slice[2].lineno)
    elif t.slice[2].type == 'NOT' and t.slice[3].type == 'BETWEEN' and t.slice[4].type == 'SYMMETRIC' :
        t[0] = Predicates(t[1],t[5],t[7], 'NOT BETWEEN SYMMETRIC', t.slice[2].lexpos,t.slice[2].lineno)

def p_data(t):
    '''data  : ID table_at''' 
    t[0] = Id(t[1],t[2], t.slice[1].lexpos,t.slice[1].lineno)

def p_table_at(t):
    '''table_at  : PUNTO ID
                 | ''' #epsilon
    if t.slice[1].type == 'PUNTO':
        t[0] = t[3]
    else :
        t[0] = None
            
def p_sub_consulta(t):
    '''sub_consulta   : PARABRE ins_select  PARCIERRE''' 
    t[0] = t[2]

def p_arg_pattern(t):
    '''arg_pattern   : data LIKE CADENA   
                     | data NOT LIKE CADENA ''' 

def p_arg_group_by(t):
    '''arg_group_by    :   GROUP BY g_list
                       |  ''' #epsilon

def p_g_list(t):
    '''g_list    : g_list COMA g_item
                 | g_item ''' 

def p_g_item(t):
    '''g_item    : ID g_refitem''' 

def p_g_refitem(t):
    '''g_refitem  : PUNTO ID
                  | ''' #epsilon

def p_arg_order_by(t):
    '''arg_order_by    :   ORDER BY o_list
                       |  ''' #epsilon

def p_o_list(t):
    '''o_list    : o_list COMA o_item
                 | o_item ''' 

def p_o_item(t):
    '''o_item    : ID o_refitem ad arg_nulls''' 

def p_o_refitem(t):
    '''o_refitem  : PUNTO ID
                  | ''' #epsilon

def p_ad(t):
    '''ad : ASC
          | DESC
          | ''' #epsilon

def p_arg_nulls(t):
    '''arg_nulls : NULLS arg_fl
                 | ''' #epsilon

def p_arg_fl(t):
    '''arg_fl : FIRST
              | LAST''' #epsilon

def p_arg_limit(t):
    '''arg_limit   :  LIMIT option_limit
                   |  ''' #epsilon

def p_option_limit(t):
    '''option_limit   : NUMERO
                      | ALL ''' 

def p_arg_offset(t):
    '''arg_offset   : OFFSET NUMERO 
                    |  ''' #epsilon


def p_ins_update(t):
    '''ins_update   : UPDATE ID SET asign_list WHERE exp PUNTO_COMA '''

def p_ins_asign_list(t):
    '''asign_list  : asign_list COMA ID SIGNO_IGUAL exp 
                   | ID SIGNO_IGUAL exp'''

def p_ins_delete(t):
    '''ins_delete   : DELETE FROM ID WHERE exp PUNTO_COMA'''

def p_error(t):
    print("Error sintáctico en '%s'" % t.value)
    print(str(t.lineno))






# metodo para realizar el analisis sintactico, que es llamado a nuestra clase principal
#"texto" -> en este parametro enviaremos el texto que deseamos analizar
def analizarSin(texto):    
    parser = yacc.yacc()
    parser.parse(texto)# el parametro cadena, es la cadena de texto que va a analizar.

