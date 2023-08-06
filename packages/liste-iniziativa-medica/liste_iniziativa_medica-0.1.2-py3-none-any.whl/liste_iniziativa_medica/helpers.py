import os, shutil
from zipfile import ZipFile
from pathlib import Path


# func to get the root of filesystem
def getRoot(__file__):
    file_path = os.path.abspath(__file__)
    BASE_DIR = os.path.dirname(file_path)
    while (os.path.isdir(BASE_DIR)):
        if (BASE_DIR==os.path.dirname(BASE_DIR)):
                break
        else:
            BASE_DIR=os.path.dirname(BASE_DIR) 
    return BASE_DIR

# func to get the data dir path where store utils file for the application
def getDataPath():
    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    if not os.path.exists(DATA_DIR): os.mkdir(DATA_DIR)
    return DATA_DIR

# func to set the path where to save the output
def setOutputPath(output_path):
    f = open(os.path.join(getDataPath(), 'path.txt'), 'w')
    f.write(output_path.strip())
    f.close()
    
# func to get the path where to save the output 
def getOutputPath():
    file = Path(os.path.join(getDataPath(), 'path.txt'))
    file.touch(exist_ok=True)
    f = open(file, 'r')
    output_path = f.readline().strip()
    f.close()
    if output_path == '':
        output_path = 'Nessun percorso selezionato'
    return output_path
    
# func to save the csv file
def saveCSV(filepath):
    if filepath.endswith('.zip'):
            with ZipFile(filepath, 'r') as zip:
                zip.extract('FoglioLavoroCompleto1.csv', getDataPath())
    else:
        shutil.copyfile(filepath, getDataPath())
    os.rename(os.path.join(getDataPath(), 'FoglioLavoroCompleto1.csv'), os.path.join(getDataPath(), 'list.csv'))

# func to get the list.csv path
def getCSVPath():
    return os.path.join(getDataPath(), 'list.csv')   
    
# func to check if the csv file exists
def existsCSV():
    if os.path.exists(os.path.join(getDataPath(), 'list.csv')): return True
    return False

def clean():
    if existsCSV(): os.remove(os.path.join(getDataPath(), 'list.csv'))
    if os.path.exists(os.path.join(getDataPath(), 'temp.pdf')): os.remove(os.path.join(getDataPath(), 'temp.pdf'))
    if os.path.exists(os.path.join(getDataPath(), 'template.html')): os.remove(os.path.join(getDataPath(), 'template.html'))

    