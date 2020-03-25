import requests
from bs4 import BeautifulSoup

from Cat import Cat
from _utils import PROPERTIES_LIST


class CatList:
    def __init__(self, cat_dict, header):
        """
        Init function

        :param cat_dict: A dictionary of all cats
        :param header: the header of the file
        """
        self.cat_dict = cat_dict
        self.header = header

    @classmethod
    def from_old_data(cls):
        """
        Read the CSV and create the CatList object

        :return: the CatList object
        """
        cat_dict = dict()

        with open("neko.csv", encoding="utf8") as in_file:
            header = in_file.readline().strip()

            for in_line in in_file:
                in_cat = Cat.from_old_data(in_line)

                cat_dict[(in_cat.ID, in_cat.form)] = in_cat

        return cls(cat_dict, header)

    def add_new_data(self):
        """
        Scrap the battlecats website to get the most updated data.

        :return: The object itself
        """
        url = "https://battlecats-db.com/unit/status_r_all.html"
        css_path = "html body div div div div table tbody tr"

        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")

        for in_line in soup.select(css_path):
            new_cat = Cat.from_new_data(in_line)

            ID, form = new_cat.ID, new_cat.form

            key = (ID, form)

            old_cat = self.cat_dict.get(key)

            new_version = Cat.compare_versions(old_cat, new_cat)

            self.cat_dict[key] = new_version

        return self

    def write_file(self):
        """
        Write the final file to a csv

        :return: None
        """
        out_cat_list = []

        for key, cat in self.cat_dict.items():
            out_list = list(key)

            for cat_property in PROPERTIES_LIST:
                out_list.append(cat.properties.get(cat_property, ""))

            out_list.append(cat.version)
            out_line = "\t".join(out_list)
            out_cat_list.append(out_line)

        out_cat_list.sort()

        with open("new_data.csv", "w", encoding="utf8") as out_file:
            out_file.write(self.header)
            out_file.write("\n")
            out_file.write("\n".join(out_cat_list))
            out_file.write("\n")
