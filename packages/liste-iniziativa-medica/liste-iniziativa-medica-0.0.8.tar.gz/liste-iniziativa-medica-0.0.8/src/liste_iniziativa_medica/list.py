import pandas as pd
import pdfkit
import os, shutil
import io
from PyPDF2 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .helpers import getDataPath, getOutputPath, getCSVPath, clean


class ListManager():
    
    # instanziate class variables
    def __init__(self):
        self.machines = {}
        self.day = ''
    
    # func for parsing the csv list taking only what we are interested in and create a dictionary with machines' names as keys
    def parseCSV(self):
        df = pd.read_csv(getCSVPath(), sep=';', usecols=[
            'GRP_DESCRIZIONE', 
            'EROG_DESCRIZIONE', 
            'SLOT_DATA', 
            'SLOT_ORA', 
            'SLOT_TIPO_SESSIONE', 
            'SLOT_COMMENTO', 
            'PRENO_ID_PRENOTATO', 
            'PRENO_TELEFONO', 
            'PRENO_CELLULARE', 
            'PRENO_NOTE', 
            'PRENO_COMMENTO', 
            'PAZ_DATA_NASCITA', 
            'PAZ_COGNOME', 
            'PAZ_NOME', 
            'PREST_DESCRIZIONE'], 
        dtype=str)
        
        # parse day
        self.day = df['SLOT_DATA'][0].split(' ')[0].replace('/', '-')
        
        i = 0
        MAX_INDEX = len(df.index)-1
        while i < MAX_INDEX:
            # a little check due to 'ECOGRAFIA' constraint
            machine = df['GRP_DESCRIZIONE'][i].strip()
            if machine == 'ECOGRAFIA':
                machine = df['EROG_DESCRIZIONE'][i].strip()
            # add key if not already in
            if machine not in self.machines.keys():
                self.machines[machine] = []
            # parse hour
            time_int = df['SLOT_ORA'][i]
            time_str = str(time_int)
            if len(time_str) > 3:
                time_str = time_str[:2] + ':' + time_str[2:]
            else:
                time_str = time_str[:1] + ':' + time_str[1:]
            # parse birthday
            birthday = df['PAZ_DATA_NASCITA'][i].split(' ')[0]
            # parse doctor
            medico_temp = df['EROG_DESCRIZIONE'][i].strip()
            medico_temp = medico_temp.split(' ')
            medico = ''
            for j in range(1, len(medico_temp)-1):
                medico = medico + ' ' +  medico_temp[j]
            # parse tel and cell info
            contatto = ''
            tel = str(df['PRENO_TELEFONO'][i]).strip()
            cell = str(df['PRENO_CELLULARE'][i]).strip()
            if tel != 'nan' and cell != 'nan':
                tel = tel[:3] + ' ' + tel[3:] if tel.startswith('3') else tel
                cell = cell[:3] + ' ' + cell[3:] if cell.startswith('3') else cell
                if tel != cell:
                    contatto = tel + '<br>' + cell
                else: contatto = cell
            elif tel != 'nan':
                tel = tel[:3] + ' ' + tel[3:] if tel.startswith('3') else tel
                contatto = tel
            else:
                cell = cell = cell[:3] + ' ' + cell[3:] if cell.startswith('3') else cell
                contatto = cell
            # parse notes
            preno_note = ''
            if str(df['PRENO_NOTE'][i]) != 'nan': 
                preno_note = str(df['PRENO_NOTE'][i]).strip()
            slot_comm = ''
            if str(df['SLOT_COMMENTO'][i]) != 'nan': 
                slot_comm = str(df['SLOT_COMMENTO'][i]).strip()
            preno_comm = ''
            if str(df['PRENO_COMMENTO'][i]) != 'nan': 
                preno_comm = str(df['PRENO_COMMENTO'][i]).strip()
            # build and add dict entry
            entry = [
                time_int, 
                time_str, 
                str(df['SLOT_TIPO_SESSIONE'][i]).strip(), 
                str(df['PRENO_ID_PRENOTATO'][i]).strip(), 
                df['PAZ_COGNOME'][i], 
                df['PAZ_NOME'][i], 
                birthday,
                str(df['PREST_DESCRIZIONE'][i]).strip(), 
                preno_note, 
                slot_comm, 
                preno_comm, 
                medico, 
                contatto
            ]
            self.machines[machine].append(entry)
            i = i+1

    # func for creating the single machine pdfs
    def generateMachinesLists(self):
        if not os.path.exists(os.path.join(getDataPath(), 'Macchine')):
            os.makedirs(os.path.join(getDataPath(), 'Macchine'))
            
        for machine in self.machines:
            ordered_list = sorted(self.machines[machine], key=lambda x: int(x[0]))
            dataframe = pd.DataFrame(ordered_list, columns=["ORA_INT", "ORA", "SESSIONE", "ID_PRENOTAZIONE", "COGNOME", "NOME", "DATA NASCITA", "PRESTAZIONE", "NOTE", "SLOT_COMMENTO", "PRENO_COMMENTO", "MEDICO", "CONTATTO"])
            file_html = open(os.path.join(getDataPath(), 'template.html'), 'w')
            head = """
                <!DOCTYPE html>
                <html>
                    <head>
                        <title>LIST</title>
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
                    <style>
                        body {
                            font-family: sans-serif; 
                        }

                        th {
                            text-align: center;
                        }

                        .grey {
                            background-color: rgb(230, 230, 230);
                        }

                        .my_table {
                            border-color: black;
                            border-width: 1rem;
                        }

                        .my_row {
                            justify-content: end;
                        }
                    </style>
                    </head>
                    <body>
                        <table class="table table-bordered my_table">
                            <thead>
                                <tr>
                                    <th scope="col">#</th>
                                    <th scope="col">ORA</th>
                                    <th scope="col">SES</th>
                                    <th scope="col">ID</th>
                                    <th scope="col">NOMINATIVO</th>
                                    <th scope="col">DATA DI NASCITA</th>
                                    <th scope="col">PRESTAZIONE</th>
                                    <th scope="col">MEDICO</th>
                                    <th scope="col">CONTATTO</th>
                                    <th scope="col">SIGLA/NOTE</th>
                                </tr>
                            </thead>
                            <tbody>
                """
            table = ""
            greyRow=True
            row_index = 1
            k = 0
            max = len(dataframe.index)
            while k != max:
                docs = []
                comments = []
                exams = []
                while k+1 != max and dataframe['COGNOME'][k] == dataframe['COGNOME'][k+1] and dataframe['NOME'][k] == dataframe['NOME'][k+1] and dataframe['DATA NASCITA'][k] == dataframe['DATA NASCITA'][k+1]:
                    docs.append(dataframe['MEDICO'][k])
                    if dataframe['NOTE'][k] != '': comments.append(dataframe['NOTE'][k])
                    if dataframe['SLOT_COMMENTO'][k] != '': comments.append(dataframe['SLOT_COMMENTO'][k])
                    if dataframe['PRENO_COMMENTO'][k] != '': comments.append(dataframe['PRENO_COMMENTO'][k])
                    exams.append(dataframe['PRESTAZIONE'][k])
                    k = k+1
                docs.append(dataframe['MEDICO'][k])
                if dataframe['NOTE'][k] != '': comments.append(dataframe['NOTE'][k])
                if dataframe['SLOT_COMMENTO'][k] != '': comments.append(dataframe['SLOT_COMMENTO'][k])
                if dataframe['PRENO_COMMENTO'][k] != '': comments.append(dataframe['PRENO_COMMENTO'][k])
                exams.append(dataframe['PRESTAZIONE'][k])
                medico = ''
                if len(docs) != 0:
                    docs = list(dict.fromkeys(docs))
                    for doc in docs:
                        if medico == '': medico = medico + doc
                        else: medico = medico + '<br>' + doc 
                note = ''
                if len(comments) != 0: 
                    note = '<br><b>Note:</b>'
                    comments = list(dict.fromkeys(comments))
                    for comment in comments:
                        note = note + '<br>' + comment
                prestazione = ''
                if len(exams) != 0: 
                    for exam in exams:
                        prestazione = prestazione + exam  + '<br>'
                prestazione = prestazione + note 
                sessione = str(dataframe['SESSIONE'][k]) if str(dataframe['SESSIONE'][k])!='nan' else ''
                if greyRow:
                    html_row= '<tr class="grey"><th scope="row">'+str(row_index)+'</th><td>'+dataframe['ORA'][k]+'</td><td>'+sessione+'</td><td>'+dataframe['ID_PRENOTAZIONE'][k]+'</td><td style="white-space:nowrap;"><b>'+dataframe['COGNOME'][k]+'</b> '+dataframe['NOME'][k]+'</td><td>'+dataframe['DATA NASCITA'][k]+'</td><td>'+str(prestazione)+'</td><td>'+medico+'</td><td>'+dataframe['CONTATTO'][k]+'</td><td></td></tr>'
                    greyRow=False
                else:
                    html_row = '<tr><th scope="row">'+str(row_index)+'</th><td>'+dataframe['ORA'][k]+'</td><td>'+sessione+'</td><td>'+dataframe['ID_PRENOTAZIONE'][k]+'</td><td style="white-space:nowrap;"><b>'+dataframe['COGNOME'][k]+'</b> '+dataframe['NOME'][k]+'</td><td>'+dataframe['DATA NASCITA'][k]+'</td><td>'+prestazione+'</td><td>'+medico+'</td><td>'+dataframe['CONTATTO'][k]+'</td><td></td></tr>' 
                    greyRow=True
                row_index = row_index+1
                table = table + html_row
                k = k+1
            tail = """	
                            </tbody>
                        </table>
                    </body>
                </html>
                """
            file_html.write(head + table + tail)
            file_html.close()
            options = {
                'margin-top': '18',
                'orientation': 'Landscape',
            }
            pdfkit.from_file(os.path.join(getDataPath(), 'template.html'), os.path.join(getDataPath(), 'temp.pdf'), options=options)
            watermark = io.BytesIO()
            # Create a new pdf consisting in only the "date - machine" watermark
            can = canvas.Canvas(watermark, pagesize=letter)
            can.setFont('Helvetica', 20)
            can.drawString(28, 560, self.day)
            can.setFont('Helvetica-Bold', 20)
            can.drawString(175, 560, machine)
            can.showPage()
            can.save()
            # Move to the beginning of the StringIO buffer
            watermark.seek(0)
            # Create the output PDF
            output_pdf = PdfFileWriter()
            # Open the Triage PDF and the "Watermark" PDF
            title_pdf = PdfFileReader(watermark)
            machine_list_pdf = PdfFileReader(open(os.path.join(getDataPath(), 'temp.pdf'), mode='rb'))
            # Add the title "watermark" on the machine list page
            for page in machine_list_pdf.pages:
                page.mergePage(title_pdf.getPage(0))
                output_pdf.addPage(page)
            # Finally, write "output" to a real file
            outputStream = open(os.path.join(getDataPath(), 'Macchine', machine+'.pdf'), 'wb')
            output_pdf.write(outputStream)
            outputStream.close()
      
    # func for creating the complete list of the day with all machines      
    def generateCompleteList(self):
        num = 1
        pdf_writer = PdfFileWriter()
        for machine in self.machines:
            pdf_reader = PdfFileReader(os.path.join(getDataPath(), 'Macchine', machine+'.pdf'))
            for page in range(pdf_reader.getNumPages()):
                watermark = io.BytesIO()
                # Create a new pdf consisting in only the "date - machine" watermark
                can = canvas.Canvas(watermark, pagesize=letter)
                can.setFont('Helvetica-Bold', 15)
                can.drawString(800, 17, str(num))
                can.showPage()
                can.save()
                # Move to the beginning of the StringIO buffer
                watermark.seek(0)
                # Add each page to the writer object
                num_pdf = PdfFileReader(watermark)
                pdf_reader.getPage(page).mergePage(num_pdf.getPage(0))
                pdf_writer.addPage(pdf_reader.getPage(page))
                num = num+1

            # Write out the merged PDF
            with open(os.path.join(getDataPath(), 'Lista Completa.pdf'), 'wb') as out:
                pdf_writer.write(out)

    # func for packing everything inside day dir
    def pack(self):
        if not os.path.exists(os.path.join(getOutputPath(), self.day)):
            os.makedirs(os.path.join(getOutputPath(), self.day))
        if os.path.exists(os.path.join(getOutputPath(), self.day, 'Macchine')):
            shutil.rmtree(os.path.join(getOutputPath(), self.day, 'Macchine'))
        if os.path.exists(os.path.join(getOutputPath(), self.day, 'Lista Completa.pdf')):
            os.remove(os.path.join(getOutputPath(), self.day, 'Lista Completa.pdf'))
        shutil.move(os.path.join(getDataPath(), 'Macchine'), os.path.join(getOutputPath(), self.day))
        shutil.move(os.path.join(getDataPath(), 'Lista Completa.pdf'), os.path.join(getOutputPath(), self.day))
        clean()
        
