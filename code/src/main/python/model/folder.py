class Folder:

    def __init__(self, name):
        self.__name = name
        self.__content = []

    def get_content(self):
        return self.__content

    def get_name(self):
        return self.__name

    def add_to_content(self, item):
        self.__content.append(item)
