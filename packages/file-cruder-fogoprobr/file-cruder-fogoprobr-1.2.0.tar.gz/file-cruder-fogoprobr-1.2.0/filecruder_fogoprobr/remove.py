from . import check
import os
import shutil

def dir(directory, file_path):
    """
    Signature:
    ----------
    remove.dir(
        directory: 'str',
        file_path: 'str'
    )

    Docstring:
    ----------
    Remove pasta 'directory' na mesma pasta de 'file_path'
    'file_path' é referencia de onde remover a pasta e
    pode ser __file__
    
    Parameters:
    ----------
    directory: Nome da pasta que será removida
    file_path: Path de referencia para remover a pasta 'directory'. Deve ser realpath (path completo) até a pasta [ou arquivo na] onde a pasta 'directory' será removida. Pode ser __file__ para criar pasta em './'

    """
    parent_dir = os.path.dirname(os.path.abspath(file_path))
    if check.isfile(file_path):
        parent_dir = os.path.dirname(os.path.abspath(file_path))
    elif check.isfolder(file_path):
        parent_dir = os.path.abspath(file_path)
    else:
        raise Exception('Invalid file_path. Make sure file or folder existis')
    
    path = os.path.join(parent_dir, directory)

    if os.path.isdir(path):
        print(path)
        shutil.rmtree(path)
        print("Pasta '% s' removida" % directory)
        return True
    else:
        print("Pasta '% s' não existe" % directory)
        return False

def patch(path, row):
    """
    Signature:
    ----------
    remove.patch(
        path: 'str',
        row: 'int'
    )

    Docstring:
    ----------
    remove a linha 'row' do arquivo 'path'
    
    Parameters:
    ----------
    path: caminho para o arquivo
    row: numero da linha removida
    """
    if check.isfile(path):
        file = open(path, 'r')
        lines = file.readlines()
        if 0 < row and row <= len(lines):
            lines.pop(row-1)
        else:
            raise Exception('Row out of range')
        file.close()
        file = open(path, 'w')
        file.writelines(lines)
        file.close()
    else:
        raise Exception('Invalid file path')