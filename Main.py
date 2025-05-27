from Sintat import SintaxisValidador
from Lex import Lexico

if __name__ == "__main__":
    lex = Lexico()
    lexico = lex.analizar()
    tokens = lex.get_tokens()
    validador = SintaxisValidador(tokens, lexico)
    validador.validar()
