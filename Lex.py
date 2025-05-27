
class AnalizadorLexico:
    """Clase responsable SOLO de tokenizar (dividir en tokens)"""
    
    def __init__(self, utils, config):
        self.utils = utils
        self.config = config
        pass
    
    def tokenizar(self, entrada):
        tokens = []
        i = 0
        
        while i < len(entrada):
            if self.utils.es_espacio(entrada[i]):
                i += 1
                continue
            
            # Verificar operadores dobles
            if i + 1 < len(entrada):
                doble = entrada[i:i+2]
                if doble in self.config.OPERADORES_DOBLES:
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
            if self.utils.es_digito(entrada[i]):
                numero, nueva_i = self._extraer_numero(entrada, i)
                tokens.append(numero)
                i = nueva_i
                continue
            
            # Manejar identificadores
            if self.utils.es_letra(entrada[i]) or entrada[i] == '_':
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
        if i + 1 >= len(entrada) or not self.utils.es_digito(entrada[i + 1]):
            return False
        
        # Verificar contexto para determinar si es signo o operador
        if i == 0:
            return True
        if entrada[i-1] in "=+-*/(" or (self.utils.es_espacio(entrada[i-1]) and tokens and tokens[-1] in "=+-*/("):
            return True
        return False
    
    def _extraer_numero_con_signo(self, entrada, i):
        signo = entrada[i]
        j = i + 1
        while j < len(entrada) and self.utils.es_digito(entrada[j]):
            j += 1
        return signo + entrada[i + 1:j], j
    
    def _extraer_numero(self, entrada, i):
        j = i
        while j < len(entrada) and self.utils.es_digito(entrada[j]):
            j += 1
        return entrada[i:j], j
    
    def _extraer_identificador(self, entrada, i):
        j = i
        while j < len(entrada) and (self.utils.es_alfanumerico(entrada[j]) or entrada[j] == '_'):
            j += 1
        return entrada[i:j], j

