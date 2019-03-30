# -*- coding: utf-8 -*-
__author__ = 'Bárdos Dávid'

from json import load
from os import makedirs
from shutil import copyfile, rmtree
from sys import argv
from uuid import uuid1
from zipfile import ZipFile
from converter import Converter


class EpubConverter(Converter):
    def __init__(self, output_file_name):
        self._output_file_path = "target/{}.epub".format(output_file_name)
        self._templates_folder = "builder/templates"
        self._workspace_folder = "target/ws"
        self._book_file_paths = []
        self._chapter_file_names = []
        self._raw_metadata = {}
        self._templates = {}
        self._nav_points = ""

    def convert(self):
        self._load_templates()
        self._create_workspace()
        self._process_content()
        self._compress_workspace()
        self._remove_workspace()

    def _load_templates(self):
        templates = ["content", "metadata", "navpoint", "title", "toc.ncx"]
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
        file_path = "{}/mimetype".format(self._workspace_folder)
        with open(file_path, "w") as file_handler:
            file_handler.write("application/epub+zip")
        self._book_file_paths.append(file_path)

    def _create_css(self):
        file_name = "stylesheet.css"
        file_path = "{}/OEBPS/{}".format(self._workspace_folder, file_name)
        copyfile("{}/{}".format(self._templates_folder, file_name), file_path)
        self._book_file_paths.append(file_path)

    def _create_container_xml(self):
        file_name = "container.xml"
        file_path = "{}/META-INF/{}".format(self._workspace_folder, file_name)
        copyfile("{}/{}".format(self._templates_folder, file_name), file_path)
        self._book_file_paths.append(file_path)

    def _process_content(self):
        sources = self._process_input_files()
        self._raw_metadata = self._read_metadata()
        self._create_title_page()
        self._create_content_pages_and_generate_nav_points(sources)
        self._create_table_of_contents()
        self._create_metadata()

    @staticmethod
    def _read_metadata():
        with open(".metadata.json", encoding='utf-8') as file_handler:
            raw_metadata = load(file_handler)
        raw_metadata["uuid"] = str(uuid1())
        return raw_metadata

    def _create_title_page(self):
        file_path = "{}/OEBPS/title.xhtml".format(self._workspace_folder)
        title_page  = self._templates["title"]
        title_page = title_page.format(title=self._raw_metadata["title"], author=self._raw_metadata["author"])
        with open(file_path, "w", encoding='utf-8') as file_handler:
            file_handler.write(title_page)
        self._book_file_paths.append(file_path)

    def _create_content_pages_and_generate_nav_points(self, sources):
        for counter, raw_content in enumerate(sources):
            xhtml_content = self._create_content_page(raw_content)
            file_name = "chapter{}.xhtml".format(counter+1)
            self._chapter_file_names.append(file_name)
            file_path = "{}/OEBPS/{}".format(self._workspace_folder, file_name)
            with open(file_path, "w", encoding='utf-8') as file_handler:
                file_handler.write(xhtml_content)
            title = raw_content[0].replace("# ", "")
            nav_point = self._templates["navpoint"]
            nav_point = nav_point.format(nav_id="chapter{}".format(counter+1),
                                         order_number=counter+1,
                                         nav_name=title,
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
        file_path = "{}/OEBPS/metadata.opf".format(self._workspace_folder)
        manifest = ""
        spine = ""
        for chapter_file_name in self._chapter_file_names:
            new_manifest_line = """    <item id="{}" href="{}" media-type="application/xhtml+xml" />\n"""
            manifest += new_manifest_line.format(chapter_file_name.replace(".xhtml", ""), chapter_file_name)
            new_spine_line = """    <itemref idref="{}" />\n"""
            spine += new_spine_line.format(chapter_file_name.replace(".xhtml", ""))
        metadata = self._templates["metadata"]
        metadata = metadata.format(title=self._raw_metadata["title"],
                                   author=self._raw_metadata["author"],
                                   uuid=self._raw_metadata["uuid"],
                                   language=self._raw_metadata["language"],
                                   manifest=manifest,
                                   spine=spine)
        with open(file_path, "w", encoding='utf-8') as file_handler:
            file_handler.write(metadata)
        self._book_file_paths.append(file_path)

    def _create_table_of_contents(self):
        file_path = "{}/OEBPS/toc.ncx".format(self._workspace_folder)
        toc = self._templates["toc.ncx"]
        toc = toc.format(uuid=self._raw_metadata["uuid"],
                         title=self._raw_metadata["title"],
                         nav_map=self._nav_points)
        with open(file_path, "w", encoding='utf-8') as file_handler:
            file_handler.write(toc)
        self._book_file_paths.append(file_path)

    def _compress_workspace(self):
        file_list = []
        file_list += self._book_file_paths
        for chapter_file_name in self._chapter_file_names:
            file_list.append("{}/OEBPS/{}".format(self._workspace_folder, chapter_file_name))
        with ZipFile(self._output_file_path, 'w') as file_handler:
            for file_path in file_list:
                file_handler.write(file_path, file_path.replace(self._workspace_folder, ""))

    def _remove_workspace(self):
        rmtree(self._workspace_folder)


if __name__ == "__main__":
    e = EpubConverter(argv[1])
    e.convert()
