from CatList import CatList


def main():

    cl = CatList.from_old_data()

    cl.add_new_data()

    cl.write_file()


if __name__ == "__main__":
    main()
