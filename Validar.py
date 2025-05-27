class ValidadorExpresion:
    """Clase principal que coordina el análisis léxico y sintáctico"""
    
    def __init__(self, lex, clasi, sintat):
        self.analizador_lexico = lex
        self.clasificador = clasi
        self.validador_sintactico = sintat
    
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

