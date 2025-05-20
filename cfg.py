import re

# listas de todo lo que se puede aceptar
id = ['x', 'y'] 
num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
oper = ['-', '+', '/', '*']
par = ['(', ')', '=']
# estos los rechaza
operadores_invalidos = ['**', '==', '!=', '<=', '>=']
lexico = []

entrada = input("Escribe una expresión: ")
tokens = re.findall(r'\*\*|==|!=|<=|>=|[=()+\-*/]|\w+', entrada) #filtra de una operadores invalidos

# hace el análisis léxico, revisa letra por letra la expresión que se ingresó
for t in tokens:
    if t in operadores_invalidos:
        print("Operador inválido:", t)
        lexico = ['Vuelva a empezar']
        break
    elif t in id: # ej. si t es 'x' o 'y' checa que pertenece a la lista de id y manda la palabra 'id'
        lexico.append('id')
    elif t in num:
        lexico.append('num')
    elif t in oper:
        lexico.append(t)
    elif t in par:
        lexico.append(t)
    else:
        # si metió algo inválido lo saca del programa
        print("Caracter inválido:", t)
        lexico = ['Vuelva a empezar']
        break

# si metió algo inválido lo saca del programa
if 'Vuelva a empezar' in lexico:
    print("Vuelva a empezar")
    exit()

# checa que si se abre un parentesis se cierre
abre = lexico.count('(')
cierra = lexico.count(')')

# checa que si se abre un parentesis se cierre
if abre != cierra:
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
    if actual in oper and anterior in oper:
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
        print("Un '+' debe estar después de un número o id. ")
        print("Vuelva a empezar")
        exit()

for elemento in lexico:
    print(elemento, end=' ')
