import time

from core.engine import Engine
from gui.gui_controller import MyGui


if __name__ == '__main__':
    engine = Engine()
    gui = MyGui(engine)
    gui.run()
