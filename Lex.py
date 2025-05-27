class Lexico:
    def __init__(self):
        self.operadores_invalidos = ['**', '==', '!=', '<=', '>=']
        self.tokens = []

    def get_tokens(self):
        return self.tokens

    def es_identificador(self, token):
        if not token[0].isalpha():
            return False
        for c in token[1:]:
            if not c.isalnum():
                return False
        return True

    def es_numero(self, token):
        if token[0] in '+-':
            token = token[1:]
        return token.isdigit()

    def es_operador(self, token):
        return token in ['+', '-', '*', '/', '=']

    def es_parentesis(self, token):
        return token in ['(', ')']

    def analizar(self):
        entrada = input("Escribe una expresión: ")
        i = 0
        while i < len(entrada):
            if entrada[i].isspace():
                i += 1
                continue

            c = entrada[i]

            if c == '*' and i + 1 < len(entrada) and entrada[i + 1] == '*':
                self.tokens.append('**')
                i += 2
                continue
            if c == '=' and i + 1 < len(entrada) and entrada[i + 1] == '=':
                self.tokens.append('==')
                i += 2
                continue
            if c == '!' and i + 1 < len(entrada) and entrada[i + 1] == '=':
                self.tokens.append('!=')
                i += 2
                continue
            if c == '<' and i + 1 < len(entrada) and entrada[i + 1] == '=':
                self.tokens.append('<=') 
                i += 2
                continue
            if c == '>' and i + 1 < len(entrada) and entrada[i + 1] == '=':
                self.tokens.append('>=')
                i += 2
                continue

            if (c == '+' or c == '-') and i + 1 < len(entrada) and entrada[i + 1].isdigit():
                if i == 0 or entrada[i-1] in "=+-*/(" or entrada[i-1].isspace() and self.tokens[-1] in "=+-*/(":
                    signo = c
                    j = i + 1
                    while j < len(entrada) and entrada[j].isdigit():
                        j += 1
                    self.tokens.append(signo + entrada[i + 1:j])
                    i = j
                    continue

            if c.isdigit():
                j = i
                while j < len(entrada) and entrada[j].isdigit():
                    j += 1
                self.tokens.append(entrada[i:j])
                i = j
                continue

            if c.isalpha() or c == '_':
                j = i
                while j < len(entrada) and (entrada[j].isalnum() or entrada[j] == '_'):
                    j += 1
                self.tokens.append(entrada[i:j])
                i = j
                continue

            if c in "=()+-*/":
                self.tokens.append(c)
                i += 1
                continue

            self.tokens.append(c)
            i += 1

        lexico = []

        for t in self.tokens:
            if t in self.operadores_invalidos:
                print("Operador inválido:", t)
                lexico = ['Vuelva a empezar']
                break
            elif self.es_identificador(t):
                lexico.append('id')
            elif self.es_numero(t):
                lexico.append('num')
            elif self.es_operador(t):
                lexico.append(t)
            elif self.es_parentesis(t):
                lexico.append(t)
            else:
                print("Caracter inválido:", t)
                lexico = ['Vuelva a empezar']
                break

        if 'Vuelva a empezar' in lexico:
            print("Vuelva a empezar")
            exit()
        else:
            print(lexico)



if __name__ == "__main__":
    lex = Lexico()
    lex.analizar()
