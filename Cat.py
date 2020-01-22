PROPERTIES_LIST = [
    "Last_form",
    "Rarity",
    "Name (E)",
    "Name (J)",
    "Level",
    "PV",
    "KB",
    "Movement Speed",
    "AP",
    "DPS",
    "Target",
    "Attack Frequency",
    "Range",
    "Cost",
    "Respawn",
    "Ability",
    "Strength_White",
    "Strength_Red",
    "Strength_Floating",
    "Strength_Black",
    "Strength_Metal",
    "Strength_Angel",
    "Strength_Alien",
    "Strength_Zombies",
    "Strength_Relic",
    "Resist_White",
    "Resist_Red",
    "Resist_Floating",
    "Resist_Black",
    "Resist_Metal",
    "Resist_Angel",
    "Resist_Alien",
    "Resist_Zombies",
    "Resist_Relic",
    "Shockwave",
    "Critic",
    "own",
]


class Cat:
    def __init__(self, ID, form, properties, version=None):
        self.ID = ID
        self.form = form
        self.properties = properties
        self.version = version or "no_update"

    @classmethod
    def from_old_data(cls, in_line):
        in_list = in_line.strip().split("\t")
        ID = in_list.pop(0)
        form = in_list.pop(0)

        properties = dict()

        for form_property in PROPERTIES_LIST:
            try:
                properties[form_property] = in_list.pop(0)
            except:
                print(ID, form)
                continue

        return cls(ID, form, properties)

    @classmethod
    def from_new_data(cls, in_line):

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
        properties["Ability"] = "".join(cells[16].get_text(separator=" ").split()[:-10])

        return cls(ID, form, properties)

    @classmethod
    def compare_versions(cls, old_cat, new_cat):

        if not old_cat:
            new_cat.version = "new"
            return new_cat

        for key, new_value in new_cat.properties.items():
            if old_cat.properties[key] != new_value:
                old_cat.version = "updated"
                old_cat.properties[key] = new_value

            return old_cat
