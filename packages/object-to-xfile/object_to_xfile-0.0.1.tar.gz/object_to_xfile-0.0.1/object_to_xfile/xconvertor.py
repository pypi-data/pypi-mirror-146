import logging
from xml.dom.minidom import parseString

import pandas as pd
from dicttoxml import dicttoxml
from flatten_json import flatten
import pdfkit


class XConvertor:
    """
    XConvertor class is used to generate csv,xml,excel,pdf and xlsx files,
    from dict objects.
    """
    def __init__(self, data):
        """
        Parameters
        ----------
        data : list of dict.
            generated file data.
        """
        self.data = data
        self.file_Name = "x_convertor"

    def to_csv(self):
        """
        create csv file from data object using pandas.
        """
        csv_file_name = f'{self.file_Name}.csv'
        flatten_objects = self.to_flatten()
        df = pd.DataFrame(flatten_objects)
        df.to_csv(csv_file_name, index=False)

    def to_html(self):
        """
        create html file from data object using pandas.
        """
        html_file_name = f'{self.file_Name}.html'
        flatten_objects = self.to_flatten()
        df = pd.DataFrame(flatten_objects)
        df['primaryImage'] = df['primaryImage'].apply(
            lambda url: f'<img src="{url}" height="100" width="100">' if url != '' else '')

        df['primaryImageSmall'] = df['primaryImageSmall'].apply(
            lambda url: f'<img src="{url}" height="100" width="100">' if url != '' else '')

        df.to_html(html_file_name, escape=False)

    def to_xml(self):
        """
        create xml file from data object using dicttoxml.
        """
        xml_file_name = f'{self.file_Name}.xml'
        objects = self.data
        xml_data = dicttoxml(objects, attr_type=False)
        formatted_xml_data = parseString(xml_data).toprettyxml()

        try:
            xml_file = open(xml_file_name, 'w')
            logging.debug(f'successfully open {xml_file_name} file')
        except OSError as err:
            logging.debug(f'OS error occurred trying to open {xml_file_name}, Error: {err}')
            return

        xml_file.write(formatted_xml_data)

    def to_excel(self):
        """
         create excel file from data object using pandas.
        """
        excel_file_name = f'{self.file_Name}.xlsx'
        object_list = self.to_flatten()
        df = pd.DataFrame(object_list)
        df.to_excel(excel_file_name, index=False)

    def to_pdf(self):
        """
         create pdf file from data object using pdfkit.
        """
        
        # pdf page size configuration for pdfKit lib.
        options = {
            'page-height': '300',
            'page-width': '900',
        }

        pdf_file_name = f'{self.file_Name}.pdf'
        object_list = self.to_flatten()
        df = pd.DataFrame(object_list)
        logging.debug('object_list converted to DataFrame df object')

        df_html = df.to_html()
        pdfkit.from_string(df_html, pdf_file_name, options=options)

    def to_flatten(self):
        """
        return flatten objects.
        """
        flatten_objects = []

        for data_object in self.data:
            flatten_object = flatten(data_object)
            flatten_objects.append(flatten_object)

        return flatten_objects
