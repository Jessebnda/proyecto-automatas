def es_identificador(token):
    if not token[0].isalpha():
        return False
    for c in token[1:]:
        if not c.isalnum():
            return False
    return True

def es_numero(token):
    if token[0] in '+-':
        token = token[1:]
    return token.isdigit()

def es_operador(token):
    return token in ['+', '-', '*', '/', '=']

def es_parentesis(token):
    return token in ['(', ')']

operadores_invalidos = ['**', '==', '!=', '<=', '>=']

entrada = input("Escribe una expresión: ")
tokens = []
i = 0
while i < len(entrada):
    if entrada[i].isspace():
        i += 1
        continue

    c = entrada[i]

    if c == '*' and i + 1 < len(entrada) and entrada[i + 1] == '*':
        tokens.append('**')
        i += 2
        continue
    if c == '=' and i + 1 < len(entrada) and entrada[i + 1] == '=':
        tokens.append('==')
        i += 2
        continue
    if c == '!' and i + 1 < len(entrada) and entrada[i + 1] == '=':
        tokens.append('!=')
        i += 2
        continue
    if c == '<' and i + 1 < len(entrada) and entrada[i + 1] == '=':
        tokens.append('<=')
        i += 2
        continue
    if c == '>' and i + 1 < len(entrada) and entrada[i + 1] == '=':
        tokens.append('>=')
        i += 2
        continue

    if (c == '+' or c == '-') and i + 1 < len(entrada) and entrada[i + 1].isdigit():
        if i == 0 or entrada[i-1] in "=+-*/(" or entrada[i-1].isspace() and tokens[-1] in "=+-*/(":
            signo = c
            j = i + 1
            while j < len(entrada) and entrada[j].isdigit():
                j += 1
            tokens.append(signo + entrada[i + 1:j])
            i = j
            continue

    if c.isdigit():
        j = i
        while j < len(entrada) and entrada[j].isdigit():
            j += 1
        tokens.append(entrada[i:j])
        i = j
        continue

    if c.isalpha() or c == '_':
        j = i
        while j < len(entrada) and (entrada[j].isalnum() or entrada[j] == '_'):
            j += 1
        tokens.append(entrada[i:j])
        i = j
        continue

    if c in "=()+-*/":
        tokens.append(c)
        i += 1
        continue

    tokens.append(c)
    i += 1

lexico = []

for t in tokens:
    if t in operadores_invalidos:
        print("Operador inválido:", t)
        lexico = ['Vuelva a empezar']
        break
    elif es_identificador(t):
        lexico.append('id')
    elif es_numero(t):
        lexico.append('num')
    elif es_operador(t):
        lexico.append(t)
    elif es_parentesis(t):
        lexico.append(t)
    else:
        print("Caracter inválido:", t)
        lexico = ['Vuelva a empezar']
        break

if 'Vuelva a empezar' in lexico:
    print("Vuelva a empezar")
    exit()

def validar_parentesis(tokens):
    nivel = 0
    for token in tokens:
        if token == '(':
            nivel += 1
        elif token == ')':
            nivel -= 1
        if nivel < 0:
            return False
    return nivel == 0

if not validar_parentesis(tokens):
    print("Hay un error en la anidación de paréntesis.")
    print("Vuelva a empezar")
    exit()

if len(lexico) < 3:
    print("Orden incorrecto de tokens o expresión incompleta.")
    print("Vuelva a empezar")
    exit()
    
if lexico[0] != 'id' or lexico[1] != '=':
    print("Orden incorrecto de tokens.")
    print("Vuelva a empezar")
    exit()

for i in range(1, len(lexico)):
    actual = lexico[i]
    anterior = lexico[i - 1]

    if actual in ['+', '-', '*', '/'] and anterior in ['+', '-', '*', '/']:
        print("No se puede tener dos operadores aritméticos juntos.")
        print("Vuelva a empezar")
        exit()

    if actual == '(' and anterior == 'num':
        print("No puede ir un '(' después de un número.")
        print("Vuelva a empezar")
        exit()

    if actual == 'num' and anterior == ')':
        print("No puede ir un número después de ')'.")
        print("Vuelva a empezar")
        exit()

    if anterior == '=' and actual in ['+', '*', '/']:
        print(f"Un '{actual}' debe estar después de un número o id.")
        print("Vuelva a empezar")
        exit()

if len(lexico) > 2 and lexico[2] in ['*', '/']:
    print("La expresión no puede comenzar con un operador multiplicativo.")
    print("Vuelva a empezar")
    exit()

for i in range(1, len(lexico)):
    if lexico[i] == ')' and lexico[i-1] in ['+', '-', '*', '/']:
        print("No puede haber un operador justo antes de un paréntesis de cierre.")
        print("Vuelva a empezar")
        exit()

for i in range(2, len(lexico)):
    actual = lexico[i]
    anterior = lexico[i - 1]
    
    if (actual == 'num' and anterior == 'num') or \
       (actual == 'id' and anterior == 'id') or \
       (actual == 'id' and anterior == 'num') or \
       (actual == 'num' and anterior == 'id'):
        print("Se requiere un operador entre números o identificadores.")
        print("Vuelva a empezar")
        exit()

if lexico[-1] in ['+', '-', '*', '/']:
    print("La expresión no puede terminar con un operador.")
    print("Vuelva a empezar")
    exit()

for i in range(1, len(lexico)):
    actual = lexico[i]
    anterior = lexico[i - 1]
    
    if actual == '(' and anterior == 'id' and i > 1:
        print("Se requiere un operador entre un identificador y un paréntesis.")
        print("Vuelva a empezar")
        exit()

for i in range(len(tokens) - 1):
    if tokens[i] == '-' and tokens[i + 1].startswith('-'):
        print("No se permite doble signo negativo.")
        print("Vuelva a empezar")
        exit()

for elemento in lexico:
    print(elemento, end=' ')
print("\nExpresión válida")
