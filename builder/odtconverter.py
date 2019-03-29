# -*- coding: utf-8 -*-
__author__ = 'Bárdos Dávid'

from odf.opendocument import OpenDocumentText
from odf.style import ParagraphProperties, Style, TextProperties
from odf.text import H, P
from os import listdir
from sys import argv


class OdtConverter(object):
    def __init__(self, output_file_name):
        self._document = OpenDocumentText()
        self._raw_document_content = []
        self._output_file_path = "target/{}.odt".format(output_file_name)
        self._h1_style = None
        self._p_style = None

    def convert(self):
        self._generate_styles()
        self._process_input_files()
        self._process_raw_document_content()
        self._document.save(self._output_file_path)

    def _generate_styles(self):
        self._h1_style = Style(name="Heading 1", family="paragraph")
        self._h1_style.addElement(ParagraphProperties(attributes={"margintop": "24pt", "marginbottom": "12pt",
                                                                  "keepwithnext": "always"}))
        self._h1_style.addElement(TextProperties(attributes={"fontsize": "16pt"}))
        self._document.styles.addElement(self._h1_style)
        self._p_style = Style(name="Body", family="paragraph")
        self._p_style.addElement(ParagraphProperties(attributes={"textindent": "1.25cm", "textalign": "justify",
                                                                 "orphans": 2, "widows": 2}))
        self._document.styles.addElement(self._p_style)

    def _process_input_files(self):
        current_folder_content = listdir(".")
        for file_name in current_folder_content:
            if file_name.endswith(".txt"):
                new_lines = self._process_file(file_name)
                self._raw_document_content += new_lines

    @staticmethod
    def _process_file(file_name):
        with open(file_name, encoding="utf8") as file_handler:
            raw_text = file_handler.read()
            raw_text = raw_text.replace("--", "\u2013")
        lines = raw_text.split("\n\n")
        return lines

    def _process_raw_document_content(self):
        for line in self._raw_document_content:
            if line[1:3] == "# ":
                new_element = H(outlinelevel=1, stylename=self._h1_style, text=line.replace("# ", ""))
            else:
                new_element = P(text=line, stylename=self._p_style)
            self._document.text.addElement(new_element)


if __name__ == "__main__":
    o = OdtConverter(argv[1])
    o.convert()
