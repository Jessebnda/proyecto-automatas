class ConfigOperadores:
    """Configuración centralizada de operadores y símbolos"""
    
    OPERADORES_DOBLES = ['**', '==', '!=', '<=', '>=']
    OPERADORES_SIMPLES = ['+', '-', '*', '/', '=']
    OPERADORES_ARITMETICOS = ['+', '-', '*', '/']
    OPERADORES_VALIDOS = OPERADORES_ARITMETICOS + ['=']
    OPERADORES_INVALIDOS = OPERADORES_DOBLES
    PARENTESIS = ['(', ')']
