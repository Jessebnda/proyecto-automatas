import re

# AFDs para cada tipo de token
def es_identificador(token):
    if not token[0].isalpha():
        return False
    for c in token[1:]:
        if not c.isalnum():
            return False
    return True

# para los números
def es_numero(token):
    if token[0] in '+-':
        token = token[1:]
    return token.isdigit()

# para los operadores
def es_operador(token):
    return token in ['+', '-', '*', '/', '=']

# parentesis
def es_parentesis(token):
    return token in ['(', ')']

# Operadores inválidos
operadores_invalidos = ['**', '==', '!=', '<=', '>=']

# Ingresar la expresión
entrada = input("Escribe una expresión: ")
tokens = re.findall(r'\*\*|==|!=|<=|>=|[+\-]?\d+|\w+|[=()+\-*/]', entrada)

lexico = []

# hace el análisis léxico, revisa letra por letra la expresión que se ingresó
for t in tokens:
    if t in operadores_invalidos:
        print("Operador inválido:", t)
        lexico = ['Vuelva a empezar']
        break
    elif es_identificador(t): #  ej. si t es 'x' o 'y' checa que pertenece a la lista de id y manda la palabra 'id'
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

# si metió algo inválido lo saca del programa
if 'Vuelva a empezar' in lexico:
    print("Vuelva a empezar")
    exit()

# checa que si se abre un parentesis se cierre
if lexico.count('(') != lexico.count(')'):
    print("Hay un desbalance de paréntesis.")
    print("Vuelva a empezar")
    exit()

# que empiece con 'id = ...'
if len(lexico) < 3 or lexico[0] != 'id' or lexico[1] != '=':
    print("Orden incorrecto de tokens")
    print("Vuelva a empezar")
    exit()

for i in range(1, len(lexico)):
    actual = lexico[i]
    anterior = lexico[i - 1]

    # que no haya dos operadores juntos
    if actual in ['+', '-', '*', '/'] and anterior in ['+', '-', '*', '/']:
        print("No se puede tener dos operadores lógicos juntos.")
        print("Vuelva a empezar")
        exit()

    # que haya un operador antes del parentesis (a menos que sea 'id = (...)')
    if actual == '(' and anterior == 'num':
        print("No puede ir un '(' después de un número.")
        print("Vuelva a empezar")
        exit()

    # mismo pedo del de arriba pero que no sea ') 5'
    if actual == 'num' and anterior == ')':
        print("No puede ir un número después de ')'.")
        print("Vuelva a empezar")
        exit()

    # que no empiece con +
    if actual == '+' and anterior == '=':
        print("Un '+' debe estar después de un número o id.")
        print("Vuelva a empezar")
        exit()

# imprime el token y te dice que es válido
for elemento in lexico:
    print(elemento, end=' ')
print("\nExpresión válida")
