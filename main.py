from core.database_controller import DatabaseController
from core.engine import Engine
from gui.gui_controller import MyGui


# global variables
database_name = "zed.db"
paths_table_name = "zed_paths_table"
previous_state_table_name = "zed_previous_state_table"
location_of_log_file = "log.txt"
pdf_scanning_coordinates = {
    'project_name': {'x1': 2135, 'y1': 1527, 'x2': 2355, 'y2': 1556},
    'project_description': {'x1': 2135, 'y1': 1565, 'x2': 2355, 'y2': 1598},
    'document_number': {'x1': 2135, 'y1': 1608, 'x2': 2310, 'y2': 1640},
}

# compile to exe: `pyinstaller --onefile --noconsole main.py`
# regular expression: https://regex101.com/r/Lo8BEL/1

if __name__ == '__main__':
    # delete the log file in the beginning
    with open(location_of_log_file, 'w') as file:
        file.write('')

    db_controller = DatabaseController(
        database_name,
        paths_table_name,
        previous_state_table_name,
    )
    engine = Engine(
        location_of_log_file,
        pdf_scanning_coordinates,
        db_controller,
        paths_table_name,
        previous_state_table_name,
    )
    gui = MyGui(
        engine,
        db_controller,
        paths_table_name,
        previous_state_table_name,
    )
    gui.run()
