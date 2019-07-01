class Folder:
    """
    Model for a folder in the filemanager.

    It has a name and a list for its content.
    """

    def __init__(self, name):
        self.__name = name
        self.__content = []

    def get_content(self):
        """
        Getter for the content list.

        :return: List - Content of the folder.
        """

        return self.__content

    def get_name(self):
        """
        Getter for the folders name.

        :return: String - Name of the folder.
        """

        return self.__name

    def add_to_content(self, item):
        """
        Adds an item to the content list.

        :param item: Item to be added.
        """

        self.__content.append(item)
