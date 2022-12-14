class Token():
    def __init__(self, lexico, id, type):
        self.lexico = lexico
        self.id = id
        self.type = type


def get_symbol_table():
    symbol_table = {}
    reserved_words = ['inicio', 'verinicio']

    for word in reserved_words:
        symbol_table[word] = Token(word, word, ' ')
    
    return symbol_table