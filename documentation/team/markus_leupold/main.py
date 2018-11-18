import grid_game_model
import grid_game_gui
import sys

"""
Ist gut gemacht, brauche ich nichts groß bemängeln, außer fehlender Funktionalität
(keine Gewinnnachricht, kein Restartbutton, keine Größenauswahl in der GUI)
und MVC pattern sollte nochmal genau angeguckt werden
"""

def main():
    args = sys.argv[1:]
    if not len(args) == 2:
        print('usage: width height')
        sys.exit()

    gui = grid_game_gui.GridGameGui(
        grid_game_model.GridGameModel(int(args[0]), int(args[1]))
    )
    gui.mainloop()

if __name__ == '__main__':
    main()
