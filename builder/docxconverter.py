# -*- coding: utf-8 -*-
__author__ = 'Bárdos Dávid'

from sys import argv
from argparse import Namespace
from converter import Converter
from docx import Document
from docx.shared import Mm



class DocxConverter(Converter):
    def __init__(self, output_file_name):
        self._document = Document()
        self._raw_document_content = []
        self._output_file_path = "target/{}.docx".format(output_file_name)

    def convert(self):
        self._set_page_size_to_a4()
        self._generate_styles()
        self._document.save(self._output_file_path)

    def _set_page_size_to_a4(self):
        zeroth_section = self._document.sections[0]
        zeroth_section.page_height = Mm(297)
        zeroth_section.page_width = Mm(210)

    def _generate_styles(self):
        from docx.enum.style import WD_STYLE_TYPE
        paragraph_styles = [s for s in self._document.styles if s.type == WD_STYLE_TYPE.PARAGRAPH]
        for style in paragraph_styles:
            print(style.name)

if __name__ == "__main__":
    d = DocxConverter(argv[1])
    d.convert()