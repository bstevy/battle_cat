from re import compile

from _utils import PROPERTIES_LIST


class Cat:
    def __init__(self, ID, form, properties, change_flag=None):
        """
        Init function

        :param ID: The ID of the cat
        :param form: The form number of the cat
        :param properties: properties dictionary
        :param change_flag: Flag to see if there is any change
        """
        self.ID = ID.zfill(3)
        self.form = form
        self.properties = self.compute_dps(properties)
        self.version = change_flag or "no_update"

    @classmethod
    def from_old_data(cls, in_line):
        """
        Create a cat from a CSV

        :param in_line: A line of CSV
        :return: A cat object
        """
        in_list = in_line.strip().split("\t")
        ID = in_list.pop(0)
        form = in_list.pop(0)

        properties = dict()

        for form_property in PROPERTIES_LIST:
            try:
                properties[form_property] = in_list.pop(0)
            except:
                print(ID, form, form_property)
                continue

        return cls(ID, form, properties)

    @classmethod
    def from_new_data(cls, in_line):
        """
        Create a cat from the website

        :param in_line: A line of the website
        :return: A cat object
        """
        cells = in_line.select("td")

        index = cells[0].getText()
        ID, form = index.split("-")

        properties = dict()

        group = cells[1].get_text(separator=" ").split()
        properties["Rarity"] = group[1]  # group in japanese

        properties["Name (J)"] = cells[3].getText()
        properties["Level"] = cells[4].getText()
        properties["PV"] = cells[5].getText()
        properties["KB"] = cells[6].getText()
        properties["Movement Speed"] = cells[7].getText()
        properties["AP"] = cells[8].getText()
        properties["DPS"] = cells[9].getText()
        properties["Target"] = cells[10].getText()
        properties["Attack Frequency"] = cells[11].getText()

        properties["Range"] = cells[13].getText()
        properties["Cost"] = cells[14].getText()
        properties["Respawn"], _ = cells[15].get_text(separator=" ").split()
        properties["Ability"] = cls.parse_ability(cells[16])

        return cls(ID, form, properties)

    @staticmethod
    def parse_ability(cells_16):
        """
        Parse the content of cells 16 to format the ability info

        :param cells_16: Content of cell 16
        :return: The formatted ability
        """
        split_pattern = compile(r"x?\d{7}\d*")
        return split_pattern.split(cells_16.get_text())[0]

    @classmethod
    def compare_versions(cls, old_cat, new_cat):
        """
        Compare two cats and return a mixed version of two.

        :param old_cat: A cat object to compare
        :param new_cat: Another cat object
        :return: A new cat object
        """
        if not old_cat:
            new_cat.version = "new"
            return new_cat

        for key, new_value in new_cat.properties.items():

            if old_cat.properties.get(key) != new_value:
                print(
                    "updated:",
                    new_cat.ID,
                    new_cat.form,
                    key,
                    old_cat.properties[key],
                    new_value,
                )
                old_cat.version = "updated"
                old_cat.properties[key] = new_value

        return old_cat

    @staticmethod
    def compute_dps(cat_properties):
        """
        Add DPS columns when possible

        :param cat_properties: Basic cat properties
        :return: Cat properties with DPS columns
        """

        try:
            DPS = float(cat_properties["DPS"].replace(",", ""))
        except ValueError:
            return cat_properties

        Shockwave = cat_properties.get("Shockwave")
        Critic = cat_properties.get("Critic")

        if (Shockwave and Critic) is None:
            return cat_properties
        else:
            ratio = (float(Shockwave) + float(Critic)) / 100

        key_list = [key for key in cat_properties.keys() if key.startswith("Strength")]

        for key in key_list:
            value = cat_properties[key]

            new_key = "DPS_{}".format(key.split("_")[-1])

            new_value = DPS * (float(value) + ratio)

            cat_properties[new_key] = str(int(new_value))

        return cat_properties
