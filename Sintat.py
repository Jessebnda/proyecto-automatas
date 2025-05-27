class ValidadorSintactico:
    """Clase responsable de las validaciones sintácticas"""
    
    def __init__(self, config):
        self.reglas_adyacencia = {
            ('num', '('): "No puede ir un '(' después de un número.",
            (')', 'num'): "No puede ir un número después de ')'.",
            ('num', 'num'): "Se requiere un operador entre números.",
            ('id', 'id'): "Se requiere un operador entre identificadores.",
            ('id', 'num'): "Se requiere un operador entre identificador y número.",
            ('num', 'id'): "Se requiere un operador entre número e identificador.",
        }
        self.config = config

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
            (lexico[-1] in self.config.OPERADORES_ARITMETICOS, 
             "La expresión no puede terminar con un operador.")
        ]
        
        for condicion, mensaje in validaciones:
            if condicion:
                raise ValueError(mensaje)
    
    def validar_secuencias(self, lexico):
        for i in range(1, len(lexico)):
            anterior, actual = lexico[i-1], lexico[i]
            
            # Operadores aritméticos consecutivos
            if anterior in self.config.OPERADORES_ARITMETICOS and actual in self.config.OPERADORES_ARITMETICOS:
                raise ValueError("No se puede tener dos operadores aritméticos juntos.")
            
            # Operador después de '='
            if anterior == '=' and actual in ['+', '*', '/']:
                raise ValueError(f"Un '{actual}' debe estar después de un número o id.")
            
            # Operador antes de ')'
            if actual == ')' and anterior in self.config.OPERADORES_ARITMETICOS:
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


