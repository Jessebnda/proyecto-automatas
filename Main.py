from Validar import ValidadorExpresion
from Lex import AnalizadorLexico
from Utils import UtilsCaracteres
from Classificador import ClasificadorTokens
from Sintat import ValidadorSintactico
from Config import ConfigOperadores

if __name__ == "__main__":
    conf = ConfigOperadores()
    util = UtilsCaracteres()
    lex = AnalizadorLexico(util, conf)
    tok = ClasificadorTokens(util, conf)
    sin = ValidadorSintactico(conf)
    validador = ValidadorExpresion(lex, tok, sin)
    entrada = input("Escribe una expresión: ")
    validador.validar_expresion(entrada)
