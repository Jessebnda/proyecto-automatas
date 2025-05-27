class UtilsCaracteres:
    """Clase con utilidades para análisis de caracteres - Evita duplicación"""
    
    @staticmethod
    def es_letra(c):
        return ('a' <= c <= 'z') or ('A' <= c <= 'Z')
    
    @staticmethod
    def es_digito(c):
        return '0' <= c <= '9'
    
    @staticmethod
    def es_alfanumerico(c):
        return UtilsCaracteres.es_letra(c) or UtilsCaracteres.es_digito(c)
    
    @staticmethod
    def es_espacio(c):
        return c in ' \t\n'


class ConfigOperadores:
    """Configuración centralizada de operadores y símbolos"""
    
    OPERADORES_DOBLES = ['**', '==', '!=', '<=', '>=']
    OPERADORES_SIMPLES = ['+', '-', '*', '/', '=']
    OPERADORES_ARITMETICOS = ['+', '-', '*', '/']
    OPERADORES_VALIDOS = OPERADORES_ARITMETICOS + ['=']
    OPERADORES_INVALIDOS = OPERADORES_DOBLES
    PARENTESIS = ['(', ')']


class AnalizadorLexico:
    """Clase responsable SOLO de tokenizar (dividir en tokens)"""
    
    def __init__(self):
        pass
    
    def tokenizar(self, entrada):
        tokens = []
        i = 0
        
        while i < len(entrada):
            if UtilsCaracteres.es_espacio(entrada[i]):
                i += 1
                continue
            
            # Verificar operadores dobles
            if i + 1 < len(entrada):
                doble = entrada[i:i+2]
                if doble in ConfigOperadores.OPERADORES_DOBLES:
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
            if UtilsCaracteres.es_digito(entrada[i]):
                numero, nueva_i = self._extraer_numero(entrada, i)
                tokens.append(numero)
                i = nueva_i
                continue
            
            # Manejar identificadores
            if UtilsCaracteres.es_letra(entrada[i]) or entrada[i] == '_':
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
        if i + 1 >= len(entrada) or not UtilsCaracteres.es_digito(entrada[i + 1]):
            return False
        
        # Verificar contexto para determinar si es signo o operador
        if i == 0:
            return True
        if entrada[i-1] in "=+-*/(" or (UtilsCaracteres.es_espacio(entrada[i-1]) and tokens and tokens[-1] in "=+-*/("):
            return True
        return False
    
    def _extraer_numero_con_signo(self, entrada, i):
        signo = entrada[i]
        j = i + 1
        while j < len(entrada) and UtilsCaracteres.es_digito(entrada[j]):
            j += 1
        return signo + entrada[i + 1:j], j
    
    def _extraer_numero(self, entrada, i):
        j = i
        while j < len(entrada) and UtilsCaracteres.es_digito(entrada[j]):
            j += 1
        return entrada[i:j], j
    
    def _extraer_identificador(self, entrada, i):
        j = i
        while j < len(entrada) and (UtilsCaracteres.es_alfanumerico(entrada[j]) or entrada[j] == '_'):
            j += 1
        return entrada[i:j], j


class ClasificadorTokens:
    """Clase responsable SOLO de clasificar tokens ya extraídos"""
    
    def es_identificador(self, token):
        if not token:
            return False
        if not UtilsCaracteres.es_letra(token[0]):
            return False
        for c in token[1:]:
            if not UtilsCaracteres.es_alfanumerico(c):
                return False
        return True
    
    def es_numero(self, token):
        if not token:
            return False
        token_sin_signo = token[1:] if token[0] in '+-' else token
        if not token_sin_signo:
            return False
        for c in token_sin_signo:
            if not UtilsCaracteres.es_digito(c):
                return False
        return True
    
    def es_operador(self, token):
        return token in ConfigOperadores.OPERADORES_VALIDOS
    
    def es_parentesis(self, token):
        return token in ConfigOperadores.PARENTESIS
    
    def clasificar_tokens(self, tokens):
        lexico = []
        
        for token in tokens:
            if token in ConfigOperadores.OPERADORES_INVALIDOS:
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
            (lexico[-1] in ConfigOperadores.OPERADORES_ARITMETICOS, 
             "La expresión no puede terminar con un operador.")
        ]
        
        for condicion, mensaje in validaciones:
            if condicion:
                raise ValueError(mensaje)
    
    def validar_secuencias(self, lexico):
        for i in range(1, len(lexico)):
            anterior, actual = lexico[i-1], lexico[i]
            
            # Operadores aritméticos consecutivos
            if anterior in ConfigOperadores.OPERADORES_ARITMETICOS and actual in ConfigOperadores.OPERADORES_ARITMETICOS:
                raise ValueError("No se puede tener dos operadores aritméticos juntos.")
            
            # Operador después de '='
            if anterior == '=' and actual in ['+', '*', '/']:
                raise ValueError(f"Un '{actual}' debe estar después de un número o id.")
            
            # Operador antes de ')'
            if actual == ')' and anterior in ConfigOperadores.OPERADORES_ARITMETICOS:
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
            # Análisis léxico (tokenización)
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
