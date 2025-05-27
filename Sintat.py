class SintaxisValidador:
    def __init__(self, tokens, lexico):
        self.tokens = tokens
        self.lexico = lexico

    def validar_parentesis(self):
        nivel = 0
        for token in self.tokens:
            if token == '(':
                nivel += 1
            elif token == ')':
                nivel -= 1
            if nivel < 0:
                return False
        return nivel == 0

    def validar(self):
        if not self.validar_parentesis():
            print("Hay un error en la anidación de paréntesis.")
            print("Vuelva a empezar")
            exit()

        if len(self.lexico) < 3:
            print("Orden incorrecto de tokens o expresión incompleta.")
            print("Vuelva a empezar")
            exit()
        
        if self.lexico[0] != 'id' or self.lexico[1] != '=':
            print("Orden incorrecto de tokens.")
            print("Vuelva a empezar")
            exit()

        for i in range(1, len(self.lexico)):
            actual = self.lexico[i]
            anterior = self.lexico[i - 1]

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

        if len(self.lexico) > 2 and self.lexico[2] in ['*', '/']:
            print("La expresión no puede comenzar con un operador multiplicativo.")
            print("Vuelva a empezar")
            exit()

        for i in range(1, len(self.lexico)):
            if self.lexico[i] == ')' and self.lexico[i-1] in ['+', '-', '*', '/']:
                print("No puede haber un operador justo antes de un paréntesis de cierre.")
                print("Vuelva a empezar")
                exit()

        for i in range(2, len(self.lexico)):
            actual = self.lexico[i]
            anterior = self.lexico[i - 1]
            
            if (actual == 'num' and anterior == 'num') or \
               (actual == 'id' and anterior == 'id') or \
               (actual == 'id' and anterior == 'num') or \
               (actual == 'num' and anterior == 'id'):
                print("Se requiere un operador entre números o identificadores.")
                print("Vuelva a empezar")
                exit()

        if self.lexico[-1] in ['+', '-', '*', '/']:
            print("La expresión no puede terminar con un operador.")
            print("Vuelva a empezar")
            exit()

        for i in range(1, len(self.lexico)):
            actual = self.lexico[i]
            anterior = self.lexico[i - 1]
            
            if actual == '(' and anterior == 'id' and i > 1:
                print("Se requiere un operador entre un identificador y un paréntesis.")
                print("Vuelva a empezar")
                exit()

        for i in range(len(self.tokens) - 1):
            if self.tokens[i] == '-' and self.tokens[i + 1].startswith('-'):
                print("No se permite doble signo negativo.")
                print("Vuelva a empezar")
                exit()

        for elemento in self.lexico:
            print(elemento, end=' ')
        print("\nExpresión válida")

# tokens = [...]
# lexico = [...]
# validador = SintaxisValidador(tokens, lexico)
# validador.validar()
