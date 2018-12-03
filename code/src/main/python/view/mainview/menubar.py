class Menubar:

    def createmenubar(self):

        """
        Erstellt die Menüleiste für das Fenster das an die Funktion übergeben wird
        """

        menubar = self.menuBar()
        programmmenu = menubar.addMenu('Programm')
        projektmenu = menubar.addMenu('Projekt')
        editMenu = menubar.addMenu('Edit')

        programmmenu.addAction('Einstellungen')
        projektmenu.addAction('Neu')
        projektmenu.addAction('Öffnen')
        projektmenu.addAction('Speichern')
        projektmenu.addAction('Speichern als')
        projektmenu.addAction('Projekteinstellungen')

