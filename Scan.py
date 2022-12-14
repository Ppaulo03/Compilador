from Symbol import *
from Automato import *

contador = [1, 0] # linha X coluna
contador_parenteses = 0

def Scan(file, table_estados, table_symbols):
    global contador_parenteses
    estado_atual = Estados.INICIO
    word = ''
    
    while True:
        last_pos = file.tell()
        char = file.read(1)
        contador[1] += 1

        if not char:
            if len(word) <= 0:
                if contador_parenteses > 0:
                    print(f'Error -> parenteses não fechado linha {contador[0]}')
                elif contador_parenteses < 0: 
                    print(f'Error -> parenteses não aberto linha {contador[0]}')
                return Token('EOF', 'EOF', ' ')
            else: 
                return verify_word_end(file, table_estados, table_symbols, last_pos, char, word, estado_atual)      

        elif char in table_estados[estado_atual]:
            estado_atual = table_estados[estado_atual][char]
            word += char

        else: 
            return verify_word_end(file, table_estados, table_symbols, last_pos, char, word, estado_atual)


def verify_word_end(file, table_estados, table_symbols, last_pos, char, word, estado_atual):
    global contador_parenteses
    if table_estados[estado_atual]['end']:
        file.seek(last_pos)
        contador[1] -= 1

        if word == '\n':
            if contador_parenteses > 0:
                    print(f'Error -> parenteses não fechado linha {contador[0]}')
            elif contador_parenteses < 0:
                print(f'Error -> parenteses não aberto linha {contador[0]}')
            contador_parenteses = 0
            contador[0] += 1
            contador[1] = 0
            return Scan(file, table_estados, table_symbols)

        elif word in [' ', '\t'] or estado_atual == Estados.COMENTARIO_FIM:
            return Scan(file, table_estados, table_symbols)
        
        elif estado_atual == Estados.ID:
            if word not in table_symbols:
                table_symbols[word] = Token(word, 'id', ' ')
            return table_symbols[word]

        elif estado_atual == Estados.INTEIRO:
            return Token(int(word), 'inteiro', ' ')
        
        elif estado_atual == Estados.FLOAT:
            return Token(float(word), 'float', ' ')

        elif estado_atual == Estados.EXPONENCIAL:
            return Token(float(word), 'float', ' ')
        
        elif estado_atual == Estados.LITERAL_FIM:
            return Token(word, 'literal', ' ')
        
        elif estado_atual == Estados.PARENTESES_ABRIR:
            contador_parenteses += 1
            return Scan(file, table_estados, table_symbols)
        
        elif estado_atual == Estados.PARENTESES_FECHAR:
            contador_parenteses -= 1
            return Scan(file, table_estados, table_symbols)
    
        return Token(word, estado_atual, ' ')

    else:
        print(f'Error -> {char} - line {contador[0]}, col {contador[1]}')
        return Scan(file, table_estados, table_symbols)
    

if __name__ == '__main__':
    table_estados = get_state_table()
    table_symbols = get_symbol_table()

    with open('teste', 'r', encoding='UTF-8') as file:
        while True:
            token = Scan(file, table_estados, table_symbols)
            if token.lexico == 'EOF': break
            else: print(f'-> {token.lexico} -> {token.id} ')