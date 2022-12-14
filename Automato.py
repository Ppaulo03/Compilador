from enum import Enum
import string

class Estados(Enum):

    INICIO = 0;  
    LITERAL = 1; LITERAL_FIM = 2
    INTEIRO = 3; FLOAT_INIT = 4; FLOAT = 5
    EXPONENCIAL_INIT = 6; EXPONENCIAL_SINAL = 7; EXPONENCIAL = 8; 
    COMENTARIO = 9; COMENTARIO_FIM = 10
    PARENTESES_ABRIR = 11; PARENTESES_FECHAR = 12
    ARITIMETICO = 13
    COMPARATIVO = 14; COMPARATIVO_IGUAL = 15; COMPARATIVO_DIFERENTE = 16; ATRIBUIR = 17
    ID = 18; VIRGULA = 19; PONTO_VIRGULA = 20; VAZIO = 21; PULA_LINHA = 22


def get_state_table():
    table = {}

    table[Estados.INICIO] = {
        'end':False,
        '{':Estados.COMENTARIO,
        '(':Estados.PARENTESES_ABRIR,
        ')':Estados.PARENTESES_FECHAR,
        '_':Estados.ID,
        '=':Estados.ATRIBUIR,
        '!':Estados.COMPARATIVO_DIFERENTE,
        ',':Estados.VIRGULA,
        ';':Estados.PONTO_VIRGULA,
        '\n':Estados.PULA_LINHA,
        }
    for c in string.digits: table[Estados.INICIO][c] = Estados.INTEIRO
    for c in string.ascii_letters: table[Estados.INICIO][c] = Estados.ID
    for c in ["'"]: table[Estados.INICIO][c] = Estados.LITERAL
    for c in ['+', '-', '*', '/']: table[Estados.INICIO][c] = Estados.ARITIMETICO
    for c in ['>', "<"]: table[Estados.INICIO][c] = Estados.COMPARATIVO
    for c in [' ', '\t']: table[Estados.INICIO][c] = Estados.VAZIO

    
    
    table[Estados.LITERAL] = {'end':False}
    for c in string.printable: 
        if c != '/n': table[Estados.LITERAL][c] = Estados.LITERAL 
    for c in ["'"]: table[Estados.LITERAL][c] = Estados.LITERAL_FIM
    
    
    table[Estados.LITERAL_FIM] = {'end':True}


    table[Estados.INTEIRO] = {
        'end':True,
        '.':Estados.FLOAT_INIT
        }
    for c in string.digits: table[Estados.INTEIRO][c] = Estados.INTEIRO
    for c in ['e', "E"]: table[Estados.INTEIRO][c] = Estados.EXPONENCIAL_INIT


    table[Estados.FLOAT_INIT] = {'end':False}
    for c in string.digits: table[Estados.FLOAT_INIT][c] = Estados.FLOAT
    

    table[Estados.FLOAT] = {'end':True}
    for c in string.digits: table[Estados.FLOAT][c] = Estados.FLOAT
    for c in ['e', "E"]: table[Estados.FLOAT][c] = Estados.EXPONENCIAL_INIT


    table[Estados.EXPONENCIAL_INIT] = {'end':False}
    for c in ['-', "+"]: table[Estados.EXPONENCIAL_INIT][c] = Estados.EXPONENCIAL_SINAL
    for c in string.digits: table[Estados.EXPONENCIAL_INIT][c] = Estados.EXPONENCIAL


    table[Estados.EXPONENCIAL_SINAL] = {'end':False}
    for c in string.digits: table[Estados.EXPONENCIAL_SINAL][c] = Estados.EXPONENCIAL


    table[Estados.EXPONENCIAL] = {'end':True}
    for c in string.digits: table[Estados.EXPONENCIAL][c] = Estados.EXPONENCIAL


    table[Estados.ID] = {
        'end':True,
        '_': Estados.ID
        }
    for c in string.ascii_letters: table[Estados.ID][c] = Estados.ID
    for c in string.digits: table[Estados.ID][c] = Estados.ID
    

    table[Estados.COMENTARIO] = {'end':False}
    for c in string.printable: table[Estados.COMENTARIO][c] = Estados.COMENTARIO
    table[Estados.COMENTARIO]['}'] = Estados.COMENTARIO_FIM


    table[Estados.COMENTARIO_FIM] = {'end':True}


    table[Estados.ATRIBUIR] = {
        'end':True,
        '=':Estados.COMPARATIVO_IGUAL
        }


    table[Estados.COMPARATIVO_DIFERENTE] = {
        'end':False,
        '=':Estados.COMPARATIVO_IGUAL
        }
    
    table[Estados.COMPARATIVO] = {
        'end':True,
        '=':Estados.COMPARATIVO_IGUAL
        }

    table[Estados.COMPARATIVO_IGUAL] = {'end':True}


    table[Estados.ARITIMETICO] = {'end':True}


    table[Estados.PARENTESES_ABRIR] = {'end':True}


    table[Estados.PARENTESES_FECHAR] = {'end':True}


    table[Estados.VIRGULA] = {'end':True}


    table[Estados.PONTO_VIRGULA] = {'end':True}


    table[Estados.VAZIO] = {'end':True}

    
    table[Estados.PULA_LINHA] = {'end':True}

    return table