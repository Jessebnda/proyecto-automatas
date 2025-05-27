class ValidadorExpresion:
    def __init__(self):
        self.operadores_invalidos = ['**', '==', '!=', '<=', '>=']
        self.operadores_aritmeticos = ['+', '-', '*', '/']
        self.operadores_validos = self.operadores_aritmeticos + ['=']
        self.parentesis = ['(', ')']
    
    def es_identificador(self, token):
        return token[0].isalpha() and all(c.isalnum() for c in token[1:])
    
    def es_numero(self, token):
        token_sin_signo = token[1:] if token[0] in '+-' else token
        return token_sin_signo.isdigit()
    
    def es_operador(self, token):
        return token in self.operadores_validos
    
    def es_parentesis(self, token):
        return token in self.parentesis
    
    def tokenizar(self, entrada):
        tokens = []
        i = 0
        
        operadores_dobles = {
            '**': '**', '==': '==', '!=': '!=', 
            '<=': '<=', '>=': '>='
        }
        
        while i < len(entrada):
            if entrada[i].isspace():
                i += 1
                continue
            
            # Verificar operadores dobles
            if i + 1 < len(entrada):
                doble = entrada[i:i+2]
                if doble in operadores_dobles:
                    tokens.append(doble)
                    i += 2
                    continue
            
            # Manejar números con signo
            if self._es_numero_con_signo(entrada, i, tokens):
                numero, nueva_i = self._extraer_numero_con_signo(entrada, i)
                tokens.append(numero)
                i = nueva_i
                continue
            
            # Manejar números
            if entrada[i].isdigit():
                numero, nueva_i = self._extraer_numero(entrada, i)
                tokens.append(numero)
                i = nueva_i
                continue
            
            # Manejar identificadores
            if entrada[i].isalpha() or entrada[i] == '_':
                identificador, nueva_i = self._extraer_identificador(entrada, i)
                tokens.append(identificador)
                i = nueva_i
                continue
            
            # Operadores y paréntesis simples
            if entrada[i] in "=()+-*/":
                tokens.append(entrada[i])
            else:
                tokens.append(entrada[i])
            
            i += 1
        
        return tokens
    
    def _es_numero_con_signo(self, entrada, i, tokens):
        if entrada[i] not in '+-':
            return False
        if i + 1 >= len(entrada) or not entrada[i + 1].isdigit():
            return False
        
        # Verificar contexto para determinar si es signo o operador
        if i == 0:
            return True
        if entrada[i-1] in "=+-*/(" or (entrada[i-1].isspace() and tokens and tokens[-1] in "=+-*/("):
            return True
        return False
    
    def _extraer_numero_con_signo(self, entrada, i):
        signo = entrada[i]
        j = i + 1
        while j < len(entrada) and entrada[j].isdigit():
            j += 1
        return signo + entrada[i + 1:j], j
    
    def _extraer_numero(self, entrada, i):
        j = i
        while j < len(entrada) and entrada[j].isdigit():
            j += 1
        return entrada[i:j], j
    
    def _extraer_identificador(self, entrada, i):
        j = i
        while j < len(entrada) and (entrada[j].isalnum() or entrada[j] == '_'):
            j += 1
        return entrada[i:j], j
    
    def clasificar_tokens(self, tokens):
        lexico = []
        
        for token in tokens:
            if token in self.operadores_invalidos:
                raise ValueError(f"Operador inválido: {token}")
            elif self.es_identificador(token):
                lexico.append('id')
            elif self.es_numero(token):
                lexico.append('num')
            elif self.es_operador(token):
                lexico.append(token)
            elif self.es_parentesis(token):
                lexico.append(token)
            else:
                raise ValueError(f"Caracter inválido: {token}")
        
        return lexico
    
    def validar_parentesis(self, tokens):
        nivel = 0
        for token in tokens:
            if token == '(':
                nivel += 1
            elif token == ')':
                nivel -= 1
                if nivel < 0:
                    return False
        return nivel == 0
    
    def validar_estructura_basica(self, lexico):
        validaciones = [
            (len(lexico) < 3, "Orden incorrecto de tokens o expresión incompleta."),
            (lexico[0] != 'id' or lexico[1] != '=', "Orden incorrecto de tokens."),
            (len(lexico) > 2 and lexico[2] in ['*', '/'], 
             "La expresión no puede comenzar con un operador multiplicativo."),
            (lexico[-1] in self.operadores_aritmeticos, 
             "La expresión no puede terminar con un operador.")
        ]
        
        for condicion, mensaje in validaciones:
            if condicion:
                raise ValueError(mensaje)
    
    def validar_secuencias(self, lexico):
        reglas_adyacencia = {
            # (token_anterior, token_actual): mensaje_error
            ('num', '('): "No puede ir un '(' después de un número.",
            (')', 'num'): "No puede ir un número después de ')'.",
            ('num', 'num'): "Se requiere un operador entre números.",
            ('id', 'id'): "Se requiere un operador entre identificadores.",
            ('id', 'num'): "Se requiere un operador entre identificador y número.",
            ('num', 'id'): "Se requiere un operador entre número e identificador.",
        }
        
        # Validar operadores consecutivos
        for i in range(1, len(lexico)):
            anterior, actual = lexico[i-1], lexico[i]
            
            # Operadores aritméticos consecutivos
            if anterior in self.operadores_aritmeticos and actual in self.operadores_aritmeticos:
                raise ValueError("No se puede tener dos operadores aritméticos juntos.")
            
            # Operador después de '='
            if anterior == '=' and actual in ['+', '*', '/']:
                raise ValueError(f"Un '{actual}' debe estar después de un número o id.")
            
            # Operador antes de ')'
            if actual == ')' and anterior in self.operadores_aritmeticos:
                raise ValueError("No puede haber un operador justo antes de un paréntesis de cierre.")
            
            # Paréntesis después de identificador (excepto después de '=')
            if actual == '(' and anterior == 'id' and i > 1:
                raise ValueError("Se requiere un operador entre un identificador y un paréntesis.")
            
            # Verificar reglas de adyacencia
            clave = (anterior, actual)
            if clave in reglas_adyacencia:
                raise ValueError(reglas_adyacencia[clave])
    
    def validar_doble_negativo(self, tokens):
        for i in range(len(tokens) - 1):
            if tokens[i] == '-' and tokens[i + 1].startswith('-'):
                raise ValueError("No se permite doble signo negativo.")
    
    def validar_expresion(self, entrada):
        try:
            # Tokenizar
            tokens = self.tokenizar(entrada)
            
            # Clasificar tokens
            lexico = self.clasificar_tokens(tokens)
            print("Tokens léxicos:", lexico)
            
            # Validaciones
            if not self.validar_parentesis(tokens):
                raise ValueError("Hay un error en la anidación de paréntesis.")
            
            self.validar_estructura_basica(lexico)
            self.validar_secuencias(lexico)
            self.validar_doble_negativo(tokens)
            
            # Si llegamos aquí, la expresión es válida
            print(' '.join(lexico))
            print("Expresión válida")
            return True
            
        except ValueError as e:
            print(str(e))
            print("Vuelva a empezar")
            return False

# Uso del validador
if __name__ == "__main__":
    validador = ValidadorExpresion()
    entrada = input("Escribe una expresión: ")
    validador.validar_expresion(entrada)
