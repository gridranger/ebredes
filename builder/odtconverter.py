# -*- coding: utf-8 -*-
__author__ = 'Bárdos Dávid'

from odf.opendocument import OpenDocumentText
from odf.style import ParagraphProperties, Style, TextProperties
from odf.text import H, P
from sys import argv
from converter import Converter


class OdtConverter(Converter):
    def __init__(self, output_file_name):
        self._document = OpenDocumentText()
        self._raw_document_content = []
        self._output_file_path = "target/{}.odt".format(output_file_name)
        self._h1_style = None
        self._p_style = None

    def convert(self):
        self._generate_styles()
        sources = self._process_input_files()
        for source in sources:
            self._raw_document_content += source
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

    def _process_raw_document_content(self):
        for line in self._raw_document_content:
            if line.startswith("# "):
                new_element = H(outlinelevel=1, stylename=self._h1_style, text=line.replace("# ", ""))
            else:
                new_element = P(text=line, stylename=self._p_style)
            self._document.text.addElement(new_element)


if __name__ == "__main__":
    o = OdtConverter(argv[1])
    o.convert()
