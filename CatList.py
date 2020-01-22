from Cat import Cat
from _utils import new_file_reader, PROPERTIES_LIST
import requests
from bs4 import BeautifulSoup


class CatList:
    def __init__(self, cat_dict, header):
        self.cat_dict = cat_dict
        self.header = header

    @classmethod
    def from_old_data(cls):

        cat_dict = dict()

        with open("neko.csv", encoding="utf8") as in_file:
            header = in_file.readline().strip()

            for in_line in in_file:
                in_cat = Cat.from_old_data(in_line)

                cat_dict[(in_cat.ID, in_cat.form)] = in_cat

        return cls(cat_dict, header)

    def add_new_data(self):

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

        with open("new_data.csv", "w", encoding="utf8") as out_file:
            out_file.write(self.header)
            out_file.write("\n")

            for key, cat in self.cat_dict.items():
                out_list = list(key)

                for cat_property in PROPERTIES_LIST:
                    out_list.append(cat.properties.get(cat_property, ""))

                out_list.append(cat.version)
                out_list.append("\n")

                out_line = "\t".join(out_list)

                out_file.write(out_line)
