from CatList import CatList
import os


def rename_cat_file():
    """
    Exchange new file and current file.

    :return: None
    """
    wd = os.path.dirname(os.path.abspath(__file__))

    current_file = os.path.join(wd, "neko.csv")
    old_file = os.path.join(wd, "new_data.csv")
    new_file = os.path.join(wd, "old_data.csv")

    if os.path.isfile(old_file):
        os.remove(old_file)

    os.rename(current_file, old_file)
    os.rename(new_file, current_file)


def main():
    """
    Main function

    :return: None
    """
    cl = CatList.from_old_data()

    cl.add_new_data()

    cl.write_file()

    rename_cat_file()


if __name__ == "__main__":
    main()
