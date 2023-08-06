import tkinter as tk
from tkinter import ACTIVE, DISABLED, ttk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from .list import ListManager
from .helpers import getRoot, getOutputPath, setOutputPath, saveCSV, existsCSV, clean

class App():
    def __init__(self, master):

        # set root
        self.master = master
        ###########################################################
        
        # path frame
        self.path_frame = ttk.Frame(self.master, padding=10)
        
        # path description label
        self.path_desc_label = ttk.Label(self.path_frame, 
                                         text = 'Scegliere il percorso dove salvare le liste:',
                                         font=("Helvetica", 13, 'bold'))
        self.path_desc_label.pack(expand=True)
        
        # path label 
        self.path_label = ttk.Label(self.path_frame, text = getOutputPath())
        self.path_label.pack(expand=True)
        
        # select path button
        self.select_path_button = ttk.Button(
            self.path_frame,
            text='Scegli percorso',
            command=self.setPath
        )
        self.select_path_button.pack(expand=True)
        self.path_frame.grid(row=0)
        ###########################################################
        
        # file frame
        self.file_frame = ttk.Frame(self.master, padding=10)
        
        # file description label
        self.file_desc_label = ttk.Label(self.file_frame, 
                                         text = 'Scegliere il file .zip o .csv scaricato da Priamo:',
                                         font=("Helvetica", 13, 'bold'))
        self.file_desc_label.pack(expand=True)

        # file label 
        self.file_label = ttk.Label(self.file_frame, text = 'Nessun file selezionato')
        self.file_label.pack(expand=True)
        
        # opne file button
        self.open_button = ttk.Button(
            self.file_frame,
            text='Scegli file',
            command=self.selectFile
        )
        self.open_button.pack(expand=True)
        self.file_frame.grid(row=1)
        ###########################################################

        # generate frame
        self.generate_frame = ttk.Frame(self.master, padding=10)
        
        # path description label
        self.gen_desc_label = ttk.Label(self.generate_frame, 
                                         text = 'Premere per generare le liste:',
                                         font=("Helvetica", 13, 'bold'))
        self.gen_desc_label.pack(expand=True)
        
        # generate lists button
        self.generate_button = ttk.Button(
            self.generate_frame,
            text='Genera Liste',
            command=self.generateList 
        )
        self.generate_button.pack(expand=True)
        self.generate_frame.grid(row=2)
        ###########################################################

    # func for updating labels text
    def changeLabelText(self, label, text):
        label.config(text=text)
        self.master.update()
    
    # func for disabling generate button while processing the lists
    def isWaiting(self, loading):
        if loading:
            self.generate_button.config(state=tk.DISABLED, text='Attendere...')
        else:
            self.generate_button.config(state=tk.ACTIVE, text='Genera Liste')
        self.master.update()
    
    # func to set the path where to save the output
    def setPath(self):
        dirpath = fd.askdirectory(
            title='Scegli dove salvare le liste',
            initialdir=getRoot(__file__),
            )
        if not dirpath:
            return
        
        setOutputPath(dirpath)
        self.changeLabelText(self.path_label, dirpath)
    
    # func to find the input file for our application
    def selectFile(self):
        clean()
        filetypes = (
            ('.zip files', '*.zip'),
            ('.csv files', '*.csv')
        )

        filepath = fd.askopenfilename(
            title='Scegli file',
            initialdir=getRoot(__file__),
            filetypes=filetypes)
        if not filepath:
            return
        
        saveCSV(filepath)      
        self.changeLabelText(self.file_label, filepath)

    # func for generating the lists
    def generateList(self):
        if not getOutputPath(): 
            mb.showerror('Errore', 'Nessun percorso selezionato dove salvare le liste')
            return
        if not existsCSV(): 
            mb.showerror('Errore', 'Nessun file selezionato')
            return
        self.isWaiting(True)
        manager = ListManager()
        manager.parseCSV()
        manager.generateMachinesLists()
        manager.generateCompleteList()
        manager.pack() 
        self.isWaiting(False)

# main function
def run():
  
    # Instantiating top level
    root = tk.Tk()
  
    # Setting the title of the window
    root.title("Liste Iniziativa Medica")
    
    # Set main window properties
    root.eval('tk::PlaceWindow . center')
    root.resizable(False, False)
    
    # Calling our App
    app = App(root)
  
    # Mainloop which will cause
    # this toplevel to run infinitely
    root.mainloop()

