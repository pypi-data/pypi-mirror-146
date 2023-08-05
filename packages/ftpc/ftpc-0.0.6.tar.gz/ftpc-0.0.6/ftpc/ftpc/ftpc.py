import logging
import os
import subprocess
from typing import Optional


class FileToPdf(object):
    """
    Convert a file to a PDF.
    """

    def __init__(self):
        """
        Initialize the class
        :return:
        """
        logging.info("Initializing file_to_pdf")

    def convert_to_pdf_linux(self, file_path: Optional[str]) -> Optional[None]:
        """
        Convert any type of file to pdf
        :return:
        """
        logging.info("Converting file to pdf")
        logging.info("File path: {}".format(file_path))
        subprocess.call(["libreoffice", "--headless", "--convert-to", "pdf", file_path])
        logging.info("Finished converting file to pdf")

    def convert_to_pdf_windows(self, doc: Optional[str]) -> Optional[None]:
        """
        Convert doc file to pdf
        :return:
        """
        try:
            from comtypes import client
        except ImportError:
            client = None
        doc = os.path.abspath(doc)
        if client is None:
            self.convert_to_pdf_linux(doc)

        name, ext = os.path.splitext(doc)
        if ext.lower() in [".doc", ".docx"]:
            logging.info("Converting doc file to pdf")
            logging.info("File path: {}".format(doc))
            word = client.CreateObject("Word.Application")
            doc = word.Documents.Open(doc)
            doc.SaveAs(name + ".pdf", FileFormat=17)
            doc.Close()
            word.Quit()
            logging.info("Finished converting doc file to pdf")
        elif ext.lower() in [".xls", ".xlsx"]:
            logging.info("Converting xls file to pdf")
            logging.info("File path: {}".format(doc))
            excel = client.CreateObject("Excel.Application")
            doc = excel.Workbooks.Open(doc)
            doc.SaveAs(name + ".pdf", FileFormat=17)
            doc.Close()
            excel.Quit()
            logging.info("Finished converting xls file to pdf")
        elif ext.lower() in [".ppt", ".pptx"]:
            logging.info("Converting ppt file to pdf")
            logging.info("File path: {}".format(doc))
            powerpoint = client.CreateObject("Powerpoint.Application")
            doc = powerpoint.Presentations.Open(doc)
            doc.SaveAs(name + ".pdf", FileFormat=17)
            doc.Close()
            powerpoint.Quit()
            logging.info("Finished converting ppt file to pdf")
        else:
            logging.info("File extension not supported")

    def convert_pdf_to_html(self, pdf_file_path: Optional[str]) -> Optional[None]:
        """
        Linux
        Convert pdf to html
        :param pdf_file_path:
        :return:
        """
        pdf_file = pdf_file_path.replace(' ', '\ ')
        html_file = pdf_file.replace('.pdf', '.html')
        command = 'pdftohtml -q -c -zoom 1 -enc UTF-8 -noframes {} > {}'.format(pdf_file, html_file)
        os.system(command)
