# check.py

import os

def isfile(path):
    """
    verifica se path é file
    """
    isfile = os.path.isfile(path)
    return isfile

def isfolder(path):
    """
    verifica se path é folder
    """
    isfolder = os.path.isdir(path)
    return isfolder

def exists(path):
    """
    Verifica se um arquivo existe
    e retorna notificacao
    """
    if os.path.exists(path):
        print('Arquivo existente:')
        print(path)
        return True
    else:
        print('Arquivo não encontrado:')
        print(path)
        return False