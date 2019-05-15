# -*- coding: utf-8 -*-
__author__ = 'Bárdos Dávid'

from abc import ABC, abstractmethod
from json import load
from os import listdir
from re import sub


class Converter(ABC):
    @abstractmethod
    def convert(self):
        pass

    @staticmethod
    def _read_metadata():
        with open(".metadata.json", encoding='utf-8') as file_handler:
            raw_metadata = load(file_handler)
        return raw_metadata

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
            raw_text = sub(r"^(\")", "\u201E", raw_text)
            raw_text = sub(r" (\")", " \u201E", raw_text)
            raw_text = sub(r"(\n\")", "\n\u201E", raw_text)
            raw_text = sub(r"(\")$", "\u201D", raw_text)
            raw_text = sub(r"(\") ", "\u201D ", raw_text)
            raw_text = sub(r"(\")\n", "\u201D\n", raw_text)
            raw_text = sub(r"(\"),", "\u201D,", raw_text)
            raw_text = sub(r"(\")!", "\u201D!", raw_text)
            raw_text = sub(r"(\")\?", "\u201D?", raw_text)
            raw_text = sub(r"(\").", "\u201D.", raw_text)
        lines = raw_text.split("\n\n")
        return lines
