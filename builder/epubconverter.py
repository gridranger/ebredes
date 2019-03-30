# -*- coding: utf-8 -*-
__author__ = 'Bárdos Dávid'

from json import load
from os import makedirs
from shutil import copyfile
from sys import argv
from converter import Converter


class EpubConverter(Converter):
    def __init__(self, output_file_name):
        self._output_file_path = "target/{}.epub".format(output_file_name)
        self._templates_folder = "builder/templates"
        self._workspace_folder = "target/ws"
        self._raw_metadata = {}
        self._templates = {}

    def convert(self):
        self._load_templates()
        self._create_workspace()
        self._process_content()
        # http://www.jedisaber.com/eBooks/Introduction.shtml
        # processing text
        #     read source files
        #     read metadata
        #     create title page
        #     create xhtml structure
        #     adding styles
        #     filling toc
        #     metadata
        # zip the workspace
        # remove workspace

    def _load_templates(self):
        templates = ["content", "navpoint", "title", "toc.ncx"]
        for template in templates:
            with open("builder/templates/{}.html".format(template)) as file_handler:
                self._templates[template] = file_handler.read()

    def _create_workspace(self):
        self._create_folders()
        self._create_mimetype_file()
        self._create_css()

    def _create_folders(self):
        makedirs(self._workspace_folder, exist_ok=True)
        makedirs("{}/META-INF".format(self._workspace_folder), exist_ok=True)
        makedirs("{}/OEBPS".format(self._workspace_folder), exist_ok=True)

    def _create_mimetype_file(self):
        with open("{}/mimetype".format(self._workspace_folder), "w") as file_handler:
            file_handler.write("application/epub+zip")

    def _create_css(self):
        file_name = "stylesheet.css"
        copyfile("{}/{}".format(self._templates_folder, file_name),
                 "{}/OEBPS/{}".format(self._workspace_folder, file_name))

    def _process_content(self):
        sources = self._process_input_files()
        self._raw_metadata = self._read_metadata()
        self._create_title_page()

    @staticmethod
    def _read_metadata():
        with open(".metadata.json", encoding='utf-8') as file_handler:
            raw_metadata = load(file_handler)
        return raw_metadata

    def _create_title_page(self):
        title_page  = self._templates["title"]
        title_page = title_page.format(title=self._raw_metadata["title"], author=self._raw_metadata["author"])
        with open("{}/OEBPS/title.xhtml".format(self._workspace_folder), "w", encoding='utf-8') as file_handler:
            file_handler.write(title_page)

    def _create_metadata(self):
        pass

    def _create_table_of_contents(self):
        with open("{}/navpoint.html".format(self._templates_folder)) as file_handler:
            navpoint_template = file_handler.read()
        with open("{}/toc.ncx.html".format(self._templates_folder)) as file_handler:
            toc_template = file_handler.read()
        nav_map = ""
        # TODO continue
        with open("{}/toc.ncx".format(self._workspace_folder), "w") as file_handler:
            file_handler.write(toc_template)

if __name__ == "__main__":
    e = EpubConverter(argv[1])
    e.convert()
