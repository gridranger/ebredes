# -*- coding: utf-8 -*-
__author__ = 'Bárdos Dávid'

from abc import ABC, abstractmethod
from os import listdir


class Converter(ABC):
    @abstractmethod
    def convert(self):
        pass

    @staticmethod
    def _process_input_files():
        sources = []
        current_folder_content = listdir(".")
        for file_name in current_folder_content:
            if file_name.endswith(".txt"):
                sources.append(Converter._process_file(file_name))
        return sources

    @staticmethod
    def _process_file(file_name):
        with open(file_name, encoding="utf8") as file_handler:
            raw_text = file_handler.read()
            raw_text = raw_text.replace("\ufeff", "")
            raw_text = raw_text.replace("--", "\u2013")
        lines = raw_text.split("\n\n")
        return lines
