from core.database_controller import DatabaseController
from core.engine import Engine
from gui.gui_controller import MyGui


location_of_log_file = "log.txt"
database_name = "zed.db"
table_name = "zed_table"

# compile to exe
# pyinstaller --onefile --noconsole main.py

if __name__ == '__main__':
    # delete the log file in the beginning
    with open(location_of_log_file, 'w') as file:
        file.write('')

    db_controller = DatabaseController(database_name, table_name)
    engine = Engine(location_of_log_file)
    gui = MyGui(engine, db_controller)
    gui.run()
