# -*- coding: utf-8 -*-
__author__ = 'Bárdos Dávid'

from time import time
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
        self._nav_points = ""

    def convert(self):
        self._load_templates()
        self._create_workspace()
        self._process_content()
        # http://www.jedisaber.com/eBooks/Introduction.shtml
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
        self._create_container_xml()

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

    def _create_container_xml(self):
        file_name = "container.xml"
        copyfile("{}/{}".format(self._templates_folder, file_name),
                 "{}/META-INF/{}".format(self._workspace_folder, file_name))

    def _process_content(self):
        sources = self._process_input_files()
        self._raw_metadata = self._read_metadata()
        self._create_title_page()
        self._create_content_pages_and_generate_nav_points(sources)
        self._create_table_of_contents()

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

    def _create_content_pages_and_generate_nav_points(self, sources):
        for counter, raw_content in enumerate(sources):
            xhtml_content = self._create_content_page(raw_content)
            file_name = "chapter{}.xhtml".format(counter+1)
            file_path = "{}/OEBPS/{}".format(self._workspace_folder, file_name)
            with open(file_path, "w", encoding='utf-8') as file_handler:
                file_handler.write(xhtml_content)
            title = raw_content[0].replace("# ", "")
            nav_point = self._templates["navpoint"]
            nav_point = nav_point.format(nav_id="chapter{}".format(counter+1), order_number=counter+1, nav_name=title,
                                         file_name=file_name)
            self._nav_points += nav_point

    def _create_content_page(self, raw_content):
        title = ""
        text = ""
        for line in raw_content:
            if line.startswith("# ") and title == "":
                title = line.replace("# ", "")
            elif line.startswith("# "):
                raise RuntimeError("More than one title defined in a chapter!")
            else:
                text += "  <p>{}</p>\n".format(line)
        content_page = self._templates["content"]
        content_page = content_page.format(title=title, text=text)
        return content_page

    def _create_metadata(self):
        pass

    def _create_table_of_contents(self):
        unique_key = "gridranger-{}".format(time())
        toc = self._templates["toc.ncx"]
        toc = toc.format(unique_key=unique_key, title=self._raw_metadata["title"], nav_map=self._nav_points)
        with open("{}/OEBPS/toc.ncx".format(self._workspace_folder), "w", encoding='utf-8') as file_handler:
            file_handler.write(toc)

if __name__ == "__main__":
    e = EpubConverter(argv[1])
    e.convert()
