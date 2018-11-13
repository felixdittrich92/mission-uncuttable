import grid__game_model
import grid_game_gui
import sys


def main():
    args = sys.argv[1:]
    if not len(args) == 2:
        print('usage: width height')
        sys.exit()

    gui = grid_gui.GridGui(grid_model.GridModel(int(args[0]), int(args[1])))
    gui.mainloop()

if __name__ == '__main__':
    main()
