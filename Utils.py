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


