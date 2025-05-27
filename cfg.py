class AnalizadorLexico:
    """Clase responsable del análisis léxico (tokenización)"""
    
    def __init__(self):
        self.operadores_dobles = ['**', '==', '!=', '<=', '>=']
        self.operadores_simples = ['+', '-', '*', '/', '=']
        self.parentesis = ['(', ')']
    
    def _es_letra(self, c):
        return ('a' <= c <= 'z') or ('A' <= c <= 'Z')
    
    def _es_digito(self, c):
        return '0' <= c <= '9'
    
    def _es_alfanumerico(self, c):
        return self._es_letra(c) or self._es_digito(c)
    
    def _es_espacio(self, c):
        return c in ' \t\n'
    
    def tokenizar(self, entrada):
        tokens = []
        i = 0
        
        while i < len(entrada):
            if self._es_espacio(entrada[i]):
                i += 1
                continue
            
            # Verificar operadores dobles
            if i + 1 < len(entrada):
                doble = entrada[i:i+2]
                if doble in self.operadores_dobles:
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
            if self._es_digito(entrada[i]):
                numero, nueva_i = self._extraer_numero(entrada, i)
                tokens.append(numero)
                i = nueva_i
                continue
            
            # Manejar identificadores
            if self._es_letra(entrada[i]) or entrada[i] == '_':
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
        if i + 1 >= len(entrada) or not self._es_digito(entrada[i + 1]):
            return False
        
        # Verificar contexto para determinar si es signo o operador
        if i == 0:
            return True
        if entrada[i-1] in "=+-*/(" or (self._es_espacio(entrada[i-1]) and tokens and tokens[-1] in "=+-*/("):
            return True
        return False
    
    def _extraer_numero_con_signo(self, entrada, i):
        signo = entrada[i]
        j = i + 1
        while j < len(entrada) and self._es_digito(entrada[j]):
            j += 1
        return signo + entrada[i + 1:j], j
    
    def _extraer_numero(self, entrada, i):
        j = i
        while j < len(entrada) and self._es_digito(entrada[j]):
            j += 1
        return entrada[i:j], j
    
    def _extraer_identificador(self, entrada, i):
        j = i
        while j < len(entrada) and (self._es_alfanumerico(entrada[j]) or entrada[j] == '_'):
            j += 1
        return entrada[i:j], j


class ClasificadorTokens:
    """Clase responsable de clasificar tokens en categorías léxicas"""
    
    def __init__(self):
        self.operadores_invalidos = ['**', '==', '!=', '<=', '>=']
        self.operadores_aritmeticos = ['+', '-', '*', '/']
        self.operadores_validos = self.operadores_aritmeticos + ['=']
        self.parentesis = ['(', ')']
    
    def _es_letra(self, c):
        return ('a' <= c <= 'z') or ('A' <= c <= 'Z')
    
    def _es_digito(self, c):
        return '0' <= c <= '9'
    
    def _es_alfanumerico(self, c):
        return self._es_letra(c) or self._es_digito(c)
    
    def es_identificador(self, token):
        if not token:
            return False
        # Primer carácter debe ser letra
        if not self._es_letra(token[0]):
            return False
        # Resto de caracteres deben ser letras o números
        for c in token[1:]:
            if not self._es_alfanumerico(c):
                return False
        return True
    
    def es_numero(self, token):
        if not token:
            return False
        token_sin_signo = token[1:] if token[0] in '+-' else token
        if not token_sin_signo:
            return False
        # Todos los caracteres deben ser dígitos
        for c in token_sin_signo:
            if not self._es_digito(c):
                return False
        return True
    
    def es_operador(self, token):
        return token in self.operadores_validos
    
    def es_parentesis(self, token):
        return token in self.parentesis
    
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


class ValidadorSintactico:
    """Clase responsable de las validaciones sintácticas"""
    
    def __init__(self):
        self.operadores_aritmeticos = ['+', '-', '*', '/']
        self.reglas_adyacencia = {
            ('num', '('): "No puede ir un '(' después de un número.",
            (')', 'num'): "No puede ir un número después de ')'.",
            ('num', 'num'): "Se requiere un operador entre números.",
            ('id', 'id'): "Se requiere un operador entre identificadores.",
            ('id', 'num'): "Se requiere un operador entre identificador y número.",
            ('num', 'id'): "Se requiere un operador entre número e identificador.",
        }
    
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
            if clave in self.reglas_adyacencia:
                raise ValueError(self.reglas_adyacencia[clave])
    
    def validar_doble_negativo(self, tokens):
        for i in range(len(tokens) - 1):
            if tokens[i] == '-' and len(tokens[i + 1]) > 0 and tokens[i + 1][0] == '-':
                raise ValueError("No se permite doble signo negativo.")


class ValidadorExpresion:
    """Clase principal que coordina el análisis léxico y sintáctico"""
    
    def __init__(self):
        self.analizador_lexico = AnalizadorLexico()
        self.clasificador = ClasificadorTokens()
        self.validador_sintactico = ValidadorSintactico()
    
    def validar_expresion(self, entrada):
        try:
            # Análisis léxico
            tokens = self.analizador_lexico.tokenizar(entrada)
            
            # Clasificación de tokens
            lexico = self.clasificador.clasificar_tokens(tokens)
            print("Tokens léxicos:", lexico)
            
            # Validaciones sintácticas
            if not self.validador_sintactico.validar_parentesis(tokens):
                raise ValueError("Hay un error en la anidación de paréntesis.")
            
            self.validador_sintactico.validar_estructura_basica(lexico)
            self.validador_sintactico.validar_secuencias(lexico)
            self.validador_sintactico.validar_doble_negativo(tokens)
            
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
