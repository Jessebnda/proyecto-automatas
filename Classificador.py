class ClasificadorTokens:
    """Clase responsable SOLO de clasificar tokens ya extraídos"""
    def __init__(self, utils, config):
        self.utils = utils
        self.config = config

    def es_identificador(self, token):
        if not token:
            return False
        if not self.utils.es_letra(token[0]):
            return False
        for c in token[1:]:
            if not self.utils.es_alfanumerico(c):
                return False
        return True
    
    def es_numero(self, token):
        if not token:
            return False
        token_sin_signo = token[1:] if token[0] in '+-' else token
        if not token_sin_signo:
            return False
        for c in token_sin_signo:
            if not self.utils.es_digito(c):
                return False
        return True
    
    def es_operador(self, token):
        return token in self.config.OPERADORES_VALIDOS
    
    def es_parentesis(self, token):
        return token in self.config.PARENTESIS
    
    def clasificar_tokens(self, tokens):
        lexico = []
        
        for token in tokens:
            if token in self.config.OPERADORES_INVALIDOS:
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


